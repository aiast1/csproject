"""Twinkle Twinkle Little Star — C major, 14 beats."""

import os
from music_basics import parse_note
from harmonize import harmonize

# "Twinkle twinkle little star, how I wonder what you are"
melody = [
    parse_note("C4"), parse_note("C4"), parse_note("G4"), parse_note("G4"),
    parse_note("A4"), parse_note("A4"), parse_note("G4"),
    parse_note("F4"), parse_note("F4"), parse_note("E4"), parse_note("E4"),
    parse_note("D4"), parse_note("D4"), parse_note("C4"),
]
tonic = 0  # C major

if __name__ == "__main__":
    print(f"Harmonizing 'Twinkle Twinkle' in C major ({len(melody)} beats)")
    save_path = os.path.join(os.path.dirname(__file__), "twinkle.mid")
    # Phrase-end beats ("star" and "are") held longer for breathing
    harmonize(melody, tonic, save_path=save_path, bpm=90, chord_change_every=2,
              long_beats=[7, 14])
