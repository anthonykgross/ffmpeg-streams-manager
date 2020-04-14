import ffmpeg
import abc


class File(object):
    def __init__(self, filename):
        self.__filename = filename
        self.__streams = []

        probe = ffmpeg.probe(filename)
        for stm in probe['streams']:
            stream = None
            if stm['codec_type'] == 'video':
                stream = VideoStream()
            if stm['codec_type'] == 'audio':
                stream = AudioStream()
            if stm['codec_type'] == 'subtitle':
                stream = SubtitleStream()
            if stream is not None:
                stream.from_json(stm)
                self.__streams.append(stream)

    def get_streams(self):
        return self.__streams

    def get_streams_by_type(self, cls):
        streams = []
        for stream in self.__streams:
            if isinstance(stream, cls):
                streams.append(stream)
        return streams

    def get_video_streams(self):
        return self.get_streams_by_type(VideoStream)

    def get_audio_streams(self):
        return self.get_streams_by_type(AudioStream)

    def get_subtitle_streams(self):
        return self.get_streams_by_type(SubtitleStream)


class Stream:
    def __init__(self):
        self.language = None
        self.map = None
        self.codec = None

    def from_json(self, params):
        self.map = params['index']
        self.codec = params['codec_name']
        if 'tags' in params:
            if 'language' in params['tags']:
                self.language = params['tags']['language']
        return


class VideoStream(Stream):
    pass


class AudioStream(Stream):
    pass


class SubtitleStream(Stream):
    pass
