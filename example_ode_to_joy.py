"""Ode to Joy (Beethoven, Symphony No. 9) — D major, 30 beats."""

import os
from music_basics import parse_note
from harmonize import harmonize

melody = [
    parse_note("F#4"), parse_note("F#4"), parse_note("G4"),  parse_note("A4"),
    parse_note("A4"),  parse_note("G4"),  parse_note("F#4"), parse_note("E4"),
    parse_note("D4"),  parse_note("D4"),  parse_note("E4"),  parse_note("F#4"),
    parse_note("F#4"), parse_note("E4"),  parse_note("E4"),
    parse_note("F#4"), parse_note("F#4"), parse_note("G4"),  parse_note("A4"),
    parse_note("A4"),  parse_note("G4"),  parse_note("F#4"), parse_note("E4"),
    parse_note("D4"),  parse_note("D4"),  parse_note("E4"),  parse_note("F#4"),
    parse_note("E4"),  parse_note("D4"),  parse_note("D4"),
]
tonic = 2  # D = pitch class 2

if __name__ == "__main__":
    print(f"Harmonizing 'Ode to Joy' in D major ({len(melody)} beats)")
    save_path = os.path.join(os.path.dirname(__file__), "ode_to_joy.mid")
    # Phrase-end beats are held longer (half notes) for breathing room
    harmonize(melody, tonic, save_path=save_path, bpm=100,
              long_beats=[8, 15, 23, 30])
