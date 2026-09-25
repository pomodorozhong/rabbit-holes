"""Shared helpers for sampler-based synthesis notebooks.

Every demo clip should be both *viewable* (waveform / spectrogram) and
*playable* (IPython Audio widget). Prefer ``hear()`` over bare ``Audio``.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio, display

SR = 44_100  # default project sample rate


def normalize(x: np.ndarray, peak: float = 0.9) -> np.ndarray:
    """Peak-normalize a mono signal; leave silence unchanged."""
    x = np.asarray(x, dtype=np.float64)
    m = np.max(np.abs(x))
    if m < 1e-12:
        return x
    return (peak / m) * x


def seconds(n: float, sr: int = SR) -> int:
    """Convert duration in seconds to sample count."""
    return int(round(n * sr))


def time_axis(x: np.ndarray, sr: int = SR) -> np.ndarray:
    return np.arange(len(x)) / sr


def plot_waveform(
    x: np.ndarray,
    sr: int = SR,
    title: str = "Waveform",
    ax: plt.Axes | None = None,
    max_seconds: float | None = None,
) -> plt.Axes:
    x = np.asarray(x, dtype=np.float64).ravel()
    if max_seconds is not None:
        x = x[: seconds(max_seconds, sr)]
    t = time_axis(x, sr)
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 2.4))
    ax.plot(t, x, color="#1f6f8b", linewidth=0.8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)
    ax.set_xlim(t[0] if len(t) else 0, t[-1] if len(t) else 1)
    ax.grid(True, alpha=0.3)
    return ax


def plot_spectrogram(
    x: np.ndarray,
    sr: int = SR,
    title: str = "Spectrogram",
    ax: plt.Axes | None = None,
    nperseg: int = 1024,
) -> plt.Axes:
    from scipy.signal import spectrogram

    x = np.asarray(x, dtype=np.float64).ravel()
    f, t, sxx = spectrogram(x, fs=sr, nperseg=min(nperseg, max(16, len(x))))
    sxx_db = 10 * np.log10(sxx + 1e-12)
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 3.2))
    mesh = ax.pcolormesh(t, f, sxx_db, shading="auto", cmap="magma")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_xlabel("Time (s)")
    ax.set_title(title)
    ax.set_ylim(0, min(sr / 2, 8000))
    plt.colorbar(mesh, ax=ax, label="dB", pad=0.02)
    return ax


def hear(
    x: np.ndarray,
    sr: int = SR,
    title: str = "Audio",
    *,
    show_spec: bool = False,
    max_waveform_seconds: float | None = 2.0,
    normalize_peak: float | None = 0.9,
) -> Audio:
    """Plot waveform (and optional spectrogram), then return a playable Audio widget.

    Always call this (or display its return value) for every clip so the notebook
    keeps both a visual and an audible representation.
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    if normalize_peak is not None:
        x = normalize(x, peak=normalize_peak)

    if show_spec:
        fig, axes = plt.subplots(
            2, 1, figsize=(10, 5.2), gridspec_kw={"height_ratios": [1, 1.3]}
        )
        plot_waveform(x, sr, title=f"{title} — waveform", ax=axes[0], max_seconds=max_waveform_seconds)
        plot_spectrogram(x, sr, title=f"{title} — spectrogram", ax=axes[1])
        fig.tight_layout()
        plt.show()
    else:
        fig, ax = plt.subplots(figsize=(10, 2.4))
        plot_waveform(x, sr, title=title, ax=ax, max_seconds=max_waveform_seconds)
        fig.tight_layout()
        plt.show()

    audio = Audio(x, rate=sr, normalize=False)
    display(audio)
    return audio


def midi_to_hz(midi: float) -> float:
    return 440.0 * (2.0 ** ((midi - 69.0) / 12.0))


def hz_to_midi(freq: float) -> float:
    return 69.0 + 12.0 * np.log2(freq / 440.0)


def semitone_ratio(semitones: float) -> float:
    return 2.0 ** (semitones / 12.0)


def apply_adsr(
    x: np.ndarray,
    sr: int = SR,
    attack: float = 0.01,
    decay: float = 0.1,
    sustain: float = 0.7,
    release: float = 0.2,
) -> np.ndarray:
    """Apply a classic ADSR amplitude envelope (sustain fills the middle)."""
    x = np.asarray(x, dtype=np.float64).ravel()
    n = len(x)
    a = seconds(attack, sr)
    d = seconds(decay, sr)
    r = seconds(release, sr)
    # Keep envelope lengths feasible for short clips.
    a = min(a, n // 4)
    d = min(d, n // 4)
    r = min(r, max(1, n - a - d))
    s_len = max(0, n - a - d - r)

    env = np.concatenate(
        [
            np.linspace(0.0, 1.0, a, endpoint=False) if a else np.array([]),
            np.linspace(1.0, sustain, d, endpoint=False) if d else np.array([]),
            np.full(s_len, sustain),
            np.linspace(sustain, 0.0, r) if r else np.array([]),
        ]
    )
    if len(env) < n:
        env = np.pad(env, (0, n - len(env)))
    elif len(env) > n:
        env = env[:n]
    return x * env


def linear_resample(x: np.ndarray, rate: float) -> np.ndarray:
    """Resample by playback-rate factor (rate>1 → higher/faster)."""
    x = np.asarray(x, dtype=np.float64).ravel()
    if rate <= 0:
        raise ValueError("rate must be positive")
    n_out = max(1, int(round(len(x) / rate)))
    t_out = np.arange(n_out) * rate
    t_in = np.arange(len(x), dtype=np.float64)
    return np.interp(t_out, t_in, x, left=0.0, right=0.0)


def one_pole_lowpass(x: np.ndarray, cutoff_hz: float, sr: int = SR) -> np.ndarray:
    """Simple one-pole low-pass filter (cheap sampler-style tone control)."""
    from scipy.signal import lfilter

    x = np.asarray(x, dtype=np.float64).ravel()
    # Clamp to avoid unstable / useless coefficients.
    cutoff_hz = float(np.clip(cutoff_hz, 20.0, sr * 0.45))
    # y[n] = (1-a)*x[n] + a*y[n-1]
    a = np.exp(-2.0 * np.pi * cutoff_hz / sr)
    return lfilter([1.0 - a], [1.0, -a], x)


def mix(tracks: list[np.ndarray], gains: list[float] | None = None) -> np.ndarray:
    """Sum mono tracks of possibly different lengths."""
    if not tracks:
        return np.zeros(1)
    if gains is None:
        gains = [1.0] * len(tracks)
    n = max(len(t) for t in tracks)
    out = np.zeros(n, dtype=np.float64)
    for t, g in zip(tracks, gains):
        t = np.asarray(t, dtype=np.float64).ravel()
        out[: len(t)] += g * t
    return out
