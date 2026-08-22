"""Config flow for the Test Bulb integration."""

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Test Bulb."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id("test_bulb_instance")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Test Bulb", data={})

        return self.async_show_form(step_id="user")


async def _async_has_devices(hass) -> bool:
    """Return if there are devices that can be discovered."""
    return False


config_entry_flow.register_discovery_flow(DOMAIN, "Test Bulb", _async_has_devices)
