"""Constants for calculate IAQ UK index."""

# Base component constants
DOMAIN = "iaquk"
VERSION = "1.2.0"
ISSUE_URL = "https://github.com/Limych/ha-iaquk/issues"
ATTRIBUTION = None
DATA_IAQUK = 'iaquk'

SUPPORT_LIB_URL = "https://github.com/Limych/iaquk/issues/new/choose"

CONF_SOURCES = "sources"
CONF_TEMPERATURE = "temperature"
CONF_HUMIDITY = "humidity"
CONF_CO2 = "co2"
CONF_TVOC = "tvoc"
CONF_PM = "pm"
CONF_NO2 = "no2"
CONF_CO = "co"
CONF_HCHO = "hcho"  # Formaldehyde

ATTR_SOURCES_SET = 'sources_set'
ATTR_SOURCES_USED = 'sources_used'

LEVEL_EXCELLENT = "Excellent"
LEVEL_GOOD = "Good"
LEVEL_FAIR = "Fair"
LEVEL_POOR = "Poor"
LEVEL_INADEQUATE = "Inadequate"

UNIT_PPM = {
    'ppm': 1,
    'ppb': 0.001,
    'mg/m³': 0.224,
    'mg/m3': 0.224,
    'mg/m^3': 0.224,
    'µg/m³': 224,
    'µg/m3': 224,
    'µg/m^3': 224,
}
UNIT_PPB = {
    'ppb': 1,
    'ppm': 1000,
    'mg/m³': 224,
    'mg/m3': 224,
    'mg/m^3': 224,
    'µg/m³': 224000,
    'µg/m3': 224000,
    'µg/m^3': 224000,
}
UNIT_UGM3 = {
    'µg/m³': 1,
    'µg/m3': 1,
    'µg/m^3': 1,
    'mg/m³': 0.001,
    'mg/m3': 0.001,
    'mg/m^3': 0.001,
    'ppm': 1 / 224,
    'ppb': 1 / 224000,
}
UNIT_MGM3 = {
    'mg/m³': 1,
    'mg/m3': 1,
    'mg/m^3': 1,
    'µg/m³': 1000,
    'µg/m3': 1000,
    'µg/m^3': 1000,
    'ppm': 1000 / 224,
    'ppb': 1 / 224,
}
