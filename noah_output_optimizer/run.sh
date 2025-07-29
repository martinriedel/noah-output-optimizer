#!/bin/bash

# The AppDaemon base image will start AppDaemon automatically.
# This script is here to handle any custom logic you might need at startup.

# For this add-on, we need to make sure the user's configuration is respected.
# The user's configuration is provided in /data/options.json

# We can use this to generate the apps.yaml file dynamically if needed,
# but for now, we will rely on the user configuring the app via the AppDaemon UI
# or by placing an apps.yaml file in the /share/appdaemon/apps/ directory.

# The Dockerfile already copies a default apps.yaml.
# The user can override it using the /share directory.

echo "Starting AppDaemon..."
echo "Please configure the Noah Output Optimizer app in the AppDaemon UI."

# The base image's entrypoint will be executed after this script.