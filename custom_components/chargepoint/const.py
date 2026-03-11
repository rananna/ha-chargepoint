"""Constants for ChargePoint."""
from homeassistant.const import Platform

NAME = "ChargePoint"
DOMAIN = "chargepoint"
VERSION = "1.1.0"
ISSUE_URL = "https://github.com/yourusername/ha-chargepoint-custom/issues"

# Platforms - Added BINARY_SENSOR for the new "EV Connected" entity
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SWITCH, Platform.SELECT, Platform.BUTTON]

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
OPTION_POLL_INTERVAL = "poll_interval"

# Safer polling intervals to prevent 403 Forbidden blocks
POLL_INTERVAL_OPTIONS = {
    900: "15 minutes",
    1800: "30 minutes",
    3600: "1 hour",
}
POLL_INTERVAL_DEFAULT = 900

TOKEN_FILE_NAME = "chargepoint_session.json"

# Data Mapping (Matches your existing integration structure)
ACCT_INFO = "account_information"
ACCT_CRG_STATUS = "charging_status"
ACCT_SESSION = "charging_session"
ACCT_HOME_CRGS = "home_chargers"

DATA_CLIENT = "chargepoint_client"
DATA_COORDINATOR = "coordinator"
