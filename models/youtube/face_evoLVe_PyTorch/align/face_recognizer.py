# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#import warnings
import torch
import cv2
import numpy as np
#import os
#import sys
#import matplotlib.pyplot as plt

from .backbone.model_irse import IR_50, IR_101, IR_152, IR_SE_50, IR_SE_101, IR_SE_152
from .head.metrics import ArcFace, CosFace, SphereFace, Am_softmax
from .video_handler import VideoPlayer

def l2_norm(input, axis = 1):
    norm = torch.norm(input, 2, axis, True)
    output = torch.div(input, norm)
    return output





def face_recognizer(backbone,HEAD,info_dic,device,skip_frames,video_path, set_name=None, \
frame_range=None,compress_scale=None,compress_width=None,video_url=None,path_to_video=None):
    
    tta = True
    
    ## load classifier model
    videoPlayer = VideoPlayer(set_name=set_name, path_to_video=path_to_video, \
    skip_frames=skip_frames, video_url=video_url,path=video_path,frame_range=frame_range, \
    compress_scale=compress_scale, compress_width=compress_width)
    
    for bb_list in videoPlayer.mark_faces(): 
        if bb_list is not []:
            for bb in bb_list:     
                bb = bb.astype(int)
                face = videoPlayer.get_face(bb)  
                
                # todo!!! get label ####################################################################################
                # resize image to [128, 128]
                try:
                    resized = cv2.resize(face, (128, 128))            
                except:
                    continue
                        
                # center crop image
                a=int((128-112)/2) # x start
                b=int((128-112)/2+112) # x end
                c=int((128-112)/2) # y start
                d=int((128-112)/2+112) # y end
                ccropped = resized[a:b, c:d] # center crop the image
                ccropped = ccropped[...,::-1] # BGR to RGB
            
                # flip image horizontally
                flipped = cv2.flip(ccropped, 1)
            
                # load numpy to tensor
                ccropped = ccropped.swapaxes(1, 2).swapaxes(0, 1)
                ccropped = np.reshape(ccropped, [1, 3, 112, 112])
                ccropped = np.array(ccropped, dtype = np.float32)
                ccropped = (ccropped - 127.5) / 128.0
                ccropped = torch.from_numpy(ccropped)
            
                flipped = flipped.swapaxes(1, 2).swapaxes(0, 1)
                flipped = np.reshape(flipped, [1, 3, 112, 112])
                flipped = np.array(flipped, dtype = np.float32)
                flipped = (flipped - 127.5) / 128.0
                flipped = torch.from_numpy(flipped)
            
            
                # extract features
                with torch.no_grad():
                    if tta:
                        emb_batch = backbone(ccropped.to(device)).cpu() + backbone(flipped.to(device)).cpu()
                        features = l2_norm(emb_batch)
                    else:
                        features = l2_norm(backbone(ccropped.to(device)).cpu())
                
                
                outputs = HEAD(features)
                label_list = outputs.tolist()[0]   
                label = label_list.index(max(label_list))
                
                ####################################################################################
                name = info_dic[label]
#                print("+++++++++++++",name,max(label_list))
                videoPlayer.label_face(name,bb)
#        (image,cast_list) = videoPlayer.output_image()
        cast_list = videoPlayer.output_image()
        yield cast_list
        
    
 
   
    
def main():
    for (image,cast_list) in face_recognizer():  
        print("=========================================")
        for cast in cast_list:
            print (cast)
            print(cast_list[cast])
        cv2.imshow("image",image)
        key = cv2.waitKey(0)
        if key == 27:  # ESC
            break
    cv2.destroyAllWindows() 
 
       
if __name__ == '__main__':
    main()
