import logging
from homeassistant.components.camera import Camera
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RoombaMapCamera(coordinator, entry)], False)

class RoombaMapCamera(CoordinatorEntity, Camera):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        Camera.__init__(self)
        self._entry = entry
        self._attr_name = f"Roomba Map {entry.data['host']}"
        self._attr_unique_id = f"{entry.entry_id}_camera"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": f"Roomba {self._entry.data['host']}",
            "manufacturer": "iRobot",
            "model": "Roomba",
            "sw_version": "1.0",
        }

    @property
    def available(self):
        """Return if the camera is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None and
            self.coordinator.data.get("map") is not None
        )

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        """Return camera image."""
        try:
            if not self.coordinator.data or "map" not in self.coordinator.data:
                _LOGGER.debug("No map data available")
                return None
                
            map_data = self.coordinator.data["map"]
            if map_data is None:
                _LOGGER.debug("Map data is None")
                return None
                
            if isinstance(map_data, bytes):
                return map_data
            elif hasattr(map_data, "image") and isinstance(map_data.image, bytes):
                return map_data.image
            else:
                _LOGGER.warning("Map data is not in expected format: %s", type(map_data))
                return None
                
        except Exception as err:
            _LOGGER.error("Error retrieving camera image: %s", err)
            return None

    @property
    def content_type(self) -> str:
        """Return the content type of the image."""
        return "image/png"
