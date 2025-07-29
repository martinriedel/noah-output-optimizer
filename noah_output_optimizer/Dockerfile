# Use the official AppDaemon base image
FROM homeassistant/appdaemon:latest

# The AppDaemon image handles the base setup.
# We just need to add our custom app and its dependencies.

# Copy the app's Python script into the apps directory
COPY apps/ /etc/appdaemon/apps/

# Copy the app's configuration into the apps directory
# This will be the default configuration.
COPY apps.yaml /etc/appdaemon/apps/apps.yaml

# If your app has specific python dependencies, you can install them.
# Create a requirements.txt file in this directory and uncomment the lines below.
# COPY requirements.txt /etc/appdaemon/
# RUN pip install --no-cache-dir -r /etc/appdaemon/requirements.txt
