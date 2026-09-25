"""Generate the progressive sampler-based synthesis notebooks.

Run: uv run python _build_notebooks.py
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

NB_DIR = Path(__file__).resolve().parent


def _id() -> str:
    return uuid.uuid4().hex[:12]


def md(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": _id(),
        "metadata": {},
        "source": _lines(source),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "id": _id(),
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _lines(source),
    }


def _lines(source: str) -> list[str]:
    source = source.strip("\n")
    if not source:
        return []
    lines = source.split("\n")
    return [ln + "\n" for ln in lines[:-1]] + [lines[-1]]


def notebook(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def write(name: str, cells: list[dict]) -> None:
    path = NB_DIR / name
    path.write_text(json.dumps(notebook(cells), indent=1) + "\n", encoding="utf-8")
    print(f"wrote {path.name} ({len(cells)} cells)")


# ---------------------------------------------------------------------------
# 01 — Samples & waveforms
# ---------------------------------------------------------------------------

nb01 = [
    md(
        """\
# 01 — Samples & Waveforms

**Level:** Beginner

A *sample* is a short buffer of digital audio — numbers that represent air-pressure over time. Sampler-based synthesis starts here: store a clip, then reshape it later with rate, envelope, and filters.

In this notebook you will:
1. Connect sample rate / amplitude to what you hear
2. Generate a few classic waveforms and a plucked “instrument” snippet
3. View **and** play every clip via `hear()`

> Checklist at the end: you should be able to explain what one sample point is, and why 44.1 kHz matters.
"""
    ),
    md("## Setup"),
    code(
        """\
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

from audio_utils import SR, hear, normalize, seconds, midi_to_hz, apply_adsr

print(f"Project sample rate: {SR} Hz")
print(f"One second of mono audio = {SR:,} floating-point samples")
"""
    ),
    md(
        """\
## Digital audio in one picture

Continuous sound pressure is measured **SR** times per second. Each measurement is one *sample* (the noun clashes with “musical sample” — context tells them apart).

Amplitude ≈ −1…+1 in our float buffers. Louder peaks → louder sound (until clipping).
"""
    ),
    code(
        """\
# A pure 440 Hz A4 tone — the simplest possible "sample"
duration = 1.0
t = np.arange(seconds(duration)) / SR
a4 = 0.4 * np.sin(2 * np.pi * 440 * t)

hear(a4, SR, title="A4 sine (440 Hz)", show_spec=True, max_waveform_seconds=0.02)
"""
    ),
    md(
        """\
## Waveform zoo

Same pitch, different spectra → different timbres. Samplers often store complex real-world spectra; these oscillators are the teaching version.
"""
    ),
    code(
        """\
def square(freq, dur, amp=0.35):
    t = np.arange(seconds(dur)) / SR
    # Band-limited-ish via odd harmonics (avoids the harshest aliasing)
    y = np.zeros_like(t)
    for k in range(1, 15, 2):
        y += (1 / k) * np.sin(2 * np.pi * freq * k * t)
    return normalize(y, peak=amp)

def saw(freq, dur, amp=0.35):
    t = np.arange(seconds(dur)) / SR
    y = np.zeros_like(t)
    for k in range(1, 20):
        y += ((-1) ** (k + 1)) / k * np.sin(2 * np.pi * freq * k * t)
    return normalize(y, peak=amp)

def noise(dur, amp=0.25):
    rng = np.random.default_rng(0)
    return normalize(rng.normal(0, 1, seconds(dur)), peak=amp)

freq = 220  # A3
for name, sig in [
    ("Square-ish A3", square(freq, 0.8)),
    ("Saw-ish A3", saw(freq, 0.8)),
    ("White noise", noise(0.8)),
]:
    hear(sig, SR, title=name, show_spec=True, max_waveform_seconds=0.03)
"""
    ),
    md(
        """\
## A musical sample (synthetic plucked string)

Real samplers load WAV/AIFF recordings. Here we synthesize a short decaying “pluck” so the repo stays self-contained — treat it like a recorded one-shot.
"""
    ),
    code(
        """\
