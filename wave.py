from math import sin, pi

def wave(frames, left, right, position, max_position, volume, bitrate, time):
    wave_bytes = bytearray()
    for i in range(frames):
        t = time + i/bitrate
        if position < max_position:
            position += 1

        wave = 0.0
        for frequency in left:
            x = 2*pi * t * frequency
            wave += sin(x)
        wave = wave / len(left)
        wave_bytes.append( int( wave * volume + 128) )

        wave = 0.0
        percent = position / max_position
        for frequency in right:
            x = 2*pi * t * frequency
            wave += sin(x)
        wave = wave / len(right)
        wave_bytes.append( int( wave * percent * percent * volume + 128) )

    return wave_bytes, position, (time + frames / bitrate)
