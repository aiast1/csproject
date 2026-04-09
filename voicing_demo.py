"""
Voicing Generator Demo
======================
Given a chord and a soprano note, find all valid ways to arrange
4 singing voices (soprano, alto, tenor, bass).

Each voice has a comfortable range (in MIDI numbers, where middle C = 60):
  Soprano: C4 (60) to G5 (79)
  Alto:    G3 (55) to D5 (74)
  Tenor:   C3 (48) to G4 (67)
  Bass:    E2 (40) to C4 (60)

Rules:
  - Every note in the chord must appear in at least one voice
  - Voices can't cross (soprano >= alto >= tenor >= bass)
  - Adjacent upper voices can't be more than an octave apart
"""

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

RANGES = {"soprano": (60, 79), "alto": (55, 74), "tenor": (48, 67), "bass": (40, 60)}

def note_name(midi):
    return f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"

def pitches_in_range(pitch_class, lo, hi):
    """All MIDI notes matching a pitch class (0-11) within [lo, hi]."""
    start = lo + (pitch_class - lo % 12) % 12
    return list(range(start, hi + 1, 12))

def generate_voicings(chord_pitches, soprano_note):
    """Find every valid SATB voicing for a chord with a fixed soprano note.
    chord_pitches: list of 3 pitch classes (e.g. [0, 4, 7] for C major)
    soprano_note:  MIDI number for the soprano
    """
    if soprano_note % 12 not in chord_pitches:
        return []

    results = []
    for bass in pitches_in_range(chord_pitches[0], *RANGES["bass"]):
        if bass > soprano_note:
            continue
        # Figure out which chord tones alto and tenor need to cover
        covered = {soprano_note % 12, bass % 12}
        missing = [pc for pc in chord_pitches if pc not in covered]
        if len(missing) == 2:
            pairs = [(missing[0], missing[1]), (missing[1], missing[0])]
        elif len(missing) == 1:
            pairs = [(missing[0], chord_pitches[0]), (chord_pitches[0], missing[0])]
        else:
            pairs = [(chord_pitches[0], chord_pitches[2])]

        for alto_pc, tenor_pc in pairs:
            for alto in pitches_in_range(alto_pc, *RANGES["alto"]):
                if alto > soprano_note or soprano_note - alto > 12:
                    continue
                for tenor in pitches_in_range(tenor_pc, *RANGES["tenor"]):
                    if tenor > alto or alto - tenor > 12 or tenor < bass:
                        continue
                    voicing = (soprano_note, alto, tenor, bass)
                    # Check all chord tones are present
                    present = {n % 12 for n in voicing}
                    if all(pc in present for pc in chord_pitches):
                        results.append(voicing)
    return results

# --- Demo ---
if __name__ == "__main__":
    chord = [0, 4, 7]  # C major triad (C=0, E=4, G=7)
    soprano = 64        # E4

    voicings = generate_voicings(chord, soprano)
    print(f"C major chord with soprano on {note_name(soprano)}: {len(voicings)} valid voicings\n")
    for i, v in enumerate(voicings):
        names = [note_name(m) for m in v]
        print(f"  {i+1:2d}.  S={names[0]:4s}  A={names[1]:4s}  T={names[2]:4s}  B={names[3]:4s}")