def make_pluck(midi=60, dur=1.2, brightness=0.55):
    \"\"\"Karplus-Strong-inspired pluck used as a stand-in instrument sample.\"\"\"
    freq = midi_to_hz(midi)
    n = seconds(dur)
    # Noise burst into a feedback delay line ≈ string length
    delay = max(2, int(round(SR / freq)))
    rng = np.random.default_rng(midi)
    buf = rng.uniform(-1, 1, delay)
    out = np.zeros(n)
    idx = 0
    for i in range(n):
        out[i] = buf[idx]
        avg = brightness * 0.5 * (buf[idx] + buf[(idx + 1) % delay])
        buf[idx] = avg
        idx = (idx + 1) % delay
    return apply_adsr(normalize(out, 0.9), attack=0.002, decay=0.05, sustain=0.55, release=0.35)

pluck_c4 = make_pluck(60)
hear(pluck_c4, SR, title="Synthetic pluck sample — C4 (MIDI 60)", show_spec=True)
"""
    ),
    md(
        """\
## Zoom: what “one cycle” looks like

Early samplers (and wavetable synths) sometimes store only a single cycle and loop it. Compare a long decaying pluck vs. a looping single-cycle tone.
"""
    ),
    code(
        """\
# Extract ~4 periods of a steady sine as a tiny loopable cycle
cycle_freq = 220
samples_per_cycle = int(round(SR / cycle_freq))
cycle = np.sin(2 * np.pi * np.arange(samples_per_cycle) / samples_per_cycle)
looped = np.tile(cycle, 80)  # ~80 cycles ≈ 0.36 s
hear(0.4 * cycle, SR, title="Single cycle (very short click-ish)", max_waveform_seconds=None)
hear(0.4 * looped, SR, title="Same cycle looped (steady tone)", max_waveform_seconds=0.05)
"""
    ),
    md(
        """\
## You should be able to…

- Say what sample rate and amplitude mean in a PCM buffer
- Tell a sine from noise on a spectrogram
- Treat a short buffer as a reusable musical *sample*

**Next:** [02 — Playback rate & pitch](02_playback_rate_and_pitch.ipynb)
"""
    ),
]

# ---------------------------------------------------------------------------
# 02 — Playback rate & pitch
# ---------------------------------------------------------------------------

nb02 = [
    md(
        """\
# 02 — Playback Rate & Pitch

**Level:** Beginner → Intermediate

The oldest sampler trick: play the buffer **faster** → higher pitch and shorter duration; **slower** → lower and longer. Chromatic mapping uses the twelfth-root-of-two:

$$
\\text{rate} = 2^{n/12}
$$

for $n$ semitones away from the sample’s root note.
"""
    ),
    md("## Setup"),
    code(
        """\
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

from audio_utils import (
    SR, hear, normalize, seconds, midi_to_hz, semitone_ratio,
    linear_resample, apply_adsr, plot_waveform,
)

def make_pluck(midi=60, dur=1.0, brightness=0.55, seed=0):
    freq = midi_to_hz(midi)
    n = seconds(dur)
    delay = max(2, int(round(SR / freq)))
    rng = np.random.default_rng(seed + midi)
    buf = rng.uniform(-1, 1, delay)
    out = np.zeros(n)
    idx = 0
    for i in range(n):
        out[i] = buf[idx]
        buf[idx] = brightness * 0.5 * (buf[idx] + buf[(idx + 1) % delay])
        idx = (idx + 1) % delay
    return apply_adsr(normalize(out), attack=0.002, decay=0.04, sustain=0.5, release=0.3)

root = make_pluck(60)
hear(root, SR, title="Root sample — C4", show_spec=True)
"""
    ),
    md(
        """\
## Rate ↔ semitones

Listen to +12 (one octave up: twice as fast) and −12 (half speed). Duration halves / doubles with pitch — classic sampler behavior (no independent time-stretch yet).
"""
    ),
    code(
        """\
for semis, label in [(-12, "−12 semitones (octave down)"), (0, "root"), (7, "+7 (fifth)"), (12, "+12 (octave up)")]:
    rate = semitone_ratio(semis)
    pitched = linear_resample(root, rate)
    hear(pitched, SR, title=f"{label}  |  rate={rate:.4f}", show_spec=True, max_waveform_seconds=0.05)
