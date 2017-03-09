import math
import numpy
import pyaudio

"""Note table

Key: Note  Value: # of half steps

"""
NOTES_TABLE = {'Bb': 1, 'B': 2,
               'C': 3, 'C#': 4,
               'D': 5, 'Eb': 6,
               'E': 7, 'F': 8,
               'F#': 9, 'G': 10,
               'Ab': 11}

BASE_FREQ = 440

def get_note(note, base_freq=BASE_FREQ):
    """
    Formula:

    frequency = 440 * 2^(n/12)

    :param note: Which note to return
    :param base_freq: 440 is A
    :return:
    """


    octave = 1

    if '-' in note:
        i = note.split('-')
        note = i[0]

        if i[1][0].lower() == 'u':
            octave = int(i[1][1])

        if i[1][0].lower() == 'd':
            octave = int(i[1][1]) * -1


    if note is 'A':
        freq = 440 * octave
    else:
        freq = (base_freq * math.pow(2, NOTES_TABLE[note] / 12)) * octave

    return [freq, note]

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequency=BASE_FREQ, length=1, rate=44100):
    chunks = []
    chunks.append(sine(frequency, length, rate))

    chunk = numpy.concatenate(chunks) * 0.25

    stream.write(chunk.astype(numpy.float32).tostring())


if __name__ == '__main__':
    p = pyaudio.PyAudio()

    RATE = 44100

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=RATE, output=1)

    note_list = (input('Enter some notes: ')).split(' ')

    for note in note_list:
        data = get_note(note)
        print('Note: ' + data[1] + " Frequency: " + str(data[0]))
        play_tone(stream, frequency=data[0])

    stream.close()
    p.terminate()