# # rke_client/content_server/protocol.py

# """
# Handles the creation of secure Type 6 protocol packets for communicating
# with the Content Server. This implementation strictly follows the detailed
# Type 6 specification document.
# """

# import logging
# import os
# import struct
# from typing import Optional

# from .. import config
# from ..crypto import aes

# logger = logging.getLogger(__name__)

# def create_initial_type6_packet(
#     encryption_key: bytes,
#     kid: bytes,
#     cs_id: str,
#     key_id: str,
#     client_sn: bytes,
#     timestamp: int,
#     raida_bitmap: int,
#     payload: bytes
# ) -> Optional[bytes]:
#     """
#     Creates the first Type 6 packet for a full DKE handshake.
#     This packet is unique because its nonce field is a structured data block
#     used by the server to derive the same encryption_key.

#     Args:
#         encryption_key (bytes): The RKE-derived key used to encrypt the payload.
#         kid (bytes): The new, random 5-byte Key ID for this key.
#         cs_id (str): The Content Server ID from DNS.
#         key_id (str): The key set identifier (e.g., 'k1') from DNS.
#         client_sn (bytes): A 5-byte random identifier for this client instance.
#         timestamp (int): The Unix timestamp from the key derivation process.
#         raida_bitmap (int): The bitmap indicating which RAIDAs responded.
#         payload (bytes): The data to be encrypted (tickets, client_nonce, etc.).

#     Returns:
#         Optional[bytes]: The full, ready-to-send Type 6 packet, or None on failure.
#     """
#     if len(kid) != 5:
#         logger.error(f"Invalid KID length: {len(kid)}. Must be 5 bytes for the header.")
#         return None
#     if len(client_sn) != 5:
#         logger.error(f"Invalid Client SN length: {len(client_sn)}. Must be 5 bytes.")
#         return None

#     try:
#         # 1. Construct the 32-byte header according to the Type 6 specification.
#         header = bytearray(32)
        
#         # Byte 0: Version/Encryption Type (always 0x06 for this protocol).
#         header[0] = 0x06
        
#         # Bytes 1-2: Body Length (a 16-bit unsigned integer in big-endian format).
#         struct.pack_into(">H", header, 1, len(payload))
        
#         # Bytes 3-7: Key ID (KI), the 5-byte random identifier for the encryption_key.
#         header[3:8] = kid

#         # --- Structured Nonce (Bytes 8-31) ---
#         # This block contains the public data the server needs to derive the key.
#         key_id_numeric = int(key_id.replace('k', ''))
#         cs_id_bytes = cs_id.encode('utf-8')

#         # Bytes 8-11: RAIDA Bitmap (32-bit unsigned integer, big-endian).
#         struct.pack_into(">I", header, 8, raida_bitmap)
        
#         # Bytes 12-19: Timestamp (64-bit unsigned integer, big-endian).
#         struct.pack_into(">Q", header, 12, timestamp)
        
#         # Bytes 20-24: Client_SN (5 bytes).
#         header[20:25] = client_sn
        
#         # Byte 25: Key_ID (the 1-byte 'k' number, e.g., 1 for 'k1').
#         header[25] = key_id_numeric
        
#         # Bytes 26-31: First 6 bytes of the CS_ID.
#         header[26:32] = cs_id_bytes.ljust(6, b'\0')[:6]

#         # 2. Encrypt the payload using the encryption_key.
#         # The AES-CTR nonce is the first 16 bytes of the structured nonce field.
#         nonce_for_aes = bytes(header[8:24])
        
#         encrypted_payload = aes.aes_ctr_crypt(encryption_key, payload, nonce_for_aes)
#         if encrypted_payload is None:
#             raise ValueError("AES-CTR encryption of payload failed.")

#         # 3. Assemble the final packet by combining the header and the encrypted body.
#         return bytes(header) + encrypted_payload

#     except Exception as e:
#         logger.error(f"Failed to create initial Type 6 packet: {e}")
#         return None


# def create_session_packet(
#     session_key: bytes,
#     kid: bytes,
#     session_token: bytes,
#     payload: bytes
# ) -> Optional[bytes]:
#     """
#     Creates a subsequent Type 6 packet for an established, ongoing session.
#     These packets use the temporary session_key for encryption and include the
#     session_token for server-side state lookup.

#     Args:
#         session_key (bytes): The temporary key derived during the handshake.
#         kid (bytes): The original 5-byte Key ID of the master key.
#         session_token (bytes): The 32-byte token provided by the server.
#         payload (bytes): The application data to send (e.g., a command, a message).

#     Returns:
#         Optional[bytes]: The full, ready-to-send Type 6 packet, or None on failure.
#     """
#     if len(kid) != 5:
#         logger.error(f"Invalid KID length: {len(kid)}. Must be 5 bytes.")
#         return None
#     if len(session_token) != 32:
#         logger.error(f"Invalid session token length: {len(session_token)}. Must be 32 bytes.")
#         return None
        
#     try:
#         # Per the final protocol, the server uses the session_token to find the
#         # correct session key. We prepend it to the user's payload before encryption.
#         full_payload = session_token + payload

#         header = bytearray(32)
        
