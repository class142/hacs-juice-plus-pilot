from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .const import DOMAIN
from .coordinator import JuiceBoosterCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SELECT
    #Platform.DEVICE_TRACKER,
    #Platform.CLIMATE,
    #Platform.SWITCH,
    #Platform.NUMBER,
    #Platform.BINARY_SENSOR,
    #Platform.IMAGE,
    #Platform.LOCK,
    #Platform.BUTTON,
]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration (required but unused here)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Juice Booster from a config entry."""
    coordinator = JuiceBoosterCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Proper forwarding to sensor and switch platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    # Do a lazy reload of integration when configuration changed
    await hass.config_entries.async_reload(entry.entry_id)
