import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import entity_registry as er
from .const import DOMAIN, PLATFORMS
from .coordinator import RoombaDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Roomba Map integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Roomba Map from a config entry."""
    _LOGGER.debug("Setting up Roomba Map integration for %s", entry.data.get("host"))
    
    try:
        coordinator = RoombaDataUpdateCoordinator(hass, entry)
        await coordinator.async_config_entry_first_refresh()
        
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

        # Set up platforms
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        
        # Register services
        await _async_register_services(hass)
        
        _LOGGER.info("Successfully set up Roomba Map integration for %s", entry.data.get("host"))
        return True
        
    except Exception as err:
        _LOGGER.error("Failed to set up Roomba Map integration: %s", err)
        raise ConfigEntryNotReady(f"Failed to connect to Roomba: {err}") from err

async def _async_register_services(hass: HomeAssistant):
    """Register services for room cleaning."""
    
    async def async_clean_room(call: ServiceCall):
        """Service to clean a specific room."""
        entity_id = call.data.get("entity_id")
        room_id = call.data.get("room_id")
        
        if not entity_id or not room_id:
            _LOGGER.error("entity_id and room_id are required for clean_room service")
            return
            
        # Get the vacuum entity
        entity_registry = er.async_get(hass)
        entity_entry = entity_registry.async_get(entity_id)
        if not entity_entry:
            _LOGGER.error("Entity %s not found", entity_id)
            return
            
        # Get the coordinator
        entry_id = entity_entry.config_entry_id
        coordinator = hass.data[DOMAIN].get(entry_id)
        if not coordinator:
            _LOGGER.error("Coordinator not found for entity %s", entity_id)
            return
            
        try:
            await coordinator.client._client.async_clean_room(room_id)
            await coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to clean room %s: %s", room_id, err)
    
    async def async_clean_rooms(call: ServiceCall):
        """Service to clean multiple rooms."""
        entity_id = call.data.get("entity_id")
        room_ids = call.data.get("room_ids", [])
        ordered = call.data.get("ordered", True)
        
        if not entity_id or not room_ids:
            _LOGGER.error("entity_id and room_ids are required for clean_rooms service")
            return
            
        # Get the vacuum entity
        entity_registry = er.async_get(hass)
        entity_entry = entity_registry.async_get(entity_id)
        if not entity_entry:
            _LOGGER.error("Entity %s not found", entity_id)
            return
            
        # Get the coordinator
        entry_id = entity_entry.config_entry_id
        coordinator = hass.data[DOMAIN].get(entry_id)
        if not coordinator:
            _LOGGER.error("Coordinator not found for entity %s", entity_id)
            return
            
        try:
            await coordinator.client._client.async_clean_rooms(room_ids, ordered)
            await coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to clean rooms %s: %s", room_ids, err)
    
    # Register services
    if not hass.services.has_service(DOMAIN, "clean_room"):
        hass.services.async_register(DOMAIN, "clean_room", async_clean_room)
    
    if not hass.services.has_service(DOMAIN, "clean_rooms"):
        hass.services.async_register(DOMAIN, "clean_rooms", async_clean_rooms)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Roomba Map integration for %s", entry.data.get("host"))
    
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
        if coordinator:
            # Properly shutdown the coordinator
            await coordinator.async_shutdown()
        
        # Remove services if this was the last entry
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, "clean_room")
            hass.services.async_remove(DOMAIN, "clean_rooms")
        
        _LOGGER.info("Successfully unloaded Roomba Map integration for %s", entry.data.get("host"))
    
    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload a config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
