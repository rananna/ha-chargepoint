import logging
from dataclasses import dataclass
from typing import Callable, Optional, Union
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.typing import StateType
from . import ChargePointChargerEntity, ChargePointEntityRequiredKeysMixin
from .const import ACCT_HOME_CRGS, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

def _safe_round(val, n=2):
    try: return round(float(val), n) if val not in [None, ""] else 0
    except: return 0

@dataclass
class ChargePointSensorEntityDescription(SensorEntityDescription, ChargePointEntityRequiredKeysMixin):
    value: Callable[[Union["ChargePointChargerSensorEntity"]], StateType]

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
    ChargePointSensorEntityDescription(key="status", name_suffix="Status", value=lambda e: str(e.charger_status.charging_status).title()),
    ChargePointSensorEntityDescription(key="energy", name_suffix="Energy", device_class=SensorDeviceClass.ENERGY, state_class=SensorStateClass.TOTAL_INCREASING, native_unit_of_measurement="kWh", value=lambda e: _safe_round(e.session.energy_kwh) if e.session else 0),
    ChargePointSensorEntityDescription(key="rssi", name_suffix="Wi-Fi Signal", device_class=SensorDeviceClass.SIGNAL_STRENGTH, native_unit_of_measurement="dBm", entity_category=EntityCategory.DIAGNOSTIC, value=lambda e: e.technical_info.wifi_signal_strength),
    ChargePointSensorEntityDescription(key="heartbeat", name_suffix="Last Heartbeat", device_class=SensorDeviceClass.TIMESTAMP, entity_category=EntityCategory.DIAGNOSTIC, value=lambda e: e.charger_status.last_connected_at),
]

async def async_setup_entry(hass, entry, async_add_entities):
    client, coordinator = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT], hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    entities = [ChargePointChargerSensorEntity(client, coordinator, d, cid) for cid in coordinator.data[ACCT_HOME_CRGS].keys() for d in CHARGER_SENSORS]
    async_add_entities(entities)
