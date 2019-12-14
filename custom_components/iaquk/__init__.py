"""
Component to calculate IAQ UK index.

For more details about this component, please refer to
https://github.com/Limych/ha-iaquk
"""

import logging
from typing import Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import DOMAIN as SENSOR
from homeassistant.const import CONF_NAME, CONF_SENSORS
from homeassistant.helpers import discovery

from .const import DOMAIN, VERSION, ISSUE_URL, SUPPORT_LIB_URL, CONF_SOURCES, \
    DATA_IAQUK
from .sensor import SENSORS

_LOGGER = logging.getLogger(__name__)

SOURCES_SCHEMA = vol.Schema({
    vol.Optional(...)
})

IAQ_SCHEMA = vol.Schema({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_SOURCES):
        vol.All(cv.ensure_list, [SOURCES_SCHEMA]),
    vol.Optional(CONF_SENSORS):
        vol.All(cv.ensure_list, [vol.In(SENSORS)]),
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: cv.schema_with_slug_keys(IAQ_SCHEMA),
}, extra=vol.ALLOW_EXTRA)


def _deslugify(string):
    return string.replace('_', ' ').title()


async def async_setup(hass, config):
    """Set up component."""
    # Print startup message
    _LOGGER.info('Version %s', VERSION)
    _LOGGER.info('If you have ANY issues with this,'
                 ' please report them here: %s', ISSUE_URL)

    hass.data.setdefault(DATA_IAQUK, {})

    for object_id, cfg in config[DOMAIN].items():
        if not cfg:
            cfg = {}

        name = cfg.get(CONF_NAME, _deslugify(object_id))
        sources = cfg.get(CONF_SOURCES)
        sensors = cfg.get(CONF_SENSORS)

        controller = Iaquk(hass, object_id, name, sources)
        hass.data[DATA_IAQUK][object_id] = controller

        if sensors:
            discovery.load_platform(hass, SENSOR, DOMAIN, {
                CONF_NAME: object_id,
                CONF_SENSORS: sensors,
            }, config)

    if not hass.data[DATA_IAQUK]:
        return False

    return True


class Iaquk:
    """IAQ UK controller."""

    def __init__(self, hass, entity_id: str, name: str, sources):
        """Initialize controller."""
        self.hass = hass
        self._entity_id = entity_id
        self._name = name

        self._iaq_index = None

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._entity_id

    @property
    def name(self):
        """Get controller name."""
        return self._name

    @property
    def iaq_index(self) -> Optional[int]:
        """Get IAQ index."""
        return self._iaq_index

    @property
    def iaq_level(self) -> Optional[str]:
        """Get IAQ level."""
        # Transform IAQ index to human readable text according
        # to Indoor Air Quality UK: http://www.iaquk.org.uk/
        if self._iaq_index is None:
            return None
        elif self._iaq_index <= 25:
            return "Inadequate"
        elif self._iaq_index <= 38:
            return "Poor"
        elif self._iaq_index <= 51:
            return "Fair"
        elif self._iaq_index <= 60:
            return "Good"
        else:
            return "Excellent"

    def update(self):
        pass
