from sneakysnek.recorder import Recorder
from sneakysnek.keyboard_keys import KeyboardKey
from sneakysnek.mouse_buttons import MouseButton
from sneakysnek.keyboard_event import KeyboardEvent, KeyboardEvents
from sneakysnek.mouse_event import MouseEvent, MouseEvents


def respond_to_input(arg):
    if isinstance(arg, KeyboardEvent):
        print(f'{arg.event.value} {arg.keyboard_key.value}')
    else:
        if arg.event.value == 'CLICK':
            print(f'{arg.button.value} {arg.direction} {arg.x}, {arg.y}')
        elif arg.event.value == 'MOVE':
            print(f'Location: {arg.x}, {arg.y}')



recorder = Recorder.record(respond_to_input)

while True:
    pass