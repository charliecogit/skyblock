import cv2
import asyncio

cap = cv2.VideoCapture('/Users/carlosco/IdeaProjects/skyblock/2020-05-16 14-31-25.mp4')

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
FPS = cap.get(cv2.CAP_PROP_FPS)
print(FPS, width, height)

ts=37
tf=35

cap.set(cv2.CAP_PROP_POS_FRAMES, FPS*ts+tf)
grab, frame = cap.read()

while True:
    cv2.imshow('window', frame)
    if cv2.waitKey(1) == ord('q'):
        break

