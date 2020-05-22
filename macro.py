import pyautogui as pag

import sneakysnek
from sneakysnek.recorder import Recorder
from sneakysnek.keyboard_event import KeyboardEvents as KE
from sneakysnek.keyboard_keys import KeyboardKey as KK
from threading import Thread
import time

ctrl_m_active = False
ctrl_j_active = False
ctrl=False

def ctrl_j():
    while ctrl_j_active:
        pag.rightClick(duration=2.5)
        pag.press('5')
        time.sleep(1)
        pag.press('6')
        
def ctrl_m():
    width, height = pag.size()
    print(width,height)
    pag.move(1000,500,duration=1.)
    # while ctrl_m_active:
    #     pag.move(width//2-10,height//2)
    #     time.sleep(1.)
    #     pag.move(width//+10,height//2)
    #     pag.mouseDown(button='right')
    #     time.sleep(2.5)
    #     pag.mouseUp(button='right')
    #     time.sleep(1.)

def user_action(arg):

    global ctrl_j_active
    global ctrl_m_active
    global ctrl
    

    if not(isinstance(arg, sneakysnek.keyboard_event.KeyboardEvent)):
        return
    if ((arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_LEFT_CTRL)):
        ctrl=True
        return
    if ((arg.event == KE.UP) and (arg.keyboard_key == KK.KEY_LEFT_CTRL)):
        ctrl=False
        return
    if ctrl:
        if (arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_J):
            if not ctrl_j_active:
                ctrl_j_active = True
                Thread(target=ctrl_j).start()
            else:
                ctrl_j_active = False

        if (arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_M):
            if not ctrl_m_active:
                ctrl_m_active = True
                Thread(target=ctrl_m).start()
            else:
                ctrl_m_active = False

recorder = Recorder.record(user_action)
print('ready')
while True:
    pass
