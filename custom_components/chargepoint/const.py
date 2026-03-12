"""Constants for ChargePoint."""
from homeassistant.const import Platform

NAME = "ChargePoint (Custom Stealth)"
DOMAIN = "chargepoint"
VERSION = "1.1.8"
ISSUE_URL = "https://github.com/rananna/ha-chargepoint/issues"

PLATFORMS: list[Platform] = [
    Platform.SENSOR, 
    Platform.BINARY_SENSOR, 
    Platform.BUTTON,
    Platform.SELECT,
    Platform.SWITCH
]

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
OPTION_POLL_INTERVAL = "poll_interval"

# Fixes config_flow.py ImportError
POLL_INTERVAL_OPTIONS = {
    900: "15 minutes",
    1800: "30 minutes",
    3600: "1 hour",
}
POLL_INTERVAL_DEFAULT = 900

TOKEN_FILE_NAME = "chargepoint_session.json"

ACCT_INFO = "account_information"
ACCT_CRG_STATUS = "charging_status"
ACCT_SESSION = "charging_session"
ACCT_HOME_CRGS = "home_chargers"

DATA_CLIENT = "chargepoint_client"
DATA_COORDINATOR = "coordinator"

CHARGER_SESSION_STATE_IN_USE = "IN_USE"
EXCEPTION_WARNING_MSG = "ChargePoint API communication error. Check connection or IP status."
