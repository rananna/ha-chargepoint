"""Config flow for ChargePoint."""

import logging
from collections import OrderedDict
from typing import Any, Mapping, Tuple

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.helpers.selector import selector
from python_chargepoint import ChargePoint
from python_chargepoint.exceptions import (
    ChargePointCommunicationException,
    ChargePointLoginError,
)

from .const import (
    DOMAIN,
    OPTION_POLL_INTERVAL,
    POLL_INTERVAL_DEFAULT,
    POLL_INTERVAL_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)

def _login_schema(username: str = "") -> vol.Schema:
    return vol.Schema(
        OrderedDict([
            (vol.Required(CONF_USERNAME, default=username), str),
            (vol.Required(CONF_PASSWORD, default=""), str),
        ])
    )

class ChargePointFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ChargePoint."""
    VERSION = 1

    async def _login(self, username: str, password: str) -> Tuple[str | None, str | None]:
        try:
            client = await self.hass.async_add_executor_job(ChargePoint, username, password)
            return client.session_token, None
        except ChargePointLoginError:
            return None, "invalid_auth"
        except Exception:
            return None, "cannot_connect"

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            token, error = await self._login(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            if token:
                return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)
            errors["base"] = error

        return self.async_show_form(step_id="user", data_schema=_login_schema(), errors=errors)

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> ConfigFlowResult:
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        if user_input is not None:
            # Logic to update existing entry goes here
            return self.async_abort(reason="reauth_successful")
        return self.async_show_form(step_id="reauth_confirm", data_schema=vol.Schema({vol.Required(CONF_PASSWORD): str}))
