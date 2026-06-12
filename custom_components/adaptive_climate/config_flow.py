"""Config flow for Adaptive Climate."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector

from .const import (
    CONF_APPLY_SETPOINTS,
    CONF_CLIMATE_ENTITY,
    CONF_COMFORT_CATEGORY,
    CONF_INDOOR_TEMP_SENSOR,
    CONF_MAX_COMFORT_TEMP,
    CONF_MIN_COMFORT_TEMP,
    CONF_OUTDOOR_TEMP_SENSOR,
    DEFAULT_APPLY_SETPOINTS,
    DEFAULT_COMFORT_CATEGORY,
    DEFAULT_MAX_COMFORT_TEMP,
    DEFAULT_MIN_COMFORT_TEMP,
    DOMAIN,
)


class AdaptiveClimateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an Adaptive Climate config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_NAME].lower().replace(" ", "_"))
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Living Room"): str,
                vol.Required(CONF_CLIMATE_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="climate")
                ),
                vol.Required(CONF_INDOOR_TEMP_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["sensor", "input_number", "weather"])
                ),
                vol.Required(CONF_OUTDOOR_TEMP_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["sensor", "input_number", "weather"])
                ),
                vol.Required(CONF_COMFORT_CATEGORY, default=DEFAULT_COMFORT_CATEGORY): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=["I", "II", "III"],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(CONF_MIN_COMFORT_TEMP, default=DEFAULT_MIN_COMFORT_TEMP): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=10.0,
                        max=25.0,
                        step=0.5,
                        unit_of_measurement="°C",
                    )
                ),
                vol.Required(CONF_MAX_COMFORT_TEMP, default=DEFAULT_MAX_COMFORT_TEMP): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=20.0,
                        max=35.0,
                        step=0.5,
                        unit_of_measurement="°C",
                    )
                ),
                vol.Required(CONF_APPLY_SETPOINTS, default=DEFAULT_APPLY_SETPOINTS): bool,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
