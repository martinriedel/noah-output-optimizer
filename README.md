# Noah Output Optimizer - Home Assistant Add-on

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fmartinriedel%2Fnoah-output-optimizer)

A Home Assistant add-on that monitors and optimizes Growatt Noah 2000 battery storage systems based on current power consumption.

## About

This add-on reads the State of Charge (SOC) from one or more Growatt Noah 2000 battery systems integrated with Home Assistant. It provides monitoring capabilities and serves as a foundation for implementing intelligent battery optimization strategies.

## Features

- Monitor SOC from multiple Noah battery systems
- Configurable update intervals
- Comprehensive logging with summary statistics
- Ready for extension with optimization algorithms
- Native Home Assistant integration via Supervisor API

## Installation

1. Add this repository to your Home Assistant add-on store:
   - In Home Assistant, go to **Supervisor** → **Add-on Store**
   - Click the menu (⋮) in the top right corner
   - Select **Repositories**
   - Add: `https://github.com/martinriedel/noah-output-optimizer`

2. Install the "Noah Output Optimizer" add-on

3. Configure the add-on with your Noah entity IDs

4. Start the add-on

## Configuration

```yaml
noah_entities:
  - sensor.noah_2000_battery_soc
  - sensor.noah_2000_2_battery_soc
update_interval: 60
log_level: info
```

### Options

- `noah_entities` (required): List of Home Assistant entity IDs for your Noah SOC sensors
- `update_interval` (optional): Seconds between SOC readings (default: 60, range: 1-3600)
- `log_level` (optional): Logging level - debug, info, warning, or error (default: info)

## Entity Setup

Before using this add-on, ensure your Growatt Noah systems are integrated with Home Assistant and expose SOC sensors. Common entity naming patterns:
- `sensor.noah_2000_battery_soc`
- `sensor.growatt_noah_soc`
- `sensor.inverter_battery_soc`

## Logs

The add-on provides detailed logging including:
- Individual SOC readings for each configured entity
- Summary statistics (count, average, min, max SOC)
- Error handling for unavailable entities
- Connection status to Home Assistant API

## Future Development

This add-on is designed to be extended with:
- Power consumption monitoring
- Intelligent charge/discharge optimization
- Time-based scheduling
- Grid export/import management
- Weather-based predictions

## Support

For issues and feature requests, please use the [GitHub repository](https://github.com/martinriedel/noah-output-optimizer/issues).

## License

This project is licensed under the terms specified in the LICENSE file.