"""Jingle Bells (chorus) — C major, 25 beats."""

import os
from music_basics import parse_note
from harmonize import harmonize

# "Jingle bells, jingle bells, jingle all the way!
#  Oh what fun it is to ride in a one-horse open sleigh"
melody = [
    parse_note("E4"), parse_note("E4"), parse_note("E4"),
    parse_note("E4"), parse_note("E4"), parse_note("E4"),
    parse_note("E4"), parse_note("G4"), parse_note("C4"),
    parse_note("D4"), parse_note("E4"),
    parse_note("F4"), parse_note("F4"), parse_note("F4"), parse_note("F4"),
    parse_note("F4"), parse_note("E4"), parse_note("E4"), parse_note("E4"),
    parse_note("E4"), parse_note("D4"), parse_note("D4"),
    parse_note("E4"), parse_note("D4"), parse_note("G4"),
]
tonic = 0  # C major

if __name__ == "__main__":
    print(f"Harmonizing 'Jingle Bells' in C major ({len(melody)} beats)")
    save_path = os.path.join(os.path.dirname(__file__), "jingle_bells.mid")
    # Phrase-end beats ("way", "ride", "sleigh") held longer for breathing
    harmonize(melody, tonic, save_path=save_path, bpm=110, chord_change_every=2,
              long_beats=[11, 19, 25])
