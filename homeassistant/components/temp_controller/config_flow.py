"""Config flow for the Temp Controller integration."""

from typing import Any, override

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DEFAULT_NAME, DOMAIN


class TempControllerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Temp Controller."""

    VERSION = 1

    @override
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title=DEFAULT_NAME, data={})

        return self.async_show_form(step_id="user")
