"""Binary sensor platform for Adaptive Climate."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .comfort_model import ComfortCategory, ComfortInputs, calculate_adaptive_comfort
from .const import (
    CONF_COMFORT_CATEGORY,
    CONF_INDOOR_TEMP_SENSOR,
    CONF_MAX_COMFORT_TEMP,
    CONF_MIN_COMFORT_TEMP,
    CONF_OUTDOOR_TEMP_SENSOR,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Adaptive Climate binary sensors."""
    async_add_entities(
        [
            AdaptiveClimateBinarySensor(entry, "comfortable", "Comfortable"),
            AdaptiveClimateBinarySensor(
                entry,
                "natural_ventilation",
                "Natural Ventilation Recommended",
            ),
        ]
    )


class AdaptiveClimateBinarySensor(BinarySensorEntity):
    """Calculated adaptive comfort binary sensor."""

    def __init__(self, entry: ConfigEntry, sensor_kind: str, label: str) -> None:
        """Initialise sensor."""
        self._entry = entry
        self._sensor_kind = sensor_kind
        self._attr_name = f"{entry.title} {label}"
        self._attr_unique_id = f"{entry.entry_id}_{sensor_kind}"

    @property
    def is_on(self) -> bool | None:
        """Return calculated binary state."""
        result = self._calculate()
        if result is None:
            return None
        if self._sensor_kind == "comfortable":
            return result.comfortable
        if self._sensor_kind == "natural_ventilation":
            return result.natural_ventilation_recommended
        return None

    def _calculate(self):
        hass = self.hass
        indoor_state = hass.states.get(self._entry.data[CONF_INDOOR_TEMP_SENSOR])
        outdoor_state = hass.states.get(self._entry.data[CONF_OUTDOOR_TEMP_SENSOR])

        if indoor_state is None or outdoor_state is None:
            return None

        try:
            indoor = float(indoor_state.state)
            outdoor = float(outdoor_state.state)
        except (TypeError, ValueError):
            return None

        return calculate_adaptive_comfort(
            ComfortInputs(
                indoor_temp=indoor,
                outdoor_temp=outdoor,
                category=ComfortCategory(self._entry.data[CONF_COMFORT_CATEGORY]),
                min_comfort_temp=float(self._entry.data[CONF_MIN_COMFORT_TEMP]),
                max_comfort_temp=float(self._entry.data[CONF_MAX_COMFORT_TEMP]),
            )
        )
