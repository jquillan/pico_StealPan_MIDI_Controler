
#include <stdio.h>
#include <pico/stdlib.h>

//# PIN | MIDI_NOTE | Pin Object | tick of last hit | state
typedef enum {
    IDLE,
    HIT_DETECTED,
    DEBOUNCED
} smstate;


typedef struct {
    uint     pin_no;
    int      midi_note;
    uint64_t last_tickhit;
    smstate  state;
} note_map_t;

note_map_t PIN_MIDI_MAP[] = {
    { 0,     0 ,  0, IDLE},
    { 1,     1 ,  0, IDLE},
    { 2,     2 ,  0, IDLE},
    { 3,     3 ,  0, IDLE},
    { 4,     4 ,  0, IDLE},
    { 5,     5 ,  0, IDLE},
    { 6,     6 ,  0, IDLE},
    { 7,     7 ,  0, IDLE},
    { 8,     8 ,  0, IDLE},
    { 9,     9 ,  0, IDLE},
    { 10,   10 ,  0, IDLE},
    { 11,   11 ,  0, IDLE},
    { 12,   12 ,  0, IDLE},
    { 13,   0 ,   0, IDLE},
    { 14,   67 ,  0, IDLE},
    { 15,   64 ,  0, IDLE},
    { 16,   60 ,  0, IDLE},
    { 17,   69 ,  0, IDLE},
    { 18,   18 ,  0, IDLE},
    { 19,   19 ,  0, IDLE},
    { 20,   20 ,  0, IDLE},
    { 21,   21 ,  0, IDLE},
    { 22,   22 ,  0, IDLE},
    { 23,   23 ,  0, IDLE},
    { 24,   22 ,  0, IDLE},
    { 25,   25 ,  0, IDLE},
    { 26,   26 ,  0, IDLE},
    { 27,   27 ,  0, IDLE},
    { 28,   28 ,  0, IDLE},
};

// 40 microseconds
uint64_t DEBOUNCE_TIME = 40*1000;

int main()
{
    stdio_init_all();

    // Initialize pins
    for(int x = 0; x < sizeof(PIN_MIDI_MAP)/sizeof(PIN_MIDI_MAP[0]); x++) {
        note_map_t* nmt = &PIN_MIDI_MAP[x];
        gpio_set_dir(nmt->pin_no, GPIO_IN);
        gpio_pull_up(nmt->pin_no);

    }


    while (true) {

        for(int x = 0; x < sizeof(PIN_MIDI_MAP)/sizeof(PIN_MIDI_MAP[0]); x++) {

            note_map_t* nmt = &PIN_MIDI_MAP[x];
            uint64_t now_tick= time_us_64 ();

            switch(nmt->state) {
            case IDLE:

                if(! gpio_get(nmt->pin_no)) {
                    nmt->state = HIT_DETECTED;
                    nmt->last_tickhit = now_tick + DEBOUNCE_TIME;
                    printf("Midi On %d\n", nmt->midi_note);
                    // * SEND MIDI NOTE ON
                }
               break;
            case HIT_DETECTED:
                    if( now_tick > nmt->last_tickhit) {
                        nmt->state = DEBOUNCED;
                    }
                break;
            case DEBOUNCED:
                if(gpio_get(nmt->pin_no)) {
                    nmt->state = IDLE;
                    printf("Midi Off %d\n", nmt->midi_note);
                    // SEND MIDI NOTE OFF
                }
                break;
            }
        }
    }
}
