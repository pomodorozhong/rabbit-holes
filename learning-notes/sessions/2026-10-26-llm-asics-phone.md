# Session record: LLM ASICs and local inference, 2026-10-26

## Starting point

- **Already knew:** The user follows AI news and checks whether newly released models around 10B parameters can run on an M2 MacBook Pro.
- **Wanted to understand:** What ASICs improve for LLM inference, whether they can reduce local memory needs, and whether frontier-level models might eventually run on phones.

## Questions and conclusions

### What does an ASIC gain for LLM inference?

- **Understood:** The explanation distinguished broad programmable inference accelerators from silicon tailored to a fixed model. Specialized hardware can improve speed and energy use for its target workload, but those gains depend on the model, serving load, and hardware comparison. A fixed model's weights can be stored in the chip, trading updateability for specialization.
- **Check:** Covered with sources, not checked by the user restating or predicting.
- **Sources:** [Google Research's TPU study](https://research.google/pubs/in-datacenter-performance-analysis-of-a-tensor-processing-unit/); [Apple's third-generation Foundation Models](https://machinelearning.apple.com/research/introducing-third-generation-apple-foundation-models).

### Can an ASIC reduce local model memory needs?

- **Understood:** A compute accelerator alone does not reduce the model's weight bytes at fixed precision. Quantization, sparse activation, or loading selected weights from flash can reduce the active memory footprint. Apple Silicon's unified memory is shared between CPU and GPU, so an M2 Mac does not have a separate VRAM pool. A 10B model at raw 4-bit precision needs about 5 GB for weights before cache and runtime overhead.
- **Example:** Apple describes a 20B sparse on-device model that activates 1–4B parameters, stores full weights in flash, and loads selected experts into DRAM. Flash is too slow to swap weights every token, so its routing design selects experts by prompt and revisits choices periodically.
- **Check:** Covered with sources, not checked by the user restating or predicting.
- **Sources:** [Apple Developer's MLX presentation](https://developer.apple.com/videos/play/wwdc2025/315/); [Apple's “LLM in a Flash” research](https://machinelearning.apple.com/research/efficient-large-language); [Apple's third-generation Foundation Models](https://machinelearning.apple.com/research/introducing-third-generation-apple-foundation-models).

### How do current LLM ASICs compare with GPUs?

- **Understood:** No single multiplier describes ASIC performance. Low-batch per-token latency, output tokens per second, and users per watt are different measures. A 2026 research preprint compared Llama 3.1 8B at low batch size and reported per-token latency relative to H100 of 0.2289 for Cerebras CS-3, 0.3003 for Groq, and 0.4861 for SambaNova SN-40. The Cerebras test used physical hardware, while the Groq and SN-40 numbers came through APIs. A separate Cerebras chart reports 2,457 versus 164 output tokens/s on Llama 3.3 70B with 10,000 input tokens, but does not specify the GPU configuration or concurrency. Furiosa reports 1.8–2x more Qwen3-32B FP8 users per kilowatt than RTX PRO 6000 at a 20–40 tokens/s/user service target. Taalas HC1 is a model-specific Llama 3.1 8B demonstrator claiming 17,000 tokens/s per user at 1,000 input and output tokens; the company says HC1 uses custom 3-bit/6-bit weights with some quality degradation versus GPU benchmarks. Its comparison draws from vendor and third-party data and is not a universal GPU speedup.
- **Check:** Covered with primary sources and a research preprint, not checked by the user restating or predicting.
- **Sources:** [The xPU-athalon preprint](https://arxiv.org/abs/2604.10852); [Cerebras's May 2026 SEC filing](https://www.sec.gov/Archives/edgar/data/2021728/000162828026029503/cerebras-sx1amay2026.htm); [FuriosaAI's RENEGADE 2026 results](https://furiosa.ai/blog/renegade-2026-summit); [Taalas HC1](https://taalas.com/products/) and [its comparison and precision details](https://taalas.com/the-path-to-ubiquitous-ai/).

### How do their architectures differ, and how long does an ASIC take?

- **Understood:** Cerebras scales one processor to wafer size and places a large SRAM pool beside its compute cores. Groq uses a compiler-scheduled streaming pipeline with on-chip SRAM. SambaNova maps model operations onto a reconfigurable dataflow processor backed by SRAM, HBM, and DDR. Furiosa RNGD is a tensor-contraction NPU with HBM3 and on-chip SRAM. These four accelerators still load model weights as data. Taalas HC1 instead hard-wires Llama 3.1 8B into silicon, which trades flexibility and easy model updates for specialization.
- **Timing:** A new chip architecture and product takes years of R&D and includes design, verification, fabrication, and validation; fabrication is only one stage and ASML describes it as taking up to four months. Taalas says its platform can realize a new model in silicon in two months. This is a company claim about model-to-silicon using its platform, not a generic timeline for inventing and delivering a new ASIC.
- **Calendar comparison (corrected):** The user clarified they want the date the cited speed result was reported, not the ASIC announcement date. In the note's comparison, the xPU-athalon study reported the Llama 3.1 8B Cerebras, Groq, and SambaNova results on April 12, 2026; Cerebras's 2,457 vs 164 tokens/s result appears in its May 4, 2026 SEC filing; Furiosa's Qwen3-32B users/kW result is in its April 2, 2026 summit report; and Taalas reported the Llama 3.1 8B speed result in February 2026. The resulting gaps from model release to cited report are approximately 21 months, 17 months, 11 months, and 19 months respectively. These are reporting delays, not hardware development times.
- **Check:** Explained with vendor specifications and semiconductor-industry sources, not checked by the user restating or predicting.
- **Sources:** [Meta's Llama 3.1 release](https://ai.meta.com/blog/meta-llama-3-1/); [Meta's Llama 3.3 model card](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct); [Qwen3 release](https://qwenlm.github.io/blog/qwen3/); [xPU-athalon](https://arxiv.org/abs/2604.10852); [Cerebras's May 4, 2026 SEC filing](https://www.sec.gov/Archives/edgar/data/2021728/000162828026029503/cerebras-sx1amay2026.htm); [Furiosa's RENEGADE 2026 results](https://furiosa.ai/blog/renegade-2026-summit); [Taalas's HC1 launch post](https://www.linkedin.com/posts/taalas_api-access-request-form-activity-7430311793438228481-IkCz) and [speed details](https://taalas.com/the-path-to-ubiquitous-ai/); [Semiconductor Industry Association overview](https://www.semiconductors.org/wp-content/uploads/2024/08/SIA-Comments-on-ANPRM-Sec.-5949-FINAL.pdf); [ASML manufacturing overview](https://www.asml.com/en/technology/all-about-microchips/how-microchips-are-made).

### Could Opus 5.5 run on an iPhone?

- **Understood:** Current on-device frontier-capable models are plausible, especially when their architecture is designed around device memory. Public Opus 5.5 documentation lists the hosted API and cloud platforms but does not provide on-device weights or specifications to estimate an iPhone deployment, so the session could not establish that the exact Opus model can run locally.
- **Check:** Covered with current public product documentation, not checked by the user restating or predicting.
- **Sources:** [Anthropic's Opus 5.5 documentation](https://platform.claude.com/docs/en/models/opus-5-5/overview); [Apple's third-generation Foundation Models](https://machinelearning.apple.com/research/introducing-third-generation-apple-foundation-models).

## The user's views and conclusions

- The user tracks whether new roughly 10B models can run on an M2 MacBook Pro and is mainly curious about what future hardware might make possible.

## Set aside

- No exact M2 memory configuration was established.
- No model was run or benchmarked on the user's Mac during the session.

## Open questions

- How might a future phone combine quantization, sparse activation, flash storage, and specialized hardware to run stronger local models?
- What memory and performance limits apply to the user's specific M2 configuration?
