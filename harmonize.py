"""
Main Harmonizer
===============
Wires the demo modules into a working MPPI solver.

Pipeline:
  1. For each melody note, pre-compute every (chord, voicing) pair that fits
  2. For each beat, sample many random "futures" looking K beats ahead
  3. Score each future using cost_demo's rules
  4. Commit to the best first step, advance, repeat
  5. Save MIDI, print result, play through pygame

Imports the rules and helpers from the demo files - those modules
do the actual work, this file just orchestrates them.
"""

import math
import os
import random
import tempfile

import mido

from music_basics import CHORD_NAMES, get_chord_notes, note_name
from voicing_demo import generate_voicings
from cost_demo import score_transition
from progression_demo import TRANSITION_WEIGHTS


def harmonize(melody, tonic, num_samples=400, lookahead=4, bpm=100,
              save_path=None, play=True, seed=42, chord_change_every=1,
              long_beats=None):
    """Harmonize a soprano melody. Returns list of (voicing, chord_degree).

    chord_change_every: 1 = chord may change every beat (busy melodies like Ode to Joy);
                        2 = chord changes every 2 beats (most folk songs);
                        3 or 4 = slower harmonic rhythm.
    long_beats:         1-indexed beat numbers held as half notes instead of quarters
                        (used at phrase ends to give the singers/listeners a breath).
    """
    random.seed(seed)

    # Step 1: Pre-compute valid voicings for every (note, chord_degree) pair
    voicing_pool = {}
    for note in set(melody):
        for degree in range(7):
            chord_pcs = get_chord_notes(degree, tonic)
            options = generate_voicings(chord_pcs, note)
            if options:
                voicing_pool[(note, degree)] = options

    def chords_for(note):
        return [d for d in range(7) if (note, d) in voicing_pool]

    # Step 2: Initialize on the tonic chord (I)
    if (melody[0], 0) in voicing_pool:
        first_options = voicing_pool[(melody[0], 0)]
        first_degree = 0
    else:
        # Fall back to whatever chord can voice the first note
        avail = chords_for(melody[0])
        first_degree = avail[0]
        first_options = voicing_pool[(melody[0], first_degree)]
    # Pick a compact voicing, but heavily avoid bass=tenor unisons
    def _initial_score(v):
        unison_penalty = 1000 if v[2] == v[3] else 0
        return (v[0] - v[3]) + unison_penalty
    first_voicing = min(first_options, key=_initial_score)
    result = [(first_voicing, first_degree)]

    # Step 3: MPPI loop for the remaining beats
    for beat in range(1, len(melody)):
        window = min(lookahead, len(melody) - beat)
        best_cost = float("inf")
        best_first = None

        for _ in range(num_samples):
            traj_cost = 0.0
            prev_voicing, prev_degree = result[-1]
            first_step = None

            for k in range(window):
                abs_beat = beat + k
                note = melody[abs_beat]
                avail = chords_for(note)
                if not avail:
                    break

                # Hold the chord on non-change beats (when prev chord can voice this note)
                is_change_beat = (abs_beat % chord_change_every == 0)
                if not is_change_beat and prev_degree in avail:
                    degree = prev_degree
                else:
                    # Sample a chord from the prior, masked to available chords
                    weights = TRANSITION_WEIGHTS[prev_degree]
                    masked = [w if d in avail else 0 for d, w in enumerate(weights)]
                    if sum(masked) == 0:
                        masked = [1 if d in avail else 0 for d in range(7)]
                    degree = random.choices(range(7), weights=masked, k=1)[0]

                # Sample a voicing biased toward smooth motion (small distance)
                pool = voicing_pool[(note, degree)]
                if len(pool) == 1:
                    voicing = pool[0]
                else:
                    distances = [
                        sum(abs(a - b) for a, b in zip(v, prev_voicing)) for v in pool
                    ]
                    vweights = [math.exp(-d / 5.0) for d in distances]
                    voicing = random.choices(pool, weights=vweights, k=1)[0]

                # Score this transition using cost_demo's full rule set
                is_last_beat = (beat + k == len(melody) - 1)
                traj_cost += score_transition(
                    prev_voicing, voicing, prev_degree, degree, tonic, is_last_beat
                )
                prev_voicing = voicing
                prev_degree = degree

                if k == 0:
                    first_step = (voicing, degree)

            if first_step is not None and traj_cost < best_cost:
                best_cost = traj_cost
                best_first = first_step

        result.append(best_first)

    # Step 4: Print a clean result table
    print(f"\n{'Beat':<5} {'Chord':<6} {'Soprano':<8} {'Alto':<8} {'Tenor':<8} {'Bass':<8}")
    print("-" * 50)
    for i, (voicing, degree) in enumerate(result):
        names = [note_name(n) for n in voicing]
        print(f"{i+1:<5} {CHORD_NAMES[degree]:<6} "
              f"{names[0]:<8} {names[1]:<8} {names[2]:<8} {names[3]:<8}")

    # Step 5: Save MIDI
    if save_path is None:
        save_path = os.path.join(tempfile.gettempdir(), "harmonize.mid")
    save_midi(result, save_path, bpm, long_beats)
    print(f"\nSaved MIDI to {save_path}")

    # Step 6: Play through pygame
    if play:
        play_midi(save_path)

    return result


def save_midi(result, path, bpm, long_beats=None):
    """Write 4 tracks (one per voice) to a Type 1 MIDI file.
    Each beat = one quarter note (re-articulated even if the pitch repeats).
    Beats listed in `long_beats` are doubled in length (half notes)."""
    long_beats = set(long_beats or [])
    mid = mido.MidiFile(type=1, ticks_per_beat=480)
    tempo_track = mido.MidiTrack()
    tempo_track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    mid.tracks.append(tempo_track)

    for voice_index in range(4):
        track = mido.MidiTrack()
        track.append(mido.Message("program_change", channel=voice_index, program=0, time=0))
        for i, (voicing, _) in enumerate(result):
            pitch = voicing[voice_index]
            duration = 480 * (2 if (i + 1) in long_beats else 1)
            track.append(mido.Message("note_on", note=pitch, velocity=64,
                                      channel=voice_index, time=0))
            track.append(mido.Message("note_off", note=pitch, velocity=0,
                                      channel=voice_index, time=duration))
        mid.tracks.append(track)

    mid.save(path)


def play_midi(path):
    """Play a MIDI file through pygame's mixer."""
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    print("Playing... (Ctrl+C to stop)")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
