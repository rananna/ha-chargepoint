import logging
from dataclasses import dataclass
from typing import Callable
from homeassistant.components.button import ButtonDeviceClass, ButtonEntity, ButtonEntityDescription
from homeassistant.helpers.entity import EntityCategory
from . import ChargePointChargerEntity, ChargePointEntityRequiredKeysMixin
from .const import ACCT_HOME_CRGS, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

@dataclass(kw_only=True)
class ChargePointButtonEntityDescription(ButtonEntityDescription, ChargePointEntityRequiredKeysMixin):
    press_action: Callable[[any], any]

class ChargePointButton(ChargePointChargerEntity, ButtonEntity):
    entity_description: ChargePointButtonEntityDescription
    def __init__(self, client, coordinator, description, charger_id):
        super().__init__(client, coordinator, charger_id)
        self.entity_description = description
        self._attr_name, self._attr_unique_id = f"{self.short_model} {description.name_suffix}", f"{charger_id}_{description.key}"
    async def async_press(self) -> None:
        await self.entity_description.press_action(self)

async def async_setup_entry(hass, entry, async_add_entities):
    client, coordinator = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT], hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    entities = [ChargePointButton(client, coordinator, ChargePointButtonEntityDescription(key="restart", name_suffix="Restart", device_class=ButtonDeviceClass.RESTART, entity_category=EntityCategory.DIAGNOSTIC, press_action=lambda e: e.hass.async_add_executor_job(e.client.reboot_home_charger, e.charger_id)), cid) for cid in coordinator.data[ACCT_HOME_CRGS].keys()]
    async_add_entities(entities)
