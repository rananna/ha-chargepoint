"""Binary sensor platform for ChargePoint."""
import logging
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_CLIENT, DATA_COORDINATOR, DOMAIN
from . import ChargePointChargerEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ChargePoint binary sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    client = data[DATA_CLIENT]
    coordinator = data[DATA_COORDINATOR]

    entities = []
    # Ensure we use the correct key from your updated const.py
    from .const import ACCT_HOME_CRGS
    
    for charger_id in coordinator.data[ACCT_HOME_CRGS].keys():
        entities.append(ChargePointPluggedInBinary(client, coordinator, charger_id))

    async_add_entities(entities)

class ChargePointPluggedInBinary(ChargePointChargerEntity, BinarySensorEntity):
    """Binary sensor to show if the EV is plugged in."""

    _attr_device_class = BinarySensorDeviceClass.PLUG
    
    def __init__(self, client, coordinator, charger_id):
        super().__init__(client, coordinator, charger_id)
        # short_model is inherited from ChargePointChargerEntity in __init__.py
        self._attr_name = f"{self.short_model} Plugged In"
        self._attr_unique_id = f"{charger_id}_plugged_in_binary"

    @property
    def is_on(self) -> bool:
        """Return True if the vehicle is plugged in."""
        return self.charger_status.plugged_in
