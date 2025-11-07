# rke_client/raida/communicator.py

"""
Handles the actual network I/O with a list of RAIDA servers.

This module is the Python equivalent of the Go 'raida.go' file.
"""

import asyncio
import logging
from typing import List, Optional

from .. import config

logger = logging.getLogger(__name__)

# -- Data Structures --

class RaidaResponse:
    """A simple dataclass to hold the result from a single RAIDA server."""
    def __init__(self, raida_index: int, data: Optional[bytes] = None, error: Optional[Exception] = None):
        self.raida_index = raida_index
        self.data = data
        self.error = error
        self.is_success = data is not None and error is None

# -- Main Communicator Class --

class RaidaCommunicator:
    """
    Manages concurrent UDP communication with a list of RAIDA servers.
    """

    class _UDPProtocol(asyncio.DatagramProtocol):
        """Internal helper class for asyncio UDP communication."""
        def __init__(self, response_future: asyncio.Future):
            self.response_future = response_future
            self.transport = None

        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            if not self.response_future.done():
                self.response_future.set_result(data)
            if self.transport: self.transport.close()

        def error_received(self, exc):
            if not self.response_future.done():
                self.response_future.set_exception(exc)
            if self.transport: self.transport.close()

        def connection_lost(self, exc):
            # If the connection is lost before a datagram is received,
            # it indicates a timeout or network issue.
            if not self.response_future.done():
                self.response_future.set_exception(exc or ConnectionRefusedError("Connection lost unexpectedly"))

    async def _send_one(self, raida_index: int, host: str, port: int, packet: bytes) -> RaidaResponse:
        """
        Sends a single UDP packet to one RAIDA server and awaits a response.
        """
        if not packet:
            # If an empty packet was passed (due to a build error), don't send.
            return RaidaResponse(raida_index=raida_index, error=ValueError("Empty packet provided"))
            
        loop = asyncio.get_running_loop()
        response_future = loop.create_future()
        
        try:
            transport, _ = await loop.create_datagram_endpoint(
                lambda: self._UDPProtocol(response_future),
                remote_addr=(host, port)
            )

            transport.sendto(packet)

            response_data = await asyncio.wait_for(
                response_future, timeout=config.RAIDA_REQUEST_TIMEOUT_SECONDS
            )
            return RaidaResponse(raida_index=raida_index, data=response_data)

        except asyncio.TimeoutError:
            logger.warning(f"RAIDA {raida_index} ({host}:{port}) timed out.")
            return RaidaResponse(raida_index=raida_index, error=asyncio.TimeoutError(f"RAIDA {raida_index} timed out"))
        except OSError as e:
            logger.warning(f"Network error for RAIDA {raida_index} ({host}:{port}): {e}")
            return RaidaResponse(raida_index=raida_index, error=e)
        except Exception as e:
            logger.error(f"Unexpected error for RAIDA {raida_index} ({host}:{port}): {e}")
            return RaidaResponse(raida_index=raida_index, error=e)

    async def send_requests_async(
        self,
        packets: List[bytes],
        server_list: List[Optional[str]]
    ) -> List[RaidaResponse]:
        """
        Sends multiple request packets to a list of RAIDA servers concurrently.
        """
        if len(packets) != config.TOTAL_RAIDA_SERVERS or len(server_list) != config.TOTAL_RAIDA_SERVERS:
            raise ValueError(f"Packets and server_list must both have {config.TOTAL_RAIDA_SERVERS} items.")

        tasks = []
        for i in range(config.TOTAL_RAIDA_SERVERS):
            endpoint = server_list[i]
            if endpoint:
                try:
                    host, port_str = endpoint.split(':', 1)
                    port = int(port_str)
                    task = asyncio.create_task(self._send_one(i, host, port, packets[i]))
                    tasks.append(task)
                except (ValueError, IndexError):
                    # Create a completed future with an error for malformed endpoints
                    future = asyncio.Future()
                    future.set_result(RaidaResponse(i, error=ValueError(f"Malformed endpoint: {endpoint}")))
                    tasks.append(future)
            else:
                # Create a completed future with an error for missing servers
                future = asyncio.Future()
                future.set_result(RaidaResponse(i, error=ConnectionRefusedError("No server specified")))
                tasks.append(future)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results, handling exceptions that might be returned by gather
        final_results = []
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                final_results.append(RaidaResponse(i, error=res))
            else:
                final_results.append(res)
        
        # Ensure the results are sorted by raida_index for consistency
        final_results.sort(key=lambda r: r.raida_index)
        
        successful_count = sum(1 for r in final_results if r.is_success)
        logger.info(f"RAIDA communication complete. Received {successful_count}/{config.TOTAL_RAIDA_SERVERS} successful responses.")

        return final_results