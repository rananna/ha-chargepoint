import logging
import requests
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from python_chargepoint import ChargePoint
from python_chargepoint.session import ChargingSession
from python_chargepoint.types import ChargePointAccount, HomeChargerStatus, HomeChargerTechnicalInfo

from .const import (
    ACCT_CRG_STATUS, ACCT_HOME_CRGS, ACCT_INFO, ACCT_SESSION,
    DATA_CLIENT, DATA_COORDINATOR, DOMAIN, OPTION_POLL_INTERVAL, POLL_INTERVAL_DEFAULT,
)

BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
_LOGGER = logging.getLogger(__package__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.BUTTON]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    username, password = entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD]
    session_token = entry.data.get(CONF_ACCESS_TOKEN)

    stealth_session = requests.Session()
    stealth_session.headers.update({"User-Agent": BROWSER_USER_AGENT})

    try:
        client = await hass.async_add_executor_job(ChargePoint, username, password, session_token, stealth_session)
        if client.session_token != session_token:
            hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_ACCESS_TOKEN: client.session_token})
    except Exception as exc:
        _LOGGER.warning("ChargePoint setup failed (likely 403 block): %s", exc)
        raise ConfigEntryNotReady from exc

    async def async_update_data():
        try:
            data = {ACCT_INFO: None, ACCT_CRG_STATUS: None, ACCT_SESSION: None, ACCT_HOME_CRGS: {}}
            data[ACCT_INFO] = await hass.async_add_executor_job(client.get_account)
            data[ACCT_CRG_STATUS] = await hass.async_add_executor_job(client.get_user_charging_status)
            if data[ACCT_CRG_STATUS]:
                data[ACCT_SESSION] = await hass.async_add_executor_job(client.get_charging_session, data[ACCT_CRG_STATUS].session_id)
            for charger in await hass.async_add_executor_job(client.get_home_chargers):
                status = await hass.async_add_executor_job(client.get_home_charger_status, charger)
                tech = await hass.async_add_executor_job(client.get_home_charger_technical_info, charger)
                data[ACCT_HOME_CRGS][charger] = (status, tech)
            return data
        except Exception as err:
            if "403" in str(err):
                _LOGGER.error("ChargePoint 403 Blocked. Backing off for 1 hour.")
                raise UpdateFailed(retry_after=3600) from err
            raise UpdateFailed(err) from err

    coordinator = DataUpdateCoordinator(hass, _LOGGER, name=DOMAIN, update_method=async_update_data, 
                                        update_interval=timedelta(seconds=entry.options.get(OPTION_POLL_INTERVAL, POLL_INTERVAL_DEFAULT)))
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {DATA_CLIENT: client, DATA_COORDINATOR: coordinator}
    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

class ChargePointChargerEntity(CoordinatorEntity):
    def __init__(self, client, coordinator, charger_id):
        super().__init__(coordinator)
        self.client, self.charger_id = client, charger_id
        self.short_model = self.charger_status.model.split("-")[0]
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, str(self.charger_id))}, manufacturer="ChargePoint", model=self.charger_status.model, name=f"Home Flex ({self.short_model})", sw_version=self.technical_info.software_version)
    @property
    def charger_status(self) -> HomeChargerStatus: return self.coordinator.data[ACCT_HOME_CRGS][self.charger_id][0]
    @property
    def technical_info(self) -> HomeChargerTechnicalInfo: return self.coordinator.data[ACCT_HOME_CRGS][self.charger_id][1]
    @property
    def session(self) -> Optional[ChargingSession]:
        s = self.coordinator.data[ACCT_SESSION]
        return s if s and s.device_id == self.charger_id else None

@dataclass
class ChargePointEntityRequiredKeysMixin: name_suffix: str
