"""Sensor platform for ChargePoint."""

import logging
from dataclasses import dataclass
from typing import Callable, Optional, Union

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import (
    ChargePointChargerEntity,
    ChargePointEntity,
    ChargePointEntityRequiredKeysMixin,
)
from .const import ACCT_HOME_CRGS, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

# --- Helper functions to prevent TypeError crashes from null/empty API data ---

def _safe_round(val, ndigits=2):
    try:
        if val is None or val == "":
            return 0
        return round(float(val), ndigits)
    except (ValueError, TypeError):
        return 0

def _safe_time(val):
    try:
        if val is None or val == "":
            return 0
        # Convert milliseconds to seconds
        return int(float(val) / 1000)
    except (ValueError, TypeError):
        return 0

def _safe_format(val):
    try:
        if val is None or val == "":
            return "0.00"
        return f"{float(val):.2f}"
    except (ValueError, TypeError):
        return "0.00"

# ----------------------------------------------------------------------------

@dataclass
class ChargePointSensorRequiredKeysMixin:
    """Mixin for required keys."""
    value: Callable[
        [Union["ChargePointSensorEntity", "ChargePointChargerSensorEntity"]], StateType
    ]

@dataclass
class ChargePointSensorEntityDescription(
    SensorEntityDescription,
    ChargePointEntityRequiredKeysMixin,
):
    """Describes a ChargePoint sensor entity."""
    unit: Optional[
        Callable[
            [Union["ChargePointSensorEntity", "ChargePointChargerSensorEntity"]],
            StateType,
        ]
    ] = None

class ChargePointSensorEntity(SensorEntity, ChargePointEntity):
    """Representation of a ChargePoint Account sensor."""

    entity_description: ChargePointSensorEntityDescription

    def __init__(self, client, coordinator, description):
        """Initialize account sensor."""
        super().__init__(client, coordinator)
        self.entity_description = description
        self._attr_name = f"{self.account.user.username} {description.name_suffix}"
        self._attr_unique_id = f"{self.account.user.user_id}_{description.key}"

    @property
    def native_unit_of_measurement(self):
        if unit_fn := self.entity_description.unit:
            return unit_fn(self)
        return self.entity_description.native_unit_of_measurement

    @property
    def native_value(self):
        return self.entity_description.value(self)

class ChargePointChargerSensorEntity(SensorEntity, ChargePointChargerEntity):
    """Representation of a ChargePoint Charging Device Sensor."""

    entity_description: ChargePointSensorEntityDescription

    def __init__(self, client, coordinator, description, charger_id):
        """Initialize charger sensor."""
        super().__init__(client, coordinator, charger_id)
        self.entity_description = description
        self._attr_name = f"{self.short_model} {description.name_suffix}"
        self._attr_unique_id = f"{charger_id}_{description.key}"

    @property
    def native_unit_of_measurement(self):
        if unit_fn := self.entity_description.unit:
            return unit_fn(self)
        return self.entity_description.native_unit_of_measurement

    @property
    def native_value(self):
        val = self.entity_description.value(self)
        if self.entity_description.state_class == SensorStateClass.TOTAL_INCREASING:
            if not self.session:
                return getattr(self, "_last_known_value", val)
            self._last_known_value = val
        return val

ACCOUNT_SENSORS = [
    ChargePointSensorEntityDescription(
        key="account_balance",
        name_suffix="Account Balance",
        icon="mdi:wallet",
        device_class=SensorDeviceClass.MONETARY,
        unit=lambda entity: entity.account.account_balance.currency,
        state_class=SensorStateClass.TOTAL,
        value=lambda entity: f"{float(entity.account.account_balance.amount):.2f}",
    ),
]

CHARGER_SENSORS = [
    ChargePointSensorEntityDescription(
        key="charging_status",
        name_suffix="Charging Status",
        icon="mdi:lightning-bolt",
        value=lambda entity: str(entity.charger_status.charging_status).replace("_", " ").title(),
    ),
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
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda entity: _safe_round(entity.session.power_kw, 2) if entity.session else 0,
        native_unit_of_measurement="kW",
    ),
    ChargePointSensorEntityDescription(
        key="session_energy_kwh",
        name_suffix="Energy Output",
        icon="mdi:lightning-bolt-circle",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value=lambda entity: _safe_round(entity.session.energy_kwh, 2) if entity.session else 0,
        native_unit_of_measurement="kWh",
    ),
    ChargePointSensorEntityDescription(
        key="session_miles_added",
        name_suffix="Miles Added",
        icon="mdi:road-variant",
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda entity: _safe_round(entity.session.miles_added, 2) if entity.session else 0,
        native_unit_of_measurement="miles",
    ),
    ChargePointSensorEntityDescription(
        key="session_cost",
        name_suffix="Charge Cost",
        icon="mdi:cash-multiple",
        state_class=SensorStateClass.TOTAL,
        device_class=SensorDeviceClass.MONETARY,
        value=lambda entity: _safe_format(entity.session.total_amount) if entity.session else "0.00",
        unit=lambda entity: entity.client.global_config.default_currency.symbol,
    ),
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    client = hass.data[DOMAIN][config_entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    entities: list[SensorEntity] = []

    for description in ACCOUNT_SENSORS:
        entities.append(ChargePointSensorEntity(client, coordinator, description))

    for charger_id in coordinator.data[ACCT_HOME_CRGS].keys():
        for description in CHARGER_SENSORS:
            entities.append(
                ChargePointChargerSensorEntity(client, coordinator, description, charger_id)
            )

    async_add_entities(entities)