"""
    ),
    md(
        """\
## Duration trade-off

Plot length vs. transposition. This is why multisampling exists: stretch a single sample too far and it sounds chipmunked or muddy.
"""
    ),
    code(
        """\
semis = np.arange(-12, 13)
durs = [len(linear_resample(root, semitone_ratio(n))) / SR for n in semis]

fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(semis, durs, marker="o", color="#c45c26")
ax.axvline(0, color="gray", ls="--", alpha=0.5)
ax.set_xlabel("Semitones from root")
ax.set_ylabel("Duration (s)")
ax.set_title("Playback-rate transposition changes length")
ax.grid(True, alpha=0.3)
plt.show()
"""
    ),
    md(
        """\
## Chromatic one-shot sampler

Map MIDI notes to rates relative to root MIDI 60 (C4). Play a short ascending phrase.
"""
    ),
    code(
        """\
def play_note(sample, root_midi, note_midi, gain=0.9):
    rate = semitone_ratio(note_midi - root_midi)
    return gain * linear_resample(sample, rate)

def sequence(sample, root_midi, notes, gap=0.05):
    parts = []
    silence = np.zeros(seconds(gap))
    for n in notes:
        parts.append(play_note(sample, root_midi, n))
        parts.append(silence)
    return normalize(np.concatenate(parts))

phrase = sequence(root, 60, [60, 62, 64, 65, 67, 69, 71, 72], gap=0.06)
hear(phrase, SR, title="Chromatic scale from one C4 sample", show_spec=True, max_waveform_seconds=None)
"""
    ),
    md(
        """\
## Extreme stretch (when one sample isn’t enough)

± an octave already strains a single recording. Listen for the “chipmunk” formant shift upward — pitch and spectral envelope move together under rate change.
"""
    ),
    code(
        """\
wide = sequence(root, 60, [48, 60, 72], gap=0.15)
hear(wide, SR, title="Same sample: C3 → C4 → C5 (formants shift)", show_spec=True)
"""
    ),
    md(
        """\
## You should be able to…

- Convert semitones to a playback-rate factor
- Explain why pitch-by-rate also changes duration and formants
- Build a tiny chromatic mapper from one root sample

**Next:** [03 — Envelopes, loops & zones](03_envelopes_loops_and_zones.ipynb)
"""
    ),
]

# ---------------------------------------------------------------------------
# 03 — Envelopes, loops & zones
# ---------------------------------------------------------------------------

nb03 = [
    md(
        """\
# 03 — Envelopes, Loops & Zones

**Level:** Intermediate

A raw sample is rarely played “as-is”. Hardware and software samplers add:

1. **ADSR** — shape loudness over the note
2. **Loops** — sustain forever from a short buffer
3. **Zones** — different samples for pitch / velocity ranges (multisampling)
"""
    ),
    md("## Setup"),
    code(
        """\
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

from audio_utils import (
    SR, hear, normalize, seconds, midi_to_hz, semitone_ratio,
    linear_resample, apply_adsr, mix,
)

def make_tone(midi=60, dur=2.0, harm=(1, 0.4, 0.2, 0.1)):
    t = np.arange(seconds(dur)) / SR
    f = midi_to_hz(midi)
    y = sum(a * np.sin(2 * np.pi * f * (k + 1) * t) for k, a in enumerate(harm))
    return normalize(y)

raw = make_tone(60, dur=2.0)
hear(raw, SR, title="Raw sustained tone (no envelope)", max_waveform_seconds=0.03)
"""
    ),
    md(
        """\
## ADSR amplitude envelope

Attack → Decay → Sustain level → Release. Same sample, four musical articulations.
"""
    ),
    code(
        """\
articulations = {
    "Pad (slow attack)": dict(attack=0.6, decay=0.3, sustain=0.7, release=0.5),
    "Pluck": dict(attack=0.005, decay=0.25, sustain=0.0, release=0.05),
    "Organ-ish": dict(attack=0.02, decay=0.05, sustain=0.9, release=0.08),
    "Swell": dict(attack=0.9, decay=0.2, sustain=0.85, release=0.4),
}

