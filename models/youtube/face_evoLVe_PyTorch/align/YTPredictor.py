import os
import time
from .face_recognizer import face_recognizer 
import torch
import warnings
from .backbone.model_irse import IR_50, IR_101, IR_152, IR_SE_50, IR_SE_101, IR_SE_152
from .head.metrics import ArcFace, CosFace, SphereFace, Am_softmax
import cv2
    

class YTPredictor:
    def __init__(self, absPath_to_youtube, cast_length=10, compress_width=400, skip_frames=15, frame_range=None):
        self.cast_length = cast_length        
        self.compress_scale = None
        self.compress_width = compress_width
        self.skip_frames = skip_frames
        self.frame_range = frame_range  # play the video between framw_range, set to None if you want to play the whole video
        # please pass the corresponding absolute path!
        current_dir = absPath_to_youtube
        module_path = os.path.abspath(os.path.join(current_dir, './face_evoLVe_PyTorch/align'))
        model_root = os.path.abspath(os.path.join(current_dir,'./models/faceClassifier/Backbone.pth'))
        head_root = os.path.abspath(os.path.join(current_dir, './models/faceClassifier/Head.pth'))
        self.video_path = os.path.join(current_dir, 'data/videos/')
               
        os.chdir(module_path)
        
        # CPU/GPU
#        self.device = torch.device("cpu")
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        # load backbone from a checkpoint
        print("Loading Backbone Checkpoint '{}'".format(model_root))
        INPUT_SIZE = [112, 112]
        num_classes = 1500
        self.backbone = IR_50(INPUT_SIZE)
        if torch.cuda.is_available():
            self.backbone.load_state_dict(torch.load(model_root))
        else:
            warnings.warn('No CUDA device found, loading model to CPU')
            self.backbone.load_state_dict(torch.load(model_root, map_location='cpu'))
        self.backbone.to(self.device)
        self.backbone.eval() # set to evaluation mode
        
        # CPU/GPU
#        self.HEAD = ArcFace(in_features = 512, out_features = num_classes, device_id = None)
        self.HEAD = ArcFace(in_features = 512, out_features = num_classes, device_id = [0])
        
        self.HEAD.load_state_dict(torch.load(head_root))        
        
        ##
        self.info_dic = {}
        f = open("id_name_rank.txt", 'r') 
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            line_split = line.split(" ")
            self.info_dic[int(line_split[0])-1] = [line_split[1], line_split[2], line_split[3], line_split[4]]
        f.close()
        
        

    def __call__(self, yt_url=None, path_to_video=None, set_name=None):  
        start = time.time()
        
        for cast_list in face_recognizer( set_name=set_name, \
        backbone=self.backbone,HEAD=self.HEAD,info_dic=self.info_dic,device=self.device, \
        skip_frames=self.skip_frames,video_url=yt_url, path_to_video=path_to_video, \
        compress_scale=self.compress_scale, compress_width=self.compress_width, frame_range=self.frame_range, \
        video_path=self.video_path):  ## yield image and cast_list.
            cast_dic = cast_list
        
        # sort the cast list by frequency        
        cast_sorted = sorted(cast_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        # compute time
        end = time.time()
        print("total time:",end-start)
        return cast_sorted[0:self.cast_length]
#        return cast_dic

    def yield_faces(self, yt_url):
        start = time.time()
        for cast_list in face_recognizer( \
        backbone=self.backbone,HEAD=self.HEAD,info_dic=self.info_dic,device=self.device, \
        skip_frames=self.skip_frames,video_url=yt_url, \
        compress_scale=self.compress_scale, compress_width=self.compress_width, frame_range=self.frame_range, \
        video_path=self.video_path):  ## yield image and cast_list.
            cast_sorted = sorted(cast_list.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
            yield cast_sorted[:self.cast_length]
#            for cast in cast_sorted[:self.cast_length]:
#                cv2.imshow("face",cast[1][3])
#                key = cv2.waitKey(0)
#                if key == 27:  # ESC
#                    cv2.destroyAllWindows() 
#                    return
        self.cast_list = cast_sorted[:self.cast_length]
        # compute time
        end = time.time()
        print("total time:",end-start)
#        return cast_dic
        
        
            
    def get_result(self):
        return (self.cast_list)