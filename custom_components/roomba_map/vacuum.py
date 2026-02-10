import logging
from homeassistant.components.vacuum import (
    VacuumEntity,
    VacuumEntityFeature,
    STATE_CLEANING,
    STATE_DOCKED,
    STATE_RETURNING,
    STATE_PAUSED,
    STATE_IDLE,
    STATE_ERROR,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RoombaMapVacuum(coordinator, entry)], False)

class RoombaMapVacuum(CoordinatorEntity, VacuumEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = f"Roomba {entry.data['host']}"
        self._attr_unique_id = f"{entry.entry_id}_vacuum"

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
    def state(self):
        """Return the state of the vacuum."""
        if not self.coordinator.data or "state" not in self.coordinator.data:
            return STATE_IDLE
            
        roomba_state = self.coordinator.data["state"]
        
        # Get phase from cleanMissionStatus if available
        mission_status = roomba_state.get("cleanMissionStatus", {})
        phase = mission_status.get("phase") if mission_status else roomba_state.get("phase", "")
        
        # Map Roomba states to HA vacuum states
        if phase in ["run", "clean"]:
            return STATE_CLEANING
        elif phase in ["stop", "pause"]:
            return STATE_PAUSED
        elif phase in ["charge", "dock"]:
            return STATE_DOCKED
        elif phase in ["home", "goHome"]:
            return STATE_RETURNING
        elif phase in ["error", "stuck"]:
            return STATE_ERROR
        else:
            return STATE_IDLE

    @property
    def battery_level(self):
        """Return the battery level."""
        if self.coordinator.data and "state" in self.coordinator.data:
            return self.coordinator.data["state"].get("batPct")
        return None

    @property
    def supported_features(self):
        """Return the supported features."""
        return (
            VacuumEntityFeature.START |
            VacuumEntityFeature.PAUSE |
            VacuumEntityFeature.RETURN_HOME |
            VacuumEntityFeature.STOP |
            VacuumEntityFeature.BATTERY
        )

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        if not self.coordinator.data:
            return {}
            
        state = self.coordinator.data.get("state", {})
        mission_status = state.get("cleanMissionStatus", {})
        
        attrs = {}
        
        # Add mission info
        if mission_status:
            attrs.update({
                "cleaning_time": mission_status.get("mssnM", 0),
                "cycle": mission_status.get("cycle", "none"),
                "error": mission_status.get("error", 0),
                "not_ready": mission_status.get("notReady", 0),
                "mission_number": mission_status.get("nMssn", 0),
            })
        
        # Add position info
        pose = state.get("pose", {})
        if pose:
            attrs.update({
                "position_x": pose.get("point", {}).get("x"),
                "position_y": pose.get("point", {}).get("y"),
                "orientation": pose.get("theta"),
            })
        
        # Add bin status
        bin_data = state.get("bin", {})
        if bin_data:
            attrs.update({
                "bin_present": bin_data.get("present", False),
                "bin_full": bin_data.get("full", False),
            })
        
        # Add available rooms
        map_data = self.coordinator.data.get("map", {})
        if map_data and map_data.get("rooms"):
            attrs["available_rooms"] = map_data["rooms"]
        
        return attrs

    async def async_start(self):
        """Start cleaning."""
        try:
            await self.coordinator.client.async_start()
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error starting vacuum: %s", err)

    async def async_pause(self):
        """Pause cleaning."""
        try:
            await self.coordinator.client.async_pause()
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error pausing vacuum: %s", err)

    async def async_stop(self):
        """Stop cleaning."""
        try:
            await self.coordinator.client.async_stop()
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error stopping vacuum: %s", err)

    async def async_return_to_base(self):
        """Return to base."""
        try:
            await self.coordinator.client.async_return_to_base()
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error returning vacuum to base: %s", err)

    async def async_clean_spot(self, **kwargs):
        """Clean a specific spot (room cleaning)."""
        try:
            # Extract room information from service call
            room_id = kwargs.get("room_id")
            if room_id:
                # Use the embedded client's room cleaning capability
                await self.coordinator.client._client.async_clean_room(room_id)
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.warning("No room_id provided for spot cleaning")
        except Exception as err:
            _LOGGER.error("Error cleaning spot: %s", err)
