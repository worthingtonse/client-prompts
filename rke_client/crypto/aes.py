# rke_client/crypto/aes.py

"""
Provides a clean wrapper for AES-CTR encryption and decryption operations.

This module is the Python equivalent of the Go 'encryption.go' file, using
the robust and widely-trusted 'pycryptodome' library as its backend.
"""

import logging
from typing import Optional

# Use a try-except block to guide the user if the library is not installed.
try:
    from Crypto.Cipher import AES
except ImportError:
    print("FATAL ERROR: The 'pycryptodome' library is required. Please install it using: pip install pycryptodome")
    exit(1)

# Configure a logger for this module
logger = logging.getLogger(__name__)

def aes_ctr_crypt(key: bytes, data: bytes, nonce: bytes) -> Optional[bytes]:
    """
    Encrypts or decrypts a buffer using AES-CTR.

    In CTR mode, encryption and decryption are the same symmetric operation (XORing
    the data with the keystream). This function handles both AES-128 and AES-256
    based on the length of the provided key.

    Args:
        key (bytes): The encryption key. Must be 16 bytes (AES-128) or
                     32 bytes (AES-256).
        data (bytes): The data buffer to be encrypted or decrypted.
        nonce (bytes): The nonce to be used for the CTR mode operation. The RAIDA
                       protocol uses a 16-byte nonce.

    Returns:
        Optional[bytes]: The resulting ciphertext or plaintext on success,
                         or None on failure.
    """
    if len(key) not in [16, 32]:
        logger.error(f"Invalid AES key size: {len(key)}. Must be 16 or 32 bytes.")
        return None
    if len(nonce) != 16:
        logger.error(f"Invalid AES-CTR nonce size: {len(nonce)}. Must be 16 bytes for this protocol.")
        return None

    try:
        # Create a new AES cipher object in CTR mode
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        
        # Perform the XOR operation on the data
        processed_data = cipher.encrypt(data)
        
        return processed_data
    except Exception as e:
        logger.error(f"An unexpected error occurred during AES-CTR operation: {e}")
        return None