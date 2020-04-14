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
                print(stream.__dict__)
                self.__streams.append(stream)


class Stream:
    def __init__(self):
        self.language = None
        self.map = None

    def from_json(self, params):
        self.map = params['index']
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
