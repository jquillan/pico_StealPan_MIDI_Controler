# Test Reading

import usb_midi
import board
import digitalio
import adafruit_midi

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

import time

# PIN | MIDI_NOTE | Pin Object | tick of last hit | last state
PIN_MIDI_MAP =  [
    [ board.GP0,     0 , None, 0, 1],
    [ board.GP1,     1 , None, 0, 1],
    [ board.GP2,     2 , None, 0, 1],
    [ board.GP3,     3 , None, 0, 1],
    [ board.GP4,     4 , None, 0, 1],
    [ board.GP5,     5 , None, 0, 1],
    [ board.GP6,     6 , None, 0, 1],
    [ board.GP7,     7 , None, 0, 1],
    [ board.GP8,     8 , None, 0, 1],
    [ board.GP9,     9 , None, 0, 1],
    [ board.GP10,   10 , None, 0, 1],
    [ board.GP11,   11 , None, 0, 1],
    [ board.GP12,   12 , None, 0, 1],
    [ board.GP13,   13 , None, 0, 1],
    [ board.GP14,   14 , None, 0, 1],
    [ board.GP15,   15 , None, 0, 1],
    [ board.GP16,   84 , None, 0, 1],
    [ board.GP17,   91 , None, 0, 1],
    [ board.GP18,   18 , None, 0, 1],
    [ board.GP19,   19 , None, 0, 1],
    [ board.GP20,   20 , None, 0, 1],
    [ board.GP21,   21 , None, 0, 1],
    [ board.GP22,   22 , None, 0, 1],
    [ board.GP23,   23 , None, 0, 1],
    [ board.GP24,   22 , None, 0, 1],
    [ board.GP25,   25 , None, 0, 1],
    [ board.GP26,   26 , None, 0, 1],
    [ board.GP27,   27 , None, 0, 1],
    [ board.GP28,   28 , None, 0, 1],
]

m = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=1)

#Initialize Pins
for indx in range(0,len(PIN_MIDI_MAP)):
    p           = digitalio.DigitalInOut(PIN_MIDI_MAP[indx][0])
    p.direction = digitalio.Direction.INPUT
    p.pull      = digitalio.Pull.UP

    PIN_MIDI_MAP[indx][2] = p

while True:
    for indx in range(0,  len(PIN_MIDI_MAP)):
        p = PIN_MIDI_MAP[indx][2]
        tic = PIN_MIDI_MAP[indx][3]
        now_tick = time.monotonic_ns()
        state = p.value
        last_state = PIN_MIDI_MAP[indx][4]
        midi_note = PIN_MIDI_MAP[indx][1]
        if state == 0 and now_tick > tic and last_state == 1:

            print("pin hit " + str(midi_note))
            PIN_MIDI_MAP[indx][3] = now_tick + 8000000 # 40ms later
            if midi_note > 28:
                # Send midi message3
                print("Sending midi")
                m.send(NoteOn(midi_note, 60))

        if state == 1 and now_tick > tic:
            if midi_note > 28:
                # Send midi message3
                print("Sending midi off")
                m.send(NoteOff(midi_note, 60))
            PIN_MIDI_MAP[indx][3] = now_tick + 8000000 # 40ms later

        PIN_MIDI_MAP[indx][4] = state
