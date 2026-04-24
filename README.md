# MPPI Voice Leading Solver

A Python system that takes a soprano melody and outputs a complete SATB (soprano, alto, tenor, bass) harmonization using Model Predictive Path Integral (MPPI) control. Instead of hard constraint trees, we treat voice leading as a trajectory optimization problem: sample many possible futures, score them with a cost function encoding music theory rules, and pick the best path.

## What's in this project

- **`music_basics.py`** - shared foundation: MIDI notes, pitch classes, the major scale, triad shapes, and voice ranges. Everything else imports from here.
- **`chord_demo.py`** - given a Roman numeral and a key, print the chord's notes.
- **`voicing_demo.py`** - given a chord and a soprano note, find every valid 4-voice arrangement that fits the singing ranges and voice-leading constraints.
- **`cost_demo.py`** - the rule engine. Scores a chord transition using music theory rules (parallel fifths/octaves penalized, stepwise motion rewarded, contrary outer voices rewarded).
- **`progression_demo.py`** - the chord transition prior from Kostka/Payne, visualized as histograms. This is what MPPI samples from.
- **`edge_cases.py`** - tests for tricky inputs (soprano at lowest/highest note, soprano not in chord, surveying which chords can voice a given note).

## Running

```bash
python music_basics.py        # no output, just shared definitions
python chord_demo.py
python voicing_demo.py
python cost_demo.py
python progression_demo.py
python edge_cases.py
```

## Attributions

Based on concepts from Schmeling, *Berklee Music Theory Book 1* (2nd ed., Berklee Press, 2011).

This project was developed with assistance from AI tools (Claude). Specifically:

- **Music theory checking** - AI was consulted throughout to verify that our encoded rules match conventional music theory. This includes cross-checking the Kostka/Payne chord transition priors, the list of common voicing rules (parallel fifths, doubled leading tones, etc.), the rules for tendency tone resolution, and the distinction between strict rules and stylistic preferences. Any rule we encode as a cost term was double-checked against textbook practice before inclusion.
- **Writing assistance** - AI helped draft this README. All was reviewed and edited by us before committing.
- **Code structure** - the general skeleton and the demo organization were developed in dialogue with AI.

All code in this repository is run, tested, and understood by us.
