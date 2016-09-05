# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:37:24 2016

@author: Lori
"""

import cv2


cap = cv2.VideoCapture("pachebell.mp4")
print cap.isOpened()   # True = read video successfully. False - fail to read video.
