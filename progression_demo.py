"""
Chord Progression Prior
=======================
Which chord tends to follow which? This table comes from music theory
textbooks (Kostka/Payne) and encodes conventional harmonic practice.

Example: after V, the most likely next chord is I (dominant resolution).
After ii, the most likely next chord is V (ii-V-I progression).

The MPPI sampler uses this to bias random sampling toward musical paths.
"""

import random
from music_basics import CHORD_NAMES

# Rows = current chord, columns = next chord. Higher = more likely.
TRANSITION_WEIGHTS = [
    [1, 4, 2, 5, 5, 3, 1],   # from I
    [1, 1, 1, 2, 6, 1, 1],   # from ii
    [1, 2, 1, 4, 1, 4, 1],   # from iii
    [3, 3, 1, 1, 5, 1, 2],   # from IV
    [6, 1, 1, 1, 1, 4, 1],   # from V
    [2, 4, 1, 3, 3, 1, 1],   # from vi
    [5, 1, 2, 1, 3, 1, 1],   # from viio
]

def sample_next_chord(current_degree, seed=None):
    """Pick a next chord degree using the prior weights."""
    if seed is not None:
        random.seed(seed)
    weights = TRANSITION_WEIGHTS[current_degree]
    return random.choices(range(7), weights=weights, k=1)[0]

def histogram(current_degree, trials=1000):
    """Run many samples, return a count per destination chord."""
    counts = [0] * 7
    for _ in range(trials):
        counts[sample_next_chord(current_degree)] += 1
    return counts

# --- Demo ---
if __name__ == "__main__":
    random.seed(42)
    trials = 1000

    for from_degree, from_name in enumerate(CHORD_NAMES):
        counts = histogram(from_degree, trials)
        bar_parts = []
        for to_name, count in zip(CHORD_NAMES, counts):
            bars = "#" * (count // 20)
            bar_parts.append(f"  {to_name:5s}{bars:<25s}{count}")
        print(f"\nFrom {from_name}: ({trials} samples)")
        for part in bar_parts:
            print(part)
