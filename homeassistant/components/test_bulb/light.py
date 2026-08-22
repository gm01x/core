"""Support for Test Bulb lights."""

from typing import Any, override

from homeassistant.components.light import (
    ATTR_COLOR_TEMP_KELVIN,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

MIN_KELVIN = 2700
MAX_KELVIN = 6500


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Test Bulb light."""
    async_add_entities([TestBulbLight(config_entry.entry_id)])


class TestBulbLight(LightEntity):
    """Representation of a Test Bulb light."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_color_mode = ColorMode.COLOR_TEMP
    _attr_supported_color_modes = {ColorMode.COLOR_TEMP}
    _attr_min_color_temp_kelvin = MIN_KELVIN
    _attr_max_color_temp_kelvin = MAX_KELVIN
    _attr_assumed_state = True

    def __init__(self, entry_id: str) -> None:
        """Initialize the Test Bulb light."""
        self._attr_unique_id = entry_id
        self._attr_is_on = False
        self._attr_color_temp_kelvin = MIN_KELVIN

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        if ATTR_COLOR_TEMP_KELVIN in kwargs:
            self._attr_color_temp_kelvin = kwargs[ATTR_COLOR_TEMP_KELVIN]
        self._attr_is_on = True
        self.async_write_ha_state()

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        self._attr_is_on = False
        self.async_write_ha_state()
