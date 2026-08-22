"""The Test Bulb integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Test Bulb from a config entry."""
    entry.runtime_data = None

    # This integration is for testing purposes only and has no external dependencies.
    # In a real integration, validation of external resources would occur here and
    # could raise ConfigEntryNotReady if setup should be retried.
    if entry.data.get("_fail_setup"):  # pragma: no cover
        raise ConfigEntryNotReady("Setup intentionally failed for testing")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
