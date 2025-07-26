from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SENSORS = [
    ("battery_level", "battery_level", "%"),
    ("bin_status", "bin_status", None),
    ("brush_health", "brush", "%"),
    ("filter_health", "filter", "%"),
]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for name, attr, unit in SENSORS:
        entities.append(RoombaMapSensor(coordinator, name, attr, unit))
    async_add_entities(entities, False)

class RoombaMapSensor(SensorEntity):
    def __init__(self, coordinator, name, attr, unit):
        self.coordinator = coordinator
        self._name = f"Roomba {name.replace('_', ' ').title()}"
        self._attr = attr
        self._unit = unit

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self.coordinator.data["state"].get(self._attr)

    @property
    def unit_of_measurement(self):
        return self._unit
