#!/usr/bin/liquidsoap

#%include "utils.liq"

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
default = mksafe(normalize(playlist(mode='randomize', reload=1, reload_mode="rounds", "/music/Balkan/Narodna")))

# Define the clock sound
clock = single("~/music/Balkan/Chimes/hour_chime_1.mp3")

# Create a request queue for song requests
songRequests = request.queue()

# Fallback to play requests if there are any, otherwise the default playlist
radio = fallback([songRequests, default])

# Add the clock jingle
radio = add([radio, switch([({0m0s}, clock)])])

# Output the full stream in OGG and MP3
output.icecast(%mp3,
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.mp3", radio)
output.icecast(%vorbis,
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.ogg", radio)

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
    res.data("Request Pushed Successfully! #{title}:#{fname}")
  else
    res.data("Invalid file.")
    res.status_code(404)
  end
end

# Register the HTTP handler with Harbor
harbor.http.register(port=7001, method="GET", "/play", playRequest)