# Visualize envelopes alone
fig, ax = plt.subplots(figsize=(10, 3.5))
for name, params in articulations.items():
    dummy = np.ones(seconds(2.0))
    env = apply_adsr(dummy, **params)
    ax.plot(np.arange(len(env)) / SR, env, label=name)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Envelope")
ax.set_title("ADSR shapes")
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()

for name, params in articulations.items():
    shaped = apply_adsr(raw, **params)
    hear(shaped, SR, title=f"ADSR — {name}", max_waveform_seconds=None)
"""
    ),
    md(
        """\
## Crossfade looping

Mark a loop region and crossfade the seam so a short vowel / pad cycle can sustain indefinitely without a click.
"""
    ),
    code(
        """\
def crossfade_loop(x, loop_start, loop_end, fade):
    \"\"\"Return one loop iteration with ends crossfaded (for tiling).\"\"\"
    x = np.asarray(x, dtype=np.float64).ravel()
    seg = x[loop_start:loop_end].copy()
    fade = min(fade, len(seg) // 3)
    if fade < 1:
        return seg
    fade_in = np.linspace(0, 1, fade)
    fade_out = 1 - fade_in
    # Blend end into start
    seg[:fade] = seg[:fade] * fade_in + seg[-fade:] * fade_out
    return seg[:-fade]  # drop the duplicated tail

# Build a breath-y vowel-ish grain and loop it
t = np.arange(seconds(0.35)) / SR
vowel = (
    0.6 * np.sin(2 * np.pi * 220 * t)
    + 0.35 * np.sin(2 * np.pi * 440 * t)
    + 0.2 * np.sin(2 * np.pi * 660 * t)
    + 0.08 * np.random.default_rng(1).normal(0, 1, len(t))
)
vowel = normalize(vowel)

loop_body = crossfade_loop(vowel, loop_start=1000, loop_end=len(vowel) - 500, fade=400)
sustained = np.tile(loop_body, 8)
sustained = apply_adsr(sustained, attack=0.15, decay=0.1, sustain=0.85, release=0.4)

hear(vowel, SR, title="Short source grain", show_spec=True)
hear(sustained, SR, title="Crossfade-looped sustain", show_spec=True, max_waveform_seconds=0.05)
"""
    ),
    md(
        """\
## Velocity layers

Harder hits → brighter / louder samples. We fake two layers (soft sine-rich vs. bright) and switch by velocity.
"""
    ),
    code(
        """\
def soft_layer(midi, dur=0.7):
    t = np.arange(seconds(dur)) / SR
    f = midi_to_hz(midi)
    y = 0.7 * np.sin(2 * np.pi * f * t) + 0.15 * np.sin(2 * np.pi * 2 * f * t)
    return apply_adsr(normalize(y), attack=0.01, decay=0.2, sustain=0.4, release=0.25)

def hard_layer(midi, dur=0.7):
    t = np.arange(seconds(dur)) / SR
    f = midi_to_hz(midi)
    y = sum((1 / k) * np.sin(2 * np.pi * f * k * t) for k in range(1, 10))
    y += 0.15 * np.random.default_rng(midi).normal(0, 1, len(t))
    return apply_adsr(normalize(y), attack=0.003, decay=0.15, sustain=0.35, release=0.2)

def velocity_sample(midi, velocity):
    # velocity 0..127
    soft = soft_layer(midi)
    hard = hard_layer(midi)
    mix_amt = np.clip(velocity / 127, 0, 1)
    return normalize((1 - mix_amt) * soft + mix_amt * hard) * (0.4 + 0.6 * mix_amt)

for vel, name in [(30, "soft (vel 30)"), (70, "medium (vel 70)"), (120, "hard (vel 120)")]:
    hear(velocity_sample(64, vel), SR, title=f"Velocity layer — {name}", show_spec=True)
"""
    ),
    md(
        """\
## Key zones (multisample map)

Split the keyboard: low zone uses a low root sample, high zone uses a high root. Less extreme stretching → more natural tone.
"""
    ),
    code(
        """\
low_root = soft_layer(48, dur=0.9)   # C3 sample
high_root = hard_layer(72, dur=0.9)  # C5 sample

def zoned_note(note_midi):
    if note_midi < 60:
        return linear_resample(low_root, semitone_ratio(note_midi - 48))
    return linear_resample(high_root, semitone_ratio(note_midi - 72))

notes = [48, 55, 60, 67, 72, 79]
parts = []
for n in notes:
    parts.append(zoned_note(n))
    parts.append(np.zeros(seconds(0.08)))
phrase = normalize(np.concatenate(parts))
hear(phrase, SR, title="Keyzone map: low root below C4, high root above", show_spec=True)
"""
    ),
    md(
        """\
## You should be able to…

- Shape the same buffer with different ADSRs
- Build a click-free crossfade loop
- Explain why velocity layers and keyzones beat extreme stretching

**Next:** [04 — Filters, FX & modulation](04_filters_fx_and_modulation.ipynb)
"""
    ),
]

# ---------------------------------------------------------------------------
# 04 — Filters, FX & modulation
# ---------------------------------------------------------------------------

nb04 = [
    md(
        """\
# 04 — Filters, FX & Modulation

**Level:** Intermediate → Advanced

Samplers rarely stop at envelopes. Tone controls, delay throws, and LFOs turn static recordings into moving instruments — the same moves you hear in classic house / hip-hop sampler workflows and modern ROMplers.
"""
    ),
    md("## Setup"),
    code(
        """\
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

from audio_utils import (
    SR, hear, normalize, seconds, midi_to_hz, apply_adsr,
    one_pole_lowpass, linear_resample, semitone_ratio,
)

def bright_sample(dur=1.5):
    t = np.arange(seconds(dur)) / SR
    f = midi_to_hz(60)
    y = sum((0.9 / k) * np.sin(2 * np.pi * f * k * t) for k in range(1, 16))
    y += 0.05 * np.random.default_rng(2).normal(0, 1, len(t))
    return apply_adsr(normalize(y), attack=0.01, decay=0.2, sustain=0.6, release=0.4)

src = bright_sample()
hear(src, SR, title="Bright source sample", show_spec=True)
"""
    ),
    md(
        """\
## Low-pass tone control

Close the filter → darker sample (classic “cutoff” knob). Compare one-pole (cheap) vs. Butterworth (steeper).
"""
    ),
    code(
        """\
def butter_lowpass(x, cutoff, order=4):
    b, a = butter(order, cutoff / (SR / 2), btype="low")
    return lfilter(b, a, x)

for cutoff in [8000, 2000, 600]:
    a = one_pole_lowpass(src, cutoff)
    b = butter_lowpass(src, cutoff)
    hear(a, SR, title=f"One-pole LPF @ {cutoff} Hz", show_spec=True)
    hear(b, SR, title=f"Butterworth LPF @ {cutoff} Hz", show_spec=True)
"""
    ),
    md(
        """\
## Filter sweep (envelope → cutoff)

Modulate cutoff over time — a staple of sampled bass / pad design.
"""
    ),
    code(
        """\
def sweeping_lpf(x, start_hz=4000, end_hz=300, sr=SR):
    x = np.asarray(x, dtype=np.float64).ravel()
    # Piecewise one-pole with slowly changing coefficient
    cutoffs = np.linspace(start_hz, end_hz, len(x))
    y = np.zeros_like(x)
    acc = 0.0
    for i, (sample, fc) in enumerate(zip(x, cutoffs)):
        coeff = np.exp(-2 * np.pi * fc / sr)
        acc = (1 - coeff) * sample + coeff * acc
        y[i] = acc
    return y

swept = sweeping_lpf(src, start_hz=6000, end_hz=250)
hear(swept, SR, title="Envelope filter sweep (bright → dark)", show_spec=True)
"""
    ),
    md(
        """\
## Tempo delay / slapback

A feedback delay is the sampler’s friend for space without a full reverb algorithm.
"""
    ),
    code(
        """\
def delay_fx(x, delay_s=0.22, feedback=0.35, mix_amt=0.4):
    x = np.asarray(x, dtype=np.float64).ravel()
    d = seconds(delay_s)
    y = np.zeros(len(x) + d * 4)
    y[: len(x)] += x
    for i in range(len(x)):
        y[i + d] += mix_amt * x[i]
        if i + 2 * d < len(y):
            y[i + 2 * d] += mix_amt * feedback * x[i]
        if i + 3 * d < len(y):
            y[i + 3 * d] += mix_amt * feedback ** 2 * x[i]
    return normalize(y)

# Short staccato hits into delay
hit = apply_adsr(src[: seconds(0.35)], attack=0.005, decay=0.1, sustain=0.0, release=0.05)
phrase = np.concatenate([hit, np.zeros(seconds(0.15)), hit, np.zeros(seconds(0.15)), hit])
wet = delay_fx(phrase, delay_s=0.18, feedback=0.45, mix_amt=0.5)
hear(phrase, SR, title="Dry staccato hits")
hear(wet, SR, title="Hits + slapback delay", show_spec=True)
"""
    ),
    md(
        """\
## LFO modulation

Low-frequency oscillators move parameters automatically — tremolo (amplitude) and wah-ish filter wobble.
"""
    ),
    code(
        """\
def tremolo(x, rate_hz=4.5, depth=0.7):
    t = np.arange(len(x)) / SR
    mod = (1 - depth) + depth * (0.5 * (1 + np.sin(2 * np.pi * rate_hz * t)))
    return x * mod

def lfo_filter(x, rate_hz=0.8, lo=400, hi=5000):
    t = np.arange(len(x)) / SR
    cutoffs = lo + (hi - lo) * (0.5 * (1 + np.sin(2 * np.pi * rate_hz * t)))
    y = np.zeros_like(x)
    acc = 0.0
    for i, (sample, fc) in enumerate(zip(x, cutoffs)):
        coeff = np.exp(-2 * np.pi * fc / SR)
        acc = (1 - coeff) * sample + coeff * acc
        y[i] = acc
    return y

pad = bright_sample(dur=2.5)
hear(tremolo(pad), SR, title="LFO tremolo (AM)", show_spec=True)
hear(lfo_filter(pad), SR, title="LFO filter wobble", show_spec=True)
"""
    ),
    md(
        """\
## Chorus-ish thickening

Two slightly detuned delayed copies → width. Common on sampled strings / guitars.
"""
    ),
    code(
        """\
def chorusish(x, depths_ms=(7, 11), detune=(0.997, 1.003)):
    x = np.asarray(x, dtype=np.float64).ravel()
    parts = [x]
    for ms, det in zip(depths_ms, detune):
        delayed = np.concatenate([np.zeros(seconds(ms / 1000)), x])[: len(x)]
        tuned = linear_resample(delayed, det)
        if len(tuned) < len(x):
            tuned = np.pad(tuned, (0, len(x) - len(tuned)))
        parts.append(tuned[: len(x)])
    return normalize(np.sum(parts, axis=0))

hear(chorusish(pad), SR, title="Chorus-ish detune thicken", show_spec=True)
"""
    ),
    md(
        """\
## You should be able to…

- Darken a sample with a low-pass and automate a sweep
- Add rhythmic space with a feedback delay
- Animate amplitude / cutoff with an LFO

**Next:** [05 — Mini sampler synth](05_mini_sampler_synth.ipynb)
"""
    ),
]

# ---------------------------------------------------------------------------
# 05 — Mini sampler synth
# ---------------------------------------------------------------------------

nb05 = [
    md(
        """\
# 05 — Mini Sampler Synth

**Level:** Advanced

Put the pieces together: a small `MiniSampler` that stores root samples, maps MIDI notes, applies ADSR + filter, and renders a sequenced phrase (melody + drums + FX).
"""
    ),
    md("## Setup"),
    code(
        """\
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

from audio_utils import (
    SR, hear, normalize, seconds, midi_to_hz, semitone_ratio,
    linear_resample, apply_adsr, one_pole_lowpass, mix,
)
"""
    ),
    md("## Design a tiny sample library"),
    code(
        """\
def synth_pluck(midi, dur=0.9, brightness=0.55):
    freq = midi_to_hz(midi)
    n = seconds(dur)
    delay = max(2, int(round(SR / freq)))
    rng = np.random.default_rng(100 + midi)
    buf = rng.uniform(-1, 1, delay)
    out = np.zeros(n)
    idx = 0
    for i in range(n):
        out[i] = buf[idx]
        buf[idx] = brightness * 0.5 * (buf[idx] + buf[(idx + 1) % delay])
        idx = (idx + 1) % delay
    return normalize(out)

def synth_kick(dur=0.45):
    t = np.arange(seconds(dur)) / SR
    # Pitch envelope: 120 Hz → 40 Hz
    freq = 120 * (40 / 120) ** (t / dur)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    body = np.sin(phase)
    click = np.exp(-t * 80) * np.random.default_rng(0).normal(0, 1, len(t)) * 0.4
    return apply_adsr(normalize(body + click), attack=0.001, decay=0.2, sustain=0.2, release=0.2)

def synth_snare(dur=0.35):
    t = np.arange(seconds(dur)) / SR
    noise = np.random.default_rng(1).normal(0, 1, len(t))
    tone = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 20)
    return apply_adsr(normalize(0.7 * noise + 0.5 * tone), attack=0.001, decay=0.15, sustain=0.05, release=0.1)

