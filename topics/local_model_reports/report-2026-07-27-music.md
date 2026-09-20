# Local Music Generation Models

**Compiled:** 2026-07-27  
**Hardware target:** Apple **M2 MacBook Pro, 16 GB unified memory** (same machine as [report-2026-07-17](./report-2026-07-17.md))  
**Scope:** Open-weight / locally runnable music & audio generation — not Suno/Udio APIs  
**Community sources:** [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/), [r/StableDiffusion](https://www.reddit.com/r/StableDiffusion/) (via Arctic Shift archive)

---

## TL;DR

| Question | Short answer |
| --- | --- |
| **Clip or full song?** | Older stack = **short clips** (~10–47 s). 2025–26 models (ACE-Step, DiffRhythm, SongGeneration, YuE) = **full songs** (~2–10 min). |
| **Endless streaming?** | **Not natively.** Autoregressive models can *continue* via sliding-window; diffusion models generate fixed lengths. “Radio forever” needs a loop/continuation wrapper ([ACE-Step jukebox](https://www.reddit.com/r/LocalLLaMA/comments/1qxn3pa/i_made_an_ai_jukebox_with_acestep_15_free_nonstop/), [24/7 radio](https://www.reddit.com/r/LocalLLaMA/comments/1v3woyv/247_subreddit_radio/)). |
| **Typical VRAM** | **4–8 GB** entry (ACE-Step DiT-only / MusicGen-small); **12–24 GB** comfortable full-song + vocals; **22–28 GB** for SongGeneration-large / YuE-class. Community often quotes YuE GP “&lt;10 GB” and ACE-Step “&lt;4 GB” with heavy offload. |
| **On your 16 GB M2?** | **Yes:** MusicGen (MLX), Stable Audio Open (MLX), ACE-Step 2B turbo (DiT-only / light LM). **Maybe:** DiffRhythm chunked. **No daily use:** SongGeneration large, YuE, ACE-Step XL. |
| **vs LLMs** | Different stack (PyTorch/MLX audio pipelines, not GGUF/Ollama), peak memory at **decode**, licenses messier, output is WAV not tokens. GGML music paths ([audio.cpp](https://www.reddit.com/r/LocalLLaMA/comments/1um2tbf/audiocpp_the_sound_of_ggml_cggml_native_acestep/), [KoboldCpp](https://www.reddit.com/r/LocalLLaMA/comments/1rxunqq/koboldcpp_1110_3_yr_anniversary_edition_native/)) are emerging but thinner than chat. |

---

## Format: clip vs song vs endless

### Two product eras

| Era | Models | Typical length | Vocals / lyrics |
| --- | --- | --- | --- |
| **Clip generators (2023–24)** | MusicGen, MAGNeT, Stable Audio Open / Open Small | **~10–47 s** | Mostly instrumental / SFX; not “verse–chorus song” |
| **Song generators (2025–26)** | ACE-Step 1.5, DiffRhythm, SongGeneration (LeVo), YuE | **~1.5–10 min** | Lyrics + singing common |

### Per-model duration caps

| Model | Native max (approx.) | Continuation / streaming |
| --- | --- | --- |
| **MusicGen** | **~30 s** per pass | Yes — condition on audio tail / sliding window; HF streamer can emit chunks while generating. Not infinite *without* a wrapper. |
| **MAGNeT** | **~10–30 s** (checkpoint-dependent) | Fixed window; continuation less polished than MusicGen |
| **Stable Audio Open Small** | **~11 s** | Fixed; great for loops / oneshots |
| **Stable Audio Open 1.0** | **~47 s** | Fixed; chunked VAE decode to cut peak VRAM |
| **DiffRhythm** | **~1 m 35 s** (base) / **~4 m 45 s** (full) | Song extension supported; not endless radio |
| **ACE-Step 1.5** | **10 s – 10 min** (VRAM-tiered; often 3–8 min on consumer GPUs) | Full-song planner (LM) + DiT; still a **bounded** job, not live stream |
| **SongGeneration** | **~2 m 30 s – 4 m 30 s** | Full songs; no endless stream |
| **YuE** | Multi-segment full songs | Heavy; segment chaining, not live endless |

### Can it stream endlessly?

**No mainstream local model is a true endless music radio out of the box.**

What people actually do:

1. **Autoregressive continuation** (MusicGen): feed the last N seconds as prompt → next segment → crossfade. Can run indefinitely with quality drift.
2. **Chunk streamers** (HF MusicGen streamer, community `musicgen-stream`): play audio as tokens decode — still capped by `max_new_tokens` / window unless you loop.
3. **Diffusion / DiT song models** (ACE-Step, DiffRhythm, Stable Audio): generate a **whole latent**, then decode. You get a finished file (or long fixed clip), not token-by-token radio.

For “endless,” treat it as an **application layer** on top of MusicGen-style continuation — not a model feature. Reddit examples of the app-layer approach:

- [AI Jukebox with ACE-Step 1.5](https://www.reddit.com/r/LocalLLaMA/comments/1qxn3pa/i_made_an_ai_jukebox_with_acestep_15_free_nonstop/) — queued generations / “nonstop” station, not token streaming  
- [24/7 Subreddit Radio](https://www.reddit.com/r/LocalLLaMA/comments/1v3woyv/247_subreddit_radio/) — ACE-Step songs + LLM DJ on 3090s  
- [Breaking the music supply constraint](https://www.reddit.com/r/LocalLLaMA/comments/1treuy3/breaking_the_music_supply_constraint/) — self-hosted catalog replacing subscriptions (302 comments)

---

## Common VRAM / memory requirements

Numbers are **indicative** (bf16/fp16, batch 1). Offload, INT8, and chunked decode change them a lot.

| Tier | VRAM / unified | What fits |
| --- | --- | --- |
| **Entry** | **~4–6 GB** | ACE-Step 2B DiT-only (turbo); MusicGen-small |
| **Consumer** | **~8–12 GB** | ACE-Step 2B + 0.6B LM; DiffRhythm (chunked); MusicGen-medium; Stable Audio Open with chunk decode |
| **Comfortable** | **~16–24 GB** | ACE-Step longer songs / larger LM; MusicGen-large; SongGeneration-base |
| **Heavy** | **~22–28 GB+** | SongGeneration-large / v2-large; ACE-Step XL without painful offload; YuE full pipeline |

### ACE-Step 1.5 VRAM tiers (official-ish)

| VRAM | DiT | LM | Max duration (order of mag.) |
| --- | --- | --- | --- |
| ≤4–6 GB | 2B turbo, DiT-only | off | ~3–6 min |
| 6–12 GB | 2B turbo/sft | 0.6B optional | ~4–6 min |
| 12–20 GB | 2B or XL+offload | 0.6B / 1.7B | ~4–8 min |
| ≥20–24 GB | XL comfortable | up to 4B LM | up to ~10 min |

Weights: 2B DiT ~**4.7 GB**; XL 4B DiT ~**9 GB** bf16.

### Other published footprints

| Model | Memory notes |
| --- | --- |
| **MusicGen** | Official: prefer **~16 GB** GPU for medium; small runs on much less. MLX Mac: small ~**1.2 GB** download; large ~**6.5 GB** weights + runtime headroom |
| **Stable Audio Open 1.0** | DiT ~**6 GB**; **VAE decode** can spike toward **~14 GB** unless chunked |
| **Stable Audio Open Small** | ~**341M**; designed for **edge / phone**; easy on laptop |
| **DiffRhythm** | **≥8 GB** with `--chunked` |
| **SongGeneration** | base **~10–16 GB**; large / v2-large **~22–28 GB** |
| **YuE** | Quantized forks claim **~12–16 GB**; full multi-segment wants big GPUs. [YuE GP](https://www.reddit.com/r/StableDiffusion/comments/1iegcxy/yue_gp_runs_the_best_open_source_song_generator/) marketed as **&lt;10 GB**; early reports also said ~**90 s on a 4090** before longer multi-segment runs ([license / length thread](https://www.reddit.com/r/StableDiffusion/comments/1ie0rar/yue_license_updated_to_apache_2_limited_rn_to_90s/)) |

Community VRAM reality checks (take with salt — configs differ):

- ACE-Step pitched as potato-GPU / **&lt;4 GB** ahead of 1.5: [LocalLLaMA pre-launch](https://www.reddit.com/r/LocalLLaMA/comments/1qtqspu/1_day_left_until_acestep_15_opensource_music_gen/)  
- XL Turbo anecdotes on **8 GB** laptops (offload / BF16): [AceStep XL + LTX on 8 GB 5060](https://www.reddit.com/r/StableDiffusion/comments/1sj8qh2/acestep_15_xl_turbo_ltx_23_on_an_8gb_rtx_5060/), [BF16 conversion ~10 GB weights](https://www.reddit.com/r/StableDiffusion/comments/1sgiqg7/acestep_15_xl_turbo_bf16_version_converted_from/)  
- DiffRhythm: full songs with vocals announced on LocalLLaMA ([thread](https://www.reddit.com/r/LocalLLaMA/comments/1j38499/diffrhythm_aslplab_generate_full_songs_4_min_with/)); watch for memorization risk ([Avicii clone report](https://www.reddit.com/r/LocalLLaMA/comments/1m4yo0g/diffrhythm_12_music_generation_model_produces/))

---

## What you can run on a 16 GB M2 Mac

Same budget rules as the LLM report: macOS + apps leave ~**8–11 GB** usable; Metal GPU working set is often capped near **~10.5 GB** on ≤32–64 GB Macs.

### Start here (practical)

| Role | Pick | Fit on 16 GB M2 | Notes |
| --- | --- | --- | --- |
| **Best “full song” local** | **ACE-Step 1.5** 2B turbo, DiT-only (or +0.6B LM if memory allows) | **Yes / tight** | Official **macOS + MLX** scripts & portable zip. Prefer short–medium songs; close other apps. |
| **Fast instrumental clips** | **MusicGen** small/medium via [musicgen-mlx](https://github.com/andrade0/musicgen-mlx) | **Yes** | ~30 s; stereo large is slower / heavier |
| **Loops / SFX / textures** | **Stable Audio Open Small** or **Open 1.0** via MLX (`mlx-audiogen` / Anvil) | **Yes** (Small easy; 1.0 use chunk decode) | ≤11 s or ≤47 s — not full songs |
| **Lyrics→song (lighter than YuE)** | **DiffRhythm** | **Maybe** | macOS supported; stay on base + `--chunked`; expect thrash if LM/UI open |
| **Commercial-grade lyrics songs** | **SongGeneration** / **YuE** | **No** for daily 16 GB | SongGen-Mac lists **≥24 GB** minimum; YuE Mac is unofficial and slow. Community Mac song ports exist for other stacks ([Khala → Apple Silicon](https://www.reddit.com/r/StableDiffusion/comments/1tuqklr/you_can_now_make_mac_generate_high_quality_songs/)) but still want more RAM than 16 GB for “high quality.” |

### Verdict matrix

| Model | 16 GB M2 | Why |
| --- | --- | --- |
| MusicGen-small / stereo-small | ✅ | Comfortable MLX path |
| MusicGen-medium | ✅ | OK if nothing else heavy |
| MusicGen-large | ⚠️ | Fits weights; generation slow / swap risk |
| Stable Audio Open Small | ✅ | Best “always works” short audio |
| Stable Audio Open 1.0 | ⚠️ | Watch VAE decode peak |
| ACE-Step 2B turbo | ✅ / ⚠️ | Best Mac song option; DiT-only safest |
| ACE-Step XL (4B) | ❌ | Needs ~12–20 GB class GPU budget |
| DiffRhythm-base | ⚠️ | Possible with chunking |
| DiffRhythm-full | ❌ / ⚠️ | Long latents + 16 GB = painful |
| SongGeneration base/large | ❌ | Target **32–64 GB** unified |
| YuE | ❌ | Skip on this machine |

**Recommended Mac stack:** ACE-Step 1.5 (songs) + MusicGen-MLX or Stable Audio Open Small (sketches / loops). Keep one model loaded at a time.

---

## Notable models & features

### ACE-Step 1.5 — current open-source song leader

- Hybrid **LM planner** (Qwen3-based 0.6B/1.7B/4B) + **DiT** decoder (2B or XL 4B)
- Full songs **10 s–10 min**, multilingual lyrics, covers, repaint, vocal→BGM, stems, LoRA from a handful of tracks
- Very fast on NVIDIA (sub-10 s / song on 3090-class); usable on Apple Silicon via **MLX**
- MIT project license; portable Mac/Windows packages
- Reddit: [1.5 pre-hype (&lt;4 GB / Suno-class claims)](https://www.reddit.com/r/LocalLLaMA/comments/1qtqspu/1_day_left_until_acestep_15_opensource_music_gen/), [XL models available](https://www.reddit.com/r/LocalLLaMA/comments/1semfx5/ace_step_15_xl_models_available/), [r/SD XL drop](https://www.reddit.com/r/StableDiffusion/comments/1ses85i/ace_step_15_xl_is_out/)

### MusicGen (Meta AudioCraft)

- Autoregressive EnCodec tokens; **text→music**, melody conditioning on some checkpoints
- Instrumental bias; **~30 s** native; continuation ecosystem is mature
- Best-documented **streaming / infinite-extend** pattern among open models
- MLX port for Apple Silicon
- Reddit: [MusicGen Web / Transformers.js](https://www.reddit.com/r/LocalLLaMA/comments/1c2d5ff/musicgen_web_inbrowser_texttomusic_w/), [SD MusicGen setup guide](https://www.reddit.com/r/StableDiffusion/comments/1i26q0j/comprehensive_tutorial_on_how_to_set_up_musicgen/)

### Stable Audio Open / Open Small (Stability)

- Latent **DiT**; excellent for **sound design, loops, textures**
- Open 1.0 ≤**47 s**; Small ≤**11 s** and edge-friendly
- Community License (check commercial terms); MLX via `mlx-audiogen`
- Now also showing up in GGML runtimes alongside ACE-Step ([audio.cpp music release](https://www.reddit.com/r/LocalLLaMA/comments/1um2tbf/audiocpp_the_sound_of_ggml_cggml_native_acestep/))

### DiffRhythm

- Diffusion song model with **lyrics**, dynamic length, song extension
- Explicit **macOS** support; **8 GB** floor with chunked decode
- Reddit: [full songs w/ vocals](https://www.reddit.com/r/LocalLLaMA/comments/1j38499/diffrhythm_aslplab_generate_full_songs_4_min_with/), [DiffRhythm+](https://www.reddit.com/r/LocalLLaMA/comments/1m3643z/diffrhythm_is_coming_soon/), [verbatim-track risk](https://www.reddit.com/r/LocalLLaMA/comments/1m4yo0g/diffrhythm_12_music_generation_model_produces/)

### SongGeneration (Tencent LeVo / v2)

- Strong **lyrics + vocals**, multilingual v2-large
- Memory-hungry; Mac ports want **24 GB+** unified
- Partial MLX token-gen + PyTorch decode bridges exist

### YuE

- High-quality lyric songs; **CUDA-first**, poor Mac story
- Treat as cloud/GPU-box model unless you enjoy pain
- Reddit inflection point for “local Suno”: [r/SD “Suno at home”](https://www.reddit.com/r/StableDiffusion/comments/1ibyrc0/we_now_have_suno_ai_at_home_with_this_new_local/) (787↑), [r/LocalLLaMA drop](https://www.reddit.com/r/LocalLLaMA/comments/1ibzmef/new_bomb_dropped_from_asian_researchers_yue_open/), demand context [“give up a kidney…”](https://www.reddit.com/r/LocalLLaMA/comments/1ia40om/would_give_up_a_kidney_for_a_local_audio_model/)

---

## Special considerations vs running LLMs

| Topic | LLMs (your usual stack) | Music models |
| --- | --- | --- |
| **Runtime** | Ollama / LM Studio / llama.cpp / MLX-LM, GGUF everywhere | Mostly **PyTorch** or **project-specific MLX**; GGML catching up ([audio.cpp](https://www.reddit.com/r/LocalLLaMA/comments/1um2tbf/audiocpp_the_sound_of_ggml_cggml_native_acestep/), [acestep.cpp / Metal](https://www.reddit.com/r/LocalLLaMA/comments/1ry1dy1/acestepcpp_portable_c17_implementation_of_acestep/), [KoboldCpp music](https://www.reddit.com/r/LocalLLaMA/comments/1rxunqq/koboldcpp_1110_3_yr_anniversary_edition_native/)) |
| **Memory shape** | Weights + **KV cache** grow with context | Weights + **latents / codebooks** grow with **duration** + channels; **VAE/codec decode** often peaks higher than the denoiser |
| **Latency feel** | Tokens stream immediately | Diffusion: long silence then a full clip. Autoregressive audio: can stream chunks, but slower than chat tok/s |
| **Quantization** | Q4/Q5 daily drivers | Spotty — some INT8/offload (ACE-Step), less universal than GGUF |
| **Disk** | One `.gguf` | Multi-file zoos (DiT + LM + VAE + vocoder); **10–70 GB** trees common |
| **Deps** | Relatively thin | **ffmpeg**, torchcodec, espeak (DiffRhythm), audio I/O; fragile on Mac MPS |
| **Batching** | Easy multi-turn chat | Batch songs only if VRAM allows; duration × batch explodes memory |
| **Licensing** | Often Apache/MIT | Mix of MIT (ACE-Step), Meta research terms, **Stability Community License**, dataset license caveats |
| **Evaluation** | MMLU / SWE-bench-ish | Subjective listening + niche metrics; don’t trust a single leaderboard |
| **Failure mode** | Nonsense text | Musical collapse, lyric misalignment, tempo drift on continuation, copyright-adjacent style copying |
| **Post-process** | Usually none | Normalize, crossfade, stem split (Demucs), loudness — part of the workflow |
| **“Context”** | Token window | **Seconds of audio** + text/lyric conditioning; longer ≠ smarter, just heavier |

**Practical Mac habits that differ from chat LLMs:**

1. Quit browsers/IDEs before a full-song run — unified memory is shared with the decoder spike.  
2. Prefer **shorter duration** and **turbo/few-step** checkpoints over “max quality” weights.  
3. Prefer **official MLX / macOS scripts** (ACE-Step, musicgen-mlx) over raw `device="mps"` ports.  
4. Don’t expect Ollama-style model swapping; unload one pipeline before loading another.  
5. Plan disk for caches under `~/.cache/huggingface/` — music weights are bulky.

---

## Suggested decision tree

```
Need ≤30–47s instrumental / loop?
  └─ MusicGen-MLX or Stable Audio Open (Small for speed)

Need a real song with structure / lyrics on this Mac?
  └─ ACE-Step 1.5 2B turbo (DiT-only first)

Need best open lyric quality and have 24 GB+ RAM or a 16–24 GB NVIDIA?
  └─ SongGeneration or ACE-Step XL / larger LM

Need endless background stream?
  └─ MusicGen continuation loop + crossfade (app code), or ACE-Step queued “station” apps — not a single infinite generate call
```

---

## Reddit discussion (curated)

Fetched via Arctic Shift from **r/LocalLLaMA** and **r/StableDiffusion**. Scores are archive snapshots (approximate). Prefer threads that discuss **local** runnability, length, VRAM, or Mac — not closed APIs alone.

### Inflection / demand

| Score | Thread | Why it matters |
| ---: | --- | --- |
| 787 | [We now have Suno AI at home… YuE](https://www.reddit.com/r/StableDiffusion/comments/1ibyrc0/we_now_have_suno_ai_at_home_with_this_new_local/) (r/SD, 2025-01) | Full-song local hype; 130 comments |
| 391 | [YuE: Open Music Foundation Models…](https://www.reddit.com/r/LocalLLaMA/comments/1ibzmef/new_bomb_dropped_from_asian_researchers_yue_open/) (r/LocalLLaMA) | Same drop on the LLM sub |
| 186 | [Would give up a kidney for a local audio model…](https://www.reddit.com/r/LocalLLaMA/comments/1ia40om/would_give_up_a_kidney_for_a_local_audio_model/) | Pre-YuE demand signal (2 days earlier) |
| 364 | [Udio just robbed… need more Open Source](https://www.reddit.com/r/LocalLLaMA/comments/1ojqvwe/udio_just_robbed_and_betrayed_its_paying/) | Why locals care about open music stacks |

### ACE-Step / runtimes

| Score | Thread | Why it matters |
| ---: | --- | --- |
| 182 | [1 Day Left Until ACE-Step 1.5… &lt;4GB VRAM](https://www.reddit.com/r/LocalLLaMA/comments/1qtqspu/1_day_left_until_acestep_15_opensource_music_gen/) | Consumer-VRAM framing |
| 133 | [Ace Step 1.5 XL is out!!!](https://www.reddit.com/r/StableDiffusion/comments/1ses85i/ace_step_15_xl_is_out/) | XL quality jump |
| 116 | [AceStep 1.5 XL Turbo… on an 8GB RTX 5060](https://www.reddit.com/r/StableDiffusion/comments/1sj8qh2/acestep_15_xl_turbo_ltx_23_on_an_8gb_rtx_5060/) | Low-VRAM XL anecdote |
| 110 | [audio.cpp… ACE-Step, Stable Audio… 10-Minute Music in 60 Seconds](https://www.reddit.com/r/LocalLLaMA/comments/1um2tbf/audiocpp_the_sound_of_ggml_cggml_native_acestep/) | GGML path (closer to llama.cpp ergonomics) |
| 49 | [acestep.cpp… CUDA, ROCm, Metal, Vulkan](https://www.reddit.com/r/LocalLLaMA/comments/1ry1dy1/acestepcpp_portable_c17_implementation_of_acestep/) | Portable C++ / Metal angle |
| 189 | [KoboldCpp 1.110… native music gen](https://www.reddit.com/r/LocalLLaMA/comments/1rxunqq/koboldcpp_1110_3_yr_anniversary_edition_native/) | Music inside a familiar local UI |

### DiffRhythm / YuE practicality / Mac

| Score | Thread | Why it matters |
| ---: | --- | --- |
| 185 | [DiffRhythm… full songs (4 min) with vocals](https://www.reddit.com/r/LocalLLaMA/comments/1j38499/diffrhythm_aslplab_generate_full_songs_4_min_with/) | Song-length diffusion before ACE-Step 1.5 |
| 52 | [DiffRhythm 1.2… Avicii nearly verbatim](https://www.reddit.com/r/LocalLLaMA/comments/1m4yo0g/diffrhythm_12_music_generation_model_produces/) | Memorization / legal risk |
| 138 | [YuE GP… less than 10 GB of VRAM](https://www.reddit.com/r/StableDiffusion/comments/1iegcxy/yue_gp_runs_the_best_open_source_song_generator/) | Quant/offload fork for GPU-poors |
| 244 | [Yue license → Apache 2… ~90s on 4090](https://www.reddit.com/r/StableDiffusion/comments/1ie0rar/yue_license_updated_to_apache_2_limited_rn_to_90s/) | Early length/VRAM constraints |
| 13 | [Mac… Khala Music AI → Apple Silicon](https://www.reddit.com/r/StableDiffusion/comments/1tuqklr/you_can_now_make_mac_generate_high_quality_songs/) | Apple Silicon song-gen port (still RAM-hungry class) |

### “Endless” / self-hosted listening

| Score | Thread | Why it matters |
| ---: | --- | --- |
| 483 | [Breaking the music supply constraint](https://www.reddit.com/r/LocalLLaMA/comments/1treuy3/breaking_the_music_supply_constraint/) | Self-hosted music supply chain (302 comments) |
| 16 | [AI Jukebox with ACE-Step 1.5… nonstop](https://www.reddit.com/r/LocalLLaMA/comments/1qxn3pa/i_made_an_ai_jukebox_with_acestep_15_free_nonstop/) | Queued generations as radio |
| 21 | [24/7 Subreddit Radio](https://www.reddit.com/r/LocalLLaMA/comments/1v3woyv/247_subreddit_radio/) | ACE-Step + LLM DJ in production |

---

## Sources (primary)

- [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) — README, GPU tiers, macOS MLX launch  
- [Meta MusicGen / AudioCraft](https://facebookresearch.github.io/audiocraft/docs/MUSICGEN.html)  
- [musicgen-mlx](https://github.com/andrade0/musicgen-mlx)  
- [Stable Audio Open 1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) / [Open Small](https://huggingface.co/stabilityai/stable-audio-open-small)  
- [DiffRhythm](https://github.com/ASLP-lab/DiffRhythm)  
- [SongGeneration](https://github.com/tencent-ailab/songgeneration) / [SongGen-Mac](https://github.com/Rdx-ai-art/SongGen-Mac)  
- Community continuation / streaming patterns (HF MusicGen streamer, sliding-window extend blogs)  
- Reddit threads listed above (r/LocalLLaMA, r/StableDiffusion)

## Method / caveats

- Vendor docs for capabilities & official VRAM tables; Reddit for adoption, pain points, Mac/low-VRAM anecdotes.  
- Archive helper (same family as the LLM report): [`fetch_localllama_posts.py`](./scripts/fetch_localllama_posts.py) against Arctic Shift — keyword searches across LocalLLaMA / StableDiffusion.  
- Memory and speed claims mix vendor docs and community reports; Apple Silicon numbers vary by macOS version and MLX build.  
- “Commercial-grade” claims (ACE-Step, SongGeneration) are vendor-positioned — listen yourself.  
- This report does **not** cover closed APIs (Suno, Udio) except as quality / motivation reference points.  
- DiffRhythm-style memorization reports are a reminder: local ≠ copyright-safe.
