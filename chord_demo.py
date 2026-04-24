"""
Chord Demo
==========
Given a key and a Roman numeral, print the chord's notes.

Examples:
  V in C major  -> G, B, D   (the G major triad)
  ii in F major -> G, Bb, D  (G minor triad)
  vi in G major -> E, G, B   (E minor triad)
"""

from music_basics import CHORD_NAMES, NOTE_NAMES, get_chord_notes, parse_note

def roman_to_degree(roman):
    """Convert a Roman numeral string to a 0-indexed scale degree."""
    lowered = [c.lower() for c in CHORD_NAMES]
    return lowered.index(roman.lower())

def chord_from_roman(roman, key_tonic):
    """Return (chord_name, [pitch_class_names]) for a Roman numeral in a key."""
    degree = roman_to_degree(roman)
    pitch_classes = get_chord_notes(degree, key_tonic)
    names = [NOTE_NAMES[pc] for pc in pitch_classes]
    return CHORD_NAMES[degree], names

# --- Demo ---
if __name__ == "__main__":
    examples = [
        ("V",    "C", 0),   # G major triad
        ("ii",   "F", 5),   # G minor triad
        ("vi",   "G", 7),   # E minor triad
        ("viio", "D", 2),   # C# diminished
        ("IV",   "Bb", 10), # Eb major triad
    ]
    print(f"{'Roman':<6} {'Key':<4} {'Chord notes':<20}")
    print("-" * 32)
    for roman, key_name, tonic in examples:
        name, notes = chord_from_roman(roman, tonic)
        print(f"{roman:<6} {key_name:<4} {', '.join(notes):<20}")
