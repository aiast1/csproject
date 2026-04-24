"""
Cost Function Demo
==================
Score the transition between two 4-voice chords.
Lower cost = better sounding. Negative = rewarded.

The cost function is the "brain" of the MPPI solver:
every music theory rule is a term with a weight.
"""

from music_basics import get_chord_notes, note_name, parse_note

def parallel_fifth_or_octave_cost(prev, curr):
    """+80 per parallel 5th or octave between any pair of voices."""
    cost = 0
    for i in range(4):
        for j in range(i + 1, 4):
            if prev[i] == curr[i] or prev[j] == curr[j]:
                continue
            d1, d2 = curr[i] - prev[i], curr[j] - prev[j]
            if (d1 > 0) != (d2 > 0):  # not same direction
                continue
            interval_before = abs(prev[i] - prev[j]) % 12
            interval_after = abs(curr[i] - curr[j]) % 12
            if interval_before == 7 and interval_after == 7:
                cost += 80  # parallel 5th
            if interval_before == 0 and interval_after == 0:
                cost += 80  # parallel octave
    return cost

def smooth_motion_reward(prev, curr):
    """-10 per voice moving by a step (1 or 2 semitones)."""
    reward = 0
    for i in range(4):
        if 1 <= abs(curr[i] - prev[i]) <= 2:
            reward -= 10
    return reward

def contrary_outer_reward(prev, curr):
    """-8 if soprano and bass move in opposite directions."""
    s_dir = curr[0] - prev[0]
    b_dir = curr[3] - prev[3]
    if s_dir != 0 and b_dir != 0 and (s_dir > 0) != (b_dir > 0):
        return -8
    return 0

def score_transition(prev, curr):
    """Total cost = sum of all rules."""
    return (
        parallel_fifth_or_octave_cost(prev, curr)
        + smooth_motion_reward(prev, curr)
        + contrary_outer_reward(prev, curr)
    )

# --- Demo: compare three V-I transitions ---
if __name__ == "__main__":
    # G major -> C major (V -> I in C major)
    clean_V   = (67, 62, 59, 55)  # G4, D4, B3, G3
    clean_I   = (72, 64, 60, 48)  # C5, E4, C4, C3 — bass leaps down, smooth upper

    # Same V chord, but resolve with parallel octaves (bad!)
    bad_V     = (67, 62, 59, 55)
    bad_I     = (72, 64, 60, 60)  # bass jumps to C4, soprano jumps to C5 = parallel octaves

    # Stepwise motion everywhere (very smooth)
    smooth_V  = (67, 62, 59, 55)
    smooth_I  = (67, 64, 60, 52)  # S holds, A steps up, T steps up, B steps down

    cases = [
        ("Clean V -> I",            clean_V,  clean_I),
        ("V -> I with parallel 8ves", bad_V,    bad_I),
        ("Very smooth V -> I",      smooth_V, smooth_I),
    ]
    for label, prev, curr in cases:
        print(f"\n{label}")
        print(f"  prev: {[note_name(n) for n in prev]}")
        print(f"  curr: {[note_name(n) for n in curr]}")
        p5 = parallel_fifth_or_octave_cost(prev, curr)
        sm = smooth_motion_reward(prev, curr)
        co = contrary_outer_reward(prev, curr)
        total = p5 + sm + co
        print(f"  parallel 5ths/8ves: {p5:+d}")
        print(f"  smooth motion:      {sm:+d}")
        print(f"  contrary outer:     {co:+d}")
        print(f"  TOTAL:              {total:+d}")
