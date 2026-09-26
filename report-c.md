# 本機可行性報告：AI News 影片中的模型與工具

**Compiled / 查核日期：** 2026-09-26  
**Source video / 來源影片：** [Claude Opus 4.7, Qwen 3.6, Happy Oyster, realtime 3D worlds, new Google TTS: AI NEWS](https://www.youtube.com/watch?v=G8fqduzB5lc) — AI Search，約 37 分鐘  
**影片發布日期：** 2026-04-19（臺灣／日本時間；YouTube 原始時間為 4 月 18 日美西時間）  
**Hardware target / 評估設備：** Apple M2 MacBook Pro，16 GB 統一記憶體，沿用參考報告條件  
**Stack assumption / 執行環境：** Metal、MLX、llama.cpp／Ollama、PyTorch MPS；無 NVIDIA CUDA

**閱讀範圍：** 依影片官方章節與英文自動字幕盤點，再用官方模型卡、程式庫、論文及產品文件核對。評估的是片中版本截至查核日的可用狀態；後續發布的程式或支援會另外標示。本次未下載模型或在 M2 上實測，因此沒有自測速度、記憶體峰值或生成品質數據。

**Memory budget / 記憶體預算：** 16 GB 由 macOS、CPU、GPU 與其他程式共用。本報告採保守試用策略：先把模型權重、快取與執行緩衝的合計預算抓在約 8–10 GB，再觀察記憶體壓力與 swap；這是規劃假設，並非這台機器的實測可用容量。下載大小也不等於執行時用量。

## TL;DR

| 判斷 | 模型／項目 |
| --- | --- |
| ✅ 最值得在這台 Mac 優先試用 | **Ternary Bonsai 8B、4B、1.7B**：官方提供 MLX 2-bit 格式；權重約 **2.30、1.13、0.48 GB**。記憶體餘裕明顯優於其他片中模型。 |
| ⚠️ 很吃緊，適合實驗 | **Qwen3.6-35B-A3B**：一般 4-bit 版本超出預算；社群極低位元 GGUF 有約 **10.8–11.5 GB** 的選項，仍須另外容納快取、執行緩衝與系統。 |
| ⚠️ 可以先試工具，模型另計 | **GameWorld**：Python 與瀏覽器的評測環境可作為 Mac 試用候選；完整離線評測還需要能在本機跑的視覺模型與相容介面。 |
| ❌ 已有權重／程式，但官方流程不適合此 Mac | **Prompt Relay 的 Wan2.2-A14B 流程、WildDet3D 的桌面 Python 流程、Motif-Video 2B、AniGen、Lyra 2、HY-World 2.0 完整生成流程**。障礙包括 CUDA、記憶體與多階段依賴。 |
| ❌ 雲端推論服務 | **GPT-Rosalind、Claude Opus 4.7、HappyOyster、Gemini 3.1 Flash TTS**。Mac 可以當用戶端，模型運算留在服務端。 |
| n/a 研究、素材或產業新聞 | **OmniShow** 公開了復現程式，但未附其訓練完成的 checkpoint；**TokenLight** 查得論文與展示；另有 **HubSpot 指南**及三則**人形機器人**新聞。 |

**這部影片對 16 GB M2 最直接的收穫，是 Ternary Bonsai 的官方 MLX 版本。** 8B 已足夠小，可以先用自己的摘要、改寫或簡單程式問題評估；4B、1.7B 則可測試在降低資源用量後，品質是否仍符合需求。尺寸依 [8B](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-mlx-2bit)、[4B](https://huggingface.co/prism-ml/Ternary-Bonsai-4B-mlx-2bit)、[1.7B 官方模型卡](https://huggingface.co/prism-ml/Ternary-Bonsai-1.7B-mlx-2bit)；Qwen 的極低位元選項見 [Unsloth 檔案清單](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main)。

影片中的「輕量」、「開放」與「即時」需要分別解讀：生成器可能依賴更大的文字編碼器；開放程式可能未附模型權重；即時探索已生成的場景，也不能推導成可在 Mac 上即時生成場景。

---

## Runnability table：全部章節

順序與時間採影片官方章節，共 20 章，包含開場及贊助段落。

| 模型／項目 | 影片 | 類型 | 權重／取得方式 | 適合 16 GB M2？ | 本機實際情況 |
| --- | --- | --- | --- | --- | --- |
| AI news intro | [0:00](https://www.youtube.com/watch?v=G8fqduzB5lc&t=0s) | 本集預告 | 無獨立發布 | n/a | 概覽；逐項判斷見下列章節。 |
| Prompt Relay | [1:00](https://www.youtube.com/watch?v=G8fqduzB5lc&t=60s) | 依時間段控制影片提示詞的方法 | 公開方法與程式；另需 Wan 模型 | ❌ 官方範例流程 | [作者範例](https://github.com/GordonChen19/Prompt-Relay) 使用 Wan2.2-T2V-A14B；[Wan 官方 720p 單卡範例](https://github.com/Wan-Video/Wan2.2#run-text-to-video-generation) 標示至少 80 GB VRAM。方法免訓練，仍須負擔底層影片模型。 |
| Ternary Bonsai | [2:45](https://www.youtube.com/watch?v=G8fqduzB5lc&t=165s) | 壓縮通用文字模型 | 8B／4B／1.7B；Apache 2.0；官方 MLX | ✅ 優先試用 | [8B 官方 MLX 權重](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-mlx-2bit) 約 2.30 GB，具 Apple Silicon 使用途徑；M2 實際速度仍需測量。 |
| GPT-Rosalind | [5:35](https://www.youtube.com/watch?v=G8fqduzB5lc&t=335s) | 生命科學研究模型 | 受控存取的託管服務 | ❌ 本機推論 | [OpenAI 後續官方文件](https://developers.openai.com/blog/rosalind-workbench) 說明經 Workbench 申請模型存取；未提供可下載的本機權重。研究工具在本機運作，不代表模型也在本機。 |
| WildDet3D | [7:39](https://www.youtube.com/watch?v=G8fqduzB5lc&t=459s) | 可用文字、點或框提示的 3D 物件偵測 | 公開約 4.7 GB checkpoint；另有 iPhone App | ❌ 桌面原版；移植待驗證 | [Python 安裝流程](https://github.com/allenai/WildDet3D) 依賴 CUDA 及 vis4d CUDA ops。[iPhone 文件](https://github.com/allenai/WildDet3D/blob/main/demo/iphone/README.md) 確有裝置端路線，但未因此提供可直接使用的 macOS MPS 流程。 |
| Motif-Video 2B | [9:09](https://www.youtube.com/watch?v=G8fqduzB5lc&t=549s) | 文字／圖片生成影片 | Apache 2.0 權重；已有 Diffusers 與 ComfyUI 支援 | ❌ 官方流程 | [模型卡](https://huggingface.co/Motif-Technologies/Motif-Video-2B) 列出約 30 GB 常規峰值、CPU offload 約 19 GB，搭配 FP8 約 15 GB；這些是 CUDA 路線的 VRAM 數據，另需主記憶體。 |
| HubSpot AI content team | [10:54](https://www.youtube.com/watch?v=G8fqduzB5lc&t=654s) | 贊助：內容工作流程指南 | 指南、skill 與研究腳本 | n/a | 影片介紹的是可重用的內容流程資源，沒有發布新的模型權重；是否離線取決於使用的模型與資料來源。 |
| AniGen | [12:06](https://www.youtube.com/watch?v=G8fqduzB5lc&t=726s) | 單圖生成帶骨架、蒙皮的 3D 資產 | 公開程式與預訓練權重；有線上展示 | ❌ | [官方要求](https://github.com/VAST-AI-Research/AniGen) 為 Linux、NVIDIA GPU 至少 18 GB 顯示記憶體與 CUDA 工具鏈；另有視覺模型依賴。 |
| HappyOyster | [13:48](https://www.youtube.com/watch?v=G8fqduzB5lc&t=828s) | 可互動的即時世界生成服務 | 影片時為申請體驗；現有雲端 API／SDK 文件 | ❌ 本機推論 | [官方架構](https://www.alibabacloud.com/help/en/model-studio/happyoyster-overview) 以 API 建立世界，再由 SDK 接收即時影音並送出操作。Web／iOS SDK 是用戶端。 |
| Lyra 2 | [15:05](https://www.youtube.com/watch?v=G8fqduzB5lc&t=905s) | 可持續探索的 3D 世界生成／重建 | 公開模型；NVIDIA 內部科研用途授權 | ❌ | [官方模型卡](https://huggingface.co/nvidia/Lyra-2.0) 標示 WAN-14B 基礎、14B 參數；[安裝文件](https://github.com/nv-tlabs/lyra/blob/main/Lyra-2/INSTALL.md) 測試環境是 Ubuntu、CUDA 12.8、H100。影片提及的 131 MB 無法代表完整系統。 |
| HY-World 2.0 | [16:40](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1000s) | 全景、世界生成與 3D 重建框架 | 多組公開權重與程式，分批發布 | ❌ 完整生成流程 | [官方模型表](https://github.com/Tencent-Hunyuan/HY-World-2.0) 區分約 1.2B 的 WorldMirror-2、約 17B 的 WorldStereo-2 等組件，安裝依賴 CUDA／FlashAttention／gsplat。重建子模型的大小不能代表整套世界生成器。 |
| OmniShow | [18:03](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1083s) | 人物與商品互動影片生成 | Wan-based 復現程式、資料與 benchmark；未附訓練完成的 checkpoint | n/a 缺可直接用的成品權重 | [官方 README](https://github.com/Correr-Zhou/OmniShow#-data-and-model-preparation) 明確說明 checkpoint 因內部政策未收錄。下載 Wan 基礎模型並不能直接重現 OmniShow 成品能力。 |
| Claude Opus 4.7 | [20:22](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1222s) | 通用、程式與視覺模型 | Claude 產品、API 及雲端平台 | ❌ 本機推論 | [官方發布頁](https://www.anthropic.com/news/claude-opus-4-7) 提供託管服務存取，沒有本機權重發布。桌面或終端工具連線使用仍屬遠端推論。 |
| Qwen3.6-35B-A3B | [24:38](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1478s) | 具視覺能力的 MoE 語言模型 | Apache 2.0 官方權重；社群 GGUF／MLX 量化 | ⚠️ 僅極低位元實驗 | [官方規格](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) 為總計 35B、啟用 3B。4-bit 權重理論下限約 17.5 GB；[社群 IQ2](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main) 約 10.8–11.5 GB 才有短上下文試驗空間，品質與 M2 速度未驗證。 |
| Unitree sprinter | [26:14](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1574s) | H1 人形機器人奔跑展示 | 實體機器人展示 | n/a | 本章展示運動控制成果；沒有提供可視為 Mac 模型安裝包的發布。 |
| Humanoid marathon | [26:57](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1617s) | 人形機器人賽事 | 活動與硬體展示 | n/a | 反映機器人系統進展；本章未交付可下載、可在 Mac 重現的完整控制模型。 |
| Automated humanoid factory | [27:51](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1671s) | 樂聚機器人生產線 | 工廠與製造流程展示 | n/a | 影片描述自動化組裝及仍有人工參與的生產流程；沒有獨立本機模型發布。 |
| TokenLight | [29:17](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1757s) | 以屬性 token 控制照片重新打光 | 論文與展示；未查得官方可下載 checkpoint | n/a 待完整發布 | [論文](https://arxiv.org/abs/2604.15310) 的任務是控制亮度、顏色、環境光及光源位置。查核尚無可據以確認 M2 安裝方式與記憶體需求的成品套件。 |
| GameWorld | [31:30](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1890s) | 瀏覽器遊戲的 agent 評測環境 | 公開 Python 程式與遊戲庫 | ⚠️ 環境可試；模型另計 | [官方安裝](https://github.com/gameworld-project/GameWorld#-installation) 使用 Python、Playwright／Chromium，可接雲端 API 或自架模型。Mac 跑遊戲與記錄結果的可行性，不代表其範例大模型也能在此 Mac 離線跑。 |
| Gemini 3.1 Flash TTS | [33:09](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1989s) | 可控制情緒、語調的文字轉語音 | Gemini API／AI Studio | ❌ 本機推論 | [官方文件](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview) 是託管的文字輸入、音訊輸出模型，且不支援 Live API；截至查核日已標記為 legacy preview。 |

**圖例：** ✅ 有官方 Apple 路線且權重具合理餘裕，值得先試；⚠️ 需額外適配、極端量化或只適用於部分環境；❌ 依目前查得的發布內容／官方流程，不適合在指定 Mac 執行模型推論；n/a 本章未提供可評估的獨立本機 checkpoint。所有判斷均不代表本次已實測。

---

## Runnable：值得試用的項目

### 1）Ternary Bonsai：本集最實際的本機選項

| 項目 | 說明 |
| --- | --- |
| 適合試驗的工作 | 文字摘要、改寫、簡單問答與程式輔助；以自己的繁體中文及領域資料檢查品質。 |
| 版本 | 8B、4B、1.7B，分別以同級 Qwen3 模型為基礎。 |
| 授權 | Apache 2.0。 |
| Mac 路線 | 官方 `prism-ml/Ternary-Bonsai-…-mlx-2bit`，透過 `mlx-lm` 載入。 |
| 初始設定 | 本報告建議先用約 4K 的總上下文預算、短輸出測試；穩定後再增加。 |
| 16 GB M2 判斷 | 權重大小與官方 MLX 路線支持優先試用；本次沒有 M2 速度測試。 |

| 版本 | 發布公告的 ternary 大小 | 官方 MLX 權重大小 | 建議用途 |
| --- | --- | --- | --- |
| 8B | 約 1.75 GB | 約 **2.30 GB**／2.15 GiB | 先用它建立品質基準。 |
| 4B | 約 0.86 GB | 約 **1.13 GB**／1.05 GiB | 與 8B 比較品質及資源差異。 |
| 1.7B | 約 0.37 GB | 約 **0.48 GB**／0.45 GiB | 測試簡短、範圍明確的任務。 |

來源：[PrismML 發布公告](https://prismml.com/news/prismml-introduces-ternary-bonsai-model-family)、[8B 模型卡](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-mlx-2bit)、[4B 模型卡](https://huggingface.co/prism-ml/Ternary-Bonsai-4B-mlx-2bit)、[1.7B 模型卡](https://huggingface.co/prism-ml/Ternary-Bonsai-1.7B-mlx-2bit)。

1.58-bit 描述的是三種權重值的資訊量；MLX 版本實際以 2-bit 加上縮放資料儲存。8B 的[整個儲存庫](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-mlx-2bit/tree/main)約 2.32 GB，含 tokenizer 等檔案；記憶體規劃則還要加入快取與運算緩衝。

官方列出的 M4 Pro 與 iPhone 速度，不能直接當成 M2 的速度。模型卡中的基準測試也無法替代繁體中文、事實正確性或特定工作流程的測試。這裡的推薦依據是小體積及官方 Apple 支援，而非本次已證明其品質優於其他模型。

### 2）Qwen3.6-35B-A3B：僅列為記憶體邊界實驗

| 項目 | 說明 |
| --- | --- |
| 工作定位 | 程式、agent 任務及視覺理解。 |
| 架構 | 總計 35B 參數，每次啟用約 3B；沒有啟用的專家權重仍須儲存或載入。 |
| 一般量化 | 以 Unsloth 為例，`UD-IQ4_XS` 約 17.7 GB，`UD-Q4_K_M` 約 22.1 GB，均超出本報告的本機預算。 |
| 極低位元選項 | `UD-IQ2_XXS` 約 10.8 GB；`UD-IQ2_M` 約 11.5 GB。 |
| 額外用量 | 圖像路線另有約 0.9 GB 的 FP16／BF16 `mmproj`；文字模式仍需要快取、緩衝與系統空間。 |
| 判斷 | ⚠️ 可研究短上下文、純文字路線，尚不足以推薦為穩定日常配置。 |

規格依 [Qwen 官方模型卡](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)；實際量化檔案及視覺投影器大小依 [Unsloth 檔案列表](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main)。

**本報告的推論：** 即使 10.8 GB 的檔案可下載，留給 macOS 與執行時的餘裕也很有限。若要實驗，先確認所用 llama.cpp 版本支援此架構，關閉其他大型程式，以短提示、短輸出及單一請求開始，記錄記憶體壓力與 swap。極低位元量化的品質損失需實測；不能沿用原始模型的排行榜分數。官方宣告的長上下文上限也不構成 16 GB 裝置的可用設定。

### 3）GameWorld：適合研究評測，離線模型要另外選

| 項目 | 說明 |
| --- | --- |
| 用途 | 評測 agent 如何觀察遊戲畫面、選擇動作並完成任務。 |
| 規模 | 34 款瀏覽器遊戲、170 項任務。 |
| 可先做的部分 | 安裝 Python 與 Chromium，先以手動遊玩驗證遊戲環境。 |
| 模型需求 | 雲端 API 或自架模型服務；完整視覺評測需要能理解畫面的模型。 |
| M2 判斷 | 評測工具本身可作為試用候選；本次未在 M2 驗證安裝。 |

依 [GameWorld 官方安裝與 Quick Start](https://github.com/gameworld-project/GameWorld)，可以先確認瀏覽器及遊戲正常，再接入模型。Ternary Bonsai 是文字模型，不能直接視為原始視覺評測所需的完整替代品。要比較結果，也應固定同一版本的協定、動作預算及任務；目前程式庫另有影片發布後新增的控制協定。

---

## Near-misses and hardware walls：接近可用與真正的限制

### 「2B」沒有涵蓋完整影片生成管線

Motif-Video 的 2B 是生成主幹規模，完整管線還有 T5Gemma2 文字編碼器、Wan VAE，以及影片處理的中間資料。官方文件中的 15 GB 低用量配置使用 CUDA、offload 與量化；CPU offload 還會占用主記憶體。對 M2 而言，CPU 與 GPU 共用同一個 16 GB 記憶體池，不能把 NVIDIA 的 15 GB VRAM 數字直接套用過來。[官方架構與記憶體表](https://huggingface.co/Motif-Technologies/Motif-Video-2B#-memory-efficient-inference)

同理，AniGen 官方至少 18 GB NVIDIA GPU 的需求，已不符合指定設備；目前合理的體驗途徑是[作者提供的線上展示](https://huggingface.co/spaces/VAST-AI/AniGen)，其推論在遠端執行。[AniGen 安裝要求](https://github.com/VAST-AI-Research/AniGen#-installation)

### Lyra 2 的 131 MB 說法不能用來判斷本機可行性

影片約 [16:28](https://www.youtube.com/watch?v=G8fqduzB5lc&t=988s) 提到約 131 MB，並推論一般裝置應可執行；官方模型卡則標示 **14B、以 WAN-14B 為基礎**。按 14B 權重以 16-bit 儲存估算，單權重約 **28 GB**，尚未包含其他組件。

因此，本報告不採用 131 MB 作為完整模型大小。無法僅由影片確定該數字指向哪個檔案；目前官方安裝還要求 CUDA、FlashAttention 及其他 CUDA 擴充。其權重授權也限定為 NVIDIA 內部科學研究與開發用途，與 Apache 2.0 模型的使用條件不同。[官方模型卡與授權標示](https://huggingface.co/nvidia/Lyra-2.0)、[安裝文件](https://github.com/nv-tlabs/lyra/blob/main/Lyra-2/INSTALL.md)

### 手機展示、3D 觀看與模型生成，要分開評估

WildDet3D 確實有官方連結的 iPhone 裝置端 App，RGBD 模式會用到 LiDAR；這個事實只能證明該手機實作存在。桌面 Python 版本仍使用 CUDA。若目標是 M2，還要找到或完成相應移植，驗證運算子及完整依賴。[iPhone 說明](https://github.com/allenai/WildDet3D/blob/main/demo/iphone/README.md)、[桌面安裝](https://github.com/allenai/WildDet3D#installation)

HY-World 2.0 與 Lyra 2 生成的 3D 資產可以交由其他工具觀看、編輯或模擬；這與在 Mac 上執行生成管線是兩件需要各自查核的事。尤其 HY-World 的 WorldMirror 重建子模型與完整世界生成流程，任務及依賴都不同。[HY-World 架構與模型表](https://github.com/Tencent-Hunyuan/HY-World-2.0)

### 程式公開與模型可用，是兩個發布狀態

OmniShow 目前公開了 Wan-based 訓練、推論及評測程式，但 README 明確註明沒有附上訓練完成的 checkpoint。TokenLight 則查得重新打光論文及展示資訊，尚未找到官方可下載的成品模型；展示站的互動頁本次回傳 403，無法進一步驗證其中的體驗方式。這兩項都應保留為追蹤項目。[OmniShow 發布說明](https://github.com/Correr-Zhou/OmniShow#-data-and-model-preparation)、[TokenLight 論文](https://arxiv.org/abs/2604.15310)、[TokenLight 展示入口](https://vrroom.github.io/tokenlight/)

---

## Suggested actions on this machine：建議行動

1. **想要本機文字助理：先試 Ternary Bonsai 8B 的官方 MLX 版本。** 準備一小組真實工作題目，例如繁體中文摘要、格式化輸出與程式修改；先看答案是否合用，再比較 4B／1.7B 的品質和資源差異。
2. **想挑戰 Qwen 3.6：把它當作極低位元、短上下文實驗。** 先從純文字開始；若持續 swap、速度不可接受或答案品質明顯下降，就不宜納入日常流程。需要一般量化與較長上下文時，改在記憶體更充裕的設備或託管服務評估。
3. **想做影片、3D 生成：先用官方展示或適配的 NVIDIA 環境看成品是否符合需求。** Motif、AniGen、Lyra 與 HY-World 的官方流程，都還不能算是這台 Mac 的直接安裝選項。
4. **想研究 agent 評測：先試 GameWorld 的遊戲環境。** 跑通一個遊戲與一項任務，再決定使用雲端模型，或另做本機視覺模型的介面適配。
5. **想做配音：將 Gemini 3.1 Flash TTS 歸入雲端方案評估。** 保留影片所談的版本，但注意官方現在將其標記為 legacy preview；新專案應重新確認當前支援的型號。若需求是完全離線，這個服務不符合條件。[目前版本狀態](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview)

## 查核日與影片日期之間的變化

- **Motif-Video：** 官方紀錄顯示，ComfyUI 及 GGUF 支援於 4 月 28 日發布，Diffusers 支援於 5 月 15 日加入；影片中的「即將支援」已發生變化，但沒有因此證明 M2／16 GB 可用。[更新紀錄](https://huggingface.co/Motif-Technologies/Motif-Video-2B#-news)
- **HY-World 2.0：** 4 月先發布部分程式及 WorldMirror；5 月再發布 HY-Pano、WorldStereo 與世界生成程式。本報告評估的是這些後續可查到的 2.0 元件。[發布紀錄](https://github.com/Tencent-Hunyuan/HY-World-2.0#-news)
- **HappyOyster：** 影片描述申請早期體驗；查核時已提供雲端 API／SDK 文件，不能沿用「只有候補名單」的描述。[目前文件](https://www.alibabacloud.com/help/en/model-studio/happyoyster-overview)
- **GPT-Rosalind：** 8 月的官方文件增加 Workbench 存取流程；本報告只據此確認服務型態與申請路徑，不把 Workbench 當成影片當時已發布的功能。[官方說明](https://developers.openai.com/blog/rosalind-workbench)
- **Gemini 3.1 Flash TTS：** 截至查核日已是 legacy preview；此處仍評估影片中的 3.1 版本。[官方模型文件](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview)

## Sources

以下以第一方資料為主；社群量化會明確標示。正文與表格內的連結對應各項判斷。

- **影片與章節：** [AI Search 原始影片](https://www.youtube.com/watch?v=G8fqduzB5lc)，使用官方說明欄與英文自動字幕。
- **參考格式：** [2026-09-20 Local Runnability report](https://github.com/pomodorozhong/rabbit-holes/blob/master/topics/local_model_reports/report-2026-09-20-video-ai-news.md)。
- **Prompt Relay：** [作者程式庫](https://github.com/GordonChen19/Prompt-Relay)、[Wan2.2 官方程式庫](https://github.com/Wan-Video/Wan2.2)。
- **Ternary Bonsai：** [PrismML 公告](https://prismml.com/news/prismml-introduces-ternary-bonsai-model-family)、[8B MLX](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-mlx-2bit)、[4B MLX](https://huggingface.co/prism-ml/Ternary-Bonsai-4B-mlx-2bit)、[1.7B MLX](https://huggingface.co/prism-ml/Ternary-Bonsai-1.7B-mlx-2bit)。
- **GPT-Rosalind：** [OpenAI Docs：Rosalind Workbench 與 GPT-Rosalind 存取說明](https://developers.openai.com/blog/rosalind-workbench)。
- **WildDet3D：** [官方程式庫](https://github.com/allenai/WildDet3D)、[iPhone App 文件](https://github.com/allenai/WildDet3D/blob/main/demo/iphone/README.md)。
- **Motif-Video 2B：** [官方模型卡](https://huggingface.co/Motif-Technologies/Motif-Video-2B)、[官方 ComfyUI 整合](https://github.com/MotifTechnologies/ComfyUI-MotifVideo2B)。
- **HubSpot：** [影片 10:54 的贊助指南介紹](https://www.youtube.com/watch?v=G8fqduzB5lc&t=654s)。
- **AniGen：** [官方程式庫與硬體要求](https://github.com/VAST-AI-Research/AniGen)、[官方線上展示](https://huggingface.co/spaces/VAST-AI/AniGen)。
- **HappyOyster：** [Alibaba Cloud 官方 API／SDK 概覽](https://www.alibabacloud.com/help/en/model-studio/happyoyster-overview)。
- **Lyra 2：** [NVIDIA 模型卡](https://huggingface.co/nvidia/Lyra-2.0)、[安裝文件](https://github.com/nv-tlabs/lyra/blob/main/Lyra-2/INSTALL.md)。
- **HY-World 2.0：** [Tencent 官方程式庫、模型表與更新紀錄](https://github.com/Tencent-Hunyuan/HY-World-2.0)。
- **OmniShow：** [官方程式庫及 checkpoint 發布限制](https://github.com/Correr-Zhou/OmniShow)。
- **Claude Opus 4.7：** [Anthropic 官方公告](https://www.anthropic.com/news/claude-opus-4-7)。
- **Qwen3.6-35B-A3B：** [Qwen 官方模型卡](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)、[Unsloth 社群 GGUF 量化與檔案大小](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main)。
- **機器人三章：** [H1 奔跑展示 26:14](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1574s)、[馬拉松 26:57](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1617s)、[生產線 27:51](https://www.youtube.com/watch?v=G8fqduzB5lc&t=1671s)。本報告僅按影片確認章節性質，未另查證其速度、產量或比賽紀錄。
- **TokenLight：** [作者論文](https://arxiv.org/abs/2604.15310)、[展示入口](https://vrroom.github.io/tokenlight/)。
- **GameWorld：** [官方程式庫](https://github.com/gameworld-project/GameWorld)、[專案頁](https://gameworld-project.github.io/)。
- **Gemini 3.1 Flash TTS：** [Google 官方模型文件](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview)。
