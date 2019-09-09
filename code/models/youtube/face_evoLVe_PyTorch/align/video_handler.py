import cv2
import numpy as np
import os.path
from .detector import detect_faces
from .visualization_utils import show_results
import PIL
import math
import sys
import time
from pytube import YouTube
from youtube_dl import YoutubeDL
import os

class VideoPlayer(object):
    
    def __init__(self, path, set_name=None, path_to_video=None, skip_frames=None, batch_range=None, \
    frame_range=None, compress_width=None, compress_scale=None, video_url=None):                         
        self.set_name = set_name        
        self.path = path        
        if video_url:
            self.download_video(video_url) 
        elif path_to_video:
            self.path = path_to_video
        self.cap = cv2.VideoCapture(self.path)
        self.frame_num_total = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_range:
            self.frame_range = frame_range
#        elif batch_range:
#            self.frame_range = (batch_range[1]*batch_range[0], (batch_range[1]+1)*batch_range[0])
        else:
            self.frame_range = (0,self.frame_num_total)
        print("frame range is:",self.frame_range)
        if self.frame_range[1]>self.frame_num_total:
            print("frame out of range, maximum is ", self.frame_num_total)
            sys.exit(0)
        self.image_static = []
        self.cast_list = dict()
        self.cast_freq = dict()
        self.face_total = 0
        self.compress_width = compress_width
        self.compress_scale = compress_scale  
        self.compress_size = None
        self.skip_frames = skip_frames
        self.count = 0
        
  
    def yield_frames_advanced(self):
#        self.cap.set(1, self.frame_range[0])    
        while self.count<self.frame_range[1]/self.skip_frames:
            self.cap.set(1, self.frame_range[0]+self.count*self.skip_frames)
            self.count = self.count+1
                
            success, image = self.cap.read()
            if not success:
                self.cap.release()
                print("End of the video")
                break
            else:
                yield image
    
    def yield_frames(self):
        cap = cv2.VideoCapture(self.path)
        
        while True:
            success, image = cap.read()
            if not success:
                cap.release()
                print("End of the video")
                break
            else:
                yield image

        
    def display_video(self, waitKey=1):
        for image in self.yield_frames():
            cv2.imshow("video",image)
            key = cv2.waitKey(waitKey)
            if key == 27:  # ESC
                break
        cv2.destroyAllWindows()
        return
    
    def mark_faces(self):
        for img in self.yield_frames_advanced():
            print("current frame: ",int(self.cap.get(1))," / ", self.frame_num_total)
            if not self.compress_size:
                print(img.shape)
                [h,w] = img.shape[0],img.shape[1]
                if not self.compress_scale:
                    if self.compress_width:
                        self.compress_scale = self.compress_width/w
                    else:
                        self.compress_scale=1
                w = int(self.compress_scale*w)
                h = int(self.compress_scale*h)
                self.compress_size = (w,h)
                    
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            pil_img = PIL.Image.fromarray(img)
            pil_img_compressed = pil_img.resize(self.compress_size,PIL.Image.ANTIALIAS)
#            cv2.imshow("video",img)
            try:            
                bb_list, landmarks = detect_faces(pil_img_compressed) # detect bboxes and landmarks for all faces in the image
            except:
                bb_list = []
                landmarks = []
            bb_list = np.asarray(bb_list)/self.compress_scale
            landmarks = np.asarray(landmarks)/self.compress_scale
            img_detected = show_results(pil_img, bb_list, landmarks) # visualize the results
            
            img_detected = np.array(img_detected) 
            self.image_static = img_detected[:, :, ::-1].copy() 
            yield (bb_list)
        return
        
        
    def label_face(self, name, bb_temp):
        self.face_total += 1
        cv2.putText(self.image_static, name[1], (bb_temp[0],bb_temp[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        if name[0] in self.cast_list:
            self.cast_list[name[0]] += 1
        else:
            self.cast_list[name[0]] = 1
            self.cast_freq[name[0]] = [0,name[1],int(name[2])/1500,0]
        self.cast_freq[name[0]][3] = self.get_face(bb_temp)

    
    def get_face(self, bb):
        face = self.image_static[bb[1]:bb[3],bb[0]:bb[2]]
        return face
            
    def output_image(self):
        for name in self.cast_list:         
            self.cast_freq[name][0] = self.cast_list[name]/self.face_total
#        return [self.image_static,self.cast_freq]
        return self.cast_freq
        
        
    def download_video(self, video_url):
        print("download video...")
        video_url = [video_url]
        if self.set_name:
            ydl_opts = {
            'outtmpl' : self.path+str(1)
            }
        else:    
            ydl_opts = {
            'outtmpl' : self.path+"%(title)s.%(ext)s"
            }
        
        ydl = YoutubeDL(ydl_opts)
        info = ydl.extract_info(video_url[0], download=False)
        if self.set_name:
            download_target = [os.path.join(self.path,str(self.set_name))]
        else:
            download_target = ydl.prepare_filename(info).split(".")[:-1]
        ydl.download(video_url)
        print(download_target)
        for r, d, f in os.walk(self.path):
            file_name = f
            break
    
        for i in file_name:
            file_temp = os.path.join(self.path,i)
            if file_temp.split(".")[:-1] == download_target:
                self.path = file_temp
        
        
        
    def test_img(self):
        pass
            

                  
class VideoRecorder(object):                

    def __init__(self, out_path,hz=30):
        self.video_writer = None
        self.out_path = str(os.path.abspath(out_path))
        self.hz = hz
        
    def record_frame(self, image):
        if self.video_writer is None:
            shape = (image.shape[1], image.shape[0])
            self.video_writer = cv2.VideoWriter(self.out_path,cv2.VideoWriter_fourcc('M','J','P','G'), self.hz, shape)            
        self.video_writer.write(image)

    def save_video(self):
        self.video_writer.release()
              




class FileHandler(object):

    def __init__(self, input_dir):
        self.input_dir = input_dir
        
    def yield_files(self):
        for (path,dirs,files) in os.walk(self.input_dir):
            if dirs or not files:
                continue
            for file in files:
                img = cv2.imread(os.path.join(path,file))
                yield img
 
       
if __name__ == '__main__':
    videoPlayer = VideoPlayer("/home/Luo/aml-group-1/Predictor_video/data/videos",video_url = "https://www.youtube.com/watch?v=G0EpmL8o4Hs")