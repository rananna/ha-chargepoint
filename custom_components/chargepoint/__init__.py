import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator, UpdateFailed
from python_chargepoint import ChargePoint
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .const import (
    ACCT_CRG_STATUS, ACCT_HOME_CRGS, ACCT_INFO, ACCT_SESSION,
    DATA_CLIENT, DATA_COORDINATOR, DOMAIN, OPTION_POLL_INTERVAL, POLL_INTERVAL_DEFAULT,
)

BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
_LOGGER = logging.getLogger(__package__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR, 
    Platform.BINARY_SENSOR, 
    Platform.SELECT, 
    Platform.SWITCH
]

@dataclass(kw_only=True)
class ChargePointEntityRequiredKeysMixin: 
    name_suffix: str

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    def create_client():
        c = ChargePoint(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD], entry.data.get(CONF_ACCESS_TOKEN))
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        for attr in ("session", "_session"):
            if hasattr(c, attr):
                session = getattr(c, attr)
                session.headers.update({"User-Agent": BROWSER_USER_AGENT})
                session.mount("https://", adapter)
                session.mount("http://", adapter)
        return c

    try:
        client = await hass.async_add_executor_job(create_client)
    except Exception as exc:
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
            raise UpdateFailed(err) from err

    coordinator = DataUpdateCoordinator(
        hass, _LOGGER, name=DOMAIN, 
        update_method=async_update_data, 
        update_interval=timedelta(seconds=entry.options.get(OPTION_POLL_INTERVAL, POLL_INTERVAL_DEFAULT))
    )
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
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self.charger_id))}, 
            manufacturer="ChargePoint", 
            name=f"Home Flex ({self.short_model})",
            model=self.charger_status.model, 
            sw_version=self.technical_info.software_version
        )
    @property
    def charger_status(self): return self.coordinator.data[ACCT_HOME_CRGS][self.charger_id][0]
    @property
    def technical_info(self): return self.coordinator.data[ACCT_HOME_CRGS][self.charger_id][1]
    @property
    def session(self):
        s = self.coordinator.data[ACCT_SESSION]
        return s if s and s.device_id == self.charger_id else None
