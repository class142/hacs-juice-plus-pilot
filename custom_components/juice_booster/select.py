from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONTROL_API

AMPERAGE_OPTIONS = [0, 6, 8, 10, 13, 16]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    device_id = await coordinator.get_device_id()
    async_add_entities([JuiceBoosterAmperageSelector(hass, coordinator, device_id)], True)

class JuiceBoosterAmperageSelector(SelectEntity):
    def __init__(self, hass: HomeAssistant, coordinator, device_id):
        self.coordinator = coordinator
        self.device_id = device_id
        self.hass = hass
        self._attr_options = [str(a) for a in AMPERAGE_OPTIONS]
        self._attr_name = "Juice Booster Charging Current"
        self._attr_unique_id = f"juice_booster_charging_current_{device_id}"

    @property
    def current_option(self):
        current = self.coordinator.data.get("device-currents", {}).get("max-supply-current", 0)
        return str(current)

    async def async_select_option(self, option: str):
        amperes = int(option)
        session = async_get_clientsession(self.hass)
        await session.put(
            CONTROL_API.format(device_id=self.device_id),
            headers=self.coordinator.get_headers(),
            json={"amperes": amperes},
            ssl=False
        )
        self.async_write_ha_state()
