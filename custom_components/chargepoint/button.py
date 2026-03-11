import logging
from homeassistant.components.button import ButtonDeviceClass, ButtonEntity, ButtonEntityDescription
from . import ChargePointChargerEntity
from .const import ACCT_HOME_CRGS, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

class ChargePointBaseButton(ChargePointChargerEntity, ButtonEntity):
    def __init__(self, client, coordinator, description, charger_id):
        super().__init__(client, coordinator, charger_id)
        self.entity_description = description
        self._attr_name, self._attr_unique_id = f"{self.short_model} {description.name_suffix}", f"{charger_id}_{description.key}"
    async def async_press(self):
        await self._handle_press()
        await self.coordinator.async_request_refresh()

class RestartButton(ChargePointBaseButton):
    async def _handle_press(self): await self.hass.async_add_executor_job(self.client.restart_home_charger, self.charger_id)

class StartButton(ChargePointBaseButton):
    async def _handle_press(self): await self.hass.async_add_executor_job(self.client.start_charging_session, self.charger_id)

class StopButton(ChargePointBaseButton):
    async def _handle_press(self):
        if self.session: await self.hass.async_add_executor_job(self.session.stop)

async def async_setup_entry(hass, entry, async_add_entities):
    client, coordinator = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT], hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    entities = []
    for cid in coordinator.data[ACCT_HOME_CRGS].keys():
        entities.append(RestartButton(client, coordinator, ButtonEntityDescription(key="restart", name_suffix="Restart", device_class=ButtonDeviceClass.RESTART), cid))
        entities.append(StartButton(client, coordinator, ButtonEntityDescription(key="start", name_suffix="Start", icon="mdi:play"), cid))
        entities.append(StopButton(client, coordinator, ButtonEntityDescription(key="stop", name_suffix="Stop", icon="mdi:stop"), cid))
    async_add_entities(entities)
