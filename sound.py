import math
import curses
import os

import pyaudio

PyAudio = pyaudio.PyAudio

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
# BITRATE = 16000 #number of frames per second/frameset.
BITRATE = 2 ** 14 #number of frames per second/frameset.

frequency = 440 #Hz, waves per second, 440 = A_4
NOTE = 2 ** (1/12) #Twelve steps to an octave
LENGTH = .125 #seconds to play sound

MAX_VOLUME = 127.0
volume = 64

if frequency > BITRATE:
    BITRATE = frequency+100

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE

key = ''
error_message = ''
p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 2,
                rate = BITRATE,
                output = True)
os.system('clear')

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
            frequency = frequency * NOTE
        elif key == curses.KEY_DOWN:
            frequency = frequency / NOTE
        elif key == curses.KEY_LEFT:
            volume -= 10
            if (volume < 0):
                volume = 0
        elif key == curses.KEY_RIGHT:
            volume += MAX_VOLUME / 20
            if (volume > MAX_VOLUME):
                volume = MAX_VOLUME

        stdscr.addstr(1, 2, str.format('{0:.2f} Hz', frequency) + ' ' * 80)
        stdscr.addstr(2, 2, str(int(100*(volume/MAX_VOLUME))) + '%' + ' ' * 80)
        stdscr.move(4,2)

        wave_bytes = bytearray()
        for i in range(NUMBEROFFRAMES):
            t = i/( (BITRATE/frequency)/math.pi )
            wave = math.sin(t)
            wave_bytes.append( int( wave * volume + 128) )

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
