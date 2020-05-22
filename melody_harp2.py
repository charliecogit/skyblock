import mss
import mss.tools
import numpy as np
import time
from pathlib import Path
import melody_harp_state as mhs
import pyautogui as pag
import ctypes
import multiprocessing as mp



def capture_screen(capture):
    i=0
    while True:
        if not capture.value:
            break
        with mss.mss() as sct:
            i+=1
            sct_img = sct.grab(mhs.box)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=Path.cwd() / f'captures/img{i:05d}.png')

def write_file(writing, write_queue):
    i=0
    with open('./captures/play_harp.csv','w') as f:
        while True:
            if not writing.value:
                break
            if not write_queue.empty():
                i+=1
                img = f'{i}, ' + np.array2string(write_queue.get(), max_line_width=300, separator=',')[1:-1] + '\n'
                f.write(img)
                # print(img, end='')
        f.flush()

def click(click_queue):
    while True:
        if not click_queue.empty():
            idx, t = click_queue.get()
            print(f'click {idx}')
            pag.moveTo(mhs.box['left']+mhs.size*idx, 488)
            while time.time()<t:
                pass
            pag.leftClick(mhs.box['left']+mhs.size*idx, 488)


def detect(click_queue, write_queue, detect_flag):
    with mss.mss() as sct:
        while True:
            if not detect_flag.value:
                pass
            else:
                sct_img = sct.grab(mhs.box)
                img = np.array(sct_img)[0,0::mhs.size,0]
                dark = img<50
                click_array = np.logical_and(dark, np.logical_not(mhs.filled))
                idx = np.argmax(click_array)
                if click_array[idx]:
                    click_queue.put((idx, time.time()+mhs.wait_time))
                    mhs.filled[idx]=True
                bright = img>90
                mhs.filled[bright]=False
                write_queue.put(img)



import sneakysnek
from sneakysnek.recorder import Recorder
from sneakysnek.keyboard_event import KeyboardEvents as KE
from sneakysnek.keyboard_keys import KeyboardKey as KK

def user_action_process(detect_flag):
    mhs.stop = False
    mhs.ctrl = False
    mhs.detecting = detect_flag

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
            if (arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_N):
                if not mhs.detecting.value:
                    print('detecting')
                    mhs.detecting.value = True
                else:
                    mhs.detecting.value = False

            if (arg.event == KE.DOWN) and (arg.keyboard_key == KK.KEY_S):
                mhs.stop=True


    recorder = Recorder.record(user_action)
    print('Ready')

    while not mhs.stop:
        pass
    return


def main():
    (Path.cwd()/'captures').mkdir(parents=True, exist_ok=True)
    ctx = mp.get_context('spawn')
    write_queue = ctx.SimpleQueue()
    click_queue = ctx.Queue()
    detecting = ctx.Value(ctypes.c_bool,False)
    writing = ctx.Value(ctypes.c_bool,True)
    user_action_proc = ctx.Process(target=user_action_process, args=(detecting,), daemon=True)
    user_action_proc.start()

    ctx.Process(target=detect, args=(click_queue, write_queue, detecting), daemon=True).start()
    ctx.Process(target=click, args=(click_queue,), daemon=True).start()
    write_proc= ctx.Process(target=write_file, args=(writing, write_queue,), daemon=True)
    write_proc.start()

    user_action_proc.join()
    writing.value = False
    write_proc.join()
    return


if __name__ == '__main__':
    main()