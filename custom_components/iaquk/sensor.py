"""Sensor platform to calculate IAQ UK index."""

import logging

from homeassistant.const import CONF_NAME, CONF_SENSORS

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    SENSOR_INDEX: 'Air Quality Index',
    SENSOR_LEVEL: 'Air Quality Level',
}

async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Set up a sensors to calculate IAQ UK index."""
    if discovery_info is None:
        return

    name = discovery_info[CONF_NAME]

    sensors = []
    for sensor_type in discovery_info[CONF_SENSORS]:
        sensors.append(IaqukSensor(sensor_type))

    async_add_entities(sensors, True)
