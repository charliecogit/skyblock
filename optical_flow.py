import mss
import mss.tools
import numpy as np
import time
from pathlib import Path
import pyautogui as pag
import ctypes
import multiprocessing as mp
import cv2

a = np.linspace(0,1,3, dtype=np.float32)
x,y=np.meshgrid(a,a)
pts = list(zip(x.flat,y.flat))
pts=np.expand_dims(pts,axis=1)


monitor = {"top": 10, "left": 10, "width": 200, "height": 100}
with mss.mss() as sct:
    img = np.array(sct.grab(monitor))[...,:3]
    prvs = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    hsv = np.zeros_like(img)
    hsv[...,1] = 255

    while True:
        img = np.array(sct.grab(monitor))[...,:3]
        nxt = cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
        # nxt_pts = cv2.calcOpticalFlowPyrLK(prvs, nxt, pts, None)
        flow = cv2.calcOpticalFlowFarneback(prvs, nxt, None , 0.5, 3, 15, 3, 5, 1.2, 0)
        print(nxt.shape)
        print(flow.shape)
        print(np.max(flow,axis=(0,1)))
        prvs = nxt

    cv2.destroyAllWindows()