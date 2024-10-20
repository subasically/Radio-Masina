#!/bin/sh

# Install inotify-tools
apk add --no-cache inotify-tools

# Monitor the radio.liq file for changes
while inotifywait -e modify /radio.liq; do
  echo "radio.liq has been modified. Restarting Liquidsoap container..."
  docker restart radio_masina_liquidsoap
done