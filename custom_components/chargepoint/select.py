import logging
from dataclasses import dataclass
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import UnitOfElectricCurrent
from homeassistant.exceptions import HomeAssistantError
from python_chargepoint.exceptions import ChargePointCommunicationException
from . import ChargePointChargerEntity, ChargePointEntityRequiredKeysMixin
from .const import ACCT_HOME_CRGS, DATA_CLIENT, DATA_COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

@dataclass(kw_only=True)
class ChargePointSelectEntityDescription(SelectEntityDescription, ChargePointEntityRequiredKeysMixin):
    pass

class ChargePointChargerChargeLimitSelectEntity(SelectEntity, ChargePointChargerEntity):
    entity_description: ChargePointSelectEntityDescription
    def __init__(self, hass, client, coordinator, description, charger_id):
        super().__init__(client, coordinator, charger_id)
        self.hass, self.entity_description = hass, description
        self._attr_name, self._attr_unique_id = f"{self.short_model} {description.name_suffix}", f"{charger_id}_{description.key}"

    @property
    def options(self) -> list[str]:
        limits = self.charger_status.possible_amperage_limits
        if isinstance(limits, int): return [str(limits)]
        if not limits: return [str(self.current_option)]
        return [str(v) for v in limits]

    @property
    def current_option(self) -> str: return str(self.charger_status.amperage_limit)

    async def async_select_option(self, option: str) -> None:
        if not self.charger_status.plugged_in: raise HomeAssistantError("Cannot set amperage if charger not plugged in!")
        try:
            await self.hass.async_add_executor_job(self.client.set_amperage_limit, self.charger_id, int(option))
        except ChargePointCommunicationException: raise HomeAssistantError("Cannot set new amperage limit!")
        await self.coordinator.async_request_refresh()

async def async_setup_entry(hass, entry, async_add_entities):
    client, coordinator = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT], hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    entities = [ChargePointChargerChargeLimitSelectEntity(hass, client, coordinator, ChargePointSelectEntityDescription(key="charging_amperage_limit", name_suffix="Charging Amperage Limit", unit_of_measurement=UnitOfElectricCurrent.AMPERE, icon="mdi:tune-variant"), cid) for cid in coordinator.data[ACCT_HOME_CRGS].keys()]
    async_add_entities(entities)
