"""Test integration setup process."""
# pylint: disable=redefined-outer-name,protected-access

from pytest import raises
from pytest_homeassistant_custom_component.common import assert_setup_component
from voluptuous import Invalid

from custom_components.iaquk import (
    ATTR_SOURCE_INDEX_TPL,
    ATTR_SOURCES_SET,
    ATTR_SOURCES_USED,
    CONF_CO,
    CONF_CO2,
    CONF_HCHO,
    CONF_HUMIDITY,
    CONF_NO2,
    CONF_PM,
    CONF_RADON,
    CONF_SOURCES,
    CONF_TEMPERATURE,
    CONF_TVOC,
    CONF_VOC_INDEX,
    DOMAIN,
    LEVEL_EXCELLENT,
    LEVEL_FAIR,
    LEVEL_GOOD,
    LEVEL_INADEQUATE,
    LEVEL_POOR,
    Iaquk,
    _deslugify,
    check_voc_keys,
)
from homeassistant.const import (
    ATTR_UNIT_OF_MEASUREMENT,
    PERCENTAGE,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component


async def async_mock_sensors(hass: HomeAssistant):
    """Mock sensor entity for tests."""
    assert await async_setup_component(
        hass,
        "sensor",
        {
            "sensor": {
                "platform": "template",
                "sensors": {
                    "test_monitored": {
                        "value_template": "{{ 29.82 }}",
                    },
                    "test_monitored2": {
                        "value_template": "{{ 29.82 }}",
                    },
                    "test_monitored3": {
                        "value_template": "{{ 29.82 }}",
                    },
                },
            }
        },
    )
    await hass.async_block_till_done()


async def test_check_voc_keys():
    """Test check_voc_keys function."""
    _ = check_voc_keys({})
    _ = check_voc_keys({CONF_TVOC: "qwe"})
    _ = check_voc_keys({CONF_VOC_INDEX: "qwe"})
    _ = check_voc_keys({"zxc": "qwe", CONF_VOC_INDEX: "asd"})
    _ = check_voc_keys({CONF_TVOC: "qwe", "zxc": "asd"})

    with raises(Invalid):
        _ = check_voc_keys({CONF_TVOC: "qwe", CONF_VOC_INDEX: "asd"})


async def test__deslugify():
    """Test deslugifying entity id."""
    assert _deslugify("test") == "Test"
    assert _deslugify("another_test") == "Another Test"


async def test_async_setup_empty(hass: HomeAssistant):
    """Test a successful setup component."""
    await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
    await hass.async_block_till_done()


async def test_async_setup(hass: HomeAssistant):
    """Test a successful setup component."""
    config = {
        "test": {
            CONF_SOURCES: {
                CONF_TEMPERATURE: "sensor.test_temperature",
                CONF_PM: ["sensor.test_temperature"],
            },
        }
    }
    with assert_setup_component(1, DOMAIN):
        await async_setup_component(hass, DOMAIN, {DOMAIN: config})
        await hass.async_block_till_done()

    await hass.async_start()
    await hass.async_block_till_done()


async def test_controller_init(hass: HomeAssistant):
    """Test controller initialization."""
    controller = Iaquk(hass, "test", "Test", {"": "sensor.test_monitored"})

    expected_attributes = {
        ATTR_SOURCES_SET: 1,
        ATTR_SOURCES_USED: 0,
    }

    assert controller.unique_id == "test"
    assert controller.name == "Test"
    assert controller.iaq_index is None
    assert controller.iaq_level is None
    assert controller.state_attributes == expected_attributes


async def test_update(hass: HomeAssistant):
    """Test update index state."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"
    config = {
        CONF_TEMPERATURE: entity_id,
        CONF_HUMIDITY: entity_id + "2",
        CONF_CO2: entity_id + "3",
    }
    controller = Iaquk(hass, "test", "Test", config)

    hass.states.async_set(
        entity_id, 17, {ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS}
    )
    hass.states.async_set(entity_id + "2", 50, {ATTR_UNIT_OF_MEASUREMENT: PERCENTAGE})
    hass.states.async_set(entity_id + "3", 800, {ATTR_UNIT_OF_MEASUREMENT: "ppm"})
    controller.update()

    expected_attributes = {
        ATTR_SOURCES_SET: 3,
        ATTR_SOURCES_USED: 3,
        ATTR_SOURCE_INDEX_TPL.format("temperature"): 4,
        ATTR_SOURCE_INDEX_TPL.format("humidity"): 5,
        ATTR_SOURCE_INDEX_TPL.format("co2"): 4,
    }

    assert controller.iaq_index == 56
    assert controller.iaq_level == LEVEL_GOOD
    assert controller.state_attributes == expected_attributes

    config = {
        CONF_TEMPERATURE: entity_id,
    }
    controller = Iaquk(hass, "test", "Test", config)

    expected_attributes = {
        ATTR_SOURCES_SET: 1,
        ATTR_SOURCES_USED: 1,
    }
    attr_temp = ATTR_SOURCE_INDEX_TPL.format("temperature")

    hass.states.async_set(
        entity_id, 18, {ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS}
    )
    expected_attributes[attr_temp] = 5
    controller.update()

    assert controller.iaq_index == 65
    assert controller.iaq_level == LEVEL_EXCELLENT
    assert controller.state_attributes == expected_attributes

    hass.states.async_set(
        entity_id, 16, {ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS}
    )
    expected_attributes[attr_temp] = 3
    controller.update()

    assert controller.iaq_index == 39
    assert controller.iaq_level == LEVEL_FAIR
    assert controller.state_attributes == expected_attributes

    hass.states.async_set(
        entity_id, 15, {ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS}
    )
    expected_attributes[attr_temp] = 2
    controller.update()

    assert controller.iaq_index == 26
    assert controller.iaq_level == LEVEL_POOR
    assert controller.state_attributes == expected_attributes

    hass.states.async_set(
        entity_id, 14, {ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS}
    )
    expected_attributes[attr_temp] = 1
    controller.update()

    assert controller.iaq_index == 13
    assert controller.iaq_level == LEVEL_INADEQUATE
    assert controller.state_attributes == expected_attributes


async def test__has_state():
    """Test state detection."""
    assert Iaquk._has_state(None) is False
    assert Iaquk._has_state(STATE_UNKNOWN) is False
    assert Iaquk._has_state(STATE_UNAVAILABLE) is False

    assert Iaquk._has_state("") is True


async def test__get_number_state(hass: HomeAssistant):
    """Test state conversion to number."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"
    config = {
        CONF_TEMPERATURE: entity_id,
    }
    controller = Iaquk(hass, "test", "Test", config)

    assert controller._get_number_state("sensor.nonexistent") is None

    assert controller._get_number_state(entity_id) == 29.82
    assert controller._get_number_state(entity_id, "") is None
    assert round(controller._get_number_state(entity_id, "", mweight=1), 2) == 729.10
    assert controller._get_number_state(entity_id, "ppb", mweight=1) == 729099

    hass.states.async_set(entity_id, STATE_UNKNOWN)
    #
    assert controller._get_number_state(entity_id, "") is None

    hass.states.async_set(entity_id, 12.5, {ATTR_UNIT_OF_MEASUREMENT: "ppm"})
    #
    assert round(controller._get_number_state(entity_id, "", mweight=10), 2) == 5.11


async def test__temperature_index(hass: HomeAssistant):
    """Test transform indoor temperature values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_HUMIDITY: entity_id})

    assert controller._temperature_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    hass.states.async_set(entity_id, 12.5, {ATTR_UNIT_OF_MEASUREMENT: "ppm"})
    with raises(ValueError):
        _ = controller._temperature_index

    for i, value in enumerate([57, 59, 60, 63, 67]):
        hass.states.async_set(
            entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.FAHRENHEIT}
        )
        assert controller._temperature_index == i + 1


async def test__humidity_index(hass: HomeAssistant):
    """Test transform indoor humidity values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._humidity_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_HUMIDITY: entity_id})

    hass.states.async_set(
        entity_id, 12.5, {ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS}
    )
    assert controller._humidity_index is None

    for i, value in enumerate([9.9, 19.9, 29.9, 39.9, 40]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: PERCENTAGE})
        assert controller._humidity_index == i + 1

    for i, value in enumerate([90.1, 80.1, 70.1, 60.1, 60]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: PERCENTAGE})
        assert controller._humidity_index == i + 1


