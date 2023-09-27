# Test Reading

import usb_midi
import board
import digitalio
import adafruit_midi

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

import time

class SM(object):
    IDLE         = 1
    HIT_DETECTED = 2
    DEBOUNCED    = 3


# PIN | MIDI_NOTE | Pin Object | tick of last hit | state
PIN_MIDI_MAP =  [
    [ board.GP0,     0 , None, 0, SM.IDLE],
    [ board.GP1,     1 , None, 0, SM.IDLE],
    [ board.GP2,     2 , None, 0, SM.IDLE],
    [ board.GP3,     3 , None, 0, SM.IDLE],
    [ board.GP4,     4 , None, 0, SM.IDLE],
    [ board.GP5,     5 , None, 0, SM.IDLE],
    [ board.GP6,     6 , None, 0, SM.IDLE],
    [ board.GP7,     7 , None, 0, SM.IDLE],
    [ board.GP8,     8 , None, 0, SM.IDLE],
    [ board.GP9,     9 , None, 0, SM.IDLE],
    [ board.GP10,   10 , None, 0, SM.IDLE],
    [ board.GP11,   11 , None, 0, SM.IDLE],
    [ board.GP12,   12 , None, 0, SM.IDLE],
    [ board.GP13,   0 , None, 0, SM.IDLE],
    [ board.GP14,   67 , None, 0, SM.IDLE],
    [ board.GP15,   64 , None, 0, SM.IDLE],
    [ board.GP16,   60 , None, 0, SM.IDLE],
    [ board.GP17,   69 , None, 0, SM.IDLE],
    [ board.GP18,   18 , None, 0, SM.IDLE],
    [ board.GP19,   19 , None, 0, SM.IDLE],
    [ board.GP20,   20 , None, 0, SM.IDLE],
    [ board.GP21,   21 , None, 0, SM.IDLE],
    [ board.GP22,   22 , None, 0, SM.IDLE],
    [ board.GP23,   23 , None, 0, SM.IDLE],
    [ board.GP24,   22 , None, 0, SM.IDLE],
    [ board.GP25,   25 , None, 0, SM.IDLE],
    [ board.GP26,   26 , None, 0, SM.IDLE],
    [ board.GP27,   27 , None, 0, SM.IDLE],
    [ board.GP28,   28 , None, 0, SM.IDLE],
]

m = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=1)

DEBOUNCE_TIME = 40*1000*1000 # 40 microseconds

#Initialize Pins
for indx in range(0,len(PIN_MIDI_MAP)):
    p           = digitalio.DigitalInOut(PIN_MIDI_MAP[indx][0])
    p.direction = digitalio.Direction.INPUT
    p.pull      = digitalio.Pull.UP

    PIN_MIDI_MAP[indx][2] = p

while True:
    for indx in range(0,  len(PIN_MIDI_MAP)):

        pin           = PIN_MIDI_MAP[indx][2]
        tic           = PIN_MIDI_MAP[indx][3]
        now_tick      = time.monotonic_ns()
        current_state = PIN_MIDI_MAP[indx][4]
        midi_note     = PIN_MIDI_MAP[indx][1]

        if current_state == SM.IDLE:
            # Waiting for Hit
            if pin.value == 0:
                PIN_MIDI_MAP[indx][4] = SM.HIT_DETECTED
                PIN_MIDI_MAP[indx][3] = now_tick + DEBOUNCE_TIME
                print("Sending midi on" +str(midi_note))
                m.send(NoteOn(midi_note, 60))

        elif current_state == SM.HIT_DETECTED:
            # Now lets debounc the hit
            if now_tick > tic:
                PIN_MIDI_MAP[indx][4] = SM.DEBOUNCED
        elif current_state == SM.DEBOUNCED:
            if pin.value == 1:
                PIN_MIDI_MAP[indx][4] = SM.IDLE
                print("Sending midi off" +str(midi_note))
                m.send(NoteOn(midi_note,0))

