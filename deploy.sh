#!/bin/bash

# Set the path to your Home Assistant configuration directory
HA_CONFIG_DIR=/path/to/your/home-assistant/config

# Create the addons directory if it doesn't exist
mkdir -p $HA_CONFIG_DIR/addons/noah_output_optimizer

# Copy the add-on files to the addons directory
cp -r addon/* $HA_CONFIG_DIR/addons/noah_output_optimizer/
