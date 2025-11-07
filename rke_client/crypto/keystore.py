# rke_client/crypto/keystore.py

"""
Provides a secure mechanism for storing and retrieving derived encryption keys
and managing the mapping between Content Server IDs and Key IDs.
"""

import base64
import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, Optional

# Use a try-except block to guide the user if libraries are not installed.
try:
    import keyring
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
except ImportError:
    print("FATAL ERROR: 'pycryptodome' and 'keyring' are required. Please install them using: pip install pycryptodome keyring")
    exit(1)

from .. import config

# Configure a logger for this module
logger = logging.getLogger(__name__)

# Constants for identifying our secret in the OS keychain
KEYRING_SERVICE_NAME = "rke_client_service"
KEYRING_USERNAME = "master_secret"
KEY_MAP_FILENAME = "key_map.json"


class KeyStore:
    """
    Manages the secure storage, retrieval, and lifecycle of encryption keys.
    """

    def __init__(self, storage_path: Path = config.KEYS_DIR):
        """
        Initializes the KeyStore.

        Args:
            storage_path (Path): The directory path to store encrypted key files.
        """
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.key_map_path = self.storage_path / KEY_MAP_FILENAME
        self._master_secret = self._get_or_create_master_secret()
        if not self._master_secret:
            raise RuntimeError("Failed to get or create a master secret from the OS keychain.")

    def _get_or_create_master_secret(self) -> Optional[bytes]:
        """
        Retrieves the master secret from the OS keychain. If it doesn't exist,
        it generates a new one, stores it, and then returns it.
        """
        try:
            encoded_secret = keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME)
            if encoded_secret:
                logger.debug("Master secret retrieved from OS keychain.")
                return base64.urlsafe_b64decode(encoded_secret)
            
            logger.info("No master secret found in OS keychain. Generating a new one.")
            new_secret_bytes = get_random_bytes(32)
            encoded_new_secret = base64.urlsafe_b64encode(new_secret_bytes).decode('ascii')
            keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_USERNAME, encoded_new_secret)
            logger.info("New master secret has been generated and securely stored.")
            return new_secret_bytes
        except Exception as e:
            logger.critical(f"A critical error occurred while accessing the OS keychain: {e}")
            logger.critical("Please ensure you have a supported keychain/credential backend installed and configured.")
            return None

    def _read_key_map(self) -> Dict[str, str]:
        """Reads the CS_ID -> KID mapping file."""
        if not self.key_map_path.is_file():
            return {}
        try:
            with open(self.key_map_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _write_key_map(self, key_map: Dict[str, str]):
        """Writes the CS_ID -> KID mapping file."""
        try:
            with open(self.key_map_path, "w") as f:
                json.dump(key_map, f, indent=2)
        except OSError as e:
            logger.error(f"Failed to write key map file: {e}")

    def save_kid_for_csid(self, cs_id: str, kid: bytes):
        """Saves or updates the KID associated with a given CS_ID."""
        key_map = self._read_key_map()
        key_map[cs_id] = kid.hex()
        self._write_key_map(key_map)
        logger.debug(f"Updated key map: CS_ID '{cs_id}' now maps to KID '{kid.hex()}'.")

    def get_kid_for_csid(self, cs_id: str) -> Optional[bytes]:
        """Retrieves the last known KID for a given CS_ID."""
        key_map = self._read_key_map()
        kid_hex = key_map.get(cs_id)
        if kid_hex:
            try:
                return bytes.fromhex(kid_hex)
            except (ValueError, TypeError):
                return None
        return None

    def _get_key_filepath(self, kid: bytes) -> Path:
        """Generates a consistent, safe filename for a given Key ID."""
        return self.storage_path / f"{kid.hex()}.key"

    def save_key(self, kid: bytes, key: bytes, ttl: int = config.DEFAULT_KEY_TTL_SECONDS):
        """
        Encrypts and saves a derived encryption key to the filesystem.
        """
        if not self._master_secret:
            logger.error("Cannot save key: Master secret is not available.")
            return

        filepath = self._get_key_filepath(kid)
        logger.debug(f"Saving new key with KID '{kid.hex()}' to {filepath}")
        try:
            header = kid
            cipher = AES.new(self._master_secret, AES.MODE_GCM)
            cipher.update(header)
            ciphertext, tag = cipher.encrypt_and_digest(key)
            key_data = {
                "kid": kid.hex(),
                "created_at": int(time.time()),
                "ttl": ttl,
                "header": header.hex(),
                "nonce": cipher.nonce.hex(),
                "ciphertext": ciphertext.hex(),
                "tag": tag.hex()
            }
            with open(filepath, "w") as f:
                json.dump(key_data, f)
            logger.info(f"Successfully saved and encrypted key with KID '{kid.hex()}'.")
        except Exception as e:
            logger.error(f"Failed to save key with KID '{kid.hex()}': {e}")

    def load_key(self, kid: bytes) -> Optional[bytes]:
        """
        Loads, validates, and decrypts a key from the filesystem.
        """
        if not self._master_secret:
            logger.error("Cannot load key: Master secret is not available.")
            return None
        filepath = self._get_key_filepath(kid)
        if not filepath.is_file():
            logger.debug(f"No cached key found for KID '{kid.hex()}'.")
            return None
        try:
            with open(filepath, "r") as f:
                key_data = json.load(f)
            if time.time() > key_data["created_at"] + key_data["ttl"]:
                logger.info(f"Key with KID '{kid.hex()}' has expired. Deleting.")
                filepath.unlink()
                return None
            header, nonce, ciphertext, tag = (
                bytes.fromhex(key_data["header"]),
                bytes.fromhex(key_data["nonce"]),
                bytes.fromhex(key_data["ciphertext"]),
                bytes.fromhex(key_data["tag"]),
            )
            cipher = AES.new(self._master_secret, AES.MODE_GCM, nonce=nonce)
            cipher.update(header)
            plaintext_key = cipher.decrypt_and_verify(ciphertext, tag)
            logger.info(f"Successfully loaded and decrypted key for KID '{kid.hex()}'.")
            return plaintext_key
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Key file for KID '{kid.hex()}' is corrupt or tampered. Deleting. Error: {e}")
            filepath.unlink()
            return None
        except Exception as e:
            logger.error(f"Failed to load key for KID '{kid.hex()}': {e}")
            return None

    def delete_key(self, kid: bytes):
        """
        Deletes a cached key file from the filesystem.
        """
        filepath = self._get_key_filepath(kid)
        if filepath.is_file():
            try:
                filepath.unlink()
                logger.info(f"Deleted stale/invalid key for KID '{kid.hex()}'.")
            except OSError as e:
                logger.error(f"Failed to delete key file for '{kid.hex()}': {e}")