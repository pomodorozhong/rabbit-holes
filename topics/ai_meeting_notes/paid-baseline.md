# Paid meeting-notes baseline

Notion AI meeting notes, Amie, and Spellar AI combine transcription and summaries with calendars, saved meeting history, editing, sharing, and follow-up work. This background note records their documented features, prices, and processing boundaries as inspected on **2026-10-06**. It explains where the [Feature catalogue](feature-catalogue.md) came from; later work tested local models in a [recording trial](README.md#what-the-recording-trial-found).

| Field | Value |
| --- | --- |
| Research date | **2026-10-06**, Asia/Taipei |
| Question | What features, prices, and processing boundaries do the reviewed meeting assistants document? |
| Products | Notion AI meeting notes, Amie, Spellar AI |
| Evidence | Official documentation, pricing controls, release notes, policies, and public product examples |
| Status | Background research. The feature catalogue is accepted; paid-product quality has not been tested. |
| Next step | [Feature catalogue](feature-catalogue.md), then the [recording trial result](README.md#what-the-recording-trial-found) |

## Prices and what the subscription buys

The table shows **USD per user or seat, before tax**, from the public monthly and annual pricing controls inspected on October 6. “Annual equivalent” divides the annual charge by 12. For example, Notion Business was $24 with monthly billing, or $240 for a year: the annual equivalent is $20 per month, but payment is billed annually. Twelve monthly payments at $24 total $288. Regional, App Store, legacy, and negotiated prices can differ.

| Product / plan | Monthly billing | Twelve monthly payments | Annual equivalent | Annual billed total | Scope at this tier |
| --- | ---: | ---: | ---: | ---: | --- |
| [Notion Business](https://www.notion.com/pricing) | $24 | $288 | $20/month | $240 | Meeting notes plus the Business workspace and its AI features. Enterprise is quoted separately. |
| [Amie Pro](https://amie.so/pricing) | $25 | $300 | $20/month | $240 | Meeting notes, chat, scheduling, and audio import. |
| [Amie Business](https://amie.so/pricing) | $50 | $600 | $40/month | $480 | Adds custom templates, shared-note branding, and advanced CRM/ATS integrations. |
| [Spellar Pro](https://www.spellar.ai/pricing) | $20 | $240 | $15/month | $180 | Recordings, transcripts, summaries, chat, model choice, templates, and integrations. Teams has custom pricing. |

### Incremental cost with an existing subscription

An existing subscription changes the added cost of meeting notes. The scenarios below use the same billing cycle on both sides of an upgrade; actual charges can also depend on prorating and the number of paid workspace members. They do not assume the reader holds any particular subscription.

| Existing subscription | Added cost for the relevant baseline |
| --- | --- |
| Notion Business or Enterprise | $0 extra subscription cost for included meeting notes. Other AI usage can incur credits. |
| Notion Plus → Business | Plus is $12 monthly or $10/month annually: the difference is **$12/month** ($144 over twelve monthly renewals) or **$120/year**. |
| Current Amie Pro | $0 extra for the Pro baseline. Business features add **$25/month** ($300 over twelve renewals) or **$240/year**. |
| Amie Personal or legacy plan | Current upgrade price and credits require account-specific verification; do not assume today's Pro entitlement. |
| Spellar Pro | $0 extra for its included features. An existing Setapp subscription has a separate AI-credit route whose incremental cost is not established here. |

The Notion calculations use the [price controls inspected on October 6](https://www.notion.com/pricing); Amie's use [Pro and Business pricing](https://amie.so/pricing). Spellar's [AI policy](https://www.spellar.ai/ai-usage-policy) distinguishes Setapp processing from its direct subscription.

### Limits, trials, and possible extra charges

- **Notion:** Meeting Notes has a **10-hour daily cap**, separate from the six-hour/monthly allowance for Agent chat. Premium models and additional Agent usage can spend credits. Custom Agents also require credits, so automated follow-ups are a separate cost consideration. [Usage allowance](https://www.notion.com/help/manage-your-usage-allowance-for-notion-ai)
- **Amie:** The inspected pricing page advertises unlimited meeting notes and AI chat and a **7-day trial**. Its billing documentation describes 25 one-time free note credits; feature documentation still refers to “Legacy Pro” and “Pro+.” The page names do not settle what an older account includes; that requires account-specific confirmation. No numerical duration, import-size, or fair-use ceiling was established. [Pricing](https://amie.so/pricing), [billing](https://amie.so/documentation/account/billing), [notes documentation](https://amie.so/documentation/features/ai-notes)
- **Spellar:** Pricing advertises unlimited recordings, transcription, summaries, and chat, included premium models, and a **14-day money-back guarantee**. The download page also describes a 7-day Pro trial; availability depends on the purchase route. Numeric usage ceilings were not established. Bringing an API key can add charges from that provider; “included models” does not establish that provider-funded calls are free. [Pricing](https://www.spellar.ai/pricing), [download](https://www.spellar.ai/download), [subscription terms](https://www.spellar.ai/terms-of-subscription)

## Language, platform, and processing boundaries

Capturing audio on a Mac does not determine where transcription or summary generation runs. **ASR** means automatic speech recognition: the step that turns audio into text. Check that step, the summary step, and saved data separately when deciding whether a workflow stays local.

| Product | English / Chinese / mixed language | Target-Mac requirements | Local capture, processing, and storage |
| --- | --- | --- | --- |
| Notion | English and Chinese listed; speaker labels **English-only**. Chinese-English switching quality unspecified. | Desktop app ≥4.7.0; macOS ≥13. Browser/mobile capture microphone only. | Desktop mic + system audio; cloud transcription; offline meeting notes unsupported. [Meeting-notes help](https://www.notion.com/help/ai-meeting-notes) |
| Amie | English and Chinese in the named language set; multilingual meetings documented, quality untested. | Installation guide: macOS ≥10.15, Intel/Apple Silicon; desktop required for bot-free system-audio recording. | Audio captured locally, uploaded after the meeting; cloud ASR and summaries; notes stored server-side. [Languages](https://amie.so/changelog/embed), [installation](https://amie.so/documentation/getting-started/installation), [processing](https://amie.so/documentation/features/ai-notes) |
| Spellar | Advertises **50+ transcription languages**. Exact Chinese coverage by engine and Chinese-English switching remain unresolved. App Store UI languages are not an ASR language list. | Download page inspected on October 6: macOS ≥15, Intel/Apple Silicon; native iPhone/iPad and browser recorder also advertised. | On-device transcription available; server transcription opt-in. AI summaries/chat send input to external providers. [Pricing](https://www.spellar.ai/pricing), [download](https://www.spellar.ai/download), [AI policy](https://www.spellar.ai/ai-usage-policy), [App Store](https://apps.apple.com/us/app/spellar-ai-meeting-note-taker/id6473629578) |

Spellar illustrates this distinction: it offers on-device transcription, but its AI policy describes sending summary and chat inputs to third-party providers. Bringing an API key changes who supplies access to that provider; it does not move the provider's model onto the Mac. The inspected evidence does not establish a completely offline paid workflow covering all catalogue features. [Spellar AI policy](https://www.spellar.ai/ai-usage-policy)

For saved data, Notion offers optional local retention of the recorder's ten most recent audio files; this does not make transcription local. Amie stores notes in encrypted cloud storage. Spellar's policy describes configurable audio retention and keeping transcripts, summaries, and speaker names until the recording is deleted; it also identifies cloud storage. Treat device-only audio retention separately from cloud text storage and inference. [Notion help](https://www.notion.com/help/ai-meeting-notes), [Amie pages](https://amie.so/documentation/features/pages), [Spellar privacy](https://www.spellar.ai/privacy)

## Feature catalogue

The [Feature catalogue](feature-catalogue.md) turns these workflows into separate input/output definitions. Speaker separation, naming people, extracting a task, and delivering that task to another app have different dependencies. Keeping them separate helps explain what a local pipeline can supply and what application work remains.

## Public examples and their limits

- **Notion:** Documented examples link summary citations to transcript lines and offer selectable summary instructions. These demonstrate intended interaction, not output quality. [Meeting-notes help](https://www.notion.com/help/ai-meeting-notes)
- **Amie:** The May 2025 changelog demonstrates labelling a speaker and asking what that person said; later entries add action grouping and shareable timestamps. These examples connect identity, retrieval, and follow-up behavior, but contain no shared audio/reference-transcript test. [Changelog](https://amie.so/changelog/embed)
- **Spellar:** The homepage's sample roadmap meeting exposes Summary, Transcript, and Actions tabs. Observed outputs include timestamped named turns, separate decisions, and owner-labelled tasks; its sample chat shows a meeting/time citation. These are curated public examples, not evidence of generation accuracy, reliable deadlines, or actual audio alignment. [Interactive example](https://www.spellar.ai/)

## Limits of the background comparison

The table below identifies where the inspected descriptions leave a practical question unanswered. For example, advertised action items do not establish whether a model will keep an unstated deadline empty. These questions limit the paid comparison; the local investigation can proceed using the catalogue definitions without further vendor research.

| Unresolved detail | Affected IDs | Limit on the background evidence |
| --- | --- | --- |
| Chinese-English speech and speaker naming | MN-04, MN-06, MN-07 | Notion documents language/setup limits; Amie claims mixed support; Spellar's engine-specific Chinese support is unestablished. Quality on the same test recording was not tested. |
| Transcript navigation/export detail | MN-05, MN-12, MN-16 | Audio retention, timestamp granularity, edit propagation, and preservation of labels/citations in exports are not established across the products. |
| Exact action ownership and deadlines | MN-09, MN-10, MN-21 | The examples do not establish reliable separation of proposals, decisions, owners, and stated deadlines. |
| Live and long meetings | MN-01, MN-04, MN-08 | Amie's August 2026 changelog calls live transcription experimental. Release availability, backlog, reliability, and per-session limits remain untested. |
| Pricing and delivery route | MN-11, MN-19, MN-21 | Legacy entitlements, advanced integration gates, optional credits, API charges, and destination-service costs vary by account and route. |
| Fully local behavior and storage | MN-20 | Spellar advertises local ASR while cloud AI/text storage is documented. Its older mobile blog and current engine choices describe different processing configurations; build/settings and fallback behavior were not tested. |
| Documentation inconsistencies | MN-02, MN-13, MN-17 | Notion's upload instructions exclude video while its storage section mentions it. Amie plan names and Spellar trial/refund routes vary across pages. |

### Scope decision

The catalogue is the accepted reference for local work. The next steps were to check the models used by the open-source projects and try a meeting recording on the M2 Pro / 16 GB Mac. That trial is reported in meeting-recap as the [HushScribe recording trial](https://github.com/pomodorozhong/meeting-recap/blob/main/docs/experiments/2026-10-24-hushscribe-trial.md) and the [full-recording run](https://github.com/pomodorozhong/meeting-recap/blob/main/docs/experiments/2026-10-24-full-recordings.md) with Whisper and Sortformer; the [topic overview](README.md#what-the-recording-trial-found) summarizes what it found.

## Sources

All sources below are primary vendor pages or the developer's App Store listing, inspected on **2026-10-06**. The [product coverage comparison](product-coverage.md) uses the source labels below.

- **N1** — [Notion meeting-notes help](https://www.notion.com/help/ai-meeting-notes) — operational workflow, language, platform, audio handling, and restrictions.
- **N2** — [Notion meeting-notes product page](https://www.notion.com/product/ai-meeting-notes) — advertised notes and follow-up behavior.
- **N3** — [Notion AI FAQ](https://www.notion.com/help/notion-ai-faqs) — Agent, search, and general AI features.
- **N4** — [Notion export documentation](https://www.notion.com/help/export-your-content) — general page export formats.
- **N5** — [Notion AI usage allowance](https://www.notion.com/help/manage-your-usage-allowance-for-notion-ai) — daily meeting cap and other AI allowances/credits.
- [Notion pricing](https://www.notion.com/pricing) — monthly and annual price controls.
- **A1** — [Amie pricing](https://amie.so/pricing) — current Pro/Business prices and feature gates.
- **A2** — [Amie AI Meeting Notes](https://amie.so/documentation/features/ai-notes) — capture, cloud processing, summaries, actions, and language modes.
- **A3** — [Amie changelog](https://amie.so/changelog/embed) — language list, timestamps, speaker naming, PDF export, vocabulary, and live-feature experiments.
- **A4** — [Amie product page](https://amie.so/) — recording controls and private-note context.
- **A5** — [Amie pages documentation](https://amie.so/documentation/features/pages) — history, search, edits, storage, and sharing.
- **A6** — [Amie installation](https://amie.so/documentation/getting-started/installation) — desktop platforms and requirements.
- [Amie billing](https://amie.so/documentation/account/billing) — free credits and subscription/legacy context.
- **S1** — [Spellar product page and public demo](https://www.spellar.ai/) — sample outputs and advertised chat, templates, recaps, and integrations.
- **S2** — [Spellar download](https://www.spellar.ai/download) — Mac requirements, other capture surfaces, and trial messaging.
- **S3** — [Spellar App Store listing and release history](https://apps.apple.com/us/app/spellar-ai-meeting-note-taker/id6473629578) — transcription engine choices and diarization changes; UI languages do not establish ASR languages.
- **S4** — [Spellar privacy policy](https://www.spellar.ai/privacy) — calendar-assisted naming, storage, retention, and provider processing.
- **S5** — [Spellar 1.9.0 release](https://www.spellar.ai/updates/v-1.9.0) — editable notes and follow-up chat commands.
- **S6** — [Spellar mobile launch explanation](https://www.spellar.ai/page/spellar-ios-official-launch) — historical cloud-processing description and synced history; current configurations require newer evidence.
- **S7** — [Spellar 1.5.0 release](https://www.spellar.ai/updates/v-1.5.0) — keyword search and custom webhooks.
- **S8** — [Spellar multilingual/export release](https://www.spellar.ai/updates/v1-3-14) — original-language output and Markdown copying.
- **S9** — [Spellar Google Drive export release](https://www.spellar.ai/updates/v-1.4.7) — summary/audio export and summary length.
- **S10** — [Spellar pricing](https://www.spellar.ai/pricing) — prices, included features, on-device transcription claim, and Teams tier.
- **S11** — [Spellar AI usage policy](https://www.spellar.ai/ai-usage-policy) — provider API processing; revised September 28, 2026.
- [Spellar subscription terms](https://www.spellar.ai/terms-of-subscription) — subscription and trial routes.

## Method and limitations

The research used official pages, release notes, monthly and yearly pricing controls, and the summary, transcript, and action views in the public Spellar demo. The cost scenarios are arithmetic based on the inspected prices. These materials show the documented workflow and advertised behavior, but cannot establish accuracy or processing time on a real meeting.

The research did not include buying subscriptions, changing account settings, or submitting meeting audio. The uncertainties above therefore remain unresolved, including mixed-language quality, export contents, access permissions, and deadline extraction. The prices and product descriptions reflect the October 6 inspection. The [local investigation](README.md#what-the-recording-trial-found) used the catalogue as its reference; its recording trial tested transcription and speaker separation, not these product uncertainties.
