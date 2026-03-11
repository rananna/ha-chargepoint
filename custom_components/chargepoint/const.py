"""Constants for ChargePoint."""
from homeassistant.const import Platform

NAME = "ChargePoint (Custom Stealth)"
DOMAIN = "chargepoint"
VERSION = "1.1.5"
ISSUE_URL = "https://github.com/rananna/ha-chargepoint/issues"

# Platforms active in v1.1.5
# Note: Switch and Select are reserved for future enhancements (Amperage/Modes)
PLATFORMS = [
    Platform.SENSOR, 
    Platform.BINARY_SENSOR, 
    Platform.BUTTON
]

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
OPTION_POLL_INTERVAL = "poll_interval"

# Conservative polling to protect against DataDome 403 blocks
POLL_INTERVAL_OPTIONS = {
    900: "15 minutes",
    1800: "30 minutes",
    3600: "1 hour",
}
POLL_INTERVAL_DEFAULT = 900

TOKEN_FILE_NAME = "chargepoint_session.json"

# Data Mapping
ACCT_INFO = "account_information"
ACCT_CRG_STATUS = "charging_status"
ACCT_SESSION = "charging_session"
ACCT_HOME_CRGS = "home_chargers"

DATA_CLIENT = "chargepoint_client"
DATA_COORDINATOR = "coordinator"

CHARGER_SESSION_STATE_IN_USE = "IN_USE"
EXCEPTION_WARNING_MSG = (
    "ChargePoint returned an exception. This may be a temporary "
    "API lockout (403) or a connection timeout."
)
