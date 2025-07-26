import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .roomba_client import RoombaClient

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)

class RoombaDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(hass, _LOGGER, name="Roomba Map", update_interval=SCAN_INTERVAL)
        self.entry = entry
        self.client = RoombaClient(
            entry.data["host"],
            entry.data["username"],
            entry.data["password"],
        )

    async def _async_update_data(self):
        try:
            return await self.client.async_fetch_all()
        except Exception as err:
            _LOGGER.error("Error fetching Roomba data: %s", err)
            raise UpdateFailed(err)