#         # Bytes 0-2: Version and Body Length (reflects the combined payload length).
#         header[0] = 0x06
#         struct.pack_into(">H", header, 1, len(full_payload))
        
#         # Bytes 3-7: The KID remains the same, identifying the master key context.
#         header[3:8] = kid

#         # Bytes 8-31: For session packets, this MUST be a completely random nonce
#         # to ensure the security of the session_key (prevent nonce reuse).
#         random_nonce_material = os.urandom(24)
#         header[8:32] = random_nonce_material

#         # The AES-CTR nonce is the first 16 bytes of the random nonce material.
#         nonce_for_aes = random_nonce_material[:16]
        
#         # Encrypt the full payload (token + data) using the temporary session_key.
#         encrypted_payload = aes.aes_ctr_crypt(session_key, full_payload, nonce_for_aes)
#         if encrypted_payload is None:
#             raise ValueError("AES-CTR encryption of payload failed.")

#         return bytes(header) + encrypted_payload
        
#     except Exception as e:
#         logger.error(f"Failed to create session packet: {e}")
#         return None


# rke_client/content_server/protocol.py

"""
Handles the creation of secure Type 6 protocol packets for communicating
with the Content Server.
"""

import logging
import os
import struct
from typing import List, Optional

from .. import config
from ..crypto import aes, kdf
from ..raida.keyshare import DKEResult
from .session import Session 

logger = logging.getLogger(__name__)

def create_combined_auth_packet(
    dke_result: DKEResult,
    cc_sn: int,
    cc_denomination: int,
    session_identifier: bytes,
    tickets: List[Optional[bytes]]
) -> Optional[bytes]:
    """
    Creates the single Type 6 packet that performs both key registration (via a
    structured nonce in the header) and session authentication (via a payload
    containing tickets and a session identifier).
    """
    try:
        # 1. Construct the unencrypted part of the payload (before HMAC)
        payload_no_hmac = bytearray()
        payload_no_hmac.append(cc_denomination)
        payload_no_hmac.extend(struct.pack(">I", cc_sn))
        payload_no_hmac.extend(b'\x00\x00') # Padding
        payload_no_hmac.extend(session_identifier)
        for ticket in tickets:
            payload_no_hmac.extend(ticket if ticket else b'\x00\x00\x00\x00')

        # 2. Calculate HMAC and create the full payload
        hmac = kdf.hmac_sha256(dke_result.encryption_key, bytes(payload_no_hmac))
        full_payload = payload_no_hmac + hmac

        # 3. Construct the Type 6 Header with the STRUCTURED NONCE
        header = bytearray(32)
        header[0] = 0x06
        struct.pack_into(">H", header, 1, len(full_payload))
        header[3:8] = dke_result.kid

        # This block contains the public data the server needs to derive the key.
        key_id_numeric = int(dke_result.key_id.replace('k', ''))
        cs_id_bytes = dke_result.cs_id.encode('utf-8')

        struct.pack_into(">I", header, 8, dke_result.raida_bitmap)
        struct.pack_into(">Q", header, 12, dke_result.timestamp)
        header[20:25] = dke_result.client_sn
        header[25] = key_id_numeric
        header[26:32] = cs_id_bytes.ljust(6, b'\0')[:6]

        # The AES-CTR nonce is the first 16 bytes of the structured nonce field.
        nonce_for_aes = bytes(header[8:24])
        
        # 4. Encrypt and assemble the final packet
        encrypted_payload = aes.aes_ctr_crypt(dke_result.encryption_key, full_payload, nonce_for_aes)
        final_packet = header + encrypted_payload
        final_packet.extend(struct.pack(">H", 0xE3E3))
        
        return bytes(final_packet)
    except Exception as e:
        logger.error(f"Failed to build combined authentication packet: {e}", exc_info=True)
        return None

def create_command_packet(
    session: Session,
    command_payload: bytes
) -> Optional[bytes]:
    """
    Creates a subsequent packet for sending commands within an established session.
    The header nonce for this packet MUST be random.
    """
    try:
        # 1. Construct the payload (session ID + command)
        payload_no_hmac = bytearray()
        payload_no_hmac.extend(session.session_identifier)
        payload_no_hmac.extend(command_payload)

        # 2. Calculate HMAC and create the full payload
        hmac = kdf.hmac_sha256(session.encryption_key, bytes(payload_no_hmac))
        full_payload = payload_no_hmac + hmac

        # 3. Construct Header with a RANDOM nonce
        header = bytearray(32)
        header[0] = 0x06
        struct.pack_into(">H", header, 1, len(full_payload))
        header[3:8] = session.kid
        random_nonce_material = os.urandom(24)
        header[8:32] = random_nonce_material
        nonce_for_aes = random_nonce_material[:16]

        # 4. Encrypt and assemble the final packet
        encrypted_payload = aes.aes_ctr_crypt(session.encryption_key, full_payload, nonce_for_aes)
        final_packet = header + encrypted_payload
        final_packet.extend(struct.pack(">H", 0xE3E3))

        return bytes(final_packet)
    except Exception as e:
        logger.error(f"Failed to build command packet: {e}", exc_info=True)
        return None