#!/usr/bin/env python3
from math import sin, pi
import curses
import random

import pyaudio

PyAudio = pyaudio.PyAudio

BITRATE = 2 ** 14 #number of frames per second/frameset.

note = 0
STEP = 2 ** (1/12) #Twelve steps to an octave
LENGTH = .125 #seconds to play sound

MAX_VOLUME = 127.0
volume_step = 10

answer_frequency = 440.0 * STEP ** random.randint(-24,24) # within 2 octaves of A_4
answer_volume = random.randint(0,20) * (MAX_VOLUME / 20)

key = ''
error_message = ''
p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 2,
                rate = BITRATE,
                output = True)

stdscr = curses.initscr()
curses.cbreak()
curses.curs_set(0)
stdscr.keypad(1)
stdscr.nodelay(1)

stdscr.addstr(0,0,"Hit 'q' to quit")
stdscr.refresh()

while key != ord('q'):
    try:
        key = stdscr.getch()
        stdscr.refresh()

        if key == curses.KEY_UP:
            note += 1
        elif key == curses.KEY_DOWN:
            note -= 1
        elif key == curses.KEY_LEFT:
            volume_step -= 1
            if (volume_step < 0):
                volume_step = 0
        elif key == curses.KEY_RIGHT:
            volume_step += 1
            if (volume_step > 20):
                volume_step = 20

        frequency = 440.0 * STEP ** note
        volume = volume_step * (MAX_VOLUME / 20)

        stdscr.addstr(1, 2, str.format('{0:.2f} Hz', frequency) + ' ' * 80)
        stdscr.addstr(2, 2, str(int(100*(volume/MAX_VOLUME) + 0.5)) + '%' + ' ' * 80)

        # stdscr.addstr(4, 2, str.format('{0:.2f} Hz', answer_frequency) + ' ' * 80)
        # stdscr.addstr(5, 2, str(int(100*(answer_volume/MAX_VOLUME) + 0.5)) + '%' + ' ' * 80)

        if frequency == answer_frequency:
            stdscr.addstr(1, 0, '*')
            # stdscr.addstr(7, 0, ' ' * 80)
        else:
            stdscr.addstr(1, 0, ' ')
            # stdscr.addstr(7, 0, str(answer_frequency - frequency) + ' ' * 80)

        if volume == answer_volume:
            stdscr.addstr(2, 0, '*')
            # stdscr.addstr(8, 0, ' ' * 80)
        else:
            stdscr.addstr(2, 0, ' ')
            # stdscr.addstr(8, 0, str(answer_volume - volume) + ' ' * 80)

        stdscr.move(10,2)

        periods = int(frequency * LENGTH) # number of whole periods in the LENGTH
        interval = periods / frequency
        frames = int(BITRATE * interval) * 2

        wave_bytes = bytearray()
        for i in range(frames):
            t = i / ( (BITRATE/frequency)/pi )
            wave = sin(t)
            wave_bytes.append( int( wave * volume + 128) )

            t = i / ( (BITRATE/answer_frequency)/pi )
            wave = sin(t)
            wave_bytes.append( int( wave * answer_volume + 128) )

        stream.write(bytes(wave_bytes))

    except Exception as e:
        key = ord('q')
        error_message = e

stream.stop_stream()
stream.close()
p.terminate()

curses.endwin()

if error_message:
    print(error_message)
