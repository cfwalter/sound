#!/usr/bin/env python3
import curses
import random

import pyaudio

from wave import wave

PyAudio = pyaudio.PyAudio

BITRATE = 2 ** 14 #number of frames per second/frameset.

NOTES = ['A','A♯','B','C','C♯','D','D♯','E','F','F♯','G','G♯',]
note = 0
STEP = 2 ** (1/12) #Twelve steps to an octave
LENGTH = 1 / 16.0 #seconds to play sound

MAX_VOLUME = 127.0
volume_step = 20

TARGET_FRAMES = BITRATE * 5.0 # the ball takes 1 second to traverse the court
target_position = 0
target_frequency = 440.0 * STEP ** random.randint(-12,12) # within 1 octave of A_4


score = 0

health_tones = [
    440.0 * STEP ** 0,
    440.0 * STEP ** 2,
    440.0 * STEP ** 4,
    440.0 * STEP ** 9,
    440.0 * STEP ** 11,
]

health = len(health_tones)

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

        frequency = 440.0 * STEP ** note
        volume = volume_step * (MAX_VOLUME / 20)

        stdscr.addstr(1, 2, NOTES[note % 12] + ' ' * 80)
        stdscr.addstr(3, 2, str(score) + ' points')
        stdscr.addstr(4, 2, str(health) + ' health')

        stdscr.move(10,2)

        periods = int(frequency * LENGTH) # number of whole periods in the LENGTH
        interval = periods / frequency
        frames = int(BITRATE * interval) * 2

        if target_position >= TARGET_FRAMES:
            if frequency >= target_frequency / STEP and frequency <= target_frequency * STEP:
                score += 1
                wave_bytes, target_position = wave(
                    frames=frames, left=[frequency], right=[target_frequency],
                    position=target_position, max_position=TARGET_FRAMES, volume=MAX_VOLUME,
                    bitrate=BITRATE)
            else:
                health -= 1
                wave_bytes, target_position = wave(
                    frames=frames, left=health_tones[:health], right=health_tones[:health],
                    position=1, max_position=1, volume=MAX_VOLUME,
                    bitrate=BITRATE)
            target_frequency = 440.0 * STEP ** random.randint(-12,12) # within 1 octave of A_4
            target_position = 0

        else:
            wave_bytes, target_position = wave(
                    frames=frames, left=[frequency], right=[target_frequency],
                    position=target_position, max_position=TARGET_FRAMES, volume=MAX_VOLUME,
                    bitrate=BITRATE)

        stream.write(bytes(wave_bytes))
        if health <= 0:
            break

    except Exception as e:
        key = ord('q')
        error_message = e

stream.stop_stream()
stream.close()
p.terminate()

curses.endwin()

if error_message:
    print(error_message)
