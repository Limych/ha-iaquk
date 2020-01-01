"""Sensor platform to calculate IAQ UK index."""

import logging

from homeassistant.const import CONF_SENSORS
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

SENSOR_INDEX = 'iaq_index'
SENSOR_LEVEL = 'iaq_level'

SENSORS = {
    SENSOR_INDEX: 'Air Quality Index',
    SENSOR_LEVEL: 'Air Quality Level',
}


async def async_setup_platform(hass, config, async_add_entities,    # pylint: disable=w0613
                               discovery_info=None):
    """Set up a sensors to calculate IAQ UK index."""
    if discovery_info is None:
        return

    # controller = hass.data[DATA_IAQUK][discovery_info[CONF_NAME]]

    # sensors = discovery_info[CONF_SENSORS]

    sensors = []
    for sensor_type in discovery_info[CONF_SENSORS]:
        sensors.append(IaqukSensor(sensor_type))

    async_add_entities(sensors, True)


class IaqukSensor(Entity):
    """IAQ UK sensor."""

    def __init__(self, sensor_type: str):
        pass    # todo   pylint: disable=w0511
