import logging
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONTROL_API

_LOGGER = logging.getLogger(__name__)
AMPERAGE_OPTIONS = [0, 6, 8, 10, 13, 16]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    _LOGGER.debug("Setting up Juice Booster amperage selector")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    device_id = await coordinator.get_device_id()
    async_add_entities([JuiceBoosterAmperageSelector(hass, coordinator, device_id)], True)

class JuiceBoosterAmperageSelector(SelectEntity):
    def __init__(self, hass: HomeAssistant, coordinator, device_id):
        _LOGGER.debug("Initializing Juice Booster amperage selector for device %s", device_id)
        self.coordinator = coordinator
        self.device_id = device_id
        self.hass = hass
        self._attr_options = [str(a) for a in AMPERAGE_OPTIONS]
        self._attr_name = "Juice Booster Charging Current"
        self._attr_unique_id = f"juice_booster_charging_current_{device_id}"
        self._attr_available = True

    @property
    def current_option(self):
        current = self.coordinator.data.get("device-currents", {}).get("max-supply-current", 0)
        _LOGGER.debug("Current amperage option is: %s", current)
        return str(current)

    async def async_select_option(self, option: str):
        _LOGGER.debug("Selecting amperage option: %s", option)
        amperes = int(option)
        session = async_get_clientsession(self.hass)
        try:
            response = await session.put(
                CONTROL_API.format(device_id=self.device_id),
                headers=self.coordinator.get_headers(),
                json={"amperes": amperes},
                ssl=False
            )
            response.raise_for_status()
            _LOGGER.debug("Successfully set amperage to %s", amperes)
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error("Failed to set amperage: %s", e)
            self._attr_available = False
        finally:
            self.async_write_ha_state()
