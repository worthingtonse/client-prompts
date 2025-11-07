# # rke_client/content_server/session.py

# """
# Provides the primary high-level function to orchestrate the entire client
# logic for establishing a secure session with a Content Server.
# """

# import asyncio
# import hashlib
# import logging
# import os
# import struct
# from dataclasses import dataclass
# from typing import Optional

# from .. import config
# from ..content_server import protocol as cs_protocol
# from ..crypto import aes, kdf
# from ..crypto.keystore import KeyStore
# from ..dns_discovery import ContentServerDiscovery
# from ..raida import communicator, discovery as raida_discovery, keyshare, ticket
# from ..wallet.wallet import Wallet

# logger = logging.getLogger(__name__)

# # --- Custom Exception for Retry Logic ---
# class StaleKeyError(Exception):
#     """Custom exception raised when a session fails due to a stale encryption key."""
#     pass

# # --- Data Structures ---
# @dataclass
# class SessionResult:
#     """Holds the successful result of a session establishment."""
#     session_key: bytes
#     session_token: str
#     lifetime: int

# # --- Internal Worker Function ---
# async def _attempt_session(
#     domain: str,
#     wallet: Wallet,
#     global_network: raida_discovery.RaidaNetwork,
#     discovery_service: ContentServerDiscovery,
#     comm: communicator.RaidaCommunicator,
#     key_store: KeyStore
# ) -> Optional[SessionResult]:
#     """
#     Performs a single attempt to establish a session. Can raise StaleKeyError
#     to signal that a retry is needed.
#     """
#     # A random identifier for this client instance, used in key derivation.
#     client_sn = os.urandom(5)

#     # Step 3 (Master Flow): Discover Content Server via DNS.
#     cs_config = discovery_service.discover(domain)
#     if not cs_config or not cs_config.target_host: return None

#     # Determine the best key set to use from the server's configuration.
#     selected_keyset = keyshare._select_best_keyset(cs_config)
#     if not selected_keyset: return None
#     cs_id = selected_keyset.cs_id

#     # Initialize variables for the key and its identifier.
#     encryption_key: Optional[bytes] = None
#     kid_to_use: Optional[bytes] = None
#     dke_result: Optional[keyshare.DKEResult] = None

#     # --- Step 4 (Master Flow): FAST PATH ---
#     # Try to find a cached key to avoid the expensive RKE process.
#     cached_kid = key_store.get_kid_for_csid(cs_id)
#     if cached_kid:
#         # A KID was found in our map, now try to load the actual key file.
#         encryption_key = key_store.load_key(cached_kid)
#         if encryption_key:
#             # Success! We have a valid, non-expired key.
#             logger.info(f"Using cached key with KID '{cached_kid.hex()}' for Fast Path.")
#             kid_to_use = cached_kid
#             # Create a DKEResult object to hold the key and metadata, mimicking
#             # the output of the RKE path for consistent logic flow.
#             dke_result = keyshare.DKEResult(
#                 key=encryption_key, kid=kid_to_use, bitmap=0, timestamp=0,
#                 client_sn=client_sn, key_id=selected_keyset.kid, cs_id=cs_id
#             )

#     # --- Step 5 (Master Flow): RKE PATH ---
#     # This block is executed if the Fast Path failed (no cached KID or key was invalid/expired).
#     if not encryption_key or not dke_result:
#         logger.info(f"No valid cached key. Executing full RKE process.")
#         dke_result = await keyshare.get_encryption_key(
#             cs_config=cs_config, global_network=global_network, wallet=wallet,
#             communicator=comm, client_sn=client_sn
#         )
#         if not dke_result: return None # RKE failed critically.
        
#         # RKE was successful. Store the new key and its KID for future Fast Path use.
#         encryption_key = dke_result.encryption_key
#         kid_to_use = dke_result.kid
#         key_store.save_key(kid_to_use, encryption_key)
#         key_store.save_kid_for_csid(cs_id, kid_to_use)

#     # Step 6 (Master Flow): Acquire RAIDA Authentication Tickets.
#     # tickets = await ticket.get_tickets(global_network, wallet, comm)
#     # if not tickets: return None


#     auth_coin, tickets = await ticket.get_tickets_with_coin(global_network, wallet, comm)
#     if not auth_coin or not tickets:
#         logger.critical("Failed to acquire authentication tickets. Cannot establish session.")
#         return None
    

#     logger.debug("Constructing session request payload with coin info and tickets.")

#     # # Step 7 (Master Flow): Construct the initial session request payload.
#     # valid_tickets = [t for t in tickets if t is not None]
#     # if not valid_tickets: return None
    
#     # This is our half of the random data for the session key derivation.
#     client_nonce = os.urandom(16)
#     # payload = bytearray(client_nonce)
#     # payload.append(len(valid_tickets))
#     # for t_hex in valid_tickets: payload.extend(bytes.fromhex(t_hex))
    

