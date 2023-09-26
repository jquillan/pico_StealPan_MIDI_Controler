# Test Reading


import board
import digitalio


# PIN | MIDI_NOTE | Pin Object | tick of last hit
PIN_MIDI_MAP =  [
    [ board.GP0, 0 , None],
    [ board.GP1, 1 , None],
    [ board.GP2, 2 , None],
    [ board.GP3,3 , None],
    [ board.GP4,4 , None],
    [ board.GP5,5 , None],
    [ board.GP6,6 , None],
    [ board.GP7,7 , None],
    [ board.GP8,8 , None],
    [ board.GP9,9 , None],
    [ board.GP10,10 , None],
    [ board.GP11,11 , None],
    [ board.GP12,12 , None],
    [ board.GP13,13 , None],
    [ board.GP14,14 , None],
    [ board.GP15,15 , None],
    [ board.GP16,16 , None],
    [ board.GP17,17 , None],
    [ board.GP18,18 , None],
    [ board.GP19,19 , None],
    [ board.GP20,20 , None],
    [ board.GP21,21 , None],
    [ board.GP22,22 , None],
    [ board.GP23,23 , None],
    [ board.GP24,224 , None],
    [ board.GP25,25 , None],
    [ board.GP26,26 , None],
    [ board.GP27,27 , None],
    [ board.GP28,28 , None],
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
