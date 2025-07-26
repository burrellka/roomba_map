from homeassistant.components.vacuum import VacuumEntity, SUPPORT_START, SUPPORT_PAUSE, SUPPORT_RETURN_HOME
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RoombaMapVacuum(coordinator)], False)

class RoombaMapVacuum(VacuumEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def name(self):
        return "Roomba Map"

    @property
    def state(self):
        return self.coordinator.data["state"].get("state")

    @property
    def supported_features(self):
        return SUPPORT_START | SUPPORT_PAUSE | SUPPORT_RETURN_HOME

    async def async_start(self):
        await self.coordinator.client._roomba.start()

    async def async_pause(self):
        await self.coordinator.client._roomba.pause()

    async def async_return_to_base(self):
        await self.coordinator.client._roomba.home()