#     payload = bytearray()
#     payload.extend(client_nonce)
    
#     # ADDED: Include the authenticating coin's info (denomination + sn)
#     payload.append(auth_coin.denomination & 0xFF)
#     payload.extend(struct.pack(">I", auth_coin.sn))

#     # Add the tickets
#     valid_tickets_bytes = [bytes.fromhex(t) for t in tickets if t is not None]
#     payload.append(len(valid_tickets_bytes))
#     for t_bytes in valid_tickets_bytes:
#         payload.extend(t_bytes)
#     # Include an HMAC for integrity protection.
#     hmac_key = hashlib.sha256(encryption_key).digest()
#     hmac_val = hashlib.sha256(hmac_key + payload).digest()
#     payload.extend(hmac_val)
#     payload.extend(b'\xE3\xE3')

#     # Step 8 (Master Flow): Create and send the first packet to the Content Server.
#     initial_packet = cs_protocol.create_initial_type6_packet(
#         encryption_key=encryption_key, kid=kid_to_use, cs_id=dke_result.cs_id,
#         key_id=dke_result.key_id, client_sn=dke_result.client_sn,
#         timestamp=dke_result.timestamp, raida_bitmap=dke_result.raida_bitmap,
#         payload=bytes(payload)
#     )
#     if not initial_packet: return None

#     # Perform the network communication.
#     try:
#         reader, writer = await asyncio.open_connection(cs_config.target_host, cs_config.target_port)
#         writer.write(initial_packet)
#         await writer.drain()
#         session_response_data = await reader.read(4096)
#         writer.close()
#         await writer.wait_closed()
#     except Exception as e:
#         logger.critical(f"Failed to communicate with Content Server: {e}")
#         return None

#     # --- Step 9 (Master Flow): Parse Server Response and Derive Session Key ---
#     if not session_response_data or len(session_response_data) < 32: return None

#     # The server's response MUST be a Type 6 packet.
#     header = session_response_data[:32]
#     encrypted_body = session_response_data[32:]
    
#     # Decrypt the body using the initial encryption_key. The nonce is read from
#     # the server's response header.
#     nonce_from_server = header[8:24]
#     body = aes.aes_ctr_crypt(encryption_key, encrypted_body, nonce_from_server)

#     if not body or len(body) < 53: return None

#     # Parse the plaintext fields from the decrypted body.
#     server_nonce = body[0:16]        # The server's half of the random data.
#     session_token_bytes = body[16:48] # The token for server-side session lookup.
#     session_lifetime = struct.unpack(">I", body[48:52])[0]
#     status = body[52]
    
#     # Check if the server accepted our request.
#     if status != config.ResponseStatus.SUCCESS:
#         if status == config.ResponseStatus.FAILED_AUTH:
#             # This indicates our cached key was stale. Delete it and trigger a retry.
#             if kid_to_use: key_store.delete_key(kid_to_use)
#             raise StaleKeyError("Cached key rejected by server.")
#         return None

#     # Both sides now have the same encryption_key, client_nonce, and server_nonce.
#     # They can now independently derive the same, shared session_key.
#     key_material = encryption_key + client_nonce + server_nonce
#     session_key = kdf.hkdf_expand(prk=key_material, info=config.DKE_SESSION_INFO, length=32)
#     if not session_key: return None

#     logger.info("Session handshake successful! A temporary session key has been derived.")
#     return SessionResult(session_key=session_key, session_token=session_token_bytes.hex(), lifetime=session_lifetime)


# async def establish_session(
#     domain: str,
#     wallet: Wallet,
#     global_network: raida_discovery.RaidaNetwork,
#     max_retries: int = 1
# ) -> Optional[SessionResult]:
#     """
#     Executes the full Master Flow to establish a secure session. This is the
#     main public-facing function of the module.
#     """
#     discovery_service = ContentServerDiscovery()
#     comm = communicator.RaidaCommunicator()
#     key_store = KeyStore()

#     # This loop handles the self-healing retry logic for stale keys.
#     for attempt in range(max_retries + 1):
#         try:
#             result = await _attempt_session(
#                 domain, wallet, global_network, discovery_service, comm, key_store
#             )
#             if result:
#                 return result
#             else:
#                 return None
#         except StaleKeyError:
#             logger.warning(f"Stale key detected. Retrying handshake (attempt {attempt + 2})...")
#             if attempt >= max_retries:
#                 logger.error("Maximum retry limit reached. Aborting.")
#                 return None
#         except Exception as e:
#             logger.critical(f"An unhandled exception occurred: {e}")
#             return None
#     return None



# rke_client/content_server/session.py

