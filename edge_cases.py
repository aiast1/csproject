"""
Edge Case Tests
===============
The voicing generator has to handle tricky inputs gracefully:

  1. What if the soprano note is at the very bottom of its range?
     There may only be one (or zero!) valid voicings.

  2. What if the soprano note is NOT in the chord?
     The function should return an empty list, not crash.

  3. What if the soprano note is at the very TOP of its range?
     Lots of voicings exist because upper voices have room below.

  4. Which chords are impossible to voice with a specific soprano?
     Good for knowing when the solver has no options.
"""

from music_basics import NOTE_NAMES, note_name, parse_note, get_chord_notes, CHORD_NAMES
from voicing_demo import generate_voicings

def test(label, chord_pitches, soprano_midi):
    voicings = generate_voicings(chord_pitches, soprano_midi)
    print(f"\n{label}")
    print(f"  soprano = {note_name(soprano_midi)} (MIDI {soprano_midi}), "
          f"chord PCs = {chord_pitches}")
    print(f"  -> {len(voicings)} valid voicings")
    for v in voicings[:3]:
        print(f"     {[note_name(n) for n in v]}")
    if len(voicings) > 3:
        print(f"     ... and {len(voicings) - 3} more")

if __name__ == "__main__":
    C_major = [0, 4, 7]
    G_major = [7, 11, 2]  # G B D (the V of C major)

    # 1. Soprano at lowest possible note
    test("Edge 1: Soprano at lowest C4 (chord tone)",
         C_major, parse_note("C4"))

    # 2. Soprano NOT in chord -> empty result, no crash
    test("Edge 2: Soprano D4 but chord is C major (D is not in C major)",
         C_major, parse_note("D4"))

    # 3. Soprano at highest note
    test("Edge 3: Soprano near top (G5)",
         C_major, parse_note("G5"))

    # 4. Survey all diatonic chords in C major for a given soprano
    print("\nEdge 4: Soprano = E4. Which diatonic chords can voice it?")
    soprano = parse_note("E4")
    tonic = 0  # C major
    for degree in range(7):
        chord = get_chord_notes(degree, tonic)
        voicings = generate_voicings(chord, soprano)
        status = f"{len(voicings):2d} voicings" if voicings else "IMPOSSIBLE"
        print(f"  {CHORD_NAMES[degree]:5s}  {status}")
