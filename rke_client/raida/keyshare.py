# rke_client/raida/keyshare.py

"""
Provides a high-level interface for orchestrating the DKE (Distributed Key
Exchange) process.

This module is responsible for:
1.  Intelligently selecting the best key set from a Content Server's config.
2.  Mapping the Content Server's RAIDA IPs to their canonical 0-24 indices.
3.  Building and sending 'get_keyshare' requests to the correct RAIDAs.
4.  Collecting the key shares and deriving the final encryption key.

This module executes Step 5 of the Master Flow.
"""

import logging
import os
import struct
import time
from typing import Dict, List, Optional, Tuple

from .. import config
from ..crypto import kdf
from ..dns_discovery import DKEConfig, KeySet
from ..raida.discovery import RaidaNetwork
from ..wallet.wallet import Wallet
from . import protocol
from .communicator import RaidaCommunicator

# Configure a logger for this module
logger = logging.getLogger(__name__)

# -- Data Structures --

class DKEResult:
    """A dataclass to hold the successful result of a DKE operation."""
    def __init__(self, key: bytes,kid: bytes, bitmap: int, timestamp: int, client_sn: bytes, key_id: str, cs_id: str):
        self.encryption_key = key
        self.kid = kid # The 5-byte Key Identifier for the Type 6 header
        self.raida_bitmap = bitmap
        self.timestamp = timestamp
        self.client_sn = client_sn
        self.key_id = key_id
        self.cs_id = cs_id

# -- Helper Functions --

def _select_best_keyset(cs_config: DKEConfig) -> Optional[KeySet]:
    """
    Selects the best available key set from the DKE config based on defined
    requirements.

    Currently, it checks the 'raidas>=X' requirement. This can be extended
    to handle other requirements as they are defined.
    """
    min_raidas_required = 0
    req_str = cs_config.requirements.get("raidas", "0")
    # Handle both ">=" and just a number
    req_str = req_str.replace(">=", "").strip()
    try:
        min_raidas_required = int(req_str)
    except ValueError:
        logger.warning(f"Invalid 'raidas' requirement found: '{req_str}'. Defaulting to 0.")

    # Find the first key set that meets the minimum RAIDA count
    for kid, key_set in cs_config.key_sets.items():
        if len(key_set.raida_servers) >= min_raidas_required:
            logger.info(f"Selected key set '{kid}' with {len(key_set.raida_servers)} servers, "
                        f"meeting requirement of >= {min_raidas_required}.")
            return key_set

    logger.error(f"No key set found that meets the minimum RAIDA requirement of {min_raidas_required}.")
    return None

def _create_ip_to_index_map(global_network: RaidaNetwork) -> Dict[str, int]:
    """
    Creates a simple lookup table mapping a RAIDA IP address to its
    canonical 0-24 index.
    """
    ip_map = {}
    for i, endpoint in enumerate(global_network.primary):
        if endpoint:
            # The endpoint is "host:port", we only need the host/IP for mapping.
            host = endpoint.split(':')[0]
            ip_map[host] = i
    return ip_map


# -- Main DKE Function --

async def get_encryption_key(
    cs_config: DKEConfig,
    global_network: RaidaNetwork,
    wallet: Wallet,
    communicator: RaidaCommunicator,
    client_sn: bytes
) -> Optional[DKEResult]:
    """
    Orchestrates the full DKE process to derive a shared encryption key.
    """
    # 1. Intelligently select the best key set based on requirements
    key_set = _select_best_keyset(cs_config)
    if not key_set:
        return None

    logger.info(f"Starting DKE process using key set '{key_set.kid}' for CS_ID '{key_set.cs_id}'.")

    # 2. Get encryption coins from the wallet
    encryption_coins = wallet.get_coins_for_encryption(count=1)
    if not encryption_coins:
        logger.error("DKE failed: Could not get a coin from the wallet for encryption.")
        return None

    # 3. Prepare the common request payload
    timestamp = int(time.time())
    try:
        key_id_numeric = int(key_set.kid.replace('k', ''))
    except ValueError:
        logger.error(f"Invalid key set ID format: {key_set.kid}. Must be 'k' followed by a number.")
        return None
        
    payload = bytearray()
    payload.extend(key_set.cs_id.encode('utf-8').ljust(16, b'\0'))
    payload.append(key_id_numeric)
    payload.extend(client_sn)
    payload.extend(struct.pack(">Q", timestamp))

    # 4. Build the server list and packets using the correct RAIDA indices
    ip_to_index_map = _create_ip_to_index_map(global_network)
    
    full_server_list: List[Optional[str]] = [None] * config.TOTAL_RAIDA_SERVERS
    packets_to_send: List[bytes] = [b''] * config.TOTAL_RAIDA_SERVERS
    
    servers_in_keyset = 0
    for server in key_set.raida_servers:
        raida_idx = ip_to_index_map.get(server.host)
        
        if raida_idx is not None:
            servers_in_keyset += 1
            full_server_list[raida_idx] = str(server)
            try:
                packets_to_send[raida_idx] = protocol.build_request_packet(
                    raida_idx=raida_idx,
                    command_group=config.COMMAND_GROUP.COMMAND_GROUP_DKE,
                    command_code=config.DKECommand.COMMAND_GET_KEY_SHARE,
                    payload=payload,
                    encryption_coins=encryption_coins
                )
            except Exception as e:
                logger.error(f"Failed to build packet for RAIDA {raida_idx}: {e}")
                full_server_list[raida_idx] = None
        else:
            logger.warning(f"RAIDA server '{server.host}' from Content Server's DNS record "
                           "was not found in the global RAIDA network list. Skipping.")

    if servers_in_keyset == 0:
        logger.error("DKE failed: None of the RAIDA servers listed in the DNS record could be mapped to the global network.")
        return None

    # 5. Send requests concurrently to the identified RAIDAs
    responses = await communicator.send_requests_async(packets_to_send, full_server_list)

    # 6. Process responses, build bitmap, and combine key shares
    key_shares = []
    bitmap = 0
    for response in responses:
        if response.is_success and response.data and len(response.data) > 0:
            key_shares.append(response.data[0])
            bitmap |= (1 << response.raida_index)

    if not key_shares:
        logger.error("DKE failed: No valid key shares received from any RAIDA server.")
        return None

    logger.info(f"Received {len(key_shares)} key shares. RAIDA bitmap: {bitmap:025b}")
    
    combined_byte = 0
    for share in key_shares:
        combined_byte ^= share

    # 7. Expand the combined byte into the final AES-256 key using HKDF
    info_string = config.DKE_ENCRYPTION_INFO + client_sn + struct.pack(">Q", timestamp)
    
    final_key = kdf.hkdf_expand(
        prk=bytes([combined_byte]),
        info=info_string,
        length=32
    )
    
    if not final_key:
        logger.error("DKE failed: HKDF key expansion failed.")
        return None
    
    # --- NEW: Generate a new 5-byte KID for this derived key ---
    new_kid = os.urandom(5)
    logger.info(f"Successfully derived final encryption key and generated new KID: {new_kid.hex()}")

    logger.info("Successfully derived final encryption key.")
    
    return DKEResult(
        key=final_key,
        kid=new_kid, # Return the new KID
        bitmap=bitmap,
        timestamp=timestamp,
        client_sn=client_sn,
        key_id=key_set.kid,
        cs_id=key_set.cs_id
    )