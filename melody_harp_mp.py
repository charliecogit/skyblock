
import mss.tools
import numpy as np
import time
from pathlib import Path
from threading import Thread
import melody_harp_state as mhs
from collections import deque
import pyautogui as pag
import ctypes

print('hello')

def capture_screen(capture):
    i=0
    while True:
        with mss.mss() as sct:
            if capture.value:
                i+=1
                sct_img = sct.grab(mhs.box)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=Path.cwd() / f'captures/img{i:05d}.png')



def write_file(write_queue):
    with open('./captures/play_harp.csv','w') as f:
        while True:
            if not write_queue.empty():
                status = write_queue.get()
                f.write(status)
                # print(status, end='')
        f.flush()

def click():
    click_idx_copy = deque(mhs.click_idx_deque)

    with mss.mss() as sct:
        while click_idx_copy:
            print(len(click_idx_copy))
            idx = click_idx_copy.popleft()
            clicked = False
            loc = mhs.check_loc[idx]
            pag.moveTo(mhs.click_loc[idx], 488)
            while not clicked:
                sct_img = sct.grab(mhs.box)
                img = np.array(sct_img)
                bright = np.mean(img[4:mhs.size,loc-mhs.size//2:loc+mhs.size//2,:3])
                if bright>230:
                    pag.leftClick(mhs.click_loc[idx], 488)
                    clicked = True


def learn(write_queue):

    with mss.mss() as sct:
        bright = np.empty([mhs.check_loc.size, 3])
        old_bright = np.empty_like(bright)
        sct_img = sct.grab(mhs.box)

        img = np.array(sct_img)
        for idx, loc in enumerate(mhs.check_loc):
            old_bright[idx] = np.mean(img[30:30+mhs.size,loc:loc+mhs.size,:3],axis=(0,1))
        while True:
            if not mhs.learning:
                break
            sct_img = sct.grab(mhs.box)
            img = np.array(sct_img)
            mhs.n_frames=mhs.n_frames+1
            for idx, loc in enumerate(mhs.check_loc):
                bright[idx, :] = np.mean(img[30:30+mhs.size,loc-mhs.size//2:loc+mhs.size//2,:3],axis=(0,1))
                change = np.sum(bright[idx,:] - old_bright[idx,:])
                if change > 100.:
                    mhs.click_idx_deque.append(idx)
                old_bright[idx,:] = np.copy(bright[idx,:])


import sneakysnek
from sneakysnek.recorder import Recorder
from sneakysnek.keyboard_event import KeyboardEvents as KE
from sneakysnek.keyboard_keys import KeyboardKey as KK

def user_action_process(write_queue, capture):
    mhs.stop = False
    mhs.ctrl = False
    capture = capture

    def user_action(arg):
        if not(isinstance(arg, sneakysnek.keyboard_event.KeyboardEvent)):
            return
        if ((arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_LEFT_CTRL)):
            mhs.ctrl=True
            return
        if ((arg.event == KE.UP) and (arg.keyboard_key == KK.KEY_LEFT_CTRL)):
            mhs.ctrl=False
            return
        if mhs.ctrl:
            if (arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_R):
                mhs.click_idx_deque=deque()
                print('Cleared Learned Pattern')
            if (arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_L):
                if not mhs.learning:
                    print('Learning')
                    mhs.learning=True
                    Thread(target=learn, args=(write_queue,)).start()
                else:
                    print('Learning Stopped')
                    mhs.learning=False
                    print(list(mhs.click_idx_deque))

            if (arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_N):
                if len(mhs.click_idx_deque)>1:
                    capture.value = True
                    Thread(target=click).start()

            if (arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_S):
                mhs.stop=True


    recorder = Recorder.record(user_action)
    print('Ready')

    while not mhs.stop:
        pass
    return


def main():
    (Path.cwd()/'captures').mkdir(parents=True, exist_ok=True)
    mhs.capture = mhs.ctx.Value(ctypes.c_bool,False)
    mhs.write_queue = mhs.ctx.SimpleQueue()
    user_action_proc = mhs.ctx.Process(target=user_action_process, args=(mhs.write_queue,mhs.capture), daemon=True)
    user_action_proc.start()
    mhs.ctx.Process(target=write_file, args=(mhs.write_queue,), daemon=True).start()
    mhs.ctx.Process(target=capture_screen, args=(mhs.capture,), daemon=True).start()

    user_action_proc.join()
    mhs.capture=False


if __name__ == '__main__':
    main()