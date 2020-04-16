from ffmpeg_streams_manager import *

"""
wget http://www.peach.themazzone.com/durian/movies/sintel-1024-surround.mp4 -O sintel.mp4
wget https://durian.blender.org/wp-content/content/subtitles/sintel_en.srt -O en.srt
wget https://durian.blender.org/wp-content/content/subtitles/sintel_es.srt -O es.srt
wget https://www.dropbox.com/s/xiiub9bmm5rd71l/Kasger%20-%20Out%20Here%20_NCS%20Release_.mp3?dl=1 -O music.mp3
"""
input1 = Input("sintel.mp4")
input2 = Input("../fixtures/en.srt")
input3 = Input("../fixtures/es.srt")

converter = Converter('sintel.mkv')
converter.add_input(input1)
converter.add_input(input2)
converter.add_input(input3)
converter.debug()
# converter.run()

"""
Result :
  {'language': 'und', 'map': 0, 'codec': 'h264'}
  {'language': 'eng', 'map': 1, 'codec': 'aac'}
  {'language': None, 'map': 0, 'codec': 'subrip'}
  {'language': None, 'map': 0, 'codec': 'subrip'}

Input : sintel-1024-surround.mp4
  Mapping :
    {'language': 'und', 'map': 0, 'codec': 'h264'}
    {'language': 'eng', 'map': 1, 'codec': 'aac'}
  ----  debug ---- 
  Video streams :
    {'language': 'und', 'map': 0, 'codec': 'h264'}
  Audio streams :
    {'language': 'eng', 'map': 1, 'codec': 'aac'}
  Subtitle streams :

Input : sintel_en.srt
  Mapping :
    {'language': None, 'map': 0, 'codec': 'subrip'}
  ----  debug ---- 
  Video streams :
  Audio streams :
  Subtitle streams :
    {'language': None, 'map': 0, 'codec': 'subrip'}

Input : sintel_es.srt
  Mapping :
    {'language': None, 'map': 0, 'codec': 'subrip'}
  ----  debug ---- 
  Video streams :
  Audio streams :
  Subtitle streams :
    {'language': None, 'map': 0, 'codec': 'subrip'}
"""
"""
This result means SRT files will be added to the video file
"""