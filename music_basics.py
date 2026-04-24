"""
Shared music helpers used by every demo in this folder.

Notes are MIDI numbers (middle C = 60, each semitone = +1).
Pitch class is the note without the octave: C=0, C#=1, ... B=11.
"""

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Each voice has a comfortable singing range (low, high) as MIDI numbers
RANGES = {
    "soprano": (60, 79),   # C4 – G5
    "alto":    (55, 74),   # G3 – D5
    "tenor":   (48, 67),   # C3 – G4
    "bass":    (40, 60),   # E2 – C4
}

# Semitone offsets of the major scale from the tonic
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]

# Triad qualities for each scale degree in a major key
# Each triad = (root, third, fifth) as semitone offsets
TRIAD_SHAPES = [
    (0, 4, 7),  # I   major
    (0, 3, 7),  # ii  minor
    (0, 3, 7),  # iii minor
    (0, 4, 7),  # IV  major
    (0, 4, 7),  # V   major
    (0, 3, 7),  # vi  minor
    (0, 3, 6),  # vii diminished
]

CHORD_NAMES = ["I", "ii", "iii", "IV", "V", "vi", "viio"]

def note_name(midi):
    """MIDI number to note name. 60 -> 'C4', 69 -> 'A4'."""
    return f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"

def parse_note(name):
    """Note name to MIDI. 'C4' -> 60, 'F#5' -> 78."""
    letter = name[0]
    sharp = "#" in name
    octave = int(name[-1])
    base = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[letter]
    return (octave + 1) * 12 + base + (1 if sharp else 0)

def get_chord_notes(degree, tonic):
    """Pitch classes of a diatonic triad.
    degree: 0-6 (0=I, 4=V, etc.)
    tonic:  pitch class of key (0=C, 2=D, 7=G)
    Returns list of 3 pitch classes.
    """
    root = (tonic + MAJOR_SCALE[degree]) % 12
    return [(root + offset) % 12 for offset in TRIAD_SHAPES[degree]]
