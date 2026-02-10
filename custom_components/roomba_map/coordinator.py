import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .roomba_client import RoombaClient

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)

class RoombaDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(
            hass, 
            _LOGGER, 
            name="Roomba Map", 
            update_interval=timedelta(seconds=entry.options.get("scan_interval", 60))
        )
        self.entry = entry
        
        self.client = RoombaClient(
            entry.data["host"],
            entry.data["blid"],
            entry.data["password"],
            hass  # Pass hass instance for callbacks
        )

    async def _async_update_data(self):
        try:
            # Ensure connection
            if not self.client.connected:
                await self.client.async_connect()
            
            data = await self.client.async_fetch_all()
            if not data:
                raise UpdateFailed("No data received from Roomba")
            return data
        except Exception as err:
            _LOGGER.error("Error fetching Roomba data: %s", err)
            raise UpdateFailed(f"Error communicating with Roomba: {err}")

    async def async_shutdown(self):
        """Shutdown the coordinator."""
        if self.client:
            await self.client.async_disconnect()
