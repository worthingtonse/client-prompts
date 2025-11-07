# rke_client/dns_discovery.py

"""
Handles the discovery of a Content Server's DKE (Distributed Key Exchange)
capabilities by querying public DNS records.

This module is responsible for:
1.  Performing SRV queries to find the Content Server's host and port.
2.  Performing TXT queries to get the detailed DKE configuration, including
    available key sets and the specific list of RAIDA servers to contact.

This module executes Step 3 of the Master Flow.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import dns.resolver
import dns.exception

# Configure a logger for this module
logger = logging.getLogger(__name__)

# -- Data Structures for Parsed Configuration --

@dataclass
class RaidaServer:
    """Represents a single RAIDA server endpoint."""
    host: str
    port: int

    def __str__(self):
        return f"{self.host}:{self.port}"

@dataclass
class KeySet:
    """Represents a single DKE key set (e.g., 'k1', 'k2')."""
    kid: str  # The identifier, e.g., "k1"
    cs_id: str # The Content Server Identifier associated with this key
    raida_servers: List[RaidaServer] = field(default_factory=list)

@dataclass
class DKEConfig:
    """Holds the fully parsed DKE configuration for a Content Server."""
    domain: str
    target_host: Optional[str] = None
    target_port: Optional[int] = None
    key_sets: Dict[str, KeySet] = field(default_factory=dict)
    requirements: Dict[str, str] = field(default_factory=dict)
    challenge: Optional[str] = None


# -- Main Discovery Class --

class ContentServerDiscovery:
    """
    Performs DNS lookups to discover and parse a Content Server's DKE
    configuration.
    """
    def __init__(self, timeout: int = 5):
        """
        Initializes the discovery client.

        Args:
            timeout (int): DNS query timeout in seconds.
        """
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout

    def discover(self, domain: str) -> Optional[DKEConfig]:
        """
        Performs the full discovery process for a given domain.

        Args:
            domain (str): The Content Server's domain (e.g., "mail.example.com").

        Returns:
            Optional[DKEConfig]: A populated DKEConfig object on success,
                                 or None if discovery fails at any step.
        """
        logger.info(f"Starting DKE discovery for domain: {domain}")
        config = DKEConfig(domain=domain)

        # 1. Perform SRV lookup
        srv_records = self._query_srv(domain)
        if not srv_records:
            logger.error(f"SRV record lookup failed for {domain}. Cannot proceed.")
            return None

        # Use the first SRV record found (highest priority)
        config.target_host = str(srv_records[0].target).rstrip('.')
        config.target_port = srv_records[0].port
        logger.debug(f"SRV lookup successful. Target: {config.target_host}:{config.target_port}")

        # 2. Perform TXT lookup
        txt_records = self._query_txt(domain)
        if not txt_records:
            logger.error(f"TXT record lookup failed for {domain}. Cannot get DKE config.")
            return None

        # 3. Parse the TXT records into the config object
        self._parse_txt_records(txt_records, config)
        
        if not config.key_sets:
            logger.error(f"No valid key sets (e.g., 'k1', 'k2') found in TXT records for {domain}.")
            return None

        logger.info(f"DKE discovery for {domain} successful. Found {len(config.key_sets)} key set(s).")
        return config

    def _query_srv(self, domain: str) -> Optional[dns.resolver.Answer]:
        """Queries for the _rke._udp SRV record."""
        query_domain = f"_rke._udp.{domain}"
        try:
            logger.debug(f"Querying SRV record: {query_domain}")
            return self.resolver.resolve(query_domain, 'SRV')
        except dns.resolver.NoAnswer:
            logger.warning(f"No SRV records found for {query_domain}.")
        except dns.resolver.NXDOMAIN:
            logger.warning(f"The domain {query_domain} does not exist.")
        except dns.exception.Timeout:
            logger.error(f"DNS query for {query_domain} timed out.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during SRV query: {e}")
        return None

    def _query_txt(self, domain: str) -> Optional[dns.resolver.Answer]:
        """Queries for the TXT record at the same domain."""
        query_domain = f"_rke._udp.{domain}"
        try:
            logger.debug(f"Querying TXT record: {query_domain}")
            return self.resolver.resolve(query_domain, 'TXT')
        except dns.resolver.NoAnswer:
            logger.warning(f"No TXT records found for {query_domain}.")
        except dns.resolver.NXDOMAIN:
            logger.warning(f"The domain {query_domain} does not exist.")
        except dns.exception.Timeout:
            logger.error(f"DNS query for {query_domain} timed out.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during TXT query: {e}")
        return None

    def _parse_txt_records(self, records: dns.resolver.Answer, config: DKEConfig):
        """
        Parses the raw TXT record strings and populates the DKEConfig object.
        This parser is specifically designed to handle the DKE config format.
        """
        raw_text = b"".join(b"".join(r.strings) for r in records).decode('utf-8')
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        for line in lines:
            line = line.lower()  # Per spec, all values are case-insensitive
            parts = [part.strip() for part in line.split()]

            if not parts:
                continue

            # Case 1: Key ID definition (e.g., "k1 = 135.23872")
            if len(parts) == 3 and parts[1] == '=' and parts[0].startswith('k'):
                kid, cs_id = parts[0], parts[2]
                if kid not in config.key_sets:
                    config.key_sets[kid] = KeySet(kid=kid, cs_id=cs_id)
                else:
                    config.key_sets[kid].cs_id = cs_id
                logger.debug(f"Parsed KeySet definition: {kid} -> {cs_id}")
                continue

            # Case 2: Requirement (e.g., "required raidas>=16")
            if parts[0] == 'required' and len(parts) > 1:
                key = parts[1]
                value = "".join(parts[2:])
                config.requirements[key] = value
                logger.debug(f"Parsed requirement: {key} -> {value}")
                continue

            # Case 3: Challenge (e.g., "challenge = 02b5...")
            if parts[0] == 'challenge' and len(parts) == 3 and parts[1] == '=':
                config.challenge = parts[2]
                logger.debug(f"Parsed challenge: {config.challenge}")
                continue
            
            # Case 4: RAIDA server mapping (e.g., "94.130.179.247:50000 k1")
            if len(parts) >= 2:
                endpoint, kids = parts[0], parts[1:]
                try:
                    host, port_str = endpoint.split(':')
                    port = int(port_str)
                    server = RaidaServer(host=host, port=port)
                    
                    for kid in kids:
                        if kid in config.key_sets:
                            config.key_sets[kid].raida_servers.append(server)
                        else:
                            # Create a placeholder if the key was not pre-defined
                            config.key_sets[kid] = KeySet(kid=kid, cs_id="<undefined>")
                            config.key_sets[kid].raida_servers.append(server)
                            logger.warning(f"Found RAIDA mapping for undefined KeySet '{kid}'. Creating placeholder.")
                    
                    logger.debug(f"Parsed RAIDA mapping: {server} -> {kids}")

                except (ValueError, IndexError) as e:
                    logger.warning(f"Skipping malformed RAIDA server line: '{line}'. Error: {e}")
                    continue