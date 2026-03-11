"""
Custom integration to integrate ChargePoint with Home Assistant.
"""

import logging
import os
import requests
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from python_chargepoint import ChargePoint
from python_chargepoint.exceptions import (
    ChargePointInvalidSession,
    ChargePointLoginError,
)
from python_chargepoint.session import ChargingSession
from python_chargepoint.types import (
    ChargePointAccount,
    HomeChargerStatus,
    HomeChargerTechnicalInfo,
)

from .const import (
    ACCT_CRG_STATUS,
    ACCT_HOME_CRGS,
    ACCT_INFO,
    ACCT_SESSION,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DOMAIN,
    OPTION_POLL_INTERVAL,
    POLL_INTERVAL_DEFAULT,
)

# Modern User-Agent to mimic a real person
BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
_LOGGER: logging.Logger = logging.getLogger(__package__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    session_token = entry.data.get(CONF_ACCESS_TOKEN)

    # Use a shared stealth session for all requests
    stealth_session = requests.Session()
    stealth_session.headers.update({"User-Agent": BROWSER_USER_AGENT})

    try:
        client = await hass.async_add_executor_job(
            ChargePoint, username, password, session_token, stealth_session
        )

        # Update entry with the STRING token ONLY (prevents JSON serialization error)
        if client.session_token != session_token:
            hass.config_entries.async_update_entry(
                entry, data={**entry.data, CONF_ACCESS_TOKEN: client.session_token}
            )
    except ChargePointLoginError as exc:
        raise ConfigEntryAuthFailed("Invalid credentials") from exc
    except Exception as exc:
        # If we hit a 403 block during setup, tell HA to wait before retrying
        _LOGGER.warning("ChargePoint is blocking requests (403). Retrying later.")
        raise ConfigEntryNotReady from exc

    async def async_update_data(is_retry: bool = False):
        try:
            data = {ACCT_INFO: None, ACCT_CRG_STATUS: None, ACCT_SESSION: None, ACCT_HOME_CRGS: {}}
            data[ACCT_INFO] = await hass.async_add_executor_job(client.get_account)
            data[ACCT_CRG_STATUS] = await hass.async_add_executor_job(client.get_user_charging_status)
            
            if data[ACCT_CRG_STATUS]:
                data[ACCT_SESSION] = await hass.async_add_executor_job(
                    client.get_charging_session, data[ACCT_CRG_STATUS].session_id
                )

            home_chargers = await hass.async_add_executor_job(client.get_home_chargers)
            for charger in home_chargers:
                status = await hass.async_add_executor_job(client.get_home_charger_status, charger)
                tech = await hass.async_add_executor_job(client.get_home_charger_technical_info, charger)
                data[ACCT_HOME_CRGS][charger] = (status, tech)
            return data

        except ChargePointInvalidSession:
            if not is_retry:
                await hass.async_add_executor_job(client.login, username, password)
                hass.config_entries.async_update_entry(
                    entry, data={**entry.data, CONF_ACCESS_TOKEN: client.session_token}
                )
                return await async_update_data(is_retry=True)
            raise ConfigEntryAuthFailed("Session expired")
        except Exception as err:
            # BACK-OFF STRATEGY: If we see a 403 error, tell HA to wait 3600 seconds (1 hour)
            if "403" in str(err):
                _LOGGER.error("ChargePoint 403 Blocked. Backing off for 1 hour.")
                raise UpdateFailed(retry_after=3600) from err
            raise UpdateFailed(f"Error: {err}") from err

    poll_interval = entry.options.get(OPTION_POLL_INTERVAL, POLL_INTERVAL_DEFAULT)
    coordinator = DataUpdateCoordinator(
        hass, _LOGGER, name=DOMAIN, update_method=async_update_data,
        update_interval=timedelta(seconds=poll_interval),
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {DATA_CLIENT: client, DATA_COORDINATOR: coordinator}
    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

class ChargePointEntity(CoordinatorEntity):
    def __init__(self, client, coordinator):
        super().__init__(coordinator)
        self.client = client
    @property
    def account(self) -> ChargePointAccount:
        return self.coordinator.data[ACCT_INFO]

class ChargePointChargerEntity(CoordinatorEntity):
    def __init__(self, client, coordinator, charger_id):
        super().__init__(coordinator)
        self.client = client
        self.charger_id = charger_id
        self.manufacturer = "ChargePoint" if self.charger_status.brand == "CP" else self.charger_status.brand
        self.short_model = self.charger_status.model.split("-")[0]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self.charger_id))},
            manufacturer=self.manufacturer,
            model=self.charger_status.model,
            name=f"ChargePoint Home Flex ({self.short_model})",
            sw_version=self.technical_info.software_version,
        )
    @property
    def charger_status(self) -> HomeChargerStatus:
        return self.coordinator.data[ACCT_HOME_CRGS][self.charger_id][0]
    @property
    def technical_info(self) -> HomeChargerTechnicalInfo:
        return self.coordinator.data[ACCT_HOME_CRGS][self.charger_id][1]
    @property
    def session(self) -> Optional[ChargingSession]:
        session_data = self.coordinator.data[ACCT_SESSION]
        if session_data and session_data.device_id == self.charger_id:
            return session_data
        return None

@dataclass
class ChargePointEntityRequiredKeysMixin:
    name_suffix: str
