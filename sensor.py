from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

SENSOR_KEYS = {
    "charge-state": "Charging State",
    "charge-control": "Charge Control",
    "charge-start-time": "Charge Start Time",
    "charge-authentication.type": "Charge Auth Type",
    "charge-cost.value-total": "Charge Cost Total",
    "charge-duration.value-total": "Charge Duration",
    "device-currents.max-device-current": "Max Device Current",
    "device-currents.max-supply-current": "Max Supply Current",
    "device-currents.smart-juice-enabled": "Smart Juice Enabled",
    "measured-energy.value-total": "Energy Total (kWh)",
    "measured-power.value": "Power Total (kW)",
    "measured-details.energy-level.value": "Energy Level (kWh)",
    "measured-details.start-energy-level.value": "Start Energy Level (kWh)",
    "measured-details.voltage.valueL1": "Voltage L1",
    "measured-details.voltage.valueL2": "Voltage L2",
    "measured-details.voltage.valueL3": "Voltage L3",
    "measured-details.ampere.valueL1": "Ampere L1",
    "measured-details.ampere.valueL2": "Ampere L2",
    "measured-details.ampere.valueL3": "Ampere L3",
    "measured-details.power.valueL1": "Power L1 (kW)",
    "measured-details.power.valueL2": "Power L2 (kW)",
    "measured-details.power.valueL3": "Power L3 (kW)",
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        JuiceBoosterSensor(coordinator, key, name)
        for key, name in SENSOR_KEYS.items()
    ]
    async_add_entities(entities, True)

class JuiceBoosterSensor(Entity):
    def __init__(self, coordinator, key, name):
        self.coordinator = coordinator
        self.key = key
        self._name = name

    def get_nested(self, data, path):
        try:
            for part in path.split("."):
                data = data[part]
            return data
        except (KeyError, TypeError):
            return None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self.get_nested(self.coordinator.data, self.key)

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def unique_id(self):
        return f"juice_booster_{self.key.replace('.', '_')}"
