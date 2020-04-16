from tqdm import tqdm
import requests
import os


def init_fixtures():
    video = "http://www.peach.themazzone.com/durian/movies/sintel-1024-surround.mp4"
    music = "https://www.dropbox.com/s/xiiub9bmm5rd71l/Kasger%20-%20Out%20Here%20_NCS%20Release_.mp3?dl=1"
    en = "https://durian.blender.org/wp-content/content/subtitles/sintel_en.srt"
    es = "https://durian.blender.org/wp-content/content/subtitles/sintel_es.srt"

    print("Fixtures loading ...")
    if not os.path.isfile('tests/fixtures/en.srt'):
        download(en, 'tests/fixtures/en.srt')
    if not os.path.isfile('tests/fixtures/es.srt'):
        download(es, 'tests/fixtures/es.srt')
    if not os.path.isfile('tests/fixtures/music.mp3'):
        download(music, 'tests/fixtures/music.mp3')
    if not os.path.isfile('tests/fixtures/sintel.mp4'):
        download(video, 'tests/fixtures/sintel.mp4')


def download (url, filename):
    response = requests.get(url, stream=True)
    with open(filename, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
