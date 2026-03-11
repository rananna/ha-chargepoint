import logging
from dataclasses import dataclass
from typing import Callable, Optional, Union
from homeassistant.components.sensor import (
    SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
)
from homeassistant.const import UnitOfTime
from . import ChargePointChargerEntity, ChargePointEntity, ChargePointEntityRequiredKeysMixin
from .const import ACCT_HOME_CRGS, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

def _safe_round(val, ndigits=2):
    try:
        return round(float(val), ndigits) if val not in [None, ""] else 0
    except: return 0

def _safe_time(val):
    try:
        return int(float(val) / 1000) if val not in [None, ""] else 0
    except: return 0

CHARGER_SENSORS = [
    ChargePointSensorEntityDescription(
        key="session_charging_time",
        name_suffix="Charging Time",
        icon="mdi:timer",
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda entity: _safe_time(entity.session.charging_time) if entity.session else 0,
        native_unit_of_measurement=UnitOfTime.SECONDS,
    ),
    ChargePointSensorEntityDescription(
        key="session_power_kw",
        name_suffix="Power Output",
        icon="mdi:transmission-tower",
        device_class=SensorDeviceClass.POWER,
        value=lambda entity: _safe_round(entity.session.power_kw, 2) if entity.session else 0,
        native_unit_of_measurement="kW",
    ),
]
# ... [Include full sensor list from previous message] ...
