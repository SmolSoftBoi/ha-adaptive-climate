# ha-adaptive-climate

Adaptive Climate is a Home Assistant custom integration for ASHRAE-style adaptive comfort control.

It starts safely as a helper/controller integration: it calculates adaptive comfort target temperatures, comfort bands, and comfort status from existing Home Assistant entities, then can optionally apply setpoints to an existing `climate.*` entity.

## MVP features

- Adaptive comfort target temperature sensor
- Comfort band high/low sensors
- Comfortable binary sensor
- Natural ventilation recommendation binary sensor
- Per-room enable switch
- Comfort category select: I / II / III
- Min/max comfort bounds
- Pure Python comfort model with tests

## Safety-first design

The first version should run in observe-only mode until you explicitly enable active setpoint control.

Planned safeguards:

- Do not apply setpoints if required sensors are unavailable
- Hard min/max comfort bounds
- Temperature-change threshold before applying updates
- Manual override cooldown
- Per-zone enable switch
- Log every applied setpoint with inputs and reason

## Installation during development

Copy `custom_components/adaptive_climate` into your Home Assistant `custom_components` directory, then restart Home Assistant.

```text
/config/custom_components/adaptive_climate
```

## HACS

This repository is structured for HACS as a custom integration, but it is not ready for publication until the integration has a working config flow, entities, tests, and documentation.
