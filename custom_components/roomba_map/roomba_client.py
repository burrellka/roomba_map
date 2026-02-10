"""
Roomba Client Wrapper
Temporarily using simple roombapy client for testing
"""

import logging
from typing import Dict, Any
from .simple_roomba_client import SimpleRoombaClient

_LOGGER = logging.getLogger(__name__)

class RoombaClient:
    """Wrapper for testing roombapy vs embedded client."""
    
    def __init__(self, host: str, blid: str, password: str, hass=None):
        self.host = host
        self._blid = blid
        self._password = password
        self._client = SimpleRoombaClient(host, blid, password)
        self._last_data = {"state": {}, "map": None}

    async def async_connect(self) -> bool:
        """Connect to the Roomba."""
        return await self._client.async_connect()

    async def async_disconnect(self):
        """Disconnect from the Roomba."""
        await self._client.async_disconnect()

    async def async_fetch_all(self) -> Dict[str, Any]:
        """Fetch all data from the Roomba."""
        try:
            data = await self._client.async_fetch_all()
            self._last_data = data
            return data
        except Exception as err:
            _LOGGER.error(f"Failed to fetch Roomba data: {err}")
            return self._last_data

    async def async_start(self):
        """Start cleaning."""
        return await self._client.async_start()

    async def async_pause(self):
        """Pause cleaning."""
        return await self._client.async_pause()

    async def async_stop(self):
        """Stop cleaning."""
        return await self._client.async_stop()

    async def async_return_to_base(self):
        """Return to base."""
        return await self._client.async_return_to_base()

    @property
    def connected(self) -> bool:
        """Check if connected."""
        return self._client.connected
