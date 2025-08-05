#!/usr/bin/env python3
"""
Noah Output Optimizer - Home Assistant Add-on
Monitors SOC of one or more Growatt Noah 2000 battery systems
"""

import json
import logging
import os
import sys
import time
from typing import Dict, List, Optional

import requests
import yaml


class HomeAssistantAPI:
    """Interface to Home Assistant API"""
    
    def __init__(self):
        self.supervisor_token = os.environ.get('SUPERVISOR_TOKEN')
        self.ha_url = "http://supervisor/core"
        self.headers = {
            "Authorization": f"Bearer {self.supervisor_token}",
            "Content-Type": "application/json",
        }
        
    def get_entity_state(self, entity_id: str) -> Optional[Dict]:
        """Get the current state of an entity"""
        try:
            url = f"{self.ha_url}/api/states/{entity_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get state for {entity_id}: {e}")
            return None


class NoahSOCMonitor:
    """Monitor SOC of Noah battery systems"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.ha_api = HomeAssistantAPI()
        self.noah_entities = config.get('noah_entities', [])
        self.update_interval = config.get('update_interval', 60)
        
        # Set up logging
        log_level = config.get('log_level', 'info').upper()
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def get_noah_soc_data(self) -> Dict[str, Optional[float]]:
        """Get SOC data from all configured Noah entities"""
        soc_data = {}
        
        for entity_id in self.noah_entities:
            logging.info(f"Reading SOC from {entity_id}")
            state_data = self.ha_api.get_entity_state(entity_id)
            
            if state_data:
                try:
                    soc_value = float(state_data.get('state', 0))
                    soc_data[entity_id] = soc_value
                    logging.info(f"{entity_id}: {soc_value}%")
                except (ValueError, TypeError):
                    logging.warning(f"Invalid SOC value for {entity_id}: {state_data.get('state')}")
                    soc_data[entity_id] = None
            else:
                logging.error(f"Could not retrieve data for {entity_id}")
                soc_data[entity_id] = None
                
        return soc_data
    
    def log_soc_summary(self, soc_data: Dict[str, Optional[float]]):
        """Log a summary of all SOC readings"""
        valid_readings = {k: v for k, v in soc_data.items() if v is not None}
        
        if valid_readings:
            total_soc = sum(valid_readings.values())
            avg_soc = total_soc / len(valid_readings)
            min_soc = min(valid_readings.values())
            max_soc = max(valid_readings.values())
            
            logging.info(f"SOC Summary - Count: {len(valid_readings)}, "
                        f"Average: {avg_soc:.1f}%, Min: {min_soc:.1f}%, Max: {max_soc:.1f}%")
        else:
            logging.warning("No valid SOC readings available")
    
    def run(self):
        """Main monitoring loop"""
        logging.info(f"Starting Noah SOC Monitor for entities: {self.noah_entities}")
        logging.info(f"Update interval: {self.update_interval} seconds")
        
        while True:
            try:
                soc_data = self.get_noah_soc_data()
                self.log_soc_summary(soc_data)
                
                # Here you could add optimization logic based on SOC data
                # For now, we just monitor and log
                
                time.sleep(self.update_interval)
                
            except KeyboardInterrupt:
                logging.info("Shutting down Noah SOC Monitor")
                break
            except Exception as e:
                logging.error(f"Unexpected error in monitoring loop: {e}")
                time.sleep(30)  # Wait before retrying


def load_config() -> Dict:
    """Load configuration from options.json"""
    try:
        with open('/data/options.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("No options.json found, using default configuration")
        return {
            'noah_entities': ['sensor.noah_2000_battery_soc'],
            'update_interval': 60,
            'log_level': 'info'
        }
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    config = load_config()
    monitor = NoahSOCMonitor(config)
    monitor.run()


if __name__ == "__main__":
    main()