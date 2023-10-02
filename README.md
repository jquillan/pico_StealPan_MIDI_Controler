# Project Title

A Steel Drum/Pan MIDI controller using the Pi Pico.

## Description

A MIDI controler to create a steelpan MIDI controller that was easy
and accessable. Because of this goal it lacks various features like
velocity sensitivity.

See https://youtu.be/ORB1h8npleA for demo of the prototype

## Getting Started

## History

I got this idea while playing in a parent steal drum band. Not owning a pan myself I was wondering how I could practice. Knowing I had the pico, and CircuitPython, this idea was born.

Turns out CircuitPython was not fast enough (or at least my implementation in python) as there was a noticeable delay between when the pad was hit and my computer would play the MIDI note. so I ported the code to C and the pico SDK, and here we are today.

The prototype folder contains the original CircuitPython implementation.

### Dependencies

You will need to build some sort of controller. The one I used consist of
* Mallets with a metal head (I used a ball of foil) that connect to the ground of the pico
* A sheet of cardboard with pads of foil, of which each is connected to one of the GPIO pins

### Installing

* Copy the uf2 file to the pi pico when it is in boot mode


## Version History

None yet.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

FWIW, it is really nothing special.

