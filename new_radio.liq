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

songs = audio_to_stereo(playlist(mode="normal", "~/music"))
jingles = audio_to_stereo(playlist("~/jingles"))

play_jingle = ref false

def on_jingle(_) =
  play_jingle := false
end

# Play a jingle when `play_jingle` is set to `true`
jingles = switch([({!play_jingle}, jingles)])

# Play one jingle at a time by setting `play_jingle` to 
# `false` immediately after one starts playing (`switch`
# above is `track_sensitive` so track will keep playing until
# it ends.
jingles = on_track(on_jingle, jingles)

songs = skip_blank(songs)
songs = crossfade(songs)

radio = random(weights=[1, 5], [jingles, songs])

security = single("/intros/intro_song.mp3")

s = fallback(track_sensitive=false, [radio, security])
s = smooth_add(normal=s, special=jingles)

def jingleover()
   log("jingleover precalled")
   play_jingle := true
   log("jingleover postcalled")
end

def add_randomjingle_command(~command)
        server.register(
                usage="randomjingle",
                description="Play random jingle over stream",
                command,
                fun(_) -> begin jingleover() "Done!" end
        )
 end

add_randomjingle_command(command="randomjingle")

output.icecast(%mp3.vbr(bitrate=128, max_bitrate=256, id3v2=true),
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.mp3", radio)

# Output as AAC
output.icecast(%fdkaac,
  host=icecast_host, port=8000, password=icecast_password,
  mount="radio.aac", radio)