import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import requests
import logging

from .const import DOMAIN, TOKEN_URL

_LOGGER = logging.getLogger(__name__)

class JuiceBoosterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                token_data = await self.hass.async_add_executor_job(self.authenticate, user_input)
                if "access_token" in token_data and "refresh_token" in token_data:
                    return self.async_create_entry(title="Juice Booster", data={
                        "username": user_input["username"],
                        "password": user_input["password"],
                        "access_token": token_data["access_token"],
                        "refresh_token": token_data["refresh_token"]
                    })
                else:
                    errors["base"] = "auth_failed"
            except Exception as e:
                _LOGGER.exception("Authentication error")
                errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str
            }),
            errors=errors
        )

    def authenticate(self, user_input):
        """Authenticate with Juice Booster OAuth2 using password grant."""
        response = requests.post(TOKEN_URL, data={
            "grant_type": "password",
            "client_id": "native-webview",
            "username": user_input["username"],
            "password": user_input["password"]
        })
        response.raise_for_status()
        return response.json()
