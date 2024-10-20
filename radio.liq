#!/usr/bin/liquidsoap

# Environment Variables
icecast_password = environment.get("ICECAST_PASSWORD")
icecast_host = environment.get("ICECAST_HOST")

# Configure logging
log.file.path := "/tmp/my_radio.log"
log.stdout := true

# Enable telnet and harbor servers
settings.server.telnet := true
settings.harbor.bind_addrs := ["0.0.0.0"]

# Define the default playlist
default = mksafe(normalize(playlist(mode='randomize', reload=1, reload_mode="rounds", "/music")))

# Define the clock sound
clock = single("~/jingles/izet_dosada.mp3")

# Define jingle for song requests
jingle = single("~/jingles/izet_fazlinovic_leave_me_in_pis.mp3")

# Create a request queue for song requests
songRequests = request.queue()

# Create a separate request queue for immediate play requests
immediateRequests = request.queue()

# Fallback to play requests if there are any; otherwise, play the default playlist
radio = fallback([songRequests, default])

# Add the clock jingle to play at the beginning
radio = add([radio, switch([({15m0s}, clock)])])

# Add the jingle for a scheduled play every 15 minutes
radio = add([radio, switch([({5m0s}, jingle)])])

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
  mount="radio.mp3", radio)

# Output as AAC
output.icecast(%fdkaac,
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.aac", radio)
