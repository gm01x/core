"""Test the Temp Controller climate platform."""

import pytest

from homeassistant.components.climate import (
    ATTR_CURRENT_TEMPERATURE,
    ATTR_HVAC_ACTION,
    ATTR_HVAC_MODE,
    ATTR_HVAC_MODES,
    DOMAIN as CLIMATE_DOMAIN,
    SERVICE_SET_HVAC_MODE,
    SERVICE_SET_TEMPERATURE,
    HVACAction,
    HVACMode,
)
from homeassistant.components.temp_controller import DOMAIN
from homeassistant.const import ATTR_ENTITY_ID, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

ENTITY_ID = "climate.temp_controller"


@pytest.mark.usefixtures("setup_integration")
async def test_climate_state(hass: HomeAssistant) -> None:
    """Test the climate entity is created with expected defaults."""
    state = hass.states.get(ENTITY_ID)
    assert state is not None
    assert state.state == HVACMode.HEAT
    assert state.attributes[ATTR_TEMPERATURE] == 21.0
    assert state.attributes[ATTR_CURRENT_TEMPERATURE] == 20.0
    assert state.attributes[ATTR_HVAC_ACTION] == HVACAction.HEATING
    assert state.attributes[ATTR_HVAC_MODES] == [HVACMode.HEAT, HVACMode.OFF]


@pytest.mark.usefixtures("setup_integration")
async def test_climate_unique_id(
    hass: HomeAssistant, entity_registry: er.EntityRegistry
) -> None:
    """Test the climate unique ID matches the config entry ID."""
    entry = hass.config_entries.async_entries(DOMAIN)[0]
    entity_entry = entity_registry.async_get(ENTITY_ID)
    assert entity_entry is not None
    assert entity_entry.unique_id == entry.entry_id


@pytest.mark.usefixtures("setup_integration")
async def test_set_temperature(hass: HomeAssistant) -> None:
    """Test setting the target temperature."""
    await hass.services.async_call(
        CLIMATE_DOMAIN,
        SERVICE_SET_TEMPERATURE,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_TEMPERATURE: 24},
        blocking=True,
    )

    state = hass.states.get(ENTITY_ID)
    assert state is not None
    assert state.attributes[ATTR_TEMPERATURE] == 24
    assert state.attributes[ATTR_CURRENT_TEMPERATURE] == 20.0


@pytest.mark.usefixtures("setup_integration")
async def test_set_hvac_mode(hass: HomeAssistant) -> None:
    """Test setting the HVAC mode."""
    await hass.services.async_call(
        CLIMATE_DOMAIN,
        SERVICE_SET_HVAC_MODE,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_HVAC_MODE: HVACMode.OFF},
        blocking=True,
    )

    state = hass.states.get(ENTITY_ID)
    assert state is not None
    assert state.state == HVACMode.OFF
    assert state.attributes[ATTR_HVAC_ACTION] == HVACAction.OFF
