"""Config flow for ChargePoint."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_ACCESS_TOKEN
from homeassistant.core import callback
from python_chargepoint import ChargePoint
from python_chargepoint.exceptions import ChargePointLoginError, ChargePointCommunicationException

from .const import DOMAIN, OPTION_POLL_INTERVAL, POLL_INTERVAL_DEFAULT, POLL_INTERVAL_OPTIONS

_LOGGER = logging.getLogger(__name__)

class ChargePointFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ChargePoint."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                client = await self.hass.async_add_executor_job(
                    ChargePoint, user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
                )
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], 
                    data={**user_input, CONF_ACCESS_TOKEN: client.session_token}
                )
            except ChargePointLoginError as exc:
                error_id = exc.response.json().get("errorId")
                errors["base"] = "account_locked" if error_id == 241 else "invalid_auth"
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ChargePointOptionsFlowHandler(config_entry)

class ChargePointOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for ChargePoint."""
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    OPTION_POLL_INTERVAL,
                    default=self.config_entry.options.get(OPTION_POLL_INTERVAL, POLL_INTERVAL_DEFAULT),
                ): vol.In(POLL_INTERVAL_OPTIONS),
            }),
        )
