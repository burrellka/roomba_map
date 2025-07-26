from homeassistant.components.camera import Camera
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RoombaMapCamera(coordinator)], False)

class RoombaMapCamera(Camera):
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def name(self):
        return "Roomba Map"

    async def camera_image(self):
        return self.coordinator.data.get("map")
