from pathlib import Path
import ffmpeg


class PrintableMixin(object):
    def __str__(self):
        return str(self.__dict__).replace('_'+self.__class__.__name__, '')

    def __repr__(self):
        return self.__str__()


class Converter(PrintableMixin):
    def __init__(self, output):
        self.__kwargs = {
            'map_metadata': '-1'
        }
        self.__args = ()
        self.__inputs = []
        self.__output = Path(output)

    def add_kwargs(self, **kwargs):
        if isinstance(kwargs, dict):
            self.__kwargs.update(kwargs)

    def add_args(self, *args):
        if isinstance(args, tuple):
            self.__args += args

    def add_input(self, input):
        if isinstance(input, Input):
            self.__inputs.append(input)

    def __init_metadata(self):
        if self.__output.suffix == '.mkv':

            video_streams = self.get_final_video_streams()
            for index in range(0, len(video_streams)):
                stream = video_streams[index]
                self.__add_metadata(stream, index)

            audio_streams = self.get_final_audio_streams()
            for index in range(0, len(audio_streams)):
                stream = audio_streams[index]
                self.__add_metadata(stream, index)

            subtitle_streams = self.get_final_subtitle_streams()
            for index in range(0, len(subtitle_streams)):
                stream = subtitle_streams[index]
                self.__add_metadata(stream, index)

    def __add_metadata(self, stream, index):
        metadata_type = None
        if isinstance(stream, VideoStream):
            metadata_type = 'v'
        if isinstance(stream, AudioStream):
            metadata_type = 'a'
        if isinstance(stream, SubtitleStream):
            metadata_type = 's'

        if metadata_type is not None and stream.language is not None:
            self.add_kwargs(**{'metadata:s:'+metadata_type+':'+str(index): 'language='+stream.language})

    def __init_ffmpeg_inputs(self):
        for index in range(0, len(self.__inputs)):
            input = self.__inputs[index]
            for map in input.get_final_maps():
                # Be careful : map must be a str in `ffmpeg_input`
                self.add_args(
                    input.get_ffmpeg_input()[str(map)]
                )

    def get_final_streams(self):
        streams = []
        for input in self.__inputs:
            for stream in input.get_final_streams():
                streams.append(stream)
        return streams

    def __get_final_streams_by_type(self, cls):
        streams = []
        for stream in self.get_final_streams():
            if isinstance(stream, cls):
                streams.append(stream)
        return streams

    def get_final_video_streams(self):
        return self.__get_final_streams_by_type(VideoStream)

    def get_final_audio_streams(self):
        return self.__get_final_streams_by_type(AudioStream)

    def get_final_subtitle_streams(self):
        return self.__get_final_streams_by_type(SubtitleStream)

    def run(self):
        self.__init_metadata()
        self.__init_ffmpeg_inputs()
        self.add_args(str(self.__output))

        ffmpeg.output(*self.__args, **self.__kwargs).run()

    def debug(self):
        self.debug_result()
        self.debug_summary()

    def debug_result(self):
        print("Result :")
        for stream in self.get_final_streams():
            print('  %s' % stream)

    def debug_summary(self):
        for input in self.__inputs:
            print('')
            input.debug()


class H265Converter(Converter):
    def __init__(self, output):
        super().__init__(output)
        self.add_kwargs(vcodec='hevc', acodec='aac')


class H264Converter(Converter):
    def __init__(self, output):
        super().__init__(output)
        self.add_kwargs(vcodec='h264', acodec='aac')


class Input(PrintableMixin):
    def __init__(self, filename, mapping="*", **kwargs):
        self.__media = Media(filename)
        self.__mapping = mapping
        self.__ffmpeg_input = ffmpeg.input(str(self.__media.get_path()), **kwargs)

    def get_media(self):
        return self.__media

    def get_mapping(self):
        return self.__mapping

    def get_ffmpeg_input(self):
        return self.__ffmpeg_input

    def get_maps_by_language(self, language):
        maps = []
        for map in self.__media.get_streams():
            stream = self.__media.get_streams()[map]
            if stream.language == language:
                maps.append(map)
        return maps

    def get_final_streams(self):
        streams = []
        for map in self.get_final_maps():
            stream = self.__media.get_streams()[map]
            streams.append(stream)
        return streams

    def get_final_maps(self):
        if self.__mapping == "*":
            return list(self.__media.get_streams().keys())

        if isinstance(self.__mapping, list):
            maps = []
            for val in self.__mapping:
                if isinstance(val, int):
                    maps += [val]
                if isinstance(val, str):
                    maps += self.get_maps_by_language(val)

            # remove duplicate entries
            return list(set(maps))
        return []

    def debug(self):
        self.debug_result()
        print('  ----  debug ---- ')
        self.debug_summary()

    def debug_result(self):
        print("Input : %s" % str(self.__media.get_path()))
        print("  Mapping :")
        for stream in self.get_final_streams():
            print('    %s' % stream)

    def debug_summary(self):
        print("  Video streams :")
        for stream in self.__media.get_video_streams():
            print('    %s' % stream)

        print("  Audio streams :")
        for stream in self.__media.get_audio_streams():
            print('    %s' % stream)

        print("  Subtitle streams :")
        for stream in self.__media.get_subtitle_streams():
            print('    %s' % stream)


class Media(PrintableMixin):
    def __init__(self, filename):
        self.__path = Path(filename)
        self.__streams = {}
        self.refresh()

    def refresh(self):
        if self.__path.exists():
            probe = ffmpeg.probe(str(self.__path))
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
                    self.__streams[stream.map] = stream
        else:
            raise Exception('Invalid filename')

    def get_path(self):
        return self.__path

    def get_streams(self):
        return self.__streams

    def __get_streams_by_type(self, cls):
        streams = []
        for map in self.__streams:
            stream = self.__streams[map]
            if isinstance(stream, cls):
                streams.append(stream)
        return streams

    def get_video_streams(self):
        return self.__get_streams_by_type(VideoStream)

    def get_audio_streams(self):
        return self.__get_streams_by_type(AudioStream)

    def get_subtitle_streams(self):
        return self.__get_streams_by_type(SubtitleStream)


class Stream(PrintableMixin):
    def __init__(self):
        self.language = None
        self.map = None
        self.codec = None

    def from_json(self, params):
        self.map = int(params['index'])
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
