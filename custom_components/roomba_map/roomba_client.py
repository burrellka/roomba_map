import logging
from roombapy import Roomba

_LOGGER = logging.getLogger(__name__)

class RoombaClient:
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self._username = username
        self._password = password
        self._roomba = None

    async def async_connect(self):
        if self._roomba:
            return
        try:
            self._roomba = Roomba(address=self.host, blid=self._username, password=self._password)
            await self._roomba.connect()
            await self._roomba.subscribe()
            _LOGGER.info("Connected to Roomba %s via local MQTT", self.host)
        except Exception as err:
            _LOGGER.error("Failed to connect locally to Roomba %s: %s", self.host, err)
            raise

    async def async_fetch_all(self):
        await self.async_connect()
        try:
            state = await self._roomba.get_state()
        except Exception as err:
            _LOGGER.error("Failed to fetch Roomba state: %s", err)
            state = {}

        map_png = None
        if hasattr(self._roomba, "get_map_png"):
            try:
                map_png = await self._roomba.get_map_png()
            except Exception as err:
                _LOGGER.warning("Failed to fetch map image: %s", err)

        return {"state": state, "map": map_png}
