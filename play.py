from tone import ToneGenerator
import time
import math

SAMPLE_RATE = 44100
FRAMES_PER_BUFFER = 4410

BASE = 440 #A4 at concert pitch

NOTE_MAP = {'A0': 1, 'A#0': 2, 'Bb0': 2, 'B0': 3,
            'C1': 4, 'C#1': 5, 'Db1': 5, 'D1': 6, 'D#1': 7, 'Eb1': 7, 'E1': 8, 'F1': 9, 'F#1': 10, 'Gb1': 10, 'G1': 11, 'G#1': 12, 'Ab1': 12, 'A1': 13, 'A#1': 14, 'Bb1': 14, 'B1': 15,
            'C2': 16, 'C#2': 17, 'Db2': 17, 'D2': 18, 'D#2': 19, 'Eb2': 19, 'E2': 20, 'F2': 21, 'F#2': 22, 'Gb2': 22, 'G2': 23, 'G#2': 24, 'Ab2': 24, 'A2': 25, 'A#2': 26, 'Bb2': 26, 'B2': 27,
            'C3': 28, 'C#3': 29, 'Db3': 29, 'D3': 30, 'D#3': 31, 'Eb3': 31, 'E3': 32, 'F3': 33, 'F#3': 34, 'Gb3': 34, 'G3': 35, 'G#3': 36, 'Ab3': 36, 'A3': 37, 'A#3': 38, 'Bb3': 38, 'B3': 39,
            'C4': 40, 'C#4': 41, 'Db4': 41, 'D4': 42, 'D#4': 43, 'Eb4': 43, 'E4': 44, 'F4': 45, 'F#4': 46, 'Gb4': 46, 'G4': 47, 'G#4': 48, 'Ab4': 48, 'A4': 49, 'A#4': 50, 'Bb4': 50, 'B4': 51,
            'C5': 52, 'C#5': 53, 'Db5': 53, 'D5': 54, 'D#5': 55, 'Eb5': 55, 'E5': 56, 'F5': 57, 'F#5': 58, 'Gb5': 58, 'G5': 59, 'G#5': 60, 'Ab5': 60, 'A5': 61, 'A#5': 62, 'Bb5': 62, 'B5': 63,
            'C6': 64, 'C#6': 65, 'Db6': 65, 'D6': 66, 'D#6': 67, 'Eb6': 67, 'E6': 68, 'F6': 69, 'F#6': 70, 'Gb6': 70, 'G6': 71, 'G#6': 72, 'Ab6': 72, 'A6': 73, 'A#6': 74, 'Bb6': 74, 'B6': 75,
            'C7': 76, 'C#7': 77, 'Db7': 77, 'D7': 78, 'D#7': 79, 'Eb7': 79, 'E7': 80, 'F7': 81, 'F#7': 82, 'Gb7': 82, 'G7': 83, 'G#7': 84, 'Ab7': 84, 'A7': 85, 'A#7': 86, 'Bb7': 86, 'B7': 87,
            'C8': 88}

def freq(note):
    """
    Formula:

    f(n) = 440 * 2^((n-49)/12)

    :param note: Note to get frequency of
    :return: Frequency of given note (Hz)
    """

    frequency = BASE * math.pow(2, ((note - 49) / 12))

    return frequency

def get_note(note):
    """
    Returns the given note, its frequency, and its piano key position
    :param note: Note to get
    :return: [given note, its frequency, piano key position]
    """
    return [note, freq(NOTE_MAP[note]), NOTE_MAP[note]]

def melody_mapper(notes):
    """
    Makes a map of a melody to be played

    each item in the list 'notes' should be formatted using these chars:

        duration - length in seconds the sound will be played
        note - the note to play
        sleep - time in seconds to pause

        (note, duration)

        example:
            [('A4', 1), ('C3', 0.5)]

    :param notes: List of notes
    :return: list of melody map info
    """

    m_map = {}

    num_of_notes = 1
    for note_info in notes:
        note, duration, sleep = note_info
        m_map[str(num_of_notes)] = {'note': note,
                                    'frequency': get_note(note)[1],
                                    'duration': duration,
                                    'sleep': sleep}
        num_of_notes += 1

    return m_map

def melody_maker():
    """
    Makes the melody from the user input
    And passes it to the melody_mapper()

    each item should have the formatting:

        d = duration
        n = note
        s = sleep time

    Example:

        n=A#3;d=0.5;s=0

    The note will be A#3 and will be played for a
    duration of 0.5 and have no pause before the
    next note

    :return: melody map
    """

    data = []

    t = True

    print("Begin making melody.")
    while t is True:
        n = input('Note, Duration, and Pause Time : ').split(' ')

        if n[0] != '':
            data.append('n={};d={};s={}'.format(n[0].upper(), n[1], n[2]))
        else:
            t = False

    notes = []

    for item in data:
        note = (item.split(';')[0]).split('=')[1]
        duration = (item.split(';')[1]).split('=')[1]
        sleep = (item.split(';')[2]).split('=')[1]
        notes.append((note, duration, sleep))



    return melody_mapper(notes)

def load_file(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    notes = []
    for item in lines:
        note = item.split(' ')[0]
        duration = item.split(' ')[1]
        sleep = item.split(' ')[2]
        notes.append((note, duration, sleep))

    return notes

def play_melody(m_map, amp=0.50):

    """
    Plays melody from m_map
    using ToneGenerator!

    :param m_map: melody_map()
    :param amp: amplitude of the sine wave
    :return:
    """


    sound = ToneGenerator(samplerate=SAMPLE_RATE, frames_per_buffer=FRAMES_PER_BUFFER)

    melody = {}

    for pos, val in m_map.items():
        if pos is 'total_rows':
            pass
        else:
            melody[pos] = val

    print('Playing Melody!')
    for key, value in melody.items():
        print('Note: #{} -> {}'.format(key, value['note']))
        sound.play(float(value['frequency']), float(value['duration']), amp)
        while sound.is_playing():
            pass
        time.sleep(float(value['sleep']))

def setsamplerate(rate=44100):
    global SAMPLE_RATE
    SAMPLE_RATE = rate

def setframesperbuffer(fpb=4410):
    global FRAMES_PER_BUFFER
    FRAMES_PER_BUFFER = fpb


def main():
    play_melody(melody_maker())


if __name__ == '__main__':
    main()