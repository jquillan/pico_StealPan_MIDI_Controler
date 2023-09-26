# Test Reading


import board
import digitalio


# PIN | MIDI_NOTE | Pin Object | tick of last hit
PIN_MIDI_MAP =  [
    [ board.GP0, 0 , None, 0],
    [ board.GP1, 1 , None, 0],
    [ board.GP2, 2 , None, 0],
    [ board.GP3,3 , None, 0],
    [ board.GP4,4 , None, 0],
    [ board.GP5,5 , None, 0],
    [ board.GP6,6 , None, 0],
    [ board.GP7,7 , None, 0],
    [ board.GP8,8 , None, 0],
    [ board.GP9,9 , None, 0],
    [ board.GP10,10 , None, 0],
    [ board.GP11,11 , None, 0],
    [ board.GP12,12 , None, 0],
    [ board.GP13,13 , None, 0],
    [ board.GP14,14 , None, 0],
    [ board.GP15,15 , None, 0],
    [ board.GP16,16 , None, 0],
    [ board.GP17,17 , None, 0],
    [ board.GP18,18 , None, 0],
    [ board.GP19,19 , None, 0],
    [ board.GP20,20 , None, 0],
    [ board.GP21,21 , None, 0],
    [ board.GP22,22 , None, 0],
    [ board.GP23,23 , None, 0],
    [ board.GP24,224 , None, 0],
    [ board.GP25,25 , None, 0],
    [ board.GP26,26 , None, 0],
    [ board.GP27,27 , None, 0],
    [ board.GP28,28 , None, 0],
]



#Initialize Pins
for indx in range(0,len(PIN_MIDI_MAP)):
    p           = digitalio.DigitalInOut(PIN_MIDI_MAP[indx][0])
    p.direction = digitalio.Direction.INPUT
    p.pull      = digitalio.Pull.UP

    PIN_MIDI_MAP[indx][2] = p

while True:
    for indx in range(0,  len(PIN_MIDI_MAP)):
        p = PIN_MIDI_MAP[indx][2]
        if p.value == 0:
            print("pin hit " + str(PIN_MIDI_MAP[indx][1]))
