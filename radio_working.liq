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
jingle = single("~/jingles/izet_srp_i_cekic.mp3")

# Create a request queue for song requests
songRequests = request.queue()

# Fallback to play requests if there are any, otherwise the default playlist
radio = fallback([songRequests, default])

# Add the clock jingle
radio = add([radio, switch([({0m0s}, clock)])])

# Add the clock jingle
radio = add([radio, switch([({10m0s}, jingle)])])

# Output the full stream in OGG and MP3
output.icecast(%mp3.vbr(bitrate=128,max_bitrate=256,id3v2=true),
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.mp3", radio)
# output.icecast(%vorbis,
#   host=icecast_host, port=8000, password=icecast_password,
#   mount="radio.ogg", radio)
# output.icecast(%opus,
#   host=icecast_host, port=8000, password=icecast_password,
#   mount="radio.opus", radio)
output.icecast(%fdkaac,
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.aac", radio)

# HTTP request handler to play songs
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
    # res.data("Request Pushed Successfully! #{title}:#{fname}")
  else
    res.data("Invalid file.")
    res.status_code(404)
  end
end

# Register the HTTP handler with Harbor
harbor.http.register(port=7001, method="GET", "/play", playRequest)