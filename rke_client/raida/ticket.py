# # rke_client/raida/ticket.py

# """
# Provides a high-level interface for the "get ticket" operation, which is used
# to authenticate ownership of a CloudCoin with the RAIDA network.

# This module is the Python equivalent of the Go 'getticket.go' file.
# """

# import logging
# import struct
# from typing import List, Optional

# from .. import config
# from ..raida.discovery import RaidaNetwork
# from ..wallet.wallet import Wallet
# from . import protocol
# from .communicator import RaidaCommunicator

# # Configure a logger for this module
# logger = logging.getLogger(__name__)

# # -- Main Ticket Acquisition Function --

# async def get_tickets(
#     global_network: RaidaNetwork,
#     wallet: Wallet,
#     communicator: RaidaCommunicator
# ) -> Optional[List[Optional[str]]]:
#     """
#     Orchestrates the process of acquiring authentication tickets from the RAIDA network.

#     It selects a high-quality coin from the wallet, builds encrypted requests,
#     sends them to all 25 global RAIDA servers, and collects the tickets from
#     successful responses.

#     Args:
#         global_network (RaidaNetwork): The discovered global list of RAIDA servers.
#         wallet (Wallet): The user's wallet, used to get an authentication coin.
#         communicator (RaidaCommunicator): The network communicator instance.

#     Returns:
#         Optional[List[Optional[str]]]: A list of 25 items. Each item is a hex-encoded
#                                        ticket string if the corresponding RAIDA
#                                        responded successfully, otherwise None.
#                                        Returns None if the entire process fails.
#     """
#     logger.info("Starting ticket acquisition process...")

#     # 1. Get a high-quality coin from the wallet for authentication
#     auth_coins = wallet.get_coins_for_encryption(count=1)
#     if not auth_coins:
#         logger.error("GetTicket failed: Could not get a coin from the wallet for authentication.")
#         return None
#     auth_coin = auth_coins[0]
#     logger.debug(f"Using SN {auth_coin.sn} for ticket acquisition.")

#     # 2. Prepare the request payload
#     # Payload is denomination (1 byte) and SN (4 bytes).
#     payload = bytearray()
#     # Handle potentially negative denomination values by getting the correct
#     # unsigned 8-bit integer representation (two's complement).
#     payload.append(auth_coin.denomination & 0xFF)
#     payload.extend(struct.pack(">I", auth_coin.sn)) # Pack SN as 32-bit big-endian

#     # 3. Build 25 encrypted packets, one for each RAIDA
#     packets_to_send: List[bytes] = [b''] * config.TOTAL_RAIDA_SERVERS
#     for i in range(config.TOTAL_RAIDA_SERVERS):
#         try:
#             # GetTicket is a Type 1 encrypted command
#             packets_to_send[i] = protocol.build_request_packet(
#                 raida_idx=i,
#                 command_group=config.COMMAND_GROUP.COMMAND_GROUP_HEALING,
#                 command_code=config.HealingCommand.COMMAND_GET_TICKET,
#                 payload=payload,
#                 encryption_coins=[auth_coin]
#             )
#         except Exception as e:
#             logger.error(f"Failed to build GetTicket packet for RAIDA {i}: {e}")
#             packets_to_send[i] = b''

#     # 4. Send requests concurrently to the full global RAIDA network
#     responses = await communicator.send_requests_async(packets_to_send, global_network.primary)

#     # 5. Process responses and collect tickets based on the exact RAIDA protocol
#     tickets: List[Optional[str]] = [None] * config.TOTAL_RAIDA_SERVERS
#     successful_tickets = 0
#     for response in responses:
#         if not response.is_success or not response.data:
#             continue

#         # A standard RAIDA response has a 5-byte header:
#         # [0]: Status (1 byte)
#         # [1:3]: Echoed RAIDA index (2 bytes, big-endian) - We can ignore this
#         # [3:5]: Body Length (2 bytes, big-endian)
#         if len(response.data) < 5:
#             logger.warning(f"RAIDA {response.raida_index} returned a malformed response (too short).")
#             continue

#         status = response.data[0]
#         body_len = struct.unpack(">H", response.data[3:5])[0]

#         if status != config.ResponseStatus.SUCCESS:
#             logger.warning(f"RAIDA {response.raida_index} returned fail status: {hex(status)}.")
#             continue
        