def synth_hat(dur=0.12):
    t = np.arange(seconds(dur)) / SR
    y = np.random.default_rng(2).normal(0, 1, len(t))
    y = one_pole_lowpass(y, 9000)  # still bright
    # crude high-pass via y - lowpass
    y = y - one_pole_lowpass(y, 5000)
    return apply_adsr(normalize(y), attack=0.001, decay=0.05, sustain=0.0, release=0.04)

# Preview library
for name, sig in [
    ("Pluck root C4", synth_pluck(60)),
    ("Kick", synth_kick()),
    ("Snare", synth_snare()),
    ("Hat", synth_hat()),
]:
    hear(sig, SR, title=name, show_spec=True)
"""
    ),
    md(
        """\
## `MiniSampler` engine

Zones, velocity → gain/brightness, ADSR, optional cutoff. This is a teaching model of a ROMpler voice path.
"""
    ),
    code(
        """\
class MiniSampler:
    def __init__(self, roots: dict[str, tuple[np.ndarray, int]]):
        \"\"\"roots: name → (buffer, root_midi)\"\"\"
        self.roots = roots

    def note(
        self,
        patch: str,
        midi: int,
        velocity: int = 100,
        attack=0.01,
        decay=0.12,
        sustain=0.5,
        release=0.2,
        cutoff_hz: float | None = None,
    ) -> np.ndarray:
        buf, root_midi = self.roots[patch]
        rate = semitone_ratio(midi - root_midi)
        x = linear_resample(buf, rate)
        # Velocity: gain + mild brightness via less filtering when hard
        vel = np.clip(velocity / 127, 0, 1)
        x = apply_adsr(x, attack=attack, decay=decay, sustain=sustain * vel, release=release)
        if cutoff_hz is not None:
            # Soft notes close the filter more
            fc = cutoff_hz * (0.4 + 0.6 * vel)
            x = one_pole_lowpass(x, fc)
        return normalize(x) * (0.35 + 0.65 * vel)

