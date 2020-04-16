from ffmpeg_streams_manager import *

"""
wget http://www.peach.themazzone.com/durian/movies/sintel-1024-surround.mp4
wget https://durian.blender.org/wp-content/content/subtitles/sintel_en.srt
wget https://durian.blender.org/wp-content/content/subtitles/sintel_es.srt
"""
input1 = Input("sintel-1024-surround.mp4")
input2 = Input("sintel_en.srt")
input3 = Input("sintel_es.srt")

input1.get_media().get_video_streams()[0].language = 'eng'
input2.get_media().get_subtitle_streams()[0].language = 'es'
input3.get_media().get_subtitle_streams()[0].language = 'eng'

converter = Converter('sintel.mkv')
converter.add_input(input1)
converter.add_input(input2)
converter.add_input(input3)
# converter.debug()
converter.run()
