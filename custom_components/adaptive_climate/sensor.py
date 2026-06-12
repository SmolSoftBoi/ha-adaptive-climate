"""Sensor platform for Adaptive Climate."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
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
    """Set up Adaptive Climate sensors."""
    async_add_entities(
        [
            AdaptiveClimateTemperatureSensor(entry, "target", "Adaptive Target Temperature"),
            AdaptiveClimateTemperatureSensor(entry, "min", "Comfort Band Low"),
            AdaptiveClimateTemperatureSensor(entry, "max", "Comfort Band High"),
        ]
    )


class AdaptiveClimateTemperatureSensor(SensorEntity):
    """Calculated adaptive comfort temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, entry: ConfigEntry, sensor_kind: str, label: str) -> None:
        """Initialise sensor."""
        self._entry = entry
        self._sensor_kind = sensor_kind
        self._attr_name = f"{entry.title} {label}"
        self._attr_unique_id = f"{entry.entry_id}_{sensor_kind}_temperature"

    @property
    def native_value(self) -> float | None:
        """Return calculated temperature."""
        result = self._calculate()
        if result is None:
            return None
        if self._sensor_kind == "target":
            return result.target_temp
        if self._sensor_kind == "min":
            return result.comfort_min
        if self._sensor_kind == "max":
            return result.comfort_max
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