sampler = MiniSampler(
    {
        "pluck_low": (synth_pluck(48, dur=1.0), 48),
        "pluck_high": (synth_pluck(72, dur=1.0, brightness=0.65), 72),
        "kick": (synth_kick(), 60),
        "snare": (synth_snare(), 60),
        "hat": (synth_hat(), 60),
    }
)

# Zone helper for melodic patch
def melodic(midi, velocity=100):
    patch = "pluck_low" if midi < 60 else "pluck_high"
    return sampler.note(patch, midi, velocity=velocity, attack=0.005, decay=0.18, sustain=0.35, release=0.25, cutoff_hz=5000)

hear(melodic(52, 60), SR, title="Zoned pluck — soft low note")
hear(melodic(76, 120), SR, title="Zoned pluck — hard high note", show_spec=True)
"""
    ),
    md("## Sequencer — place notes on a timeline"),
    code(
        """\
def place(events, bpm=96):
    \"\"\"events: list of (beat, signal). Return mixed timeline.\"\"\"
    beat_s = 60.0 / bpm
    rendered = []
    for beat, sig in events:
        start = int(round(beat * beat_s * SR))
        rendered.append((start, np.asarray(sig, dtype=np.float64).ravel()))
    n = max(start + len(sig) for start, sig in rendered) + seconds(0.5)
    out = np.zeros(n)
    for start, sig in rendered:
        out[start : start + len(sig)] += sig
    return normalize(out)

