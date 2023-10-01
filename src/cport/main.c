
#include <stdio.h>
#include <pico/stdlib.h>
#include "hardware/gpio.h"
#include "pico/binary_info.h"
#include "pico/util/queue.h"
#include "pico/multicore.h"

#include "bsp/board.h"

#include "tusb.h"

typedef enum {
    IDLE,
    HIT_DETECTED,
    DEBOUNCED,
    UP_DETECTED,
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

// 100 mils
uint64_t DOWN_DEBOUNCE_TIME = 100*1000;
// 10 mils
uint64_t UP_DEBOUNCE_TIME = 10*1000;

// START From pico-example-midi.c
enum  {
  BLINK_NOT_MOUNTED = 250,
  BLINK_MOUNTED = 1000,
  BLINK_SUSPENDED = 2500,
};


static uint32_t blink_interval_ms = BLINK_NOT_MOUNTED;
const uint LED_PIN = PICO_DEFAULT_LED_PIN;

// Invoked when device is mounted
void tud_mount_cb(void)
{
  blink_interval_ms = BLINK_MOUNTED;
}

// Invoked when device is unmounted
void tud_umount_cb(void)
{
  blink_interval_ms = BLINK_NOT_MOUNTED;
}

// END pico-example-midi.c

void led_blinking_task(void);


void note_onoff(uint note_no, bool onoff)
{


    // TODO: Fix channel here
    uint8_t msg[3];

    // Send Note On for current position at full velocity (127) on channel 1.
    if(onoff) {
        msg[0] = 0x90;                    // Note On - Channel 1
        msg[2] = 64;                     // Velocity
    }
    else {
        msg[0] = 0x80;                    // Note Off - Channel 1
        msg[2] = 0;                     // Velocity
    }
    msg[1] = note_no;

    tud_midi_stream_write(0, msg, 3);
}

typedef struct
{
    int32_t midi_note;
    bool    onoff;
} queue_entry_t;

queue_t midi_queue;

void gpio_read_tasks()
{
   while (true) {

        // Loop through all of the pins looking for state changes
        for(int x = 0; x < sizeof(PIN_MIDI_MAP)/sizeof(PIN_MIDI_MAP[0]); x++) {

            note_map_t* nmt = &PIN_MIDI_MAP[x];
            uint64_t now_tick= time_us_64 ();

            switch(nmt->state) {
            case IDLE:

                if(! gpio_get(nmt->pin_no)) {
                    nmt->state = HIT_DETECTED;
                    nmt->last_tickhit = now_tick + DOWN_DEBOUNCE_TIME;
                    printf("Midi On %d\n", nmt->midi_note);

                    queue_entry_t entry = { nmt->midi_note, true};
                    queue_try_add(&midi_queue, &entry);
                }
               break;
            case HIT_DETECTED:
                    if( now_tick > nmt->last_tickhit) {
                        nmt->state = DEBOUNCED;
                    }
                break;
            case DEBOUNCED:
                if(gpio_get(nmt->pin_no)) {
                    nmt->last_tickhit = now_tick + UP_DEBOUNCE_TIME;
                    nmt->state = UP_DETECTED;
                    printf("Midi Off %d\n", nmt->midi_note);
                    // SEND MIDI NOTE OFF
                    queue_entry_t entry = { nmt->midi_note, false};
                    queue_try_add(&midi_queue, &entry);
                }
                break;
            case UP_DETECTED:
                    if( now_tick > nmt->last_tickhit) {
                        nmt->state = IDLE;
                    }
                break;
            }
        }
    }

}

int main()
{
    stdio_init_all();

    board_init();
    tusb_init();

    queue_init(&midi_queue, sizeof(queue_entry_t), 4);

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    // Initialize pins
    for(int x = 0; x < sizeof(PIN_MIDI_MAP)/sizeof(PIN_MIDI_MAP[0]); x++) {
        note_map_t* nmt = &PIN_MIDI_MAP[x];
        gpio_set_dir(nmt->pin_no, GPIO_IN);
        gpio_pull_up(nmt->pin_no);
    }

    multicore_launch_core1(gpio_read_tasks);

    queue_entry_t entry;
    // Main Loop
    while (true) {

        tud_task();
        //led_blinking_task();

        while(queue_try_remove(&midi_queue, &entry)) {
            note_onoff(entry.midi_note, entry.onoff);
        }
    }
}

//--------------------------------------------------------------------+
// BLINKING TASK
//--------------------------------------------------------------------+
void led_blinking_task(void)
{
  static uint32_t start_ms = 0;
  static bool led_state = false;

  // Blink every interval ms
  if ( board_millis() - start_ms < blink_interval_ms) return; // not enough time
  start_ms += blink_interval_ms;

  gpio_put(LED_PIN, led_state);
  led_state = !led_state; // toggle
}
