"""Amazing Grace — G major, 16 beats."""

import os
from music_basics import parse_note
from harmonize import harmonize

# "Amazing grace, how sweet the sound / that saved a wretch like me"
melody = [
    parse_note("D4"), parse_note("G4"), parse_note("B4"), parse_note("G4"),
    parse_note("B4"), parse_note("A4"), parse_note("G4"), parse_note("E4"),
    parse_note("D4"), parse_note("G4"), parse_note("B4"), parse_note("G4"),
    parse_note("B4"), parse_note("A4"), parse_note("D5"), parse_note("G4"),
]
tonic = 7  # G major

if __name__ == "__main__":
    print(f"Harmonizing 'Amazing Grace' in G major ({len(melody)} beats)")
    save_path = os.path.join(os.path.dirname(__file__), "amazing_grace.mid")
    # Phrase-end beats ("sound" and final "me") held longer for breathing
    harmonize(melody, tonic, save_path=save_path, bpm=80, chord_change_every=2,
              long_beats=[9, 16])
