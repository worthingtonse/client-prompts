# rke_client/raida/discovery.py

"""
Handles the discovery of the global RAIDA network by contacting a
consensus of trusted "Guardian" servers.

This module is the Python equivalent of the Go 'guardians.go' file.
"""

import asyncio
import hashlib
import logging
import ssl
from collections import Counter
from typing import Dict, List, Optional, Tuple

from .. import config

# Configure a logger for this module
logger = logging.getLogger(__name__)

# -- Data Structures --

class RaidaNetwork:
    """A dataclass to hold the discovered primary and backup RAIDA lists."""
    def __init__(self):
        # Initialize with None placeholders to detect incomplete lists
        self.primary: List[Optional[str]] = [None] * config.TOTAL_RAIDA_SERVERS
        self.backup: List[Optional[str]] = [None] * config.TOTAL_RAIDA_SERVERS

class GuardianResponse:
    """Holds the result from a single Guardian query."""
    def __init__(self, name: str):
        self.name = name
        self.success = False
        self.network = RaidaNetwork()
        self.hash = ""

# -- Main Discovery Logic --

async def _fetch_from_guardian(guardian_host: str, coin_id: int) -> Optional[GuardianResponse]:
    """
    Asynchronously fetches and parses the hosts file from a single Guardian.
    """
    url_path = f"/coin{coin_id}.txt"
    response = GuardianResponse(name=guardian_host)
    
    try:
        # Create a non-verifying SSL context for compatibility, as in guardians.go
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Using a timeout for the entire connection operation
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(guardian_host, 443, ssl=ssl_context),
            timeout=config.GUARDIAN_HTTP_TIMEOUT
        )

        request = (
            f"GET {url_path} HTTP/1.1\r\n"
            f"Host: {guardian_host}\r\n"
            "Connection: close\r\n\r\n"
        )
        
        writer.write(request.encode('utf-8'))
        await writer.drain()

        # Read status line
        status_line = await reader.readline()
        if not status_line.startswith(b"HTTP/1.1 200 OK"):
            logger.warning(f"Guardian {guardian_host} returned non-200 status: {status_line.decode(errors='ignore').strip()}")
            writer.close()
            return None

        # Skip headers
        while await reader.readline() != b'\r\n':
            pass

        body_bytes = await reader.read()
        writer.close()
        body_str = body_bytes.decode('utf-8', errors='ignore')
        
        if _parse_guardian_body(body_str, response):
            response.success = True
            return response

    except asyncio.TimeoutError:
        logger.warning(f"Timeout connecting to or reading from Guardian {guardian_host}")
    except Exception as e:
        logger.error(f"Error fetching from Guardian {guardian_host}: {e}")
    
    return None

def _parse_guardian_body(body: str, response: GuardianResponse) -> bool:
    """
    Parses the raw text body from a Guardian's hosts.txt file.
    This logic is ported from SetRaidas() in guardians.go.
    """
    lines = body.strip().split('\n')
    
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 2: continue

        endpoint_parts = parts[0].split(':')
        trailer_parts = parts[1].split('-')
        
        if len(endpoint_parts) != 2 or len(trailer_parts) != 4: continue
            
        try:
            host, port_str = endpoint_parts[0], endpoint_parts[1]
            port = int(port_str)
            raida_idx = int(trailer_parts[0])
            is_primary = trailer_parts[3] == "P"
            
            if not (0 <= raida_idx < config.TOTAL_RAIDA_SERVERS): continue
                
            full_endpoint = f"{host}:{port}"
            
            if is_primary:
                response.network.primary[raida_idx] = full_endpoint
            else: # Assuming "M" for Mirror/Backup
                response.network.backup[raida_idx] = full_endpoint
                
        except (ValueError, IndexError):
            logger.warning(f"Skipping malformed line from {response.name}: {line}")
            continue
            
    # Verify that all servers were found in the file
    if None in response.network.primary or None in response.network.backup:
        logger.warning(f"Guardian {response.name} provided an incomplete RAIDA list.")
        return False
        
    # --- CORRECTED HASHING LOGIC ---
    # The Go code joins the primary and backup lists and calculates an MD5 hash.
    # This logic is now replicated exactly.
    primary_list_str = "".join(response.network.primary)
    backup_list_str = "".join(response.network.backup)
    full_list_str = primary_list_str + backup_list_str

    # Calculate MD5 hash and get the hexadecimal digest string.
    md5_hash = hashlib.md5(full_list_str.encode('utf-8')).hexdigest()
    response.hash = md5_hash
    # --- END CORRECTION ---

    return True

async def discover_network(coin_id: int = 4) -> Optional[RaidaNetwork]:
    """
    Discovers the global RAIDA network by querying Guardians and establishing a consensus.

    Args:
        coin_id (int): The coin ecosystem ID to query for (e.g., 4 for CloudCoin).

    Returns:
        Optional[RaidaNetwork]: A RaidaNetwork object on success, or None on failure.
    """
    logger.info("Starting global RAIDA network discovery via Guardians...")
    
    tasks = [_fetch_from_guardian(host, coin_id) for host in config.GUARDIAN_SERVERS]
    results = await asyncio.gather(*tasks)
    
    successful_responses = [res for res in results if res and res.success]
    
    if len(successful_responses) < 3:
        logger.error("Failed to get successful responses from at least 3 Guardians. Cannot establish consensus.")
        return None
        
    # Find consensus by counting the matching MD5 hashes
    hash_counts = Counter(res.hash for res in successful_responses)
    
    consensus_network: Optional[RaidaNetwork] = None
    for res_hash, count in hash_counts.items():
        if count >= 3:
            logger.info(f"Consensus found! {count} Guardians agree on the network configuration.")
            # Find the first response with this hash and use its network data
            for res in successful_responses:
                if res.hash == res_hash:
                    consensus_network = res.network
                    break
            break
            
    if not consensus_network:
        logger.error("Failed to find a consensus among Guardians. At least 3 must agree.")
        return None
        
    logger.info("Global RAIDA network discovered successfully.")
    return consensus_network