from youtube.face_evoLVe_PyTorch.align.YTPredictor import YTPredictor
import os
import cv2


current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
absPath_to_youtube = os.path.abspath(os.path.join(current_dir, 'youtube'))

## create the object
## absPath_to_youtube : please pass the absolute path to the directory 'youtube' 
## cast_length : decides the length of the cast list
## compress_width : set it smaller will speed up face detection, however increase the difficulty to detect face with small size
## skip_frames : set it bigger will speed up face recognition, however loose more frames 
## frame_range : set to None will loop through whole video, while set it to [start_frame, end_frame] will only loop in this range, optimal for debugging             
ytPredictor = YTPredictor(absPath_to_youtube=absPath_to_youtube, \
cast_length=8, compress_width=400, skip_frames=12, frame_range=[0,400])


#############################################################################################
################################## output explaination ################################################
## cast_list is a list of list, each entry contains the information of a actor/actress, and is sorted with its 
## show-up-frequency in the movie
## [string'imdb_id' , [ float(show-up-frequency), string'name', float(rank-of-popularity)], numpy.ndarray(face_image)]
    ## cast[0]: imdb_id
    ## cast[1][0] : show-up-frequency is between [0,1], if only one person shows up then his frequency is 1.
    ## cast[1][1] : name
    ## cast[1][2] : rank-of-popularity is between [0,1], 0 corresponds to the most famous star
    ## cast[1][3] : face_image 
#############################################################################################



#############################################################################################
################################## Option 1 ################################################
## Uncomment this part to call face detection and returns a cast list of length cast_length only at the end of movie, 
## which is picked out according to their show-up-frequency in the movie
## reuse the same object for all videos to save time
############################################################################################
## to use youtube url
#path_to_video = os.path.join(current_dir, "youtube/data/videos/The Hummingbird Project Trailer #1 (2019) _ Movieclips Trailers.mkv")
#cast_list1 = ytPredictor.__call__(yt_url=None, path_to_video=path_to_video)
##cast_list2 = ytPredictor.__call__(yt_url="https://www.youtube.com/watch?v=2NwHpkEjn84",path_to_video=None)
#for cast in cast_list1:
#    print("=============================================================")
#    print("imdb id:", cast[0])
#    print("predicted label:", cast[1][1])
#    print("the accumulated show-up-frequency:", cast[1][0])
#    print("rank-of-popularity:", cast[1][2])


print("=============================================================")
print("=============================================================")
print("=============================================================")

#############################################################################################
## to use local video
cast_list1 = ytPredictor.__call__(yt_url="https://www.youtube.com/watch?v=Y_JcTg5mrEY", path_to_video=None, set_name=1)
#cast_list2 = ytPredictor.__call__(yt_url="https://www.youtube.com/watch?v=2NwHpkEjn84",path_to_video=None)
for cast in cast_list1:
    print("=============================================================")
    print("imdb id:", cast[0])
    print("predicted label:", cast[1][1])
    print("the accumulated show-up-frequency:", cast[1][0])
    print("rank-of-popularity:", cast[1][2])
#############################################################################################





#############################################################################################
################################ Option 2 ################################################
## Uncomment this part to call face detection and returns a cast list of length cast_length at each frame of movie, 
## which is picked out according to their show-up-frequency in the movie
## if you only want the final result at the end of video please use option 1 to save time
## please comment the imshow part if you want to run it on aws
#############################################################################################
## loop through faces in each frame
## press any key except esc to continue
#key=None
#for cast_list in ytPredictor.yield_faces(yt_url="https://www.youtube.com/watch?v=Y_JcTg5mrEY",path_to_video=None):    
#    for cast in cast_list:
#        print("imdb id:", cast[0])
#        print("predicted label:", cast[1][1])
#        print("the accumulated show-up-frequency:", cast[1][0])
#        print("rank-of-popularity:", cast[1][2])
#        
#        ## uncomment this part to show the face        
##        cv2.imshow("face",cast[1][3])
##        key = cv2.waitKey(0)
##        if key == 27:  # ESC
##            cv2.destroyAllWindows() 
##            break
##    if key == 27:  # ESC
##        cv2.destroyAllWindows() 
##        break
#        
### get final result at the end of video
#cast_list = ytPredictor.get_result()
#for cast in cast_list:
#    print(cast[0],cast[1][:-1])
#############################################################################################

