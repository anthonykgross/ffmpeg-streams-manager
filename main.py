from models import *

# input1 = Input("westworld.mkv", ['fre'])
# input2 = Input("southpark.mkv")
input1 = Input("inputs/sintel.mp4")
input2 = Input("inputs/es.srt")
input3 = Input("inputs/en.srt")

input1.get_media().get_video_streams()[0].language = 'eng'
input2.get_media().get_subtitle_streams()[0].language = 'es'
input3.get_media().get_subtitle_streams()[0].language = 'eng'

# input1.debug()
# input2.debug()

converter = H264Converter('plop.mkv')
converter.add_input(input1)
converter.add_input(input2)
converter.add_input(input3)
# converter.debug()
converter.run()