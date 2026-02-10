import logging
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSORS = [
    ("battery_level", "batPct", PERCENTAGE, SensorDeviceClass.BATTERY),
    ("bin_status", "bin", None, None),
    ("phase", "phase", None, None),
    ("cleaning_time", "cleanMissionStatus.mssnM", "minutes", SensorDeviceClass.DURATION),
]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for name, attr, unit, device_class in SENSORS:
        entities.append(RoombaMapSensor(coordinator, entry, name, attr, unit, device_class))
    async_add_entities(entities, False)

class RoombaMapSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, name, attr, unit, device_class):
        super().__init__(coordinator)
        self._entry = entry
        self._name = name
        self._attr = attr
        self._unit = unit
        self._device_class = device_class
        self._attr_name = f"Roomba {name.replace('_', ' ').title()}"
        self._attr_unique_id = f"{entry.entry_id}_{name}"

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
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data or "state" not in self.coordinator.data:
            return None
            
        state_data = self.coordinator.data["state"]
        
        # Handle nested attributes (e.g., "cleanMissionStatus.mssnM")
        if "." in self._attr:
            keys = self._attr.split(".")
            value = state_data
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return None
            return value
        else:
            return state_data.get(self._attr)

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def device_class(self):
        """Return the device class."""
        return self._device_class

    @property
    def available(self):
        """Return if the sensor is available."""
        return (
            self.coordinator.last_update_success and 
            self.coordinator.data is not None
        )
