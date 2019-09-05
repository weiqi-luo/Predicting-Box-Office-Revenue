from youtube.face_evoLVe_PyTorch.align.YTPredictor import YTPredictor
import os
import cv2


current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
absPath_to_youtube = os.path.abspath(os.path.join(current_dir, 'youtube'))
ytPredictor = YTPredictor(absPath_to_youtube=absPath_to_youtube, \
cast_length=8, compress_width=400, skip_frames=12, frame_range=[0,400])

f = open(os.path.join(current_dir,'trailer_list.txt'),'r')
list_of_trailer = f.read().splitlines()
f.close()
print(list_of_trailer)
cast_list=[]
weight_list=[]

for i in range(len(list_of_trailer)):
    path_to_video = os.path.join(current_dir, "videos/"+list_of_trailer[i])
    result = ytPredictor.__call__(yt_url=None, path_to_video=path_to_video)
    cast_ = [result[i][0] for i in range(len(result))]
    freq_ = [result[i][1][0] for i in range(len(result))]
    weight_ = [float(itm)/sum(freq_list) for itm in freq_]
    cast_list.append(cast_)
    weight_list.append(weight_)
    if i>2:
        break