from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, CONTROL_API
import aiohttp

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    device_id = await coordinator.get_device_id()
    async_add_entities([JuiceBoosterSwitch(coordinator, device_id)], True)

class JuiceBoosterSwitch(SwitchEntity):
    def __init__(self, coordinator, device_id):
        self.coordinator = coordinator
        self.device_id = device_id
        self._is_on = True

    @property
    def name(self):
        return "Juice Booster Charging Switch"

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self.set_amperes(10)

    async def async_turn_off(self, **kwargs):
        await self.set_amperes(0)

    async def set_amperes(self, amperes):
        async with aiohttp.ClientSession() as session:
            await session.put(
                CONTROL_API.format(device_id=self.device_id),
                headers=self.coordinator.get_headers(),
                json={"amperes": amperes},
                ssl=False
            )
        self._is_on = amperes > 0
        self.async_write_ha_state()
