from collections import deque
import numpy as np

check_loc = np.array([ 33,  87, 141, 196, 249, 303, 357], dtype=np.int32)
click_loc = check_loc + 764
filled = np.array([False]*check_loc.size)
ctrl = False
stop = False


monitor_number = 1

size = 6
box = {
    "top": 470,
    "left": 764,
    "width": 373,
    "height": 50,
    "mon": monitor_number,
}
n_frames=0

write_queue = None
writing = None

learning = False
write_file_proc = None

click_idx_deque = deque()

capture = None

import multiprocessing as mp
ctx = mp.get_context('spawn')
