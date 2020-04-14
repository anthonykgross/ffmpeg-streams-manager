import ffmpeg
from tqdm import tqdm
import requests
import os
import json
from models import *


def init_inputs():
    video = "http://www.peach.themazzone.com/durian/movies/sintel-1024-surround.mp4"
    music = "https://www.dropbox.com/s/xiiub9bmm5rd71l/Kasger%20-%20Out%20Here%20_NCS%20Release_.mp3?dl=1"
    en = "https://durian.blender.org/wp-content/content/subtitles/sintel_en.srt"
    es = "https://durian.blender.org/wp-content/content/subtitles/sintel_es.srt"

    if not os.path.isfile('inputs/en.srt'):
        download(en, 'inputs/en.srt')
    if not os.path.isfile('inputs/es.srt'):
        download(es, 'inputs/es.srt')
    if not os.path.isfile('inputs/music.mp3'):
        download(music, 'inputs/music.mp3')
    if not os.path.isfile('inputs/sintel.mp4'):
        download(video, 'inputs/sintel.mp4')


def download (url, filename):
    response = requests.get(url, stream=True)
    with open(filename, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)


init_inputs()

media = ffmpeg.input('inputs/sintel.mp4')
music = ffmpeg.input('inputs/music.mp3')
en = ffmpeg.input('inputs/en.srt')
es = ffmpeg.input('inputs/es.srt')

# probe = File("westworld.mkv")
probe = File("inputs/sintel.mp4")
# probe = File("inputs/music.mp3")
# probe = File("inputs/en.srt")
# parsed = json.loads(json.dumps(probe))

# print(json.dumps(parsed, indent=4, sort_keys=True))

# Generate output with 5 streams
# outfile = ffmpeg.output(media, music, en, es, 'test-out.mkv').run()