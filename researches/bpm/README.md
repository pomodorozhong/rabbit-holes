# BPM — Beat Per Minute: Theory, Common Tempos & Interactive Practice Tool

A research notebook covering the science and practice of musical tempo, with an embedded **interactive web metronome** built entirely in browser technologies.

## What's inside

| Section | Content |
|---|---|
| 1. What is a beat? | Beat period, frequency, IBI — formulas and unit table |
| 2. IBI vs BPM curve | Annotated plot: Largo → Andante → Allegro → Presto |
| 3. Classical tempo markings | Larghissimo → Prestissimo, BPM ranges as a horizontal bar chart |
| 4. Genre BPM landscape | Ballad, Hip-Hop, Pop, House, Techno, D&B … colour-coded range chart |
| 5. Beat waveform | 4-beat 120 BPM metronome click rendered as a NumPy waveform |
| 6. BPM ruler | Table + grouped bar chart of note durations across 7 tempos & 6 subdivisions |
| 7. Half-time & double-time | How a 170 BPM D&B track feels like 85 BPM; visualised with a 3-line plot |
| 8. **Interactive metronome** | Full Web Audio API + tap tempo tool embedded in the notebook output |
| 9. Tap tempo math | Convergence simulation: how many taps needed to estimate BPM accurately |
| 10. Key takeaways | Summary table |

## Interactive metronome features

- BPM slider (20 – 300)
- **Tap Tempo** — click the button or press `Space` / `T`; averages the last 5 taps
- Web Audio API synthesised click: 1000 Hz sine burst, accent on beat 1 at 1200 Hz
- Visual flash overlay on every beat (brighter accent on beat 1)
- Beat-dot grid with animated highlight
- Subdivision bar (quarter / 8th / 16th)
- Time signature selector: 2/4, 3/4, 4/4, 6/8
- Live info panel: beat period, IBI, bar duration

## Quick answer

> **What BPM should I practice at?**
>
> - Start 20–30% slower than your target tempo; a common classical rule of thumb.
> - Pop and EDM producers often lock to 120–128 BPM — the "sweet spot" where most people instinctively tap their foot.
> - Drum & Bass sits around 174 BPM, but the snare on beat 3 creates a half-time feel at 87 BPM.

## Run the notebook

```bash
cd researches/bpm
uv sync
uv run jupyter notebook bpm_research.ipynb
```

Or with plain pip:

```bash
cd researches/bpm
pip install matplotlib numpy jupyter ipykernel
jupyter notebook bpm_research.ipynb
```
