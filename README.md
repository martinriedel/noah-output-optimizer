# NOAH Output Optimizer for Home Assistant

This project provides an AppDaemon application, packaged as a Home Assistant Add-on, to dynamically control the output of one or more Growatt Noah 2000 battery storage devices.

The primary goal is to maximize self-consumption by adjusting the battery's discharge power to match the household's real-time energy needs, while respecting user-defined charging periods and safety thresholds.

## Features

- **Dynamic Power Adjustment**: Automatically adjusts the battery output every few seconds to match household consumption.
- **Configurable Time Windows**: Define a "charging" window (e.g., during the day) where the script will not interfere, allowing the battery to charge via solar or other routines.
- **Multi-Device Support**: Control and coordinate multiple Noah 2000 devices simultaneously.
- **Safety First**: Set a minimum State of Charge (SoC) for each device to prevent deep discharge and prolong battery life.
- **Flexible Configuration**: All settings, including entity IDs, time windows, and devices, are managed via a simple `apps.yaml` file.
- **Home Assistant Add-on**: Packaged for easy installation and management within your Home Assistant environment.

---

## How It Works

The application runs on a continuous loop (e.g., every 30 seconds) and performs the following actions:

1.  **Check Time**: It first checks if the current time is within the user-defined `charging_start_time` and `charging_end_time`. If it is, the script does nothing, allowing the battery's default behavior to take over.
2.  **Read Consumption**: If outside the charging window, it reads the current power consumption from your specified household power sensor (e.g., a Shelly Pro 3EM).
3.  **Check Battery Status**: It checks the SoC for each configured Noah device.
4.  **Distribute Load**: It calculates the required output power and distributes it among the available devices (those with an SoC above their configured `min_soc` threshold).
5.  **Set Output**: It then makes a service call to Home Assistant to set the `value` of the `number` entity that controls each Noah's output power.

---

## Prerequisites

Before you begin, ensure you have the following:

- A running Home Assistant instance.
- One or more Growatt Noah 2000 devices integrated into Home Assistant.
- A sensor entity that reports your total household power consumption in Watts (W).
- A `number` entity for each Noah device that allows you to set its output power. This is crucial for the script to function.

---

## Installation

Adding this add-on to your Home Assistant instance is straightforward.

1.  **Add the Repository:**
    *   In Home Assistant, go to **Settings > Add-ons > Add-on Store**.
    *   Click the three dots in the top right corner and select **Repositories**.
    *   Paste the following URL and click **Add**:
        ```
        https://github.com/martinriedel/noah-output-optimizer
        ```

2.  **Install the Add-on:**
    *   Close the repository manager.
    *   A new "NOAH Output Optimizer" card should now appear in the add-on store.
    *   Click on the card, then click **Install**.

3.  **Configure the App:**
    *   Once installed, start the add-on.
    *   Open the AppDaemon web UI by clicking the "Open Web UI" button on the add-on's page.
    *   In the AppDaemon UI, navigate to the `/apps/apps.yaml` file.
    *   Edit the file to match your specific entity IDs and preferences. The default configuration is provided as a starting point.

4.  **Restart the Add-on:** After saving your changes to `apps.yaml`, restart the "NOAH Output Optimizer" add-on from the Home Assistant UI for the new configuration to take effect.
