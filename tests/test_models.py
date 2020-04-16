import unittest
from ffmpeg_streams_manager import *
from pathlib import Path


class TestInput(unittest.TestCase):
    def test_init(self):
        input = Input('fixtures/sintel.mp4')
        self.assertEqual(input.get_mapping(), '*')


class TestMedia(unittest.TestCase):
    def test_init_video(self):
        path = 'fixtures/sintel.mp4'
        media = Media(path)
        self.assertEqual(str(media.get_path()), path)
        self.assertIsInstance(media.get_path(), Path)
        self.assertEqual(len(media.get_streams()), 2)
        self.assertEqual(len(media.get_video_streams()), 1)
        self.assertEqual(len(media.get_audio_streams()), 1)
        self.assertEqual(len(media.get_subtitle_streams()), 0)

        streams = media.get_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'und')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], AudioStream)
        self.assertEqual(streams[1].language, 'eng')
        self.assertEqual(streams[1].codec, 'aac')
        self.assertEqual(streams[1].map, 1)

    def test_init_audio(self):
        path = 'fixtures/music.mp3'
        media = Media(path)
        self.assertEqual(str(media.get_path()), path)
        self.assertIsInstance(media.get_path(), Path)
        self.assertEqual(len(media.get_streams()), 1)
        self.assertEqual(len(media.get_video_streams()), 0)
        self.assertEqual(len(media.get_audio_streams()), 1)
        self.assertEqual(len(media.get_subtitle_streams()), 0)

        streams = media.get_streams()

        self.assertIsInstance(streams[0], AudioStream)
        self.assertEqual(streams[0].language, None)
        self.assertEqual(streams[0].codec, 'mp3')
        self.assertEqual(streams[0].map, 0)

    def test_init_subtitle(self):
        path = 'fixtures/es.srt'
        media = Media(path)
        self.assertEqual(str(media.get_path()), path)
        self.assertIsInstance(media.get_path(), Path)
        self.assertEqual(len(media.get_streams()), 1)
        self.assertEqual(len(media.get_video_streams()), 0)
        self.assertEqual(len(media.get_audio_streams()), 0)
        self.assertEqual(len(media.get_subtitle_streams()), 1)

        streams = media.get_streams()

        self.assertIsInstance(streams[0], SubtitleStream)
        self.assertEqual(streams[0].language, None)
        self.assertEqual(streams[0].codec, 'subrip')
        self.assertEqual(streams[0].map, 0)

    def test_wrong_file(self):
        with self.assertRaises(Exception):
            # File doesn't exist
            path = 'fixtures/sintel.mp3'
            media = Media(path)


class TestStream(unittest.TestCase):
    def test_init(self):
        stream = Stream()
        stream.from_json({
            'index': 0,
            'codec_name': 'h264',
            'tags': {
                'language': 'fre'
            }
        })
        self.assertEqual(stream.map, 0)
        self.assertEqual(stream.codec, 'h264')
        self.assertEqual(stream.language, 'fre')
