from collections import deque
import numpy as np

filled = np.array([False]*7)
ctrl = False
stop = False

monitor_number = 1

size = 54
box = {
    "top": 414,
    "left": 784,
    "width": size*6+1,
    "height": 1,
    "mon": monitor_number,
}
n_frames=0


detecting = False
write_file_proc = None

click_queue = None
wait_time = 0.2

capture = None

