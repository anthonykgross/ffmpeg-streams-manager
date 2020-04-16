from ffmpeg_streams_manager import *

"""
wget http://www.peach.themazzone.com/durian/movies/sintel-1024-surround.mp4 -O sintel.mp4
wget https://durian.blender.org/wp-content/content/subtitles/sintel_en.srt -O en.srt
wget https://durian.blender.org/wp-content/content/subtitles/sintel_es.srt -O es.srt
wget https://www.dropbox.com/s/xiiub9bmm5rd71l/Kasger%20-%20Out%20Here%20_NCS%20Release_.mp3?dl=1 -O music.mp3
"""
input1 = Input("sintel.mp4")
input2 = Input("en.srt")
input3 = Input("es.srt")

input1.get_media().get_video_streams()[0].language = 'eng'
input2.get_media().get_subtitle_streams()[0].language = 'es'
input3.get_media().get_subtitle_streams()[0].language = 'eng'

converter = Converter('sintel.mkv')
converter.add_input(input1)
converter.add_input(input2)
converter.add_input(input3)
# converter.debug()
converter.run()