# 2-bar groove
melody_notes = [
    (0.0, 60), (0.5, 63), (1.0, 67), (1.5, 63),
    (2.0, 70), (2.5, 67), (3.0, 63), (3.5, 60),
    (4.0, 58), (4.5, 60), (5.0, 63), (5.5, 67),
    (6.0, 65), (7.0, 63),
]
mel_events = [(b, melodic(n, velocity=90 + (i % 3) * 10)) for i, (b, n) in enumerate(melody_notes)]

drum_events = []
for bar in (0, 4):
    for step in range(8):
        beat = bar + step * 0.5
        drum_events.append((beat, sampler.note("hat", 60, velocity=70, attack=0.001, decay=0.04, sustain=0.0, release=0.03)))
    drum_events.append((bar + 0.0, sampler.note("kick", 60, velocity=120, attack=0.001, decay=0.2, sustain=0.15, release=0.15)))
    drum_events.append((bar + 1.0, sampler.note("snare", 60, velocity=110)))
    drum_events.append((bar + 2.0, sampler.note("kick", 60, velocity=100)))
    drum_events.append((bar + 2.5, sampler.note("kick", 60, velocity=80)))
    drum_events.append((bar + 3.0, sampler.note("snare", 60, velocity=115)))

melody = place(mel_events, bpm=96)
drums = place(drum_events, bpm=96)
hear(melody, SR, title="Melody stem (zoned plucks)", show_spec=True)
hear(drums, SR, title="Drum stem", show_spec=True)
"""
    ),
    md("## Mix bus + FX"),
    code(
        """\
