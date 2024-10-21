#!/bin/sh

# Install inotify-tools and curl
apk add --no-cache inotify-tools curl

# Monitor the radio.liq file for changes
while inotifywait -e modify /radio.liq; do
  echo "radio.liq has been modified. Restarting Liquidsoap container..."
  curl --unix-socket /var/run/docker.sock -X POST "http://localhost/containers/radio_masina_liquidsoap/restart"
done