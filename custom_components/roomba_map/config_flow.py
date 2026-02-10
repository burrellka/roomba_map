import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class RoombaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        
        if user_input is not None:
            try:
                # Basic validation
                if not user_input.get("host"):
                    errors["host"] = "invalid_host"
                elif not user_input.get("blid"):
                    errors["blid"] = "invalid_blid"
                elif not user_input.get("password"):
                    errors["password"] = "invalid_password"
                else:
                    # Create entry if validation passes
                    return self.async_create_entry(
                        title=f"Roomba at {user_input['host']}",
                        data=user_input,
                    )
            except Exception as err:
                _LOGGER.error("Unexpected error: %s", err)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host", default="" if user_input is None else user_input.get("host", "")): str,
                vol.Required("blid", default="" if user_input is None else user_input.get("blid", "")): str,
                vol.Required("password", default="" if user_input is None else user_input.get("password", "")): str,
            }),
            errors=errors,
            description_placeholders={
                "setup_info": "Enter your Roomba's network details for local MQTT connection"
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return RoombaOptionsFlowHandler(config_entry)


class RoombaOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional("scan_interval", default=self.config_entry.options.get("scan_interval", 60)): int,
            }),
        )