def delay_fx(x, delay_s=0.31, feedback=0.3, mix_amt=0.28):
    d = seconds(delay_s)
    y = np.zeros(len(x) + d * 3)
    y[: len(x)] = x
    for i in range(len(x)):
        y[i + d] += mix_amt * x[i]
        if i + 2 * d < len(y):
            y[i + 2 * d] += mix_amt * feedback * x[i]
    return y

melody_wet = delay_fx(one_pole_lowpass(melody, 4500))
# Match lengths and blend
bus = mix([melody_wet, drums], gains=[0.85, 0.9])
# Soft clip for glue
bus = np.tanh(1.2 * bus)
bus = normalize(bus, peak=0.95)

hear(bus, SR, title="Full mix — mini sampler jam", show_spec=True, max_waveform_seconds=None)
"""
    ),
    md(
        """\
## Parameter exploration — same sequence, different tone
"""
    ),
    code(
        """\
# Darker, slower pad-like articulation of the same pitches
pad_events = []
for b, n in melody_notes:
    patch = "pluck_low" if n < 60 else "pluck_high"
    pad_events.append(
        (
            b,
            sampler.note(
                patch, n, velocity=75,
                attack=0.2, decay=0.3, sustain=0.7, release=0.5,
                cutoff_hz=1800,
            ),
        )
    )
pad_take = place(pad_events, bpm=80)
hear(pad_take, SR, title="Same pitches, pad articulation + closed filter", show_spec=True)
"""
    ),
    md(
        """\
## You should be able to…

- Describe a sampler voice path: zone → rate → ADSR → filter → FX
- Sequence melodic and percussive patches onto a beat grid
- Change articulation without changing the stored samples

### Where to go next

- Independent time-stretch / pitch-shift (phase vocoder, granular)
- Round-robin layers and release samples
- Convolution reverb and modulation FX racks
- Loading real WAV libraries into the same `MiniSampler` API
"""
    ),
]


def main() -> None:
    write("01_samples_and_waveforms.ipynb", nb01)
    write("02_playback_rate_and_pitch.ipynb", nb02)
    write("03_envelopes_loops_and_zones.ipynb", nb03)
    write("04_filters_fx_and_modulation.ipynb", nb04)
    write("05_mini_sampler_synth.ipynb", nb05)


if __name__ == "__main__":
    main()
