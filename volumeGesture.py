import cv2
import numpy as np

import hantrackingmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]
print(volRange)
#volume.SetMasterVolumeLevel(-15.0, None)


detector=htm.handDetector()
#######################################################
w_cam,h_cam=640,480
#######################################################
cap=cv2.VideoCapture(0)
cap.set(3,w_cam)
cap.set(4,h_cam)



while cap.isOpened():
    ret,frame=cap.read()
    frame=detector.findHands(frame)
    lmList=detector.findPosition(frame,draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])
        # Les deux pouces

        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(frame,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(frame, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        #print(length)

        vol=np.interp(length,[50,300],[minVol,maxVol])
        print(int(vol))
        volume.SetMasterVolumeLevel(vol+10,None)
        if length<50:
            cv2.circle(frame, (cx, cy), 15, (0, 255, 0), cv2.FILLED)



    cv2.imshow('frame',frame)


    if cv2.waitKey(1) == 13:  # 13 is the Enter Key
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()