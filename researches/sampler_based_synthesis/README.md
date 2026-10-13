# Sampler-Based Synthesis

A progressive Jupyter series on **sampler-based synthesis**: building musical sound from recorded (or synthetic) snippets — pitch shifting by playback rate, envelopes, loops, keyzones, filters, and a tiny end-to-end sampler.

Unlike subtractive or FM synthesis (which *generate* oscillators from scratch), a sampler **plays back stored audio** and shapes it with rate, envelope, filter, and mapping rules. Classic ROMplers, MPC-style drum machines, and many modern soft-synths are sampler engines under the hood.

## Learning path

Work through the notebooks in order. Difficulty increases gradually; each notebook ends with a short “you should be able to…” checklist.

| # | Notebook | Level | What you’ll hear & see |
|---|----------|-------|------------------------|
| 01 | [`01_samples_and_waveforms.ipynb`](01_samples_and_waveforms.ipynb) | Beginner | PCM basics; sine / noise / pluck clips with waveforms |
| 02 | [`02_playback_rate_and_pitch.ipynb`](02_playback_rate_and_pitch.ipynb) | Beginner→Intermediate | Pitch by rate (`2^(n/12)`); chromatic one-shot sampler |
| 03 | [`03_envelopes_loops_and_zones.ipynb`](03_envelopes_loops_and_zones.ipynb) | Intermediate | ADSR, crossfade loops, velocity / key zones |
| 04 | [`04_filters_fx_and_modulation.ipynb`](04_filters_fx_and_modulation.ipynb) | Intermediate→Advanced | Tone filters, delay, LFO sweeps on samples |
| 05 | [`05_mini_sampler_synth.ipynb`](05_mini_sampler_synth.ipynb) | Advanced | Full mini sampler: melody + drums + FX chain |

Shared helpers live in [`audio_utils.py`](audio_utils.py). The key helper is **`hear(signal, sr, title=...)`**: it always plots a waveform (optional spectrogram) and shows a playable `IPython.display.Audio` widget so every clip is viewable and audible.

## Run the notebooks

```bash
cd researches/sampler_based_synthesis
uv sync
uv run jupyter notebook
```

Or execute all notebooks headlessly (embeds outputs):

```bash
for nb in 0*.ipynb; do
  uv run jupyter nbconvert --to notebook --execute "$nb" --inplace
done
```

## Mental model

```text
[sample buffer]
      │
      ├─▶ playback rate  →  pitch + duration
      ├─▶ loop / one-shot
      ├─▶ ADSR amplitude
      ├─▶ filter / FX
      └─▶ keyzone / velocity map
              │
              ▼
           output
```

## Notes

- Sample rate defaults to **44.1 kHz**.
- Instrument-like clips are **synthesized in-notebook** (no external sample packs), so the repo stays small and reproducible.
- Generated `.wav` / plot image files are gitignored; notebook outputs carry the audio widgets and figures.
