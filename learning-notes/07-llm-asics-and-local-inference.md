# ASICs and Local LLMs

**Bottom line:** An ASIC can make a particular LLM workload faster or more energy-efficient, but a compute accelerator does not automatically make the same model's weights smaller. The clearest path to larger local models combines specialized hardware with quantization, sparse activation, and memory designs that load only the needed weights. *(As of 2026-10-26.)*

**What does an ASIC gain?**

- An application-specific integrated circuit (ASIC) is designed around a more limited set of operations than a general-purpose GPU. That focus can reduce overhead and move data between memory and compute more efficiently, but the best result depends on model, batch size, context length, and utilization. A 2026 accelerator study found Cerebras and Groq's memory-heavy designs could reduce token latency at low batch sizes, while the best platform changed for larger batches and models ([the xPU-athalon preprint](https://arxiv.org/abs/2604.10852)).
- The size of the gain is workload-specific. A 2017 Google study found its first Tensor Processing Unit was 15–30 times faster and 30–80 times more efficient per watt than contemporary CPUs and GPUs on Google's production neural-network workloads. That historical result illustrates what specialization can do; it is not a prediction for current LLMs or consumer devices ([Google Research's TPU study](https://research.google/pubs/in-datacenter-performance-analysis-of-a-tensor-processing-unit/)).

**Can an ASIC reduce memory needs?**

- On an M2 Mac, the CPU and GPU share unified memory, so “VRAM” is not a separate pool from system RAM. A 10-billion-parameter model in raw 4-bit weights takes about 5 GB before quantization metadata, the KV cache, activations, and runtime memory; the actual working set must also share the Mac's memory with macOS and other apps ([Apple Developer's MLX overview](https://developer.apple.com/videos/play/wwdc2025/315/)).
- At the same model and precision, changing the compute chip alone does not change the weight bytes. Quantization reduces the bits per weight. Sparse models can use only a subset of their parameters for a request. Flash-backed designs can keep weights outside DRAM and load selected parts when needed.
- A model-specific ASIC can encode fixed weights into the chip, as Taalas does with HC1. That reduces dependence on external model memory by moving weight storage into the chip, but the weights still occupy physical area and are much harder to update ([Taalas on HC1](https://taalas.com/the-path-to-ubiquitous-ai/)).
- Apple describes an on-device 20-billion-parameter sparse model that activates 1–4 billion parameters depending on the request. It stores the full model in flash and loads selected experts into DRAM; since flash is too slow to swap weights every token, the model makes routing decisions by prompt and revisits them periodically. This is an example of model and memory co-design, not a generic accelerator making every 20B model fit in RAM ([Apple's model announcement](https://machinelearning.apple.com/research/introducing-third-generation-apple-foundation-models)).

**What do current ASIC-to-GPU comparisons show?**

The first three rows are the same metric from one low-batch Llama 3.1 8B study. Their latency is relative to H100 (`1.00×`); lower is better. The remaining rows use different models and metrics, so they do not form one ranking.

| Example | Reported number *(metric and caveat)* |
| --- | --- |
| Cerebras CS-3 | **0.229× H100** — per-token latency; physical-device test ([xPU-athalon](https://arxiv.org/abs/2604.10852)). |
| Groq LPU | **0.300× H100** — per-token latency; API result, not a physical-chip test ([xPU-athalon](https://arxiv.org/abs/2604.10852)). |
| SambaNova SN-40 | **0.486× H100** — per-token latency; API result, not a physical-chip test ([xPU-athalon](https://arxiv.org/abs/2604.10852)). |
| Cerebras, Llama 3.3 70B | **2,457 vs 164 output tokens/s** — 10,000-token input; GPU configuration and concurrency unspecified ([Cerebras's May 2026 SEC filing](https://www.sec.gov/Archives/edgar/data/2021728/000162828026029503/cerebras-sx1amay2026.htm)). |
| Furiosa RNGD | **1.8–2× users per kW** — Qwen3-32B FP8, 20–40 tokens/s/user target; company-reported vs RTX PRO 6000 ([Furiosa's RENEGADE 2026 results](https://furiosa.ai/blog/renegade-2026-summit)). |
| Taalas HC1 | **17,000 tokens/s/user** — Llama 3.1 8B at 1k input/1k output; hardwired 3/6-bit demo with some reported quality loss and mixed baselines ([HC1 product page](https://taalas.com/products/), [benchmark details](https://taalas.com/the-path-to-ubiquitous-ai/)). |

- Token latency, total throughput, and users served per watt answer different questions. A chip that is quickest for one user at low batch may not lead when a server is kept busy with many simultaneous requests ([xPU-athalon](https://arxiv.org/abs/2604.10852)).

**How do these accelerator architectures differ?**

The terminology can be slippery: GPUs are designed for graphics and parallel compute, but remain programmable across many workloads. Here, “GPU” means a conventional programmable GPU as the reference point; the examples below are AI accelerators designed more narrowly around AI workloads.

| Example | Architecture | Where model weights go |
| --- | --- | --- |
| GPU reference | Many programmable parallel compute units | Separate HBM; on Apple Silicon, shared unified memory |
| Cerebras CS-3 | One wafer-scale processor with 900,000 AI cores and 44 GB SRAM | 44 GB on-wafer SRAM, with larger external memory in the system ([Cerebras WSE-3](https://www.cerebras.ai/press-release/cerebras-announces-third-generation-wafer-scale-engine)) |
| Groq LPU | Compiler-scheduled, deterministic streaming “assembly line” | Loaded into SRAM across one or more chips ([Groq LPU](https://groq.com/blog/the-groq-lpu-explained)) |
| SambaNova SN40L | Reconfigurable dataflow processor with SRAM, HBM, and DDR | Loaded as data; HBM holds the active model ([SN40L architecture](https://sambanova.ai/blog/sn40l-chip-best-inference-solution)) |
| Furiosa RNGD | Tensor Contraction Processor (TCP) NPU | Loaded as data into 48 GB HBM3, with 256 MB on-chip SRAM ([RNGD specifications](https://developer.furiosa.ai/docs/v2024.2.1/en/overview/rngd.html)) |
| Taalas HC1 | Silicon specialized for a particular model | Llama 3.1 8B is hard-wired into the silicon ([Taalas architecture](https://taalas.com/the-path-to-ubiquitous-ai/)) |

The first four are specialized computers that still load model weights as data. They differ in how much compute they put in one package, how they schedule operations, and how they arrange fast and large memory. Taalas goes further: it builds silicon around one model, joining weight storage and computation. That can avoid repeatedly moving the weights from external memory, but each model update or replacement needs compatible silicon. Its HC1 demo also uses custom 3-bit and 6-bit weights and reports some quality loss against GPU comparisons ([Taalas's HC1 details](https://taalas.com/the-path-to-ubiquitous-ai/)).

**How long does an AI ASIC take to make?**

- **A new chip architecture and product:** Think years, not weeks. The semiconductor industry describes advanced chip design as years of R&D, with work spanning requirements, architecture, circuit design, verification, and post-silicon validation; exact schedules depend on scope and how much proven design can be reused ([Semiconductor Industry Association overview](https://www.semiconductors.org/wp-content/uploads/2024/08/SIA-Comments-on-ANPRM-Sec.-5949-FINAL.pdf)).
- **Fabrication after the design is ready:** ASML says the wafer manufacturing process can take up to four months. That covers making the chip, not the earlier architecture, verification, software, and bring-up work ([ASML's chip manufacturing overview](https://www.asml.com/en/technology/all-about-microchips/how-microchips-are-made)).
- **A new model on Taalas's existing platform:** Taalas claims it can turn a previously unseen model into silicon in two months. Treat that as a company-reported model-to-silicon turnaround; the public description does not provide a detailed schedule breakdown or independent validation ([Taalas](https://taalas.com/the-path-to-ubiquitous-ai/)).

So the practical distinction is **years to create a platform, potentially months to adapt that platform to a model**. Taalas's short claim depends on its reusable platform and model-specific silicon; it is not a general schedule for designing a new AI chip.

The table compares each model's public release with the publication date of the source reporting the speed result cited earlier. It does **not** use the ASIC's product-announcement date. These gaps show when the cited result appeared relative to the model's release; they do not measure how long the chip or benchmark took to develop. The cited source date may also be later than an earlier public mention of the same result.

| Speed result | Model first released | Cited speed report published | Approx. gap |
| --- | --- | --- | --- |
| Cerebras CS-3, per-token latency | Llama 3.1 8B — [2024-07-23](https://ai.meta.com/blog/meta-llama-3-1/) | [2026-04-12](https://arxiv.org/abs/2604.10852) | ~21 months |
| Groq LPU, per-token latency | Llama 3.1 8B — [2024-07-23](https://ai.meta.com/blog/meta-llama-3-1/) | [2026-04-12](https://arxiv.org/abs/2604.10852) | ~21 months |
| SambaNova SN-40, per-token latency | Llama 3.1 8B — [2024-07-23](https://ai.meta.com/blog/meta-llama-3-1/) | [2026-04-12](https://arxiv.org/abs/2604.10852) | ~21 months |
| Cerebras, 2,457 vs 164 output tokens/s | Llama 3.3 70B — [2024-12-06](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) | [2026-05-04](https://www.sec.gov/Archives/edgar/data/2021728/000162828026029503/cerebras-sx1amay2026.htm) | ~17 months |
| Furiosa RNGD, 1.8–2× users/kW | Qwen3-32B — [2025-04-29](https://qwenlm.github.io/blog/qwen3/) | [2026-04-02](https://furiosa.ai/blog/renegade-2026-summit) | ~11 months |
| Taalas HC1, 17,000 tokens/s/user | Llama 3.1 8B — [2024-07-23](https://ai.meta.com/blog/meta-llama-3-1/) | February 2026 ([launch post](https://www.linkedin.com/posts/taalas_api-access-request-form-activity-7430311793438228481-IkCz); [speed details](https://taalas.com/the-path-to-ubiquitous-ai/)) | ~19 months |

The Cerebras, Groq, and SambaNova latency figures all come from the same April 2026 preprint. Furiosa's figure was reported in its April 2026 summit results; Taalas reported its Llama 3.1 result in February 2026. In every row, the interval is the time from the model's public release to the cited speed report—not the ASIC design or model-porting time.

**Could Opus 5.5 run on an iPhone?**

- On-device models with substantially more capability are plausible, especially when designed around a device's memory from the start. Apple's sparse model is evidence for that direction, but Apple says it is optimized for its most capable Apple silicon; the announcement does not say that model runs on every iPhone.
- The public Opus 5.5 documentation reviewed here lists hosted platforms and an API, but no downloadable on-device weights or the details needed to estimate an iPhone memory footprint. Its listed 1-million-token context window is the amount of text the service can handle, not the model's parameter count or a local memory estimate ([Anthropic's Opus 5.5 documentation](https://platform.claude.com/docs/en/models/opus-5-5/overview)). The session therefore could not establish that this exact model can run on an iPhone.
- A reasonable inference from Apple's and Taalas's approaches is that future local systems will pair accelerators with models built for their memory and power limits. That is a different path from installing an unchanged server model onto a phone.

**For me:** I follow new model releases and check whether roughly 10B models can run on my M2 MacBook Pro. I'm curious about what future hardware may make possible, rather than looking for a model recommendation now.

**Open**

- The M2 chip and unified-memory configuration were not established, so this note does not estimate the user's exact local model capacity.
- The published information does not determine whether a future phone could run Opus 5.5 or an equivalent model locally.
