"""Test the Test Bulb light platform."""

from unittest.mock import AsyncMock

import pytest

from homeassistant.components.light import (
    ATTR_COLOR_TEMP_KELVIN,
    DOMAIN as LIGHT_DOMAIN,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests.common import MockConfigEntry


@pytest.fixture
async def test_bulb_setup(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> MockConfigEntry:
    """Set up the Test Bulb integration."""
    from homeassistant.components.test_bulb.const import DOMAIN

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={},
        unique_id="test_bulb_instance",
    )
    entry.add_to_hass(hass)
    
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    
    return entry


async def test_light_on_off(hass: HomeAssistant, test_bulb_setup: MockConfigEntry) -> None:
    """Test turning the light on and off."""
    entity_id = "light.test_bulb"
    
    state = hass.states.get(entity_id)
    assert state
    assert state.state == STATE_OFF

    await hass.services.async_call(
        LIGHT_DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )

    state = hass.states.get(entity_id)
    assert state.state == STATE_ON

    await hass.services.async_call(
        LIGHT_DOMAIN,
        SERVICE_TURN_OFF,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )

    state = hass.states.get(entity_id)
    assert state.state == STATE_OFF


async def test_light_color_temp(hass: HomeAssistant, test_bulb_setup: MockConfigEntry) -> None:
    """Test setting the color temperature."""
    entity_id = "light.test_bulb"
    
    await hass.services.async_call(
        LIGHT_DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity_id, ATTR_COLOR_TEMP_KELVIN: 6500},
        blocking=True,
    )

    state = hass.states.get(entity_id)
    assert state.state == STATE_ON
    assert state.attributes[ATTR_COLOR_TEMP_KELVIN] == 6500

    await hass.services.async_call(
        LIGHT_DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity_id, ATTR_COLOR_TEMP_KELVIN: 2700},
        blocking=True,
    )

    state = hass.states.get(entity_id)
    assert state.attributes[ATTR_COLOR_TEMP_KELVIN] == 2700


async def test_light_unique_id(hass: HomeAssistant, test_bulb_setup: MockConfigEntry) -> None:
    """Test the light has a unique ID."""
    entity_registry = er.async_get(hass)
    
    entity = entity_registry.async_get("light.test_bulb")
    assert entity
    assert entity.unique_id == f"{test_bulb_setup.entry_id}_light"
