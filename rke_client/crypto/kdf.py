# rke_client/crypto/kdf.py

"""
Provides a clean implementation of the HKDF-Expand key derivation function.

This module is used to derive cryptographic keys from a shared secret, such as
expanding the single combined byte into a full 256-bit encryption key during
the DKE process.
"""

import hashlib
import hmac
import logging
from typing import Optional

# Configure a logger for this module
logger = logging.getLogger(__name__)

def hkdf_expand(prk: bytes, info: bytes, length: int) -> Optional[bytes]:
    """
    Implements the HKDF-Expand function using HMAC-SHA256, as per RFC 5869.

    This function is used to expand a pseudorandom key (PRK) into a longer
    output keying material (OKM) of the desired length.

    Args:
        prk (bytes): A pseudorandom key of at least 32 bytes. This is the
                     "Input Keying Material" for the expansion phase.
        info (bytes): Optional context and application-specific information. This
                      is the "info" string used for domain separation.
        length (int): The desired length in bytes of the output key.

    Returns:
        Optional[bytes]: The derived key of the specified length, or None on failure.
    """
    if not isinstance(prk, bytes) or not isinstance(info, bytes) or not isinstance(length, int):
        logger.error("Invalid input types for hkdf_expand.")
        return None
    
    hash_len = hashlib.sha256().digest_size  # 32 bytes for SHA-256
    
    if length > 255 * hash_len:
        logger.error(f"Cannot produce an output key longer than {255 * hash_len} bytes.")
        return None

    try:
        # Calculate the number of blocks needed to generate the desired key length
        num_blocks = (length + hash_len - 1) // hash_len
        
        output_key_material = b""
        previous_block = b""
        
        for i in range(1, num_blocks + 1):
            # Construct the message for the HMAC function:
            # T(i) = HMAC-Hash(PRK, T(i-1) | info | i)
            message = previous_block + info + bytes([i])
            
            # Calculate the next block of the key material
            h = hmac.new(prk, message, hashlib.sha256)
            current_block = h.digest()
            
            output_key_material += current_block
            previous_block = current_block
            
        # Return only the required number of bytes
        return output_key_material[:length]

    except Exception as e:
        logger.error(f"An unexpected error occurred during HKDF-Expand: {e}")
        return None