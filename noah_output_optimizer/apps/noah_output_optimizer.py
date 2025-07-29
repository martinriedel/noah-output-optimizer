import hassapi as hass
import adbase as ad
from datetime import time

# ======================================================================================
# Noah Output Optimizer App
#
# Description:
# This AppDaemon application dynamically adjusts the output power of one or more
# Growatt Noah 2000 battery storage devices based on household energy consumption.
# It operates outside of a user-defined "charging" window, during which it will not
# adjust the output.
#
# Configuration (`apps.yaml`):
#
# noah_optimizer:
#   module: noah_output_optimizer
#   class: NoahOutputOptimizer
#   # --- General Settings ---
#   adjustment_interval: 30  # (seconds) How often to run the adjustment logic.
#   consumption_sensor: sensor.shelly_pro_3em_total_power # Total household power consumption sensor.
#
#   # --- Time-based Control ---
#   # The script will NOT adjust output between these times (e.g., 8:00 AM to 8:00 PM)
#   charging_start_time: "08:00:00"
#   charging_end_time: "20:00:00"
#
#   # --- Device Configuration ---
#   # List of all Noah devices to be controlled.
#   noah_devices:
#     - name: "Noah Living Room"  # A friendly name for logging.
#       soc_sensor: sensor.growatt_noah_2000_soc   # State of Charge sensor entity.
#       output_control_entity: number.growatt_noah_2000_output_power # Entity to control output power (must be a number entity).
#       min_soc: 15  # (percent) Stop discharging if SoC is below this value.
#
#     - name: "Noah Garage"
#       soc_sensor: sensor.growatt_noah_2000_garage_soc
#       output_control_entity: number.growatt_noah_2000_garage_output_power
#       min_soc: 20
# ======================================================================================

class NoahOutputOptimizer(ad.ADBase):

    def initialize(self):
        """Initialize the AppDaemon application."""
        self.adapi = self.get_ad_api()
        self.hass = self.get_hass_api()

        # --- Load Configuration ---
        self.adjustment_interval = self.args.get("adjustment_interval", 60)
        self.consumption_sensor = self.args.get("consumption_sensor")
        self.start_time = self.parse_time(self.args.get("charging_start_time", "08:00:00"))
        self.end_time = self.parse_time(self.args.get("charging_end_time", "20:00:00"))
        self.noah_devices = self.args.get("noah_devices", [])

        # --- Validate Configuration ---
        if not self.consumption_sensor or not self.hass.entity_exists(self.consumption_sensor):
            self.adapi.log("Error: Consumption sensor not found or not configured.", level="ERROR")
            return

        if not self.noah_devices:
            self.adapi.log("Error: No Noah devices configured.", level="ERROR")
            return

        # --- Setup Runtime ---
        self.adapi.log(f"Noah Output Optimizer initialized. Adjusting every {self.adjustment_interval} seconds.")
        self.adapi.log(f"Charging window is from {self.start_time} to {self.end_time}. No adjustments will be made during this time.")

        # Schedule the main adjustment logic to run at the specified interval.
        self.run_every(self.adjust_output_callback, "now", self.adjustment_interval)


    def adjust_output_callback(self, kwargs):
        """
        The main callback function that is triggered at each interval.
        It checks conditions and calls the core logic.
        """
        # 1. Check if we are within the "charging" window. If so, do nothing.
        if self.hass.now_is_between(str(self.start_time), str(self.end_time)):
            self.adapi.log("Within charging window. Skipping adjustment.", level="DEBUG")
            return

        # 2. Get current household consumption.
        try:
            total_consumption = float(self.hass.get_state(self.consumption_sensor))
            self.adapi.log(f"Current total consumption: {total_consumption} W", level="DEBUG")
        except (ValueError, TypeError):
            self.adapi.log(f"Warning: Could not get valid consumption value from {self.consumption_sensor}", level="WARNING")
            return

        # 3. Distribute the load across available devices.
        self.distribute_load(total_consumption)


    def distribute_load(self, total_consumption):
        """
        Distributes the required output power across all configured Noah devices.
        """
        # For now, we split the load equally. This can be enhanced later.
        active_devices = [dev for dev in self.noah_devices if self.is_device_available(dev)]
        if not active_devices:
            self.adapi.log("No available Noah devices to dispatch load to.", level="INFO")
            return

        output_per_device = round(total_consumption / len(active_devices))
        self.adapi.log(f"Calculated output per device: {output_per_device} W", level="DEBUG")

        for device in active_devices:
            self.set_device_output(device, output_per_device)


    def is_device_available(self, device_config):
        """
        Checks if a device is available to provide power (i.e., its SoC is above min_soc).
        """
        try:
            soc = float(self.hass.get_state(device_config["soc_sensor"]))
            min_soc = device_config["min_soc"]
            if soc > min_soc:
                return True
            else:
                self.adapi.log(f"Device '{device_config['name']}' is below minimum SoC ({soc}% <= {min_soc}%). Not using.", level="INFO")
                # Ensure its output is set to 0 if it's unavailable.
                self.set_device_output(device_config, 0)
                return False
        except (ValueError, TypeError):
            self.adapi.log(f"Warning: Could not get valid SoC from {device_config['soc_sensor']}", level="WARNING")
            return False


    def set_device_output(self, device_config, power_watts):
        """
        Sets the output power for a single Noah device.
        """
        entity_id = device_config["output_control_entity"]
        name = device_config["name"]
        self.adapi.log(f"Setting output for '{name}' ({entity_id}) to {power_watts} W.", level="INFO")

        # Use the 'number.set_value' service to change the output power.
        self.hass.call_service(
            "number/set_value",
            entity_id=entity_id,
            value=power_watts
        )