# Can a Bard Hear Doppler in a Charging Fighter’s War Cry?

A D&D-flavored walk through the **Doppler effect**: how much pitch shift humans can notice, how fast a sound source must move to produce it, and whether a bard could hear that rise when a fighter charges straight at them.

## Quick answer

Assuming ideal listening (steady tone, head-on approach, ~20 °C air, speed of sound ≈ 343 m/s):

| Threshold | Approaching speed | Everyday comparison |
|-----------|-------------------|---------------------|
| Just-noticeable (~5 cents) | ~1.0 m/s (~3.6 km/h) | walking pace |
| One semitone (100 cents) | ~19.3 m/s (~69 km/h) | city driving |

A common D&D charge (30–60 ft/round ≈ 1.5–3.0 m/s) is already enough for a keen ear to notice. A full musical semitone would need something more like a car than a fighter.

## Run the notebook

```bash
cd topics/doppler_semitone
uv sync
uv run jupyter notebook doppler_semitone.ipynb
```

Or execute all cells headlessly:

```bash
uv run jupyter nbconvert --to notebook --execute doppler_semitone.ipynb --inplace
```

## What’s in the notebook

The notebook starts with the Doppler formula, then pitch discrimination (~5 cents vs one semitone), then solves for the speeds those thresholds imply, and finally plugs in D&D movement to answer the bard question.

## Physics (stationary observer, moving source)

$$
f' = f \cdot \frac{v}{v \mp v_s}
$$

A pitch interval of $c$ cents is the frequency ratio $r = 2^{c/1200}$. Solving for source speed $v_s$ gives different values for approach vs. recession because the Doppler map is asymmetric.

## Sources

| Constant / rule | Value used | Link |
|-----------------|------------|------|
| Doppler (moving source) | $f' = f\,v/(v\mp v_s)$ | [HyperPhysics](https://hyperphysics.gsu.edu/hbase/Sound/dopp.html), [Wikipedia](https://en.wikipedia.org/wiki/Doppler_effect) |
| Speed of sound (dry air) | ~331.3√(1+T/273.15) m/s; ~343 m/s at 20 °C | [HyperPhysics](https://hyperphysics.gsu.edu/hbase/Sound/souspe.html), [OpenStax](https://openstax.org/books/university-physics-volume-1/pages/17-2-speed-of-sound) |
| Cent / semitone | 100 cents = 1 semitone | [HyperPhysics](http://hyperphysics.phy-astr.gsu.edu/hbase/Music/cents.html), [Wikipedia](https://en.wikipedia.org/wiki/Cent_(music)) |
| Pitch JND | ~5 cents | [HyperPhysics](http://hyperphysics.phy-astr.gsu.edu/hbase/Music/cents.html), [Wikipedia — JND](https://en.wikipedia.org/wiki/Just-noticeable_difference) |
| D&D round | 6 seconds | [5e SRD — Combat](https://www.5esrd.com/gamemastering/combat/) |
| Typical walk speed | 30 ft/round | [5e SRD — Human](https://www.5esrd.com/races/human/) |
| Dash | +speed that turn (e.g. 30→60 ft) | [5e SRD — Combat](https://www.5esrd.com/gamemastering/combat/) |
| Foot → meter | 1 ft = 0.3048 m (exact) | [NIST](https://www.nist.gov/pml/owm/si-units-length) |
| Official SRD | — | [Wizards SRD](https://dnd.wizards.com/resources/systems-reference-document) |
