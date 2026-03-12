import logging
from dataclasses import dataclass
from typing import Callable, Union
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.typing import StateType
from . import ChargePointChargerEntity, ChargePointEntityRequiredKeysMixin
from .const import ACCT_HOME_CRGS, ACCT_INFO, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

def _safe_float(val) -> float:
    try: return float(val) if val not in [None, "", "None", "NaN"] else 0.0
    except: return 0.0

def _format_duration(ms):
    if not ms: return "00:00:00"
    s = int(float(ms)) // 1000
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

@dataclass(kw_only=True)
class ChargePointSensorEntityDescription(SensorEntityDescription, ChargePointEntityRequiredKeysMixin):
    value: Callable[[Union["ChargePointChargerSensorEntity"]], StateType]

class ChargePointChargerSensorEntity(SensorEntity, ChargePointChargerEntity):
    def __init__(self, client, coordinator, description, charger_id):
        super().__init__(client, coordinator, charger_id)
        self.entity_description = description
        self._attr_name, self._attr_unique_id = f"{self.short_model} {description.name_suffix}", f"{charger_id}_{description.key}"
        self._last_val = 0.0

    @property
    def native_value(self):
        val = self.entity_description.value(self)
        if self.entity_description.state_class == SensorStateClass.TOTAL_INCREASING:
            if not self.session or val == 0.0: return self._last_val
            self._last_val = val
        return val

CHARGER_SENSORS = [
    ChargePointSensorEntityDescription(key="charge_cost", name_suffix="Charge Cost", device_class=SensorDeviceClass.MONETARY, native_unit_of_measurement="CAD", icon="mdi:cash-multiple", value=lambda e: _safe_float(e.session.total_amount) if e.session else 0.0),
    ChargePointSensorEntityDescription(key="energy_output", name_suffix="Energy Output", device_class=SensorDeviceClass.ENERGY, state_class=SensorStateClass.TOTAL_INCREASING, native_unit_of_measurement="kWh", value=lambda e: _safe_float(e.session.energy_kwh) if e.session else 0.0),
    ChargePointSensorEntityDescription(key="power_output", name_suffix="Power Output", device_class=SensorDeviceClass.POWER, state_class=SensorStateClass.MEASUREMENT, native_unit_of_measurement="kW", value=lambda e: _safe_float(e.session.power_kw) if e.session else 0.0),
    ChargePointSensorEntityDescription(key="miles_added", name_suffix="Miles Added", icon="mdi:map-marker-distance", native_unit_of_measurement="mi", value=lambda e: _safe_float(e.session.miles_added) if e.session else 0.0),
    ChargePointSensorEntityDescription(key="miles_per_hour", name_suffix="Miles / Hour Added", icon="mdi:speedometer", native_unit_of_measurement="mph", value=lambda e: _safe_float(e.session.miles_added_per_hour) if e.session else 0.0),
    ChargePointSensorEntityDescription(key="charging_time", name_suffix="Charging Time", icon="mdi:timer-outline", value=lambda e: _format_duration(e.session.charging_time) if e.session else "00:00:00"),
    ChargePointSensorEntityDescription(key="status", name_suffix="Status", value=lambda e: str(e.charger_status.charging_status).title() if e.charger_status.plugged_in else "Not Connected"),
    ChargePointSensorEntityDescription(key="charger_state", name_suffix="Charger State", value=lambda e: str(e.session.charging_state).title() if e.session and e.session.charging_state else "Not Charging"),
    ChargePointSensorEntityDescription(key="account_balance", name_suffix="Account Balance", device_class=SensorDeviceClass.MONETARY, native_unit_of_measurement="CAD", icon="mdi:wallet", value=lambda e: _safe_float(getattr(e.coordinator.data[ACCT_INFO], 'balance', getattr(e.coordinator.data[ACCT_INFO], 'credit_balance', 0.0))) if e.coordinator.data.get(ACCT_INFO) else 0.0),
    ChargePointSensorEntityDescription(key="rssi", name_suffix="Wi-Fi Signal", device_class=SensorDeviceClass.SIGNAL_STRENGTH, native_unit_of_measurement="dBm", entity_category=EntityCategory.DIAGNOSTIC, value=lambda e: getattr(e.technical_info, 'wifi_signal', None)),
    ChargePointSensorEntityDescription(key="heartbeat", name_suffix="Last Heartbeat", device_class=SensorDeviceClass.TIMESTAMP, entity_category=EntityCategory.DIAGNOSTIC, value=lambda e: e.charger_status.last_connected_at if e.charger_status.last_connected_at and e.charger_status.last_connected_at.year > 1970 else None),
]

async def async_setup_entry(hass, entry, async_add_entities):
    client, coordinator = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT], hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    entities = [ChargePointChargerSensorEntity(client, coordinator, d, cid) for cid in coordinator.data[ACCT_HOME_CRGS].keys() for d in CHARGER_SENSORS]
    async_add_entities(entities)

