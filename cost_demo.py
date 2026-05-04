"""
Cost Function Demo
==================
Score the transition between two 4-voice chords.
Lower cost = better sounding. Negative = rewarded.

The cost function is the "brain" of the MPPI solver:
every music theory rule becomes a term with a weight.
"""

from music_basics import note_name

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

def leading_tone_resolution_cost(prev, curr, prev_degree, curr_degree, tonic):
    """+25 if leading tone in a V chord doesn't resolve up to tonic in V->I."""
    if prev_degree != 4 or curr_degree != 0:  # only applies to V -> I
        return 0
    leading_tone = (tonic - 1) % 12
    fifth = (tonic + 7) % 12
    cost = 0
    for i in range(4):
        if prev[i] % 12 != leading_tone:
            continue
        # Resolved up by semitone? Good.
        if curr[i] - prev[i] == 1:
            continue
        # Inner-voice exception: alto or tenor may go down to the 5th
        if i in (1, 2) and curr[i] % 12 == fifth:
            continue
        cost += 25
    return cost

def upper_voice_leap_cost(prev, curr):
    """+8 per upper voice (S/A/T) leaping more than a perfect 5th (>7 semitones)."""
    cost = 0
    for i in range(3):  # soprano, alto, tenor
        if abs(curr[i] - prev[i]) > 7:
            cost += 8
    return cost

def cadence_reward(curr, curr_degree, tonic, is_last_beat):
    """Reward a strong final cadence: -50 if last chord is I with soprano on tonic,
    -25 if last chord is I but soprano on a different tone."""
    if not is_last_beat:
        return 0
    if curr_degree != 0:  # not the I chord
        return 0
    if curr[0] % 12 == tonic:
        return -50
    return -25

def bass_tenor_unison_cost(curr):
    """+15 if bass and tenor share the exact same MIDI note (sounds thin)."""
    return 15 if curr[2] == curr[3] else 0

def retrogression_cost(prev_degree, curr_degree):
    """+10 for strong backward motion (V->IV, V->iii, V->ii). +5 for milder cases."""
    if prev_degree == 4 and curr_degree in (1, 2, 3):
        return 10
    if prev_degree == 5 and curr_degree in (1, 3):  # vi->ii, vi->IV
        return 5
    return 0

def repeated_chord_cost(prev_degree, curr_degree):
    """+3 if the same chord repeats (mild — sometimes fine, often boring)."""
    return 3 if prev_degree == curr_degree else 0

def score_transition(prev, curr, prev_degree=4, curr_degree=0, tonic=0, is_last_beat=False):
    """Total cost = sum of all rules.
    Defaults to V->I in C major (most common case)."""
    return (
        parallel_fifth_or_octave_cost(prev, curr)
        + smooth_motion_reward(prev, curr)
        + contrary_outer_reward(prev, curr)
        + leading_tone_resolution_cost(prev, curr, prev_degree, curr_degree, tonic)
        + upper_voice_leap_cost(prev, curr)
        + cadence_reward(curr, curr_degree, tonic, is_last_beat)
        + bass_tenor_unison_cost(curr)
        + retrogression_cost(prev_degree, curr_degree)
        + repeated_chord_cost(prev_degree, curr_degree)
    )

# --- Demo: compare four V->I transitions in C major ---
if __name__ == "__main__":
    # G major -> C major (V -> I in C major, tonic=0)
    clean_V   = (67, 62, 59, 55)  # G4, D4, B3, G3
    clean_I   = (72, 64, 60, 48)  # C5, E4, C4, C3 - bass leaps down, smooth upper

    # Same V chord, but resolve with parallel octaves (bad!)
    bad_V     = (67, 62, 59, 55)
    bad_I     = (72, 64, 60, 60)  # bass jumps to C4 = parallel octaves with soprano

    # Stepwise motion everywhere (very smooth)
    smooth_V  = (67, 62, 59, 55)
    smooth_I  = (67, 64, 60, 52)  # S holds, A steps up, T steps up, B steps down

    # Soprano on B (the leading tone) but it leaps DOWN to A instead of resolving up to C
    unresolved_V = (71, 67, 62, 55)   # B4, G4, D4, G3
    unresolved_I = (69, 64, 60, 48)   # A4, E4, C4, C3 - leading tone B leapt down!

    # Final-cadence case: V -> I on the very last beat, soprano lands on tonic
    cadence_V = (71, 67, 62, 55)         # B4, G4, D4, G3
    cadence_I = (72, 67, 64, 48)         # C5, G4, E4, C3 - soprano on C (tonic)

    # Retrogression case: V -> ii (backward harmonic motion, cleanly voiced)
    retro_V   = (67, 62, 59, 55)         # G4, D4, B3, G3 (V chord)
    retro_ii  = (69, 65, 62, 50)         # A4, F4, D4, D3 (ii chord)

    cases = [
        # label,                              prev,         curr,         prev_d, curr_d, last
        ("Clean V -> I",                      clean_V,      clean_I,      4, 0, False),
        ("V -> I with parallel octaves",      bad_V,        bad_I,        4, 0, False),
        ("Very smooth V -> I",                smooth_V,     smooth_I,     4, 0, False),
        ("Leading tone unresolved (B -> A)",  unresolved_V, unresolved_I, 4, 0, False),
        ("Final cadence: V -> I (last beat)", cadence_V,    cadence_I,    4, 0, True),
        ("Retrogression V -> ii",             retro_V,      retro_ii,     4, 1, False),
    ]
    for label, prev, curr, pd, cd, last in cases:
        print(f"\n{label}")
        print(f"  prev: {[note_name(n) for n in prev]}")
        print(f"  curr: {[note_name(n) for n in curr]}")
        p5  = parallel_fifth_or_octave_cost(prev, curr)
        sm  = smooth_motion_reward(prev, curr)
        co  = contrary_outer_reward(prev, curr)
        lt  = leading_tone_resolution_cost(prev, curr, pd, cd, 0)
        leap = upper_voice_leap_cost(prev, curr)
        cad  = cadence_reward(curr, cd, 0, last)
        bt   = bass_tenor_unison_cost(curr)
        retro = retrogression_cost(pd, cd)
        rep  = repeated_chord_cost(pd, cd)
        total = p5 + sm + co + lt + leap + cad + bt + retro + rep
        print(f"  parallel 5ths/8ves: {p5:+d}")
        print(f"  smooth motion:      {sm:+d}")
        print(f"  contrary outer:     {co:+d}")
        print(f"  leading tone res:   {lt:+d}")
        print(f"  upper-voice leaps:  {leap:+d}")
        print(f"  cadence reward:     {cad:+d}")
        print(f"  bass=tenor unison:  {bt:+d}")
        print(f"  retrogression:      {retro:+d}")
        print(f"  repeated chord:     {rep:+d}")
        print(f"  TOTAL:              {total:+d}")
