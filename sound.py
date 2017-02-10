import math
import curses
import os

import pyaudio

PyAudio = pyaudio.PyAudio

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 16000 #number of frames per second/frameset.

frequency = 512 #Hz, waves per second, 261.63=C4-note.
NOTE = 2 ** (1/12)
LENGTH = .125 #seconds to play sound

volume = 64
MAX_VOLUME = 127.0

if frequency > BITRATE:
    BITRATE = frequency+100

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''

# for i in range(NUMBEROFFRAMES):
#     WAVEDATA = WAVEDATA + chr( int( math.sin( i/( (BITRATE/frequency)/math.pi ) ) * 127+128))

# for i in range(RESTFRAMES):
#     WAVEDATA = WAVEDATA + chr(128)

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
b = True
counter = 0
while key != ord('q'):
    try:
        counter += 1
        # if (counter % 8 == 0):
        #     b = not b
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
            volume += 10
            if (volume > MAX_VOLUME):
                volume = MAX_VOLUME

        stdscr.addstr(1, 2, str.format('{0:.2f}', frequency) + ' ' * 80)
        # stdscr.addstr(1, 2, str(BITRATE) + ' ' * 80)
        stdscr.addstr(2, 2, str(int(100*(volume/MAX_VOLUME))) + '%' + ' ' * 80)
        if(b):
            stdscr.addstr(3, 2, 'bytes ')
        else:
            stdscr.addstr(3, 2, 'string')
        stdscr.move(4,2)

        WAVEDATA = ''
        wave_bytes = bytearray()
        for i in range(NUMBEROFFRAMES):
            t = i/( (BITRATE/frequency)/math.pi )
            wave = math.sin(t)
            WAVEDATA += chr( int( wave * volume + 128))
            wave_bytes.append( int( wave * volume + 128) )
            # WAVEDATA = WAVEDATA + chr( int( math.sin( i/( (BITRATE/frequency)/math.pi ) ) * 127+128))

        if(b):
            stream.write(bytes(wave_bytes))
        else:
            stream.write(WAVEDATA)
    except Exception as e:
        key = ord('q')
        error_message = e

stream.stop_stream()
stream.close()
p.terminate()

curses.endwin()

if error_message:
    print(error_message)
