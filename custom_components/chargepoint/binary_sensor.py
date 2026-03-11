from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from . import ChargePointChargerEntity
from .const import DATA_CLIENT, DATA_COORDINATOR, DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    entities = [ChargePointPluggedInBinary(data["client"], data["coordinator"], cid) 
                for cid in data["coordinator"].data["home_chargers"].keys()]
    async_add_entities(entities)

class ChargePointPluggedInBinary(ChargePointChargerEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PLUG
    def __init__(self, client, coordinator, charger_id):
        super().__init__(client, coordinator, charger_id)
        self._attr_name = f"EV Connected ({self.short_model})"
        self._attr_unique_id = f"{charger_id}_plugged_in_binary"
    @property
    def is_on(self) -> bool:
        return self.charger_status.plugged_in
