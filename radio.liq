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
settings.log.stdout := false

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
immediateRequests = request.queue()  # Queue for immediate requests

# 5. Functions

# Function to handle metadata updates
def apply_metadata(m) =
  title = m["title"]
  artist = m["artist"]
  print("Now playing: #{title} by #{artist}")
end

# HTTP request handler to enqueue song requests
def playRequest(req, res) =
  uri = req.path
  args = req.query

  log.important("Serving URI: #{uri}")

  fname = args["file"]
  title = args["title"]

  if file.exists(fname) then
    songRequests.push.uri("annotate:title=#{string.quote(title)}:#{fname}")
    log.important("User request pushed into the request queue")
    res.data("Request Pushed Successfully! :#{fname}")
  else
    res.data("Invalid file.")
    res.status_code(404)
  end
end

# HTTP request handler to play songs immediately
def playImmediate(req, res) =
  uri = req.path
  args = req.query

  log.important("Serving immediate play URI: #{uri}")

  fname = args["file"]
  title = args["title"]

  if file.exists(fname) then
    # Play the specific request jingle before the immediate request
    immediateRequests.push(request_jingle)  # Add the specific jingle before the request
    immediateRequests.push.uri("annotate:title=#{string.quote(title)}:#{fname}")  # Add the requested song
    
    log.important("Request Jingle + Immediate request pushed into immediate request queue")
    res.data("Request Jingle + Immediate Request Queued! :#{fname}")
  else
    res.data("Invalid file.")
    res.status_code(404)
  end
end

# 6. Fallbacks and Processing

# Play a jingle every 3rd song
jingle_sequence = rotate(weights=[3, 1], [songs, jingles])
jingle_sequence = crossfade(fade_out=3., fade_in=3., duration=5., jingle_sequence)

# Apply fallback with security track and silence fallback to ensure it's non-fallible
# The order of fallback: immediateRequests > song/jingle sequence > security track > silence
main_stream_fallback = fallback(track_sensitive=false, [immediateRequests, jingle_sequence, security, silence])

# Now apply the metadata handler to the non-fallible main stream
main_stream = source.on_metadata(main_stream_fallback, apply_metadata)

# 7. Outputs

# Output the stream as AAC using environment variable for mount name with hardcoded '.aac'
output.icecast(%fdkaac(bitrate=256),
  host=icecast_host, port=icecast_port, password=icecast_password,
  mount="#{icecast_mount}.aac", main_stream)

# Output the stream as MP3 using environment variable for mount name with hardcoded '.mp3'
output.icecast(%mp3(bitrate=192),
  host=icecast_host, port=icecast_port, password=icecast_password,
  mount="#{icecast_mount}.mp3", main_stream)

# Output the stream as Ogg using environment variable for mount name with hardcoded '.ogg'
output.icecast(%vorbis,
  host=icecast_host, port=icecast_port, password=icecast_password,
  mount="#{icecast_mount}.ogg", main_stream)

# Log the stream URLs
log.important("AAC stream available at: http://#{icecast_host}:#{icecast_port}/#{icecast_mount}.aac")
log.important("MP3 stream available at: http://#{icecast_host}:#{icecast_port}/#{icecast_mount}.mp3")
log.important("Ogg stream available at: http://#{icecast_host}:#{icecast_port}/#{icecast_mount}.ogg")

# 8. Register HTTP Handlers

# Register the HTTP handlers with a hardcoded port for Liquidsoap
harbor.http.register(port=liquidsoap_port, method="GET", "/play", playRequest)
harbor.http.register(port=liquidsoap_port, method="GET", "/immediate", playImmediate)
