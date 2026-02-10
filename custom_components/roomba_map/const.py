"""Constants for the Roomba Map integration."""

DOMAIN = "roomba_map"
PLATFORMS = ["vacuum", "camera", "sensor"]

# Default values
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_TIMEOUT = 30

# Roomba state mappings
ROOMBA_STATES = {
    "run": "cleaning",
    "clean": "cleaning", 
    "stop": "paused",
    "pause": "paused",
    "charge": "docked",
    "dock": "docked",
    "home": "returning",
    "goHome": "returning",
    "error": "error",
    "stuck": "error",
}

# Configuration keys
CONF_HOST = "host"
CONF_BLID = "blid"
CONF_PASSWORD = "password"
CONF_SCAN_INTERVAL = "scan_interval"
