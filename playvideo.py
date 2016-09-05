# %%         Play video in Static Box 1
#
#
# 
# %%
import sitecustomize
import wx
import os
import numpy as np
import cv2
#from pvg_common import previewPanel, options
#import pysolovideo

 #%%   print('Playing Video')
cap = cv2.VideoCapture('fly_movie.avi')

print('cap is set')
while True:

    print('while looped')
    ret, frame = cap.read()

    if ret == True:

        print('ret was true')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame',gray)


        if cv2.waitKey(30) & 0xFF == ord('q'):
            print('waiting')
            break

    else:
        print('ret was false')
        print(ret)
        print(frame)
        break
print('exiting')
cap.release()
cv2.destroyAllWindows()