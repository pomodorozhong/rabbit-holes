# Your real memory budget

Hardware: Apple **M2 MacBook Pro, 16 GB unified memory**.  
Stack: Metal / MLX / llama.cpp / Ollama / PyTorch-MPS — **no CUDA**.

16 GB unified ≠ 16 GB for the model.

- macOS + browser + IDE typically leave **~8–11 GB** usable for weights + KV / activations.
- Metal’s default GPU working set on ≤32–64 GB Macs is often ~**10.5 GB**.
- Prefer artifacts whose **on-disk size is ≤ ~8 GB**; keep context short unless measured.
- If a file is **>11 GB**, treat as “does not run” for daily use.
