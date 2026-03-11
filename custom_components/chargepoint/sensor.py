import logging
from dataclasses import dataclass
from typing import Callable, Optional, Union
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import UnitOfTime
from homeassistant.helpers.typing import StateType
from . import ChargePointChargerEntity, ChargePointEntity, ChargePointEntityRequiredKeysMixin
from .const import ACCT_HOME_CRGS, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

def _safe_round(val, n=2):
    try: return round(float(val), n) if val not in [None, ""] else 0
    except: return 0

def _safe_time(val):
    try: return int(float(val) / 1000) if val not in [None, ""] else 0
    except: return 0

@dataclass
class ChargePointSensorEntityDescription(SensorEntityDescription, ChargePointEntityRequiredKeysMixin):
    value: Callable[[Union["ChargePointSensorEntity", "ChargePointChargerSensorEntity"]], StateType]
    unit: Optional[Callable] = None

class ChargePointChargerSensorEntity(SensorEntity, ChargePointChargerEntity):
    def __init__(self, client, coordinator, description, charger_id):
        super().__init__(client, coordinator, charger_id)
        self.entity_description = description
        self._attr_name, self._attr_unique_id = f"{self.short_model} {description.name_suffix}", f"{charger_id}_{description.key}"
        self._last_val = 0
    @property
    def native_value(self):
        val = self.entity_description.value(self)
        if self.entity_description.state_class == SensorStateClass.TOTAL_INCREASING:
            if not self.session: return self._last_val
            self._last_val = val
        return val

CHARGER_SENSORS = [
    ChargePointSensorEntityDescription(key="charging_status", name_suffix="Status", icon="mdi:lightning-bolt", value=lambda e: str(e.charger_status.charging_status).title()),
    ChargePointSensorEntityDescription(key="power_kw", name_suffix="Power", device_class=SensorDeviceClass.POWER, native_unit_of_measurement="kW", value=lambda e: _safe_round(e.session.power_kw) if e.session else 0),
    ChargePointSensorEntityDescription(key="energy_kwh", name_suffix="Energy", device_class=SensorDeviceClass.ENERGY, state_class=SensorStateClass.TOTAL_INCREASING, native_unit_of_measurement="kWh", value=lambda e: _safe_round(e.session.energy_kwh) if e.session else 0),
]

async def async_setup_entry(hass, entry, async_add_entities):
    client, coordinator = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT], hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    entities = []
    for cid in coordinator.data[ACCT_HOME_CRGS].keys():
        for desc in CHARGER_SENSORS: entities.append(ChargePointChargerSensorEntity(client, coordinator, desc, cid))
    async_add_entities(entities)
