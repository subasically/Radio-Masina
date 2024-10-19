#!/usr/bin/liquidsoap

#%include "utils.liq"

# Environment Variables
ICECAST_PASSWORD = environment.get("ICECAST_PASSWORD")
ICECAST_HOST = environment.get("ICECAST_HOST")
ICECAST_MOUNT = environment.get("ICECAST_MOUNT")
CHIME_PATH = environment.get("CHIME_PATH")
MUSIC_DIR = environment.get("MUSIC_DIR")

print("ICECAST_PASSWORD: #{ICECAST_PASSWORD}")
print("ICECAST_HOST: #{ICECAST_HOST}")
print("ICECAST_MOUNT: #{ICECAST_MOUNT}.mp3 and #{ICECAST_MOUNT}.ogg")
print("CHIME_PATH: #{CHIME_PATH}")
print("MUSIC_DIR: #{MUSIC_DIR}")

# Configure logging
log.file.path := "/tmp/my_radio.log"
log.stdout := true

# Enable telnet and harbor servers
settings.server.telnet := true
settings.harbor.bind_addrs := ["0.0.0.0"]

# Define the default playlist
default = mksafe(normalize(playlist(mode='randomize', reload=1, reload_mode="rounds", MUSIC_DIR)))

# Define the clock sound
clock = single(CHIME_PATH)

# Create a request queue for song requests
songRequests = request.queue()

# Fallback to play requests if there are any, otherwise the default playlist
radio = fallback([songRequests, default])

# Add the clock jingle
radio = add([radio, switch([({0m0s}, clock)])])

# Output the full stream in OGG and MP3
output.icecast(%mp3,
  host=ICECAST_HOST, port=8000, password=ICECAST_PASSWORD,
  mount="radio.mp3", radio)
output.icecast(%vorbis,
  host=ICECAST_HOST, port=8000, password=ICECAST_PASSWORD,
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