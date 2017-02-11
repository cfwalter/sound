from math import sin, pi

def wave(frames, left, right, position, max_position, volume, bitrate):
    wave_bytes = bytearray()
    for i in range(frames):
        if position < max_position:
            position += 1

        wave = 0.0
        for frequency in left:
            t = i / ( (bitrate/frequency)/pi )
            # t = 0
            wave += sin(t)
        wave = wave / len(left)
        wave_bytes.append( int( wave * volume + 128) )

        wave = 0.0
        percent = position / max_position
        for frequency in right:
            t = i / ( (bitrate/frequency)/pi )
            wave += sin(t)
        wave = wave / len(right)
        wave_bytes.append( int( wave * percent * volume + 128) )

    return wave_bytes, position
