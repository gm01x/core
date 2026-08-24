"""Climate platform for the Temp Controller integration."""

from typing import Any, override

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TempControllerConfigEntry, TempControllerData
from .const import DEFAULT_NAME, DOMAIN, MAX_TEMP, MIN_TEMP


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TempControllerConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Temp Controller climate platform."""
    async_add_entities([TempControllerClimate(entry)])


class TempControllerClimate(ClimateEntity):
    """Virtual in-memory heat / temperature controller."""

    _attr_has_entity_name = False
    _attr_name = DEFAULT_NAME
    _attr_should_poll = False
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_min_temp = MIN_TEMP
    _attr_max_temp = MAX_TEMP
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_OFF
        | ClimateEntityFeature.TURN_ON
    )
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(self, entry: TempControllerConfigEntry) -> None:
        """Initialize the climate entity."""
        self._data: TempControllerData = entry.runtime_data
        self._attr_unique_id = entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=DEFAULT_NAME,
        )

    @property
    @override
    def current_temperature(self) -> float:
        """Return the current temperature."""
        return self._data.current_temperature

    @property
    @override
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""
        return self._data.target_temperature

    @property
    @override
    def hvac_mode(self) -> HVACMode:
        """Return hvac operation mode."""
        return self._data.hvac_mode

    @property
    @override
    def hvac_action(self) -> HVACAction:
        """Return the current running hvac action."""
        if self._data.hvac_mode == HVACMode.OFF:
            return HVACAction.OFF
        if self._data.current_temperature < self._data.target_temperature:
            return HVACAction.HEATING
        return HVACAction.IDLE

    @override
    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        self._data.target_temperature = float(temperature)
        self.async_write_ha_state()

    @override
    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        self._data.hvac_mode = hvac_mode
        self.async_write_ha_state()
