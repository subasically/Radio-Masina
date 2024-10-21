#!/usr/bin/liquidsoap

# Environment Variables
icecast_password = environment.get("ICECAST_PASSWORD")
icecast_host = environment.get("ICECAST_HOST")

# Configure logging
log.file.path := "/tmp/my_radio.log"
log.stdout := false

# Enable telnet and harbor servers
settings.server.telnet := true
settings.harbor.bind_addrs := ["0.0.0.0"]

# This function is called when a new metadata block is passed in the stream.
def apply_metadata(m) =
  title = m["title"]
  artist = m["artist"]
  print("Now playing: #{title} by #{artist}")
end

# Playlists
songs = playlist(mode='randomize', reload=1, reload_mode="rounds", "/music")
jingles = playlist(mode='randomize', reload=1, reload_mode="rounds", "/jingles")

# Create a request queue for song requests
songRequests = request.queue()

# Create a separate request queue for immediate play requests
immediateRequests = request.queue()

radio = random(weights=[1, 3], [jingles, songs])
security = single("/intros/intro_song.mp3")
s = fallback(track_sensitive=false, [radio, security])
s = smooth_add(normal=s, special=jingles)

radio = source.on_metadata(radio, apply_metadata)

# HTTP request handler to play songs (regular requests)
def playRequest(req, res) =
  uri = req.path
  args = req.query

  log.important("Serving uri: #{uri}")

  fname = args["file"]
  title = args["title"]

  if file.exists(fname) then
    songRequests.push.uri("annotate:title=#{string.quote(title)}:#{fname}")
    log.important("User request pushed into request queue")
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

  log.important("Serving immediate play uri: #{uri}")

  fname = args["file"]
  title = args["title"]

  if file.exists(fname) then
    # Push the immediate request to the immediateRequests queue
    immediateRequests.push.uri("annotate:title=#{string.quote(title)}:#{fname}")
    log.important("Immediate request pushed into request queue")

    # Create a fallback to play the immediate request
    immediatePlay = single(fname)

    # Use fallback.skip to play the immediate song and skip the current track
    radio = fallback.skip(immediatePlay, fallback=radio)

    res.data("Immediate Request Playing Now! :#{fname}")
  else
    res.data("Invalid file.")
    res.status_code(404)
  end
end

# Register the HTTP handlers with Harbor
harbor.http.register(port=7001, method="GET", "/play", playRequest)
harbor.http.register(port=7001, method="GET", "/immediate", playImmediate)

# Output the full stream in OGG and MP3
output.icecast(%mp3.vbr(bitrate=128, max_bitrate=256, id3v2=true),
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.mp3", s)

# Output as AAC
output.icecast(%fdkaac,
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.aac", s)
