"""Button platform for ChargePoint."""
import logging
from datetime import datetime
from typing import Any, Optional, Type

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from python_chargepoint.exceptions import ChargePointCommunicationException

from . import ChargePointChargerEntity
from .const import (
    ACCT_HOME_CRGS,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class ChargePointChargerButtonEntity(ChargePointChargerEntity, ButtonEntity):
    """Representation of a ChargePoint Charger Device Button."""

    def __init__(
        self,
        client: Any,
        coordinator: Any,
        description: ButtonEntityDescription,
        charger_id: str,
    ) -> None:
        """Initialize the button."""
        super().__init__(client, coordinator, charger_id)
        self.entity_description = description
        self._attr_name = f"{self.short_model} {description.name_suffix}"
        self._attr_unique_id = f"{charger_id}_{description.key}"

    async def async_press(self) -> None:
        """Press the button."""
        # This is the standard HA method for buttons
        await self._handle_press()
        await self.coordinator.async_request_refresh()

    async def _handle_press(self) -> None:
        """Subclasses must implement this."""
        raise NotImplementedError()

class ChargePointRestartButton(ChargePointChargerButtonEntity):
    """Button to restart the home charger."""
    async def _handle_press(self) -> None:
        try:
            await self.hass.async_add_executor_job(
                self.client.restart_home_charger, self.charger_id
            )
        except Exception as err:
            _LOGGER.error("Failed to restart charger %s: %s", self.charger_id, err)

class ChargePointStartButton(ChargePointChargerButtonEntity):
    """Button to start a charging session."""
    async def _handle_press(self) -> None:
        try:
            await self.hass.async_add_executor_job(
                self.client.start_charging_session, self.charger_id
            )
        except Exception as err:
            _LOGGER.error("Failed to start charge for %s: %s", self.charger_id, err)

class ChargePointStopButton(ChargePointChargerButtonEntity):
    """Button to stop a charging session."""
    async def _handle_press(self) -> None:
        if self.session:
            try:
                await self.hass.async_add_executor_job(self.session.stop)
            except Exception as err:
                _LOGGER.error("Failed to stop charge for %s: %s", self.charger_id, err)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the buttons."""
    client = hass.data[DOMAIN][config_entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    entities = []

    for charger_id in coordinator.data[ACCT_HOME_CRGS].keys():
        # Restart Button
        entities.append(ChargePointRestartButton(
            client, coordinator, 
            ButtonEntityDescription(
                key="restart_charger",
                name_suffix="Restart Charger",
                device_class=ButtonDeviceClass.RESTART,
                icon="mdi:restart",
            ), 
            charger_id
        ))
        # Start Button
        entities.append(ChargePointStartButton(
            client, coordinator,
            ButtonEntityDescription(
                key="start_charge",
                name_suffix="Start Charge",
                icon="mdi:play-circle",
            ),
            charger_id
        ))
        # Stop Button
        entities.append(ChargePointStopButton(
            client, coordinator,
            ButtonEntityDescription(
                key="stop_charge",
                name_suffix="Stop Charge",
                icon="mdi:stop-circle",
            ),
            charger_id
        ))

    async_add_entities(entities)