#         # The total packet length should be header (5) + body_len
#         if len(response.data) != 5 + body_len:
#             logger.warning(f"RAIDA {response.raida_index} returned inconsistent length. Header says {body_len}, actual is {len(response.data) - 5}.")
#             continue

#         # Based on cmd_healing.c, the response body for a successful get_ticket
#         # is exactly the 32-byte ticket.
#         if body_len != 32:
#             logger.warning(f"RAIDA {response.raida_index} returned a ticket with incorrect length: {body_len} bytes.")
#             continue
            
#         ticket_bytes = response.data[5 : 5 + body_len]
#         tickets[response.raida_index] = ticket_bytes.hex()
#         successful_tickets += 1
#         logger.debug(f"Received valid 32-byte ticket from RAIDA {response.raida_index}.")

    
#     if successful_tickets < config.MIN_QUORUM:
#         logger.error(f"Ticket acquisition failed. Only received {successful_tickets} tickets, "
#                      f"which is less than the required quorum of {config.MIN_QUORUM}.")
#         return None

#     logger.info(f"Successfully acquired {successful_tickets} tickets from the RAIDA network.")
#     return tickets


# rke_client/raida/ticket.py

import logging
import struct
from typing import List, Optional, Tuple

from .. import config
from ..raida.discovery import RaidaNetwork
from ..wallet.cloudcoin import CloudCoin
from ..wallet.wallet import Wallet
from . import protocol
from .communicator import RaidaCommunicator

logger = logging.getLogger(__name__)

async def get_tickets_with_coin(
    global_network: RaidaNetwork,
    wallet: Wallet,
    communicator: RaidaCommunicator
) -> Tuple[Optional[CloudCoin], Optional[List[Optional[str]]]]:
    """
    Orchestrates acquiring tickets and returns the tickets AND the coin used.
    This is the primary function for the session establishment process.

    Args:
        global_network (RaidaNetwork): The discovered global list of RAIDA servers.
        wallet (Wallet): The user's wallet, used to get an authentication coin.
        communicator (RaidaCommunicator): The network communicator instance.

    Returns:
        Tuple[Optional[CloudCoin], Optional[List[Optional[str]]]]: A tuple containing
            the CloudCoin object used for authentication and the list of tickets.
            Returns (None, None) on failure.
    """
    logger.info("Starting ticket acquisition process...")

    auth_coins = wallet.get_coins_for_encryption(count=1)
    if not auth_coins:
        logger.error("GetTicket failed: No high-quality coin available for authentication.")
        return None, None
    auth_coin = auth_coins[0]
    logger.debug(f"Using SN {auth_coin.sn} for ticket acquisition.")

    # Payload is denomination (1 byte) and SN (4 bytes).
    payload = bytearray()
    payload.append(auth_coin.denomination & 0xFF)
    payload.extend(struct.pack(">I", auth_coin.sn))

    packets_to_send: List[bytes] = [b''] * config.TOTAL_RAIDA_SERVERS
    for i in range(config.TOTAL_RAIDA_SERVERS):
        try:
            packets_to_send[i] = protocol.build_request_packet(
                raida_idx=i,
                command_group=config.COMMAND_GROUP.COMMAND_GROUP_HEALING,
                command_code=config.HealingCommand.COMMAND_GET_TICKET,
                payload=payload,
                encryption_coins=[auth_coin]
            )
        except Exception as e:
            logger.error(f"Failed to build GetTicket packet for RAIDA {i}: {e}")
            packets_to_send[i] = b''

    responses = await communicator.send_requests_async(packets_to_send, global_network.primary)

    tickets: List[Optional[str]] = [None] * config.TOTAL_RAIDA_SERVERS
    successful_tickets = 0
    for response in responses:
        if not response.is_success or not response.data or len(response.data) < 5:
            continue

        status = response.data[0]
        body_len = struct.unpack(">H", response.data[3:5])[0]

        if status == config.ResponseStatus.SUCCESS and body_len == 4:
            ticket_bytes = response.data[5 : 5 + body_len]
            tickets[response.raida_index] = ticket_bytes.hex()
            successful_tickets += 1
        else:
            logger.warning(f"RAIDA {response.raida_index} returned fail status or incorrect ticket length.")

    if successful_tickets < config.MIN_QUORUM:
        logger.error(f"Ticket acquisition failed. Only received {successful_tickets} tickets.")
        return auth_coin, None

    logger.info(f"Successfully acquired {successful_tickets} tickets.")
    return auth_coin, tickets