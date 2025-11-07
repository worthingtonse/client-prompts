# rke_client/raida/protocol.py

"""
Handles the low-level creation of raw byte packets for communicating with the
RAIDA network. This includes constructing headers, handling different encryption
types, and generating authentication data.

This module is the Python equivalent of the Go 'packet.go' file.
"""

import hashlib
import hmac
import logging
import os
import struct
from typing import List

from .. import config
from ..crypto import aes
from ..wallet.cloudcoin import CloudCoin

logger = logging.getLogger(__name__)

def _crc32b(data: bytes) -> int:
    """
    Calculates the CRC32 checksum using the specific polynomial (0xEDB88320).
    This is a direct port of the Crc32b function from the Go client's utils
    to ensure the checksum matches exactly what the RAIDA server expects.
    """
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            mask = -(crc & 1)
            crc = (crc >> 1) ^ (0xEDB88320 & mask)
    return ~crc & 0xFFFFFFFF

def _get_challenge() -> bytes:
    """
    Creates the 16-byte unencrypted challenge header for legacy protocols.
    It consists of a 12-byte challenge and a 4-byte CRC32 checksum.
    This is a port of GetChallenge() from packet.go.
    """
    challenge = bytearray([0xEE] * 12)
    crc = _crc32b(bytes(challenge))
    
    # Pack the CRC as a 4-byte big-endian integer and append it.
    challenge.extend(struct.pack(">I", crc))
    return bytes(challenge)

def _get_nonce(sn: int) -> bytes:
    """
    Creates the 16-byte nonce for AES-CTR, based on the coin's serial number.
    """
    nonce = bytearray(16)
    nonce[3] = 0x11
    nonce[4] = 0x11
    sn_bytes = struct.pack(">I", sn)
    nonce[5:8] = sn_bytes[1:]
    return bytes(nonce)

def build_request_packet(
    raida_idx: int,
    command_group: config.COMMAND_GROUP,
    command_code: int,
    payload: bytes,
    encryption_coins: List[CloudCoin],
    shard_id: int = 0
) -> bytes:
    """
    Constructs a complete, encrypted RAIDA request packet.
    """
    if not encryption_coins:
        raise ValueError("At least one encryption coin is required.")

    key = b""
    encryption_type: config.ENCRYPTION_TYPE

    # --- 1. Determine Encryption Type and Derive Key ---
    if len(encryption_coins) == 2:
        # --- TYPE 5: AES-256 with two coins and HMAC ---
        encryption_type = config.ENCRYPTION_TYPE.ENCRYPTION_TYPE_AES_256_DOUBLE_KEY
        
        coin1_an_hex = encryption_coins[0].ans[raida_idx]
        coin2_an_hex = encryption_coins[1].ans[raida_idx]
        if not coin1_an_hex or not coin2_an_hex:
            raise ValueError(f"Missing AN for RAIDA {raida_idx} in one of the Type-5 encryption coins.")

        combined_an = bytes.fromhex(coin1_an_hex) + bytes.fromhex(coin2_an_hex)
        key = hashlib.sha256(combined_an).digest()

    elif len(encryption_coins) == 1:
        # --- TYPE 1: AES-128 with one coin ---
        encryption_type = config.ENCRYPTION_TYPE.ENCRYPTION_TYPE_AES
        
        an_hex = encryption_coins[0].ans[raida_idx]
        if not an_hex:
            raise ValueError(f"Missing AN for RAIDA {raida_idx} in Type-1 encryption coin.")
        key = bytes.fromhex(an_hex)
    
    else:
        raise ValueError("Invalid number of encryption coins. Must be 1 (Type 1) or 2 (Type 5).")

    # --- 2. Prepare and Encrypt Payload ---
    nonce = _get_nonce(encryption_coins[0].sn)
    
    body_to_encrypt = bytearray()
    
    # ** CORRECTION: Add logic to conditionally include Challenge or HMAC **
    if encryption_type == config.ENCRYPTION_TYPE.ENCRYPTION_TYPE_AES:
        # Type 1 and other legacy types prepend the CRC32 challenge.
        body_to_encrypt.extend(_get_challenge())
        body_to_encrypt.extend(payload)
    elif encryption_type == config.ENCRYPTION_TYPE.ENCRYPTION_TYPE_AES_256_DOUBLE_KEY:
        # Type 5 prepends the payload and appends an HMAC.
        body_to_encrypt.extend(payload)
        hmac_val = hmac.new(key, payload, hashlib.sha256).digest()
        body_to_encrypt.extend(hmac_val)

    encrypted_body = aes.aes_ctr_crypt(key, bytes(body_to_encrypt), nonce)
    if encrypted_body is None:
        raise RuntimeError("AES encryption failed.")

    # Append trailer bytes after encryption
    final_body = bytearray(encrypted_body)
    final_body.extend(b'\x3e\x3e')
    body_length = len(final_body)

    # --- 3. Construct Header ---
    header_size = config.RAIDA_REQUEST_HEADER_SIZE_LEGACY if encryption_type == config.ENCRYPTION_TYPE.ENCRYPTION_TYPE_AES else config.RAIDA_REQUEST_HEADER_SIZE_MODERN
    header = bytearray(header_size)

    # Common fields
    header[0] = 1  # VR
    header[2] = raida_idx
    header[4] = command_group.value
    header[5] = command_code
    struct.pack_into(">H", header, 6, config.COIN_ID)

    # Type-specific fields
    if encryption_type == config.ENCRYPTION_TYPE.ENCRYPTION_TYPE_AES:
        struct.pack_into("B", header, 16, encryption_type.value)
        struct.pack_into("B", header, 17, encryption_coins[0].denomination & 0xFF)
        struct.pack_into(">I", header, 18, encryption_coins[0].sn)
        struct.pack_into(">H", header, 22, body_length)
        header[24:32] = nonce[:8]
    elif encryption_type == config.ENCRYPTION_TYPE.ENCRYPTION_TYPE_AES_256_DOUBLE_KEY:
        struct.pack_into("B", header, 16, encryption_type.value)
        struct.pack_into(">H", header, 17, body_length)
        struct.pack_into("B", header, 19, encryption_coins[0].denomination & 0xFF)
        struct.pack_into(">I", header, 20, encryption_coins[0].sn)
        
        nonce_material = bytearray(24)
        struct.pack_into("B", nonce_material, 0, encryption_coins[1].denomination & 0xFF)
        struct.pack_into(">I", nonce_material, 1, encryption_coins[1].sn)
        nonce_material[5:] = os.urandom(19)
        header[24:48] = nonce_material

    # --- 4. Assemble Final Packet ---
    return bytes(header + final_body)