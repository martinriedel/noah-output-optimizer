# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant add-on that controls the Growatt Noah 2000 battery storage system based on current power consumption. The add-on optimizes battery usage by monitoring power demand and intelligently managing charge/discharge cycles.

## Development Commands

```bash
# Build the add-on locally (requires Home Assistant Developer Add-on)
docker build -t noah-output-optimizer .

# Test the Python application locally (requires mock HA environment)
python3 noah_optimizer.py

# Check configuration syntax
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Install as local add-on in Home Assistant
# 1. Copy files to /usr/share/hassio/addons/local/noah-output-optimizer/
# 2. Refresh Home Assistant Supervisor add-on store
# 3. Install from Local add-ons section
```

## Architecture

The add-on will integrate with:
- Home Assistant APIs for power consumption monitoring
- Growatt Noah 2000 battery system APIs for charge/discharge control
- Configuration management for optimization parameters

## Key Components

- `noah_optimizer.py` - Main application that monitors SOC from Noah entities
- `config.yaml` - Add-on configuration with entity list and settings
- `HomeAssistantAPI` class - Interface to Home Assistant Supervisor API
- `NoahSOCMonitor` class - Core monitoring and logging functionality

## Configuration

The add-on accepts these options in Home Assistant:
- `noah_entities` - List of entity IDs for Noah SOC sensors (e.g., `sensor.noah_2000_battery_soc`)
- `update_interval` - Seconds between SOC readings (default: 60)
- `log_level` - Logging level (debug, info, warning, error)

## Important Notes

- Currently reads SOC from configured Noah entities via Home Assistant API
- Uses Home Assistant Supervisor API for entity access
- Logs SOC data with summaries (average, min, max)
- Ready for extension with optimization logic based on SOC readings