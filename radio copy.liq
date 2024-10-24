#!/usr/bin/liquidsoap

# 1. Environment Variables
icecast_password = environment.get("ICECAST_PASSWORD")
icecast_host = environment.get("ICECAST_HOST")
icecast_mount = environment.get("ICECAST_MOUNT")

# Hardcoded integer values for ports
icecast_port = 8000
liquidsoap_port = 7001

# 2. Configure Logging
settings.log.file.path := "/tmp/my_radio.log"
settings.log.stdout := true

# 3. Enable Telnet and Harbor Servers
set("server.telnet", true)
settings.harbor.bind_addrs := ["0.0.0.0"]

# 4. Inputs (Sources)
songs = playlist(mode='randomize', reload=1, reload_mode="rounds", "/music")
jingles = playlist(mode='randomize', reload=1, reload_mode="rounds", "/jingles")
security = single("/intros/intro_song.mp3")  # Security track as backup if no songs are available
silence = blank()  # Ensure the fallback is non-fallible with silence

# Specific jingle to play before each request
request_jingle = request.create("/jingles/izet_srp_i_cekic.mp3")

# Create request queues
songRequests = request.queue()  # Queue for regular song requests
djRequests = request.queue()  # Queue for DJ requests

# 5. Functions

# Function to handle metadata updates
def apply_metadata(m) =
  title = m["title"]
  artist = m["artist"]
  print("Now playing: #{title} by #{artist}")
end

# Function to handle track ending event
def on_track_ending(source, metadata) =
  # Dummy operations to suppress warnings
  _ = source
  _ = metadata
  # Call the HTTP endpoint to queue the next announcement and song
  title = metadata["title"]
  artist = metadata["artist"]
  print("Track ending event triggered for #{title} by #{artist}")
  url = "http://radio_masina:5000/queue_next"
  result = http.post(url, headers=[("Content-Type", "application/x-www-form-urlencoded")], data="title=#{title}&artist=#{artist}")
  print("HTTP request result: #{result}")
end

# HTTP request handler to enqueue song requests
def playRequest(req, res) =
  uri = req.path
  args = req.query

  fname = args["file"]
  title = args["title"]
  
  print("Requested: #{fname}")

  if file.exists(fname) then
    songRequests.push.uri("annotate:title=#{string.quote(title)}:#{fname}")
    print("User request pushed into the request queue")
    res.data("Request Pushed Successfully! :#{fname}")
  else
    res.data("Invalid file.")
    res.status_code(404)
  end
end

def playDJRequests(req, res) =
  uri = req.path
  args = req.query

  fname = args["file"]
  title = args["title"]
  
  print("Requested: #{fname}")

  if file.exists(fname) then
    djRequests.push(request_jingle) # Play the jingle before the requested song
    djRequests.push.uri("annotate:title=#{string.quote(title)}:#{fname}")
    print("DJ request pushed into the request queue")
    res.data("DJ Request Pushed Successfully! :#{fname}")
  else
    res.data("Invalid file.")
    res.status_code(404)
  end
end

# 6. Fallbacks and Processing

# Apply crossfading to the main stream
main_stream_crossfaded = crossfade(fade_out=3., fade_in=3., duration=5., main_stream_fallback)
main_stream_fallback = fallback(track_sensitive=false, [djRequests, songRequests, songs, jingles, security, silence])

# Now apply the metadata handler to the non-fallible main stream
main_stream_metadata = source.on_metadata(main_stream_crossfaded, apply_metadata)

# Register the track ending event
main_stream = source.on_end(main_stream_metadata, on_track_ending)

# 7. Output to Icecast
output.icecast(%mp3(bitrate=192),
  host=icecast_host, port=icecast_port, password=icecast_password,
  mount="#{icecast_mount}.mp3", main_stream_fallback)

# Output the stream as Ogg using environment variable for mount name with hardcoded '.ogg'
output.icecast(%vorbis,
  host=icecast_host, port=icecast_port, password=icecast_password,
  mount="#{icecast_mount}.ogg", main_stream_fallback)

# Log the stream URLs
print("MP3 stream available at: http://#{icecast_host}:#{icecast_port}/#{icecast_mount}.mp3")
print("Ogg stream available at: http://#{icecast_host}:#{icecast_port}/#{icecast_mount}.ogg")

# 8. Register HTTP Handlers
harbor.http.register(port=liquidsoap_port, method="GET", "/play", playRequest)
harbor.http.register(port=liquidsoap_port, method="GET", "/dj", playDJRequests)