async def test__co2_index(hass: HomeAssistant):
    """Test transform indoor eCO2 values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._co2_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_CO2: "sensor.nonexistent"})

    assert controller._co2_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_CO2: entity_id})

    for i, value in enumerate([1801, 1800, 1500, 800, 600]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "ppm"})
        assert controller._co2_index == i + 1

    for i, value in enumerate([1801, 1501, 801, 601, 600]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "ppm"})
        assert controller._co2_index == i + 1


async def test__tvoc_index(hass: HomeAssistant):
    """Test transform indoor tVOC values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._tvoc_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_TVOC: "sensor.nonexistent"})

    assert controller._tvoc_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_TVOC: entity_id})

    for i, value in enumerate([1.01, 1.0, 0.49, 0.29, 0.09]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
        assert controller._tvoc_index == i + 1

    for i, value in enumerate([1.01, 0.5, 0.3, 0.1, 0.09]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
        assert controller._tvoc_index == i + 1


async def test__voc_index_index(hass: HomeAssistant):
    """Test transform indoor VOC index values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._voc_index_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_VOC_INDEX: "sensor.nonexistent"})

    assert controller._voc_index_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_VOC_INDEX: entity_id})

    for i, value in enumerate([261, 181, 116, 51, 0]):
        hass.states.async_set(entity_id, value)
        assert controller._voc_index_index == i + 1

    for i, value in enumerate([500, 260, 180, 115, 50]):
        hass.states.async_set(entity_id, value)
        assert controller._voc_index_index == i + 1


async def test__pm_index(hass: HomeAssistant):
    """Test transform indoor particulate matters values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._pm_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_PM: []})

    assert controller._pm_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_PM: ["sensor.nonexistent"]})

    assert controller._pm_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_PM: [entity_id]})

    for i, value in enumerate([0.065, 0.064, 0.053, 0.041, 0.023]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
        assert controller._pm_index == i + 1

    for i, value in enumerate([0.065, 0.054, 0.042, 0.024, 0.023]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
        assert controller._pm_index == i + 1


async def test__no2_index(hass: HomeAssistant):
    """Test transform indoor NO2 values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._no2_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_NO2: "sensor.nonexistent"})

    assert controller._no2_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_NO2: entity_id})

    for i, value in enumerate([0.41, 0.4, 0.19]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
        assert controller._no2_index == i * 2 + 1

    hass.states.async_set(entity_id, 0.2, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
    assert controller._no2_index == 3


async def test__co_index(hass: HomeAssistant):
    """Test transform indoor CO values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._co_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_CO: "sensor.nonexistent"})

    assert controller._co_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_CO: entity_id})

    for i, value in enumerate([7.1, 7, 0.9]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
        assert controller._co_index == i * 2 + 1

    hass.states.async_set(entity_id, 1, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
    assert controller._co_index == 3


async def test__hcho_index(hass: HomeAssistant):
    """Test transform indoor Formaldehyde (HCHO) values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._hcho_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_HCHO: "sensor.nonexistent"})

    assert controller._hcho_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_HCHO: entity_id})

    for i, value in enumerate([0.201, 0.20, 0.10, 0.05, 0.019]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
        assert controller._hcho_index == i + 1

    for i, value in enumerate([0.201, 0.101, 0.051, 0.02, 0.019]):
        hass.states.async_set(entity_id, value, {ATTR_UNIT_OF_MEASUREMENT: "mg/m3"})
        assert controller._hcho_index == i + 1


async def test__radon_index(hass: HomeAssistant):
    """Test transform indoor Radon (Rn) values to IAQ points."""
    await async_mock_sensors(hass)

    entity_id = "sensor.test_monitored"

    controller = Iaquk(hass, "test", "Test", {CONF_TEMPERATURE: entity_id})

    assert controller._radon_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_RADON: "sensor.nonexistent"})

    assert controller._radon_index is None

    controller = Iaquk(hass, "test", "Test", {CONF_RADON: entity_id})

    hass.states.async_set(entity_id, 101, {ATTR_UNIT_OF_MEASUREMENT: "Bq/m3"})
    assert controller._radon_index == 1

    hass.states.async_set(entity_id, 100, {ATTR_UNIT_OF_MEASUREMENT: "Bq/m3"})
    assert controller._radon_index == 2

    hass.states.async_set(entity_id, 20, {ATTR_UNIT_OF_MEASUREMENT: "Bq/m3"})
    assert controller._radon_index == 2

    hass.states.async_set(entity_id, 19, {ATTR_UNIT_OF_MEASUREMENT: "Bq/m3"})
    assert controller._radon_index == 3

    hass.states.async_set(entity_id, 1, {ATTR_UNIT_OF_MEASUREMENT: "Bq/m3"})
    assert controller._radon_index == 3

    hass.states.async_set(entity_id, 0, {ATTR_UNIT_OF_MEASUREMENT: "Bq/m3"})
    assert controller._radon_index == 5
