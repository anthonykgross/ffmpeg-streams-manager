from models import *
from pathlib import Path
import csv

"""
sudo mount -t cifs -o username=username,password=password //192.168.1.10/series /mnt/series
"""
columns = [
    'video',
    'nb_streams',
    'video_language',
    'video_codec',
    'audio_language',
    'audio_codec',
    'nb_subtitles',
]

filename = 'export.csv'
with open(filename, 'w+', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(columns)

    for path in Path('/mnt/series').rglob('*'):
        if not path.is_dir():
            print(str(path))
            file = File(str(path))

            video_codec = 'NA'
            video_language = 'NA'
            video_streams = file.get_video_streams()
            if len(video_streams) > 0:
                video_codec = video_streams[0].codec
                video_language = video_streams[0].language

            audio_codec = 'NA'
            audio_language = 'NA'
            audio_streams = file.get_audio_streams()
            if len(audio_streams) > 0:
                audio_codec = audio_streams[0].codec
                audio_language = audio_streams[0].language

            writer.writerow([
                str(path),
                len(file.get_streams()),
                video_language,
                video_codec,
                audio_language,
                audio_codec,
                len(file.get_subtitle_streams()),
            ])
f.close()
