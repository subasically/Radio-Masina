#!/usr/bin/liquidsoap

# 1. Environment Variables
icecast_password = environment.get("ICECAST_PASSWORD")
icecast_host = environment.get("ICECAST_HOST")
icecast_mount = environment.get("ICECAST_MOUNT")

# Hardcoded integer values for ports
icecast_port = 8000
# liquidsoap_port = 7001

# 2. Configure Logging
settings.log.file.path := "/tmp/my_radio.log"
settings.log.stdout := true

# 3. Enable Telnet and Harbor Servers
set("server.telnet", true)
settings.harbor.bind_addrs := ["0.0.0.0"]

# 4. Inputs (Sources)
songs = playlist(mode='randomize', reload=1, reload_mode="rounds", "/music")
jingles = playlist(mode='randomize', reload=1, reload_mode="rounds", "/jingles")

# Security track as backup if no songs are available
security = single("/intros/intro_song.mp3")
# Ensure the fallback is non-fallible with silence
silence = blank()

# Start building the feed with music
radio = songs

# Define the fallback stream first
radio = random(weights = [1, 1], [jingles, radio])

# Apply crossfading to the main stream
radio = crossfade(fade_out=1.5, fade_in=1.5, duration=3., radio)

# Ensure the main stream is non-fallible
radio = fallback(track_sensitive=false, [radio, security, silence])

# 7. Output to Icecast
# Output the stream as AAC using environment variable for mount name with hardcoded '.aac'
output.icecast(%fdkaac(bitrate=192),
  host=icecast_host, port=icecast_port, password=icecast_password,
  mount="#{icecast_mount}.aac", normalize(radio))

# Output the stream as MP3 using environment variable for mount name with hardcoded '.mp3'
# output.icecast(%mp3(bitrate=192),
#   host=icecast_host, port=icecast_port, password=icecast_password,
#   mount="#{icecast_mount}.mp3", normalize(radio))

# Output the stream as Ogg using environment variable for mount name with hardcoded '.ogg'
# output.icecast(%vorbis,
#   host=icecast_host, port=icecast_port, password=icecast_password,
#   mount="#{icecast_mount}.ogg", normalize(radio))