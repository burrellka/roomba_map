import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class RoombaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("host"): str,
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                }),
            )
        return self.async_create_entry(
            title=f"Roomba at {user_input['host']}",
            data=user_input,
        )
