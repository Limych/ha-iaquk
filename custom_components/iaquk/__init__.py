"""
Component to calculate IAQ UK index.

For more details about this component, please refer to
https://github.com/Limych/ha-iaquk
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_NAME, CONF_SENSORS

from .const import DOMAIN, VERSION, ISSUE_URL, \
    SUPPORT_LIB_URL, CONF_SOURCES
from .sensor import SENSORS

_LOGGER = logging.getLogger(__name__)

SOURCES_SCHEMA = vol.Schema({
    vol.Optional(...)
})

IAQ_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_SOURCES):
        vol.All(cv.ensure_list, [SOURCES_SCHEMA]),
    vol.Optional(CONF_SENSORS):
        vol.All(cv.ensure_list, [vol.In(SENSORS)]),
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.All(cv.ensure_list, [IAQ_SCHEMA])
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up component."""
    # Print startup message
    _LOGGER.info('Version %s', VERSION)
    _LOGGER.info('If you have ANY issues with this,'
                 ' please report them here: %s', ISSUE_URL)

    return True