"""
Provides the primary high-level function to orchestrate the client logic for
establishing a secure session with a Content Server. This implementation uses
a single, combined packet for key registration and session authentication.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

from .. import config
from . import protocol as cs_protocol
from ..crypto.keystore import KeyStore
from ..dns_discovery import ContentServerDiscovery
from ..raida import communicator, discovery as raida_discovery, keyshare, ticket
from ..wallet.wallet import Wallet
from . import communicator as cs_communicator

logger = logging.getLogger(__name__)

# --- Custom Exception for Retry Logic ---
class StaleKeyError(Exception):
    """Custom exception raised when a session fails due to a stale encryption key."""
    pass

# --- Data Structure for the established session ---
@dataclass
class Session:
    """Holds the successful result of a session establishment."""
    encryption_key: bytes
    kid: bytes
    session_identifier: bytes

# --- Internal Worker Function ---
async def _attempt_session(
    domain: str,
    wallet: Wallet,
    global_network: raida_discovery.RaidaNetwork,
    discovery_service: ContentServerDiscovery,
    raida_comm: communicator.RaidaCommunicator,
    key_store: KeyStore
) -> Optional[Session]:
    """
    Performs a single attempt to establish a session. This involves a full
    RKE and the sending of a single combined registration/authentication packet.
    """
    # 1. Discover Content Server configuration
    cs_config = await discovery_service.get_dke_config(domain)
    if not cs_config:
        logger.error(f"Could not retrieve DKE configuration for '{domain}'.")
        return None

    # 2. Always perform RKE to get a fresh key for this new session attempt.
    logger.info("Performing RKE to derive a shared encryption key...")
    client_sn = os.urandom(config.CS_PAYLOAD["SESSION_ID_LEN"] - 3) # A random serial number for this client instance
    dke_result = await keyshare.get_encryption_key(cs_config, global_network, wallet, raida_comm, client_sn)
    if not dke_result:
        logger.error("Failed to derive encryption key via RKE.")
        return None

    # 3. Get a CloudCoin for authentication tickets
    coin = wallet.get_coin_for_ticket()
    if not coin:
        logger.error("No available CloudCoin in wallet to get tickets.")
        return None
        
    # 4. Get authentication tickets from RAIDA
    tickets = await ticket.get_tickets(coin.sn, coin.denomination, raida_comm, global_network)
    if not tickets:
        logger.error("Failed to acquire authentication tickets from RAIDA.")
        return None

    # 5. Generate the 8-byte session identifier
    session_identifier = os.urandom(config.CS_PAYLOAD["SESSION_ID_LEN"])
    
    # 6. Build the single, combined packet for registration and authentication.
    initial_packet = cs_protocol.create_combined_auth_packet(
        dke_result=dke_result,
        cc_sn=coin.sn,
        cc_denomination=coin.denomination,
        session_identifier=session_identifier,
        tickets=tickets
    )
    if not initial_packet:
        logger.error("Failed to build the combined authentication packet.")
        return None

    # 7. Send the packet to the Content Server.
    cs_comm = cs_communicator.ContentServerCommunicator(cs_config.host, cs_config.port)
    response = await cs_comm.send_request(initial_packet)

    # 8. Handle the response.
    if not response:
        logger.error("No response from Content Server.")
        return None

    # A stale key response is still possible if the server's state is unusual
    if response.status_code == config.CS_STATUS_CODE.STALE_KEY:
        raise StaleKeyError("Server indicated a stale key, which is unexpected in this flow.")

    if response.status_code != config.CS_STATUS_CODE.SESSION_ESTABLISHED:
        logger.error(f"Failed to establish session. Server responded with status: {response.status_code}")
        return None

    logger.info("Session established successfully in a single request!")
    return Session(
        encryption_key=dke_result.encryption_key, 
        kid=dke_result.kid,
        session_identifier=session_identifier
    )

# --- Main Public Function ---
async def establish_session(
    domain: str,
    wallet: Wallet,
    global_network: raida_discovery.RaidaNetwork,
    max_retries: int = 1
) -> Optional[Session]:
    """
    Establishes a secure session with the Content Server in a single request.
    Includes retry logic for network errors or stale keys.
    """
    discovery_service = ContentServerDiscovery()
    raida_comm = communicator.RaidaCommunicator()
    key_store = KeyStore() # Keystore can be used later if needed, but not for this flow

    for attempt in range(max_retries + 1):
        try:
            return await _attempt_session(
                domain, wallet, global_network, discovery_service, raida_comm, key_store
            )
        except StaleKeyError as e:
            logger.warning(f"{e} Retrying (attempt {attempt + 2})...")
            if attempt >= max_retries:
                logger.error("Maximum retry limit reached. Aborting.")
                return None
        except Exception as e:
            logger.critical(f"An unexpected error occurred during session establishment: {e}", exc_info=True)
            return None
    return None