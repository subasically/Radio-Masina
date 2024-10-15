%include "config.liq"

base_dir = path.dirname(argv(0))
audio_dir = path.concat(base_dir, "audio")
# Removed background_dir and hls_dir since they are not needed for audio only

## AI functions

def mk_prompt(old, new) =
  old =
    list.map(
      fun (m) ->
        begin
          title = m["title"]
          artist = m["artist"]
          "#{title} by #{artist}"
        end,
      old
    )

  old =
    string.concat(
      separator=
        ", ",
      old
    )

  new_title = new["title"]
  new_artist = new["artist"]

  new =
    "#{new_title} by #{new_artist}"

  "You are a radio DJ, you speak in the style of the old 50s early rock'n'roll \
   DJs. The following songs were just played: #{old}. Next playing is #{new}. \
   Can you describe the musical characteristics of each song that ended and how \
   they connect with each other? Then introduce the next song. Make sure to \
   include style, year, instruments and cultural context and anecdotes and fun \
   facts. Limit your response to 200 words and make sure that it sounds \
   entertaining and fun."
end

def generate_speech(prompt) =
  let {choices = [{message = {content}}]} =
    openai.chat(
      key=openai_api_key,
      [
        {
          role="system",
          content=
            "You are a helpful assistant."
        },
        {role="user", content=prompt}
      ]
    )

  tmp_file = file.temp("dj", ".mp3")

  on_data = file.write.stream(tmp_file)

  openai.speech(key=openai_api_key, voice="onyx", on_data=on_data, content)

  request.create(
    "annotate:title=\"AI DJ\":tmp:#{tmp_file}"
  )
end

## Audio setup

next_song = ref([])
def check_next(r) =
  ignore(request.resolve(r))
  request.read_metadata(r)
  next_song := request.metadata(r)
  true
end

radio = playlist(audio_dir, prefetch=2, check_next=check_next)

append_queue = request.queue()

past_songs = ref([])

def process_dj_metadata(m) =
  past_songs := [...past_songs(), m]

  if
    list.length(past_songs()) == 4
  then
    songs_history = past_songs()
    past_songs := []
    prompt = mk_prompt(songs_history, next_song())

    thread.run({append_queue.push(generate_speech(prompt))})
  end
end

radio = source.on_metadata(radio, process_dj_metadata)

radio = fallback(track_sensitive=true, [append_queue, radio])

current_title = ref("")
current_artist = ref("")

def update_current_song(m) =
  current_title := m["title"]
  current_artist := m["artist"]
end
radio.on_metadata(update_current_song)

def position() =
  source.elapsed(radio) / source.duration(radio)
end

def remaining() =
  time = source.remaining(radio)
  seconds = string.of_int(digits=2, int(time mod 60.))
  minutes = string.of_int(digits=2, int(time / 60.))
  "#{minutes}:#{seconds}"
end

## Output setup
# Directly outputting audio stream without video
enc = %ffmpeg(format = "mpegts", %audio(codec = "aac", b = "192k"))

streams = [("radio", enc)]

# Remove HLS output and directly output the audio stream
output.file.radio(hls_dir, streams, mksafe(radio))
