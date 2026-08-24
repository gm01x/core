"""The Temp Controller integration."""

from dataclasses import dataclass

from homeassistant.components.climate import HVACMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DEFAULT_CURRENT_TEMPERATURE, DEFAULT_TARGET_TEMPERATURE, DOMAIN

PLATFORMS: list[Platform] = [Platform.CLIMATE]

__all__ = ["DOMAIN"]


@dataclass
class TempControllerData:
    """In-memory state for the virtual temperature controller."""

    current_temperature: float = DEFAULT_CURRENT_TEMPERATURE
    target_temperature: float = DEFAULT_TARGET_TEMPERATURE
    hvac_mode: HVACMode = HVACMode.HEAT


type TempControllerConfigEntry = ConfigEntry[TempControllerData]


async def async_setup_entry(
    hass: HomeAssistant, entry: TempControllerConfigEntry
) -> bool:
    """Set up Temp Controller from a config entry."""
    entry.runtime_data = TempControllerData()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: TempControllerConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
