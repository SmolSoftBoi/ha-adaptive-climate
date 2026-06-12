"""Pure adaptive comfort calculations for Adaptive Climate."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ComfortCategory(StrEnum):
    """ASHRAE-style adaptive comfort category."""

    I = "I"
    II = "II"
    III = "III"


TOLERANCE_C: dict[ComfortCategory, float] = {
    ComfortCategory.I: 2.0,
    ComfortCategory.II: 3.0,
    ComfortCategory.III: 4.0,
}


@dataclass(frozen=True, slots=True)
class ComfortInputs:
    """Inputs for adaptive comfort calculation."""

    indoor_temp: float
    outdoor_temp: float
    category: ComfortCategory = ComfortCategory.II
    min_comfort_temp: float = 18.0
    max_comfort_temp: float = 28.0
    occupied: bool = True
    setback_offset: float = 2.0


@dataclass(frozen=True, slots=True)
class ComfortResult:
    """Calculated adaptive comfort result."""

    target_temp: float
    comfort_min: float
    comfort_max: float
    comfortable: bool
    natural_ventilation_recommended: bool
    notes: tuple[str, ...]


def calculate_adaptive_comfort(data: ComfortInputs) -> ComfortResult:
    """Calculate an ASHRAE-style adaptive comfort target and band.

    This is intentionally conservative for residential use. It treats the
    adaptive target as a comfort guide, then clamps it to hard min/max bounds.
    """

    notes: list[str] = []

    if data.min_comfort_temp >= data.max_comfort_temp:
        raise ValueError("min_comfort_temp must be lower than max_comfort_temp")

    base_target = 18.9 + (0.255 * data.outdoor_temp)

    if data.outdoor_temp < 10 or data.outdoor_temp > 33.5:
        notes.append("Outdoor temperature is outside the normal adaptive-comfort range.")

    tolerance = TOLERANCE_C[data.category]

    comfort_min = max(base_target - tolerance, data.min_comfort_temp)
    comfort_max = min(base_target + tolerance, data.max_comfort_temp)

    target = base_target

    if not data.occupied:
        target = max(data.min_comfort_temp, target - data.setback_offset)

    target = min(max(target, data.min_comfort_temp), data.max_comfort_temp)
    comfortable = comfort_min <= data.indoor_temp <= comfort_max

    natural_ventilation_recommended = (
        data.outdoor_temp >= comfort_min
        and data.outdoor_temp <= comfort_max
        and abs(data.outdoor_temp - data.indoor_temp) <= 2.0
    )

    return ComfortResult(
        target_temp=round(target, 1),
        comfort_min=round(comfort_min, 1),
        comfort_max=round(comfort_max, 1),
        comfortable=comfortable,
        natural_ventilation_recommended=natural_ventilation_recommended,
        notes=tuple(notes),
    )
