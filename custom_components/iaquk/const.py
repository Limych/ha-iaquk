"""Constants for calculate IAQ UK index."""

# Base component constants
NAME = "Indoor Air Quality UK Index"
DOMAIN = "iaquk"
VERSION = "1.3.5.dev0"
ISSUE_URL = "https://github.com/Limych/ha-iaquk/issues"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have ANY issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

# Icons

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
PLATFORMS = [BINARY_SENSOR, SENSOR]

# Configuration and options
CONF_SOURCES = "sources"
CONF_TEMPERATURE = "temperature"
CONF_HUMIDITY = "humidity"
CONF_CO2 = "co2"
CONF_TVOC = "tvoc"
CONF_PM = "pm"
CONF_NO2 = "no2"
CONF_CO = "co"
CONF_HCHO = "hcho"  # Formaldehyde
CONF_RADON = "radon"

# Defaults

# Attributes
ATTR_SOURCES_SET = "sources_set"
ATTR_SOURCES_USED = "sources_used"


LEVEL_EXCELLENT = "Excellent"
LEVEL_GOOD = "Good"
LEVEL_FAIR = "Fair"
LEVEL_POOR = "Poor"
LEVEL_INADEQUATE = "Inadequate"

UNIT_PPM = {
    "ppm": 1,  # Target unit -- conversion rate will be ignored
    "ppb": 0.001,
}
UNIT_PPB = {
    "ppb": 1,  # Target unit -- conversion rate will be ignored
    "ppm": 1000,
}
UNIT_UGM3 = {
    "µg/m³": 1,  # Target unit -- conversion rate will be ignored
    "µg/m3": 1,
    "µg/m^3": 1,
    "mg/m³": 0.001,
    "mg/m3": 0.001,
    "mg/m^3": 0.001,
}
UNIT_MGM3 = {
    "mg/m³": 1,  # Target unit -- conversion rate will be ignored
    "mg/m3": 1,
    "mg/m^3": 1,
    "µg/m³": 1000,
    "µg/m3": 1000,
    "µg/m^3": 1000,
}

MWEIGTH_TVOC = 56.1060  # g/mol
MWEIGTH_HCHO = 30.0260  # g/mol
MWEIGTH_CO = 28.0100  # g/mol
MWEIGTH_NO2 = 46.0100  # g/mol
MWEIGTH_CO2 = 44.0100  # g/mol
