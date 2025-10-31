from datetime import timedelta
import logging
import time
import jwt
import aiohttp
from homeassistant import config_entries
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant

from .const import TOKEN_URL, USER_API, DEVICE_API, CHARGING_API, DOMAIN

_LOGGER = logging.getLogger(__name__)

class JuiceBoosterCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config_entry):
        self.config_entry = config_entry
        self.hass = hass
        self.username = config_entry.data["username"]
        self.password = config_entry.data["password"]
        self.access_token = config_entry.data["access_token"]
        self.refresh_token = config_entry.data["refresh_token"]
        self.session = aiohttp.ClientSession()

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=30))

    async def refresh_access_token(self):
        """Refresh token using the refresh_token grant."""
        _LOGGER.debug("Refreshing access token")
        async with self.session.post(TOKEN_URL, data={
            "grant_type": "refresh_token",
            "client_id": "native-webview",
            "refresh_token": self.refresh_token
        }, ssl=False) as response:
            if response.status != 200:
                try:
                    error_json = await response.json()
                    error_description = error_json.get("error_description", "")
                    _LOGGER.error("Token refresh failed: %s", error_description)
                    _LOGGER.debug("Token: %s", self.refresh_token)
                    raise Exception(f"Token refresh failed: {error_description}")
                except Exception:
                    _LOGGER.exception("Error during token refresh")
                    text = await response.text()
                    raise Exception(f"Token refresh failed with status {response.status}: {text}")
            
            response.raise_for_status()
            tokens = await response.json()
            self.access_token = tokens["access_token"]

            if not self.access_token:
                _LOGGER.error("Access token is empty, re-authenticating")
                await self.re_authenticate()
                return

            if not tokens["refresh_token"]:
                _LOGGER.error("Refresh token is empty, re-authenticating")
                await self.re_authenticate()
                return
            
            self.refresh_token = tokens["refresh_token"]

    def get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def token_expired(self, token):
        payload = jwt.decode(token, options={"verify_signature": False})
        if payload.get("exp") < time.time():
            return True
        else:
            return False
    
    async def check_tokens(self):
        if self.token_expired(self.access_token):
            if self.token_expired(self.refresh_token):
                _LOGGER.info("Refresh token is expired, re-authenticating")
                await self.re_authenticate(self)
            else:
                _LOGGER.info("Access token is expired, refreshing token")
                await self.refresh_access_token(self)
        else:
            _LOGGER.info("Access token is still valid")

    async def get_device_id(self):
        """Fetch user info and extract device ID."""
        payload = jwt.decode(self.access_token, options={"verify_signature": False})
        _LOGGER.debug("decoded JWT: %s", payload)
        user_id = payload["sub"]
        async with self.session.get(USER_API.format(user_id=user_id), headers=self.get_headers(), ssl=False) as response:
            response.raise_for_status()
            user_info = await response.json()
            _LOGGER.debug("fetched user info: %s", user_info)
        return user_info["devices"][0]["id"]

    async def get_charging_status(self, device_id):
        """Fetch charging data for a given device ID."""
        _LOGGER.debug("Fetch charging data for a given device ID %s", device_id)
        async with self.session.get(CHARGING_API.format(device_id=device_id), headers=self.get_headers(), ssl=False) as response:
            response.raise_for_status()
            charging_info = await response.json()
            _LOGGER.debug("fetched charging info: %s", charging_info)
            return charging_info

    async def re_authenticate(self):
        """Re-authenticate using the config flow."""
        _LOGGER.info("Re-authenticating via config flow")
        
        # Import the config flow
        from custom_components.juice_booster import config_flow

        # Initiate a new authentication
        try:
            flow = config_flow.JuiceBoosterConfigFlow()
            token_data = await self.hass.async_add_executor_job(flow.authenticate, {"username": self.username, "password": self.password})
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data["refresh_token"]
            self.hass.config_entries.async_update_entry(
                self.config_entry, data={**self.config_entry.data, "access_token": self.access_token, "refresh_token": self.refresh_token}
            )
        except Exception as e:
            _LOGGER.error("Re-authentication failed: %s", e)

    async def _async_update_data(self):
        """Fetch the latest charging view from the Juice Booster API."""
        try:
            await self.check_tokens()
            device_id = await self.get_device_id()
            status = await self.get_charging_status(device_id)
            return status
        except Exception as e:
            _LOGGER.error("Failed to update Juice Booster data: %s", e)
            raise
