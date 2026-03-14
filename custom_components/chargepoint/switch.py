"""Switch platform for ChargePoint (Custom Stealth)."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from python_chargepoint.exceptions import ChargePointCommunicationException

from . import ChargePointChargerEntity
from .const import (
    ACCT_HOME_CRGS,
    CHARGER_SESSION_STATE_IN_USE,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DOMAIN,
    EXCEPTION_WARNING_MSG,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ChargePoint switch platform."""
    client = hass.data[DOMAIN][config_entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    entities = [
        ChargePointChargingSwitch(client, coordinator, charger_id) 
        for charger_id in coordinator.data[ACCT_HOME_CRGS].keys()
    ]

    async_add_entities(entities)

class ChargePointChargingSwitch(ChargePointChargerEntity, SwitchEntity):
    """Switch to start/stop charging sessions."""

    def __init__(self, client, coordinator, charger_id):
        """Initialize the switch."""
        super().__init__(client, coordinator, charger_id)
        self._attr_name = f"{self.short_model} Charge Control"
        self._attr_unique_id = f"{charger_id}_charge_control"
        self._attr_icon = "mdi:ev-station"

    @property
    def is_on(self) -> bool:
        """Return true if the charger is currently in use."""
        if not self.charger_status:
            return False
        return self.charger_status.charging_status == CHARGER_SESSION_STATE_IN_USE

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Start a charging session."""
        try:
            _LOGGER.debug("Starting ChargePoint session for %s", self.charger_id)
            await self.hass.async_add_executor_job(
                self.client.start_charging_session, self.charger_id
            )
        except ChargePointCommunicationException:
            _LOGGER.error(EXCEPTION_WARNING_MSG)
        
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop the active charging session."""
        if self.session:
            try:
                _LOGGER.debug("Stopping ChargePoint session for %s", self.charger_id)
                await self.hass.async_add_executor_job(self.session.stop)
            except ChargePointCommunicationException:
                _LOGGER.error(EXCEPTION_WARNING_MSG)
        
        await self.coordinator.async_request_refresh()
