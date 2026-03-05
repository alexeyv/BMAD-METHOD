---
source_artifacts:
  - upstream/project-idea-pyramid.md
  - upstream/brainstorming-pyramid.md
  - upstream/domain-research-pyramid.md
synthesis_tensions:
  - "TASK#5: Open-source purity vs. premium monetization"
  - "TASK#6: Voice-first as advantage vs. kitchen noise degradation"
  - "TASK#7: Recipe format strategy — YAML gap-filling vs. Cooklang interop"
  - "TASK#8: Push-mode coaching vs. beginner/chef skill level ambiguity"
  - "TASK#9: Hardware sensor integration scope vs. software-only TAM"
  - "TASK#10: Bash timer implementation vs. ±1s precision risk"
  - "TASK#11: Food safety liability — critical risk vs. manageable via guardrails"
evidence_gaps:
  - "Adoption demand for community-contributed protocols (no demand signal cited)"
  - "User segmentation research — home cook vs. professional chef mix is inferred not surveyed"
  - "Monetization model — open-source vs. premium unresolved across all artifacts"
  - "Sensor integration minimum viable scope (mock APIs vs. real hardware) — unresolved in project-idea"
  - "Recipe format adoption path — YAML vs. Cooklang vs. hybrid — no comparative user evidence"
  - "Bash vs. Python timer implementation decision — mitigations referenced but implementation language not decided"
date: 2026-03-04
---

# PRD: Sous-Chef Agent Skill

## Governing Insight

The Sous-Chef Agent Skill is the right product at the right moment: a timer-driven, push-mode cooking companion that prevents planning failures (not technique failures) through structured pre-flight briefings, file-backed state persistence, and voice-first guidance — delivered as the first open-source, software-only, cross-platform AI cooking skill in a nascent Agent Skills ecosystem where the high-AI + full-cooking-integration quadrant is currently held only by proprietary hardware costing $700–$1,700. With 86% of meals cooked at home, the Agent Skills standard newly opened in December 2025, and smart kitchen adoption accelerating toward 30.8% household penetration by 2029, this skill can define a category before the window closes.

---

## Executive Summary

The Sous-Chef Agent Skill addresses five real gaps in home cooking: no AI-guided real-time support, no structured machine-readable recipe format that spans temperature targets and sensor checkpoints, no timer-aware sequential coordination, no proactive guidance during the dead time between cooking phases, and no cooking skill anywhere in the Anthropic Agent Skills ecosystem. [project-idea s2, domain-research s3]

Three forces converge to make this the right moment:

1. **Market**: Home cooking demand is at historic highs (86% of meals at home, surpassing COVID peaks), with 25% of adults skipping recipes they want to make due to lack of confidence. [domain-research s2]
2. **Platform**: The Agent Skills standard opened December 2025, adopted by Anthropic, OpenAI, and Microsoft — creating cross-platform distribution that bypasses crowded app stores. [domain-research s5]
3. **Competitive vacuum**: The high-AI + full-cooking-integration market quadrant is occupied only by closed, expensive proprietary hardware. Yummly (backed by Whirlpool) shut down December 2024, demonstrating that well-funded cooking apps fail without genuine differentiation. [domain-research s3]

The skill's governing design insight — from the brainstorming artifact — is that most cooking mistakes are planning failures, not technique failures. Checklists and pre-flight briefings fix this better than real-time monitoring or reactive instruction. [brainstorming s6] The architecture is therefore a timer-driven event loop: timer fires → agent reads state file + protocol → pushes voice summary + screen detail → updates state. [brainstorming s4] This produces a skill that is proactive, not reactive — a push-mode coach that owns the timeline so the cook never has to ask "what's next?"

### What Makes This Special

- **Open-source, software-only, hardware-agnostic**: No $700–$1,700 appliance required. Works with existing kitchen equipment and off-the-shelf sensors. [domain-research s3, s6]
- **First in category on a new platform**: The Agent Skills standard is under three months old as a public standard. Category definition now = category leadership later. [domain-research s1]
- **The right architecture for the actual problem**: Push-mode + pre-flight briefings is derived from real concurrent kitchen experience — tested mid-braise, not imagined from user stories. [brainstorming s7]
- **YAML protocol as emerging standard**: The first format to natively support temperature targets, sensor checkpoints, timer scripts, phase-based execution, and scaling rules together — filling a gap no existing format addresses. [domain-research s5]
- **Distributed as a skill, not an app**: Runs anywhere an AI agent runs (Claude, Gemini, Copilot, Cursor) — no download, no account, no proprietary lock-in. [domain-research s3]

---

## Target Users & User Journeys

### Primary Users

The primary user is the **home cook** — specifically the food enthusiast who wants to execute complex, multi-phase recipes (braises, stocks, roasts) with precision, but lacks the internalized muscle memory that transforms protocol knowledge into confident real-time execution. The brainstorming session was explicit about the design target: "single guy kitchen assumptions — one pan, one pot, one cutting board, one pair of hands." [brainstorming s3, Theme 9]

Secondary user segments from domain research:
- **Home Cooks (Casual)**: ~55–60% of recipe app users — primary volume target [domain-research s2]
- **Food Enthusiasts**: ~25–30% — high-value segment, willing to invest in precision [domain-research s2]
- **Professional Chefs**: ~10–15% — secondary target for recipe standardization and multi-dish coordination [domain-research s2]

> **TENSION [TASK#8]**: The brainstorming artifact's push-mode coaching model (proactive, directive, step-by-step drip-feed) [brainstorming s2] is well-suited to the home cook who hasn't memorized the protocol. However, the project-idea artifact explicitly flags "How should the skill balance simplicity (beginner cooks) vs. sophistication (chefs)?" as an unresolved design question [project-idea s13]. A professional chef or advanced home cook would find push-mode briefings patronizing and interruptive. This architectural choice — which user is the skill optimized for — is unresolved and would reshape guidance verbosity, protocol schema, and sensor integration depth.

### Core Pain Points

1. **Recipe execution friction**: No AI-guided real-time support that understands protocols deeply. [project-idea s2]
2. **Planning failures dominate**: Most cooking mistakes are forgetting steps — misaligned expectations, skipped prep, surprised by phase transitions — not technique failures. Checklists and briefings fix this; monitoring does not. [brainstorming s6]
3. **Protocol complexity**: Multi-phase recipes require precise temperature control, timing, and sequential logic that humans struggle to coordinate without support. [project-idea s2]
4. **Timer/tracking is manual**: Cooks manage separate timers, temperature probes, and step checklists without AI integration. [project-idea s2]
5. **"What does perfect look like?"**: Reference photos showing target state at each step are the number-one unmet need — what words and descriptions cannot adequately convey. [brainstorming s6]
6. **Kitchen confidence gap**: 25% of adults skip specific recipes due to lack of confidence. [domain-research s2]

### User Journeys

**Journey 1: First-Time Execution** [project-idea s5]
1. User selects a protocol or loads from library
2. Sous-Chef validates ingredients, surfaces gaps before cooking begins
3. Pre-flight briefing: phase overview, critical timings, upcoming equipment needs
4. Agent drip-feeds one instruction at a time with timing, temperature targets, sensory cues
5. During dead time (e.g., 90-min braise), agent delivers lookahead briefings for the next phase
6. Timer fires → agent pushes voice summary (2 lines) + screen detail
7. Sensors polled via voice ("TC reading?") — human reads, agent calculates
8. Dish completed with audit log for reproducibility

**Journey 2: Troubleshooting / Mistake Recovery** [project-idea s5, brainstorming s3 Theme 4]
1. User reports a failure state ("The onions are burning")
2. Agent recognizes the failure mode, calculates forward — no dead ends, only forks
3. Agent is transparent about impact ("2 out of 10 on the final dish — here's how we compensate")
4. Dish recovered with explicit adjusted path

**Journey 3: Dead-Time Learning** [brainstorming s2, s6]
1. Long hold phase begins (e.g., braise at 90°C for 90 minutes)
2. Agent grants explicit permission to leave: "You can walk away. I'll call you back in 75 minutes."
3. Agent uses the hold to deliver lookahead briefings on the next phase
4. Q&A window opens: hash out confusion before the next phase is under heat

**Journey 4: Ingredient Substitution** [project-idea s5] *(Phase 2)*
1. User lacks an ingredient
2. Agent suggests compatible substitutes with flavor/texture impact explanation
3. User proceeds with confidence

---

## Core Design Principles

These five principles emerged as the foundational truths of the brainstorming session and govern all architectural decisions. [brainstorming s2]

1. **Use dead time to eliminate live confusion** — Pre-flight briefings during wait periods prevent mistakes and reduce cognitive load during active cooking. The briefing IS the error prevention mechanism AND the teaching moment AND the technique explainer. [brainstorming s2, s6]

2. **Push-mode, not pull-mode** — The agent owns the timeline and proactively delivers guidance. The cook should never have to ask "what's next?" The timer is the event loop — not a utility but the core runtime driving all interaction. [brainstorming s2, s4]

3. **The agent IS your missing muscle memory** — The protocol exists, you've read it, but you haven't memorized it. The agent drip-feeds it to you at the right moment. "One instruction, one action, one confirmation, next instruction." [brainstorming s2, s3 #34]

4. **Voice is the headline, screen is the article** — Hard rule: voice output never more than two short sentences. Full text + science + reference photos on screen for when you need more. The screen is a glanceable instrument panel, not a chat log. [brainstorming s2, s3 #44, #45]

5. **Science serves diagnostics, not education** — Full physics/chemistry depth because understanding the process gives you the power to reason about failures. Every science explanation comes with "so here's what goes wrong if..." [brainstorming s2, s3 #42]

> **TENSION [TASK#6]**: Principle 4 designates voice as primary output for hands-free cooking. However, domain research flags that kitchen noise (ventilation fans, sizzling, running water) degrades voice recognition and recommends push-to-talk as fallback [domain-research s5]. Voice-first may not be optimal in the exact environment it is designed for. Both perspectives are preserved here; the implementation must address noise robustness.

---

## Success Criteria & Metrics

### MVP Success (Phase 1) [project-idea s6]

| Criterion | Definition |
|-----------|-----------|
| **Functionality** | Skill successfully guides a user through a complete cooking protocol end-to-end |
| **Accuracy** | Temperature targets met, timing honored, sensory cues validated |
| **Usability** | Agent provides clear, contextual guidance at each step with no user confusion |
| **Reliability** | Timers function correctly; file-backed state survives session interruption |
| **Documentation** | Protocol schema is clear and complete; 3–5 example protocols validated |

### Extended Success [project-idea s6]

| Metric | Target | Evidence Strength |
|--------|--------|-------------------|
| Platform adoption | Skill used across Claude, Gemini, Copilot, Cursor | moderate |
| Community protocols | 10+ community-contributed protocols in library | anecdotal |
| Sensor integration | Real FireBoard/MEATER data successfully integrated | moderate |
| Marketplace presence | Featured on agentskills.io, SkillsMP, agentskill.sh | anecdotal |
| External citations | Referenced in cooking blogs and chef communities | anecdotal |

> **EVIDENCE GAP**: The 10+ community-contributed protocols target [project-idea s6] has no supporting demand signal or prior adoption evidence. It is an aspirational target without research backing.

### Market-Level Success Signals [domain-research s6]

- First mover position established in high-AI + full-cooking-integration quadrant before Google/Samsung entry matures
- YAML cooking protocol recognized as an emerging open standard
- Agent Skills ecosystem penetration growing — Gartner projects 40% of enterprise apps will feature AI agents by end of 2026 [domain-research s1]

---

## Domain & Regulatory Considerations

### Food Safety (CRITICAL) [domain-research s4]

The FDA/USDA temperature standards are non-negotiable and must be hard-coded into the skill with minimums that **bypass LLM reasoning** — they cannot be overridden by user instruction or model response.

| Food Type | Minimum Safe Temperature |
|-----------|-------------------------|
| Poultry | 165°F (74°C) |
| Ground meats | 155°F (68°C) |
| Whole cuts, seafood | 145°F (63°C) |
| Temperature Danger Zone | 41–135°F (5–57°C) — bacteria double every 20 minutes |

**Implementation requirement**: Local Python/MCP safety overrides that fire when temperature thresholds are breached, bypassing the LLM response path entirely. Conservative defaults. Clear disclaimers. Audit logs of all safety-critical advice. [domain-research s7]

> **TENSION [TASK#11]**: Domain research flags food safety liability as CRITICAL severity, then claims it is manageable through guardrails [domain-research s4, s7]. The interaction between FDA/USDA liability for AI-guided cooking temperature advice, the AI LEAD Act's classification of AI as "product" under federal product liability, state AI laws (California, Texas, Colorado, Illinois effective Jan–June 2026), and Anthropic's AUP is not fully mapped in any artifact. The claim that guardrails make this manageable is moderate-evidence; the full regulatory surface is larger than stated.

### AI/ML Regulatory Framework [domain-research s4]

- **EU AI Act**: Cooking assistant classified as limited/minimal risk. Article 50 transparency obligations (must disclose AI nature) effective **August 2, 2026** — before the skill's extended success horizon.
- **US**: Federal-state tension active. Trump EO (Dec 2025) attempting to preempt state laws; FTC policy statement due March 2026. Companies should continue to comply with applicable state AI laws while landscape resolves.
- **Anthropic AUP**: Must disclose AI nature at session start.

### Open Source Licensing [domain-research s4]

**Recommendation: Apache 2.0** — permissive, includes patent protection, aligns with Anthropic ecosystem. Basic recipe instructions (ingredient lists, temperatures, times) are not copyrightable. The YAML cooking protocol format can be freely developed and open-sourced.

> **TENSION [TASK#5]**: All three artifacts frame the project as open-source throughout. Domain research explicitly positions open-source as a competitive differentiator [domain-research s3]. However, project-idea's questions section asks "Is this open-source only, or are there premium features?" [project-idea s13], and domain research notes a potential B2B revenue path via HACCP-as-a-Service for commercial kitchens [domain-research s6]. The business model — pure open-source, open-core, or dual-license — is unresolved. The human decides.

### Data Protection [domain-research s4]

- GDPR (EU users), CCPA/CPRA (California, ADMT rules Jan 2026), COPPA (children under 13)
- Data at risk: cooking preferences (may reveal religion, health), voice commands, sensor data, usage patterns
- **Design principle**: privacy-by-design, local-first sensor data, minimal collection

### Key Regulatory Dates

| Date | Event |
|------|-------|
| Jan 1, 2026 | CCPA ADMT rules + State AI laws effective |
| Aug 2, 2026 | EU AI Act transparency obligations enforceable |
| Sept 2026 | EU CRA IoT vulnerability reporting mandatory |

---

## Scope & MVP Definition

### What's In v0.1 [brainstorming s5, project-idea s3, domain-research s7]

**1. Smart Protocol Format + Compiler**
- YAML schema that carries: phases, steps, calibrated sensor targets, voice summaries (2-line), briefing text, reference photo links
- `references/PROTOCOL_FORMAT.md` specification
- `references/TEMPERATURE_GUIDE.md` — temperature targets for common techniques
- `scripts/validate-protocol.sh` — validates recipe protocols against schema
- `scripts/parse-protocol.sh` — YAML to executable steps
- 3–5 example protocols: beef stew, chicken stock, risotto, sauce béarnaise, roasted vegetables

**2. Timer-Driven Execution Engine with Push-Mode**
- Core runtime event loop: timer fires → agent reads state file + protocol → determines phase/next step → pushes voice summary (2 lines) + screen detail → updates state file
- `scripts/timer.sh` — background timer with progress callbacks
- Pre-flight briefings during dead time phases
- Aviation-style checklists at phase transitions

**3. File-Backed State Manager**
- Cook state on disk: phase, elapsed time, temperatures, deviations
- Self-compacting: completed phases collapse to one-line summaries
- Crash-recoverable: new session reads file, picks up where it left off
- Context-window immune: state never grows beyond agent context capacity

**4. Sensing Stack (Voice-In, Human-Read)**
- No hardware integration in v0.1 — human reads the thermocouple/IR display and speaks the number
- Agent does the calibration math
- Camera via photo-in-chat (drag-and-drop, no pipeline needed)

**5. Interface Layer**
- Voice: macOS `say` for TTS (low latency, free) — cross-platform upgrade deferred
- Screen: glanceable dashboard (current step bolded, timer visible, key numbers prominent)
- Two-line voice discipline enforced in all agent responses

**6. Skill Collection Architecture (BMM Pattern)** [brainstorming s3 #74, s4]
- `/sous-chef help` — orchestrator, routes to right workflow
- `/sous-chef research` — deep science dive on a dish
- `/sous-chef compile` — research/recipe → structured protocol YAML
- `/sous-chef cook` — real-time execution engine
- `/sous-chef review` — post-cook debrief *(deliberately cut from v0.1)*

**7. Food Safety Guardrails (Non-Negotiable)**
- Hard-coded FDA/USDA temperature minimums that bypass LLM reasoning
- Conservative defaults, clear disclaimers
- Audit log for all safety-critical guidance

### What's Cut from v0.1 [brainstorming s5]

| Cut Feature | Rationale |
|-------------|-----------|
| Hardware sensor integration (FireBoard, MEATER APIs) | Voice-in is sufficient; hardware integration is Phase 2 |
| Camera pipeline (watched folder, continuous feed) | Drag-and-drop photo-in-chat is sufficient for v0.1 |
| Reference photo library | Describe in text for now; library is Phase 2 |
| Familiarity decay / depth adaptation modes | v-future |
| Ingredient scaling and substitution | Phase 2 |
| Multi-recipe coordination | Phase 2 |
| Learning from past cooks | v-future |
| `/sous-chef review` (post-cook debrief) | v-future |
| Community protocol contributions | Phase 3 |
| Marketplace submissions | Phase 3 |
| Cross-platform TTS (Piper, ElevenLabs) | Phase 2 upgrade from macOS `say` |
| Cooklang / Schema.org interoperability | Phase 3 |

> **TENSION [TASK#9]**: Brainstorming explicitly cuts sensor hardware integration from v0.1 [brainstorming s5], relying on human voice-read sensors. Domain research positions the skill as "software-only, cross-platform" and argues this is the strategic differentiator [domain-research governing insight]. However, project-idea includes sensor integration hooks in Phase 1 and "temperature probe integration hooks" as a Phase 1 deliverable [project-idea s3]. These are partially reconcilable (hooks in Phase 1 ≠ live integration), but the scope of Phase 1 sensor work remains ambiguous.

### Phase 2: Sensor Integration + Extended Features (Weeks 7–12) [project-idea s3, domain-research s7]

- FireBoard 2 Drive REST API integration via MCP server (primary sensor target — documented REST API + Python client) [domain-research s5]
- MEATER Cloud API as secondary
- Real-time temperature monitoring with alerts
- Ingredient scaling and substitution guidance
- Cross-platform TTS upgrade (Piper TTS — open-source, neural voices)
- Recipe validation tool

### Phase 3: Ecosystem (Months 4–6) [project-idea s3, domain-research s7]

- Schema.org/Recipe import/export
- Cooklang compatibility parser (hybrid interoperability strategy) [domain-research s5]
- Community recipe contributions framework
- Marketplace submissions: SkillsMP, agentskill.sh, agentskills.io
- Cross-platform testing (OpenAI, Copilot)
- Open-source GitHub publication with Apache 2.0 license

---

## Technical Architecture

### Five Core Systems [brainstorming s4]

```
                    ┌─────────────────────┐
                    │   SOUS-CHEF SKILL   │
                    │  (BMM-style family) │
                    └─────────┬───────────┘
                              │
        ┌─────────┬───────────┼───────────┬──────────┐
        ▼         ▼           ▼           ▼          ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ ┌─────────┐
   │PROTOCOL │ │EXECUTION│ │ SENSING │ │INTERFACE│ │  STATE  │
   │ LAYER   │ │ ENGINE  │ │  STACK  │ │ LAYER  │ │ MANAGER │
   └─────────┘ └─────────┘ └─────────┘ └────────┘ └─────────┘
```

1. **Protocol Layer** — Dual-format (human card + agent-rich YAML). Science-rich. Calibration-aware. Carries voice summaries, briefing text, reference photo links. [brainstorming s4]
2. **Execution Engine** — Timer-driven event loop. Push-mode. Pre-flight briefings. Aviation checklists. One instruction at a time. [brainstorming s4]
3. **Sensing Stack** — TC, IR, camera. All human-read via voice in v0.1. Agent does calibration math. Camera via photo-in-chat. [brainstorming s4, s3 #68]
4. **Interface Layer** — Voice-first (2-line TTS out, STT in). Screen as glanceable dashboard with full detail. [brainstorming s4]
5. **State Manager** — File-backed on disk. Self-compacting. Crash-recoverable. Context-window immune. [brainstorming s4]

### Three-Stage Pipeline [brainstorming s4]

```
Research (any LLM) → Compile (protocol YAML) → Execute (sous-chef skill)
```

The research agent and execution agent are deliberately separated: "Different capabilities, different models. Protocol is the handoff." [brainstorming s3 #59] The protocol YAML is the contract between skills; the file system is the integration layer.

### Core Runtime Loop [brainstorming s4]

```
Timer fires event
    → Agent reads state file + protocol
    → Determines: what phase? what's next? what should user know?
    → Pushes voice summary (2 lines) + screen detail
    → Polls sensors if needed ("TC reading?")
    → Updates state file
    → Timer continues
```

### File Structure [project-idea s4]

```
sous-chef-skill/
├── SKILL.md                          # Main skill definition
├── references/
│   ├── PROTOCOL_FORMAT.md            # Spec for cooking protocols
│   ├── TEMPERATURE_GUIDE.md          # Technique temps & targets
│   ├── TIMER_REFERENCE.md            # Timer capabilities
│   └── SENSOR_INTEGRATION.md         # TC/IR probe APIs
├── scripts/
│   ├── timer.sh                      # Background timer with progress
│   ├── validate-protocol.sh          # Protocol validation
│   ├── parse-protocol.sh             # YAML/JSON to executable steps
│   └── sensor-reader.sh              # Read temperature probe data
├── assets/
│   ├── protocol-schema.json          # JSON schema for protocols
│   ├── example-protocols/
│   │   ├── beef-stew.yaml
│   │   ├── stock.yaml
│   │   ├── risotto.yaml
│   │   └── sauce-bearnaise.yaml
│   └── technique-reference.md
└── README.md
```

### Agent Responsibilities [project-idea s4]

The Sous-Chef Skill teaches agents to:

1. **Parse Protocols** — Read YAML, extract phases, steps, timers, temperatures
2. **Validate Ingredients** — Cross-check user's ingredients against protocol requirements pre-cook
3. **Guide Execution** — Walk the user through each step with timing, temperature guidance, sensory cues
4. **Monitor Progress** — Track elapsed time, temperature stability, sensory checkpoints (color, texture, aroma)
5. **Adjust on Fly** — Mistake-forward adaptation; no dead ends, only forks [brainstorming s3 #17]
6. **Manage Timers** — Set background timers with progress callbacks (every 1 minute or 10% interval, whichever is less)
7. **Log & Audit** — Record cooking data for reproducibility and safety accountability

### YAML Protocol Format [project-idea s4, domain-research s5]

The YAML protocol is the first format to natively support temperature targets, sensor checkpoints, timer scripts, phase-based execution, and scaling rules together. YAML provides 27–40% fewer tokens than equivalent JSON representations. [domain-research s5 — anecdotal evidence, single-source claim]

See `beef-stew.yaml` in `assets/example-protocols/` for the full reference implementation.

> **TENSION [TASK#10]**: Project-idea proposes bash scripts as the core timer implementation (`timer.sh`) yet simultaneously flags bash `sleep` ±1s error as a HIGH-impact risk [project-idea s7]. Brainstorming's entire value proposition rests on timer accuracy as the event loop driver [brainstorming s4]. The mitigation ("use system timers") does not clarify whether the primary implementation language remains bash or shifts to Python. This decision must be made before Phase 1 implementation begins.

> **TENSION [TASK#7]**: Domain research positions the YAML cooking protocol as filling a genuine gap that no existing format addresses [domain-research s5], yet the same artifact recommends a "hybrid interoperability strategy — using Cooklang for community recipe discovery/sharing and YAML protocol for agentic execution" [domain-research s5 tensions]. Project-idea's Phase 3 targets AllRecipes and Serious Eats (free-form text). Three incompatible recipe format strategies exist with no hierarchy: structured YAML, Cooklang interop, and free-form platform integration. The primary format driving adoption and network effects is unresolved.

### Technology Dependencies [project-idea s8, domain-research s5]

**Required:**
- Bash (timer scripts)
- Python 3.8+ (validation tools, safety overrides)
- YAML 1.2 (protocol definition)
- JSON Schema (validation)
- Anthropic Agent Skills specification (SKILL.md format)
- MCP (hardware integration layer, Phase 2+)

**Phase 1 TTS:**
- macOS: `say` (free, low latency)
- Linux: `espeak` (fallback)

**Phase 2 TTS Upgrade:**
- Piper TTS (open-source, neural voices, cross-platform)
- ElevenLabs / OpenAI TTS (premium option)

**Phase 2 Sensor Priority:**
- FireBoard 2 Drive: REST API + Python client, documented, $200–250 [domain-research s5]
- MEATER Plus/Block: Community BLE library, secondary [domain-research s5]

---

## Competitive Positioning

### The Competitive Vacuum [domain-research s3]

The market position is defined by the competitive positioning map:

```
                        HIGH AI SOPHISTICATION
                              |
   Google Gemini for Home     |     [SOUS-CHEF SKILL TARGET]
   Microsoft Copilot          |
   Tasty Botatouille          |     Thermomix TM7 + Cookidoo
                              |     Tovala Smart Oven
   OpenAI Cooking GPTs        |     Breville Joule + Breville+
   Samsung Food (AI features) |     upliance.ai
                              |
  RECIPE-ONLY ----------------+---------------- FULL COOKING LOOP
                              |
   Allrecipes                 |     MEATER (hardware, low AI)
   Epicurious                 |     June Oven
   Paprika                    |
   Mealime                    |     SideChef (guided cooking)
                              |
                        LOW AI SOPHISTICATION
```

**The upper-right quadrant (high AI + full cooking loop) is held only by closed, expensive proprietary hardware.** The Sous-Chef Skill targets this space as an open-source, software-only, hardware-agnostic alternative. [domain-research s3]

### Key Competitive Differentiators [domain-research s3]

| Dimension | Recipe Apps | Smart Appliance AI | Sous-Chef Agent Skill |
|-----------|-------------|-------------------|----------------------|
| Distribution | App stores (crowded) | Bundled with hardware | AI platform ecosystems |
| Device dependency | Smartphone only | Specific brand | Any device with AI agent |
| Interoperability | Siloed | Brand-locked | Cross-platform by design |
| Real-time guidance | Limited | Appliance-specific | Comprehensive orchestration |
| Cost | Free–$80/yr | $700–$1,700+ | Free (open-source) |

### Key Threats [domain-research s3]

1. **Google Gemini for Home** (launched Oct 2025): 100M+ smart home devices; cooking features will improve rapidly
2. **Samsung Food + Gemini** (CES 2026 hardware): Free, well-funded, Gemini-powered in kitchen hardware
3. **Platform risk**: Agent Skills standard launched Dec 2025 — still early, ecosystem could fragment
4. **Incumbent content moats**: Allrecipes, America's Test Kitchen have decades of trusted recipe libraries

### Why the Window Exists Now [domain-research s1, s6]

The Agent Skills standard is less than three months old as a public standard (February 2026). Gartner projects 40% of enterprise apps will feature AI agents by end of 2026, up from less than 5% in 2025. The opportunity is to define the cooking category before that platform maturation occurs. Yummly's shutdown in December 2024 — despite Whirlpool backing — demonstrates that apps without genuine differentiation fail regardless of funding. [domain-research s3]

### Recommended Positioning Statement [domain-research s3]

*"The open, AI-native cooking companion that works with your existing kitchen — no new hardware required, no ecosystem lock-in, powered by the Agent Skills standard."*

---

## Appendix: Synthesis Metadata

### Unresolved Tensions

**TENSION TASK#5: Open-source purity vs. premium monetization**
- project-idea frames the project as open-source throughout but raises "Is this open-source only, or are there premium features?" as an unresolved question [project-idea s13]
- domain-research explicitly positions open-source as a competitive differentiator [domain-research s3] but also notes a potential B2B revenue path (HACCP-as-a-Service for commercial kitchens) [domain-research s6]
- Both perspectives preserved. Business model decision belongs to the human.

**TENSION TASK#6: Voice-first as advantage vs. kitchen noise degradation**
- brainstorming: voice-first is a primary design principle; "TTS as primary output — `say` command is the main channel, not a nice-to-have" [brainstorming s2, s3 #39]
- domain-research: "Ventilation fans, sizzling, running water degrade voice recognition; push-to-talk preferred" [domain-research s5]
- The primary interaction channel is unreliable in the exact environment it is designed for. Unresolved; implementation must test in real kitchen conditions.

**TENSION TASK#7: Recipe format strategy — YAML gap-filling vs. Cooklang interop**
- domain-research claims YAML fills a genuine gap that no format addresses [domain-research s5]
- Same artifact recommends Cooklang hybrid interoperability for community discovery [domain-research s5 tensions]
- project-idea Phase 3 targets AllRecipes/Serious Eats (free-form text) [project-idea s3]
- Three incompatible format strategies; no adoption hierarchy established.

**TENSION TASK#8: Push-mode coaching vs. beginner/chef skill level ambiguity**
- brainstorming's push-mode, directive coaching is suited to the home cook who hasn't memorized the protocol [brainstorming s2]
- project-idea explicitly leaves "How should the skill balance simplicity (beginner cooks) vs. sophistication (chefs)?" unresolved [project-idea s13]
- An expert cook would find push-mode briefings patronizing. Target user defines the architecture.

**TENSION TASK#9: Hardware sensor integration scope vs. software-only TAM**
- domain-research governing insight: "software-only, cross-platform" is the strategic differentiator [domain-research governing insight]
- brainstorming deliberately cuts sensor hardware integration from v0.1 [brainstorming s5]
- project-idea includes "Temperature probe integration hooks" in Phase 1 deliverables [project-idea s3]
- Phase 1 sensor scope (hooks only vs. live integration) is ambiguous across artifacts.

**TENSION TASK#10: Bash timer implementation vs. ±1s precision risk**
- project-idea flags bash `sleep` ±1s error as HIGH impact [project-idea s7]
- project-idea proposes bash scripts as the core timer implementation [project-idea s3]
- brainstorming's entire value proposition depends on timer accuracy as the event loop [brainstorming s4]
- Implementation language for timers is unresolved; this must be decided before Phase 1 begins.

**TENSION TASK#11: Food safety liability — critical risk vs. manageable via guardrails**
- domain-research flags food safety liability as CRITICAL severity [domain-research s4]
- Same artifact claims it is manageable through hard-coded guardrails [domain-research s7]
- FDA/USDA + AI LEAD Act + Anthropic AUP + state AI laws interaction is not fully mapped
- project-idea does not address food safety regulatory risk in its scope or architecture sections
- The claim that guardrails make this manageable is moderate-evidence at best.

---

### Evidence Gaps

1. **Community protocol adoption demand**: The "10+ community-contributed protocols" extended success metric [project-idea s6] has no demand signal or prior adoption evidence. No artifact provides evidence that community contributors will create or share protocols.

2. **User segmentation research**: Home cook vs. professional chef ratio targets are inferred from domain research on recipe app users [domain-research s2], not from primary user research on the target population for this skill.

3. **Monetization model**: Open-source vs. open-core vs. dual-license is unresolved across all three artifacts. No financial modeling or comparable project benchmarks provided.

4. **Sensor integration minimum viable scope**: Project-idea asks "What's the minimum viable sensor integration (mock APIs vs. real hardware)?" [project-idea s13] without answering it. No artifact resolves this for Phase 1.

5. **Recipe format adoption path**: YAML vs. Cooklang vs. hybrid has no comparative user evidence, adoption benchmark, or format migration strategy.

6. **Timer implementation language**: Bash vs. Python vs. system timers decision is referenced in risk mitigations [project-idea s7] but never resolved. No performance benchmarks or implementation comparisons provided.

7. **YAML token efficiency claim**: The "27–40% fewer tokens than JSON" claim [domain-research s5] is flagged as anecdotal, single-source. No reproducible benchmark cited.

---

### Source Traceability

| PRD Claim | Source | Section |
|-----------|--------|---------|
| 86% of meals cooked at home | domain-research | s2, Key Growth Drivers |
| Agent Skills standard opened Dec 2025 | domain-research | s5, AI Agent Frameworks |
| $500M → $20B+ AI Kitchen market at 48% CAGR | domain-research | s2, Market Size |
| High-AI + full-cooking quadrant = proprietary hardware only | domain-research | s3, Competitive Positioning Map |
| Yummly shutdown Dec 2024 | domain-research | s3, Cooking/Recipe Applications |
| Most cooking mistakes are planning failures | brainstorming | s6, Key Insights |
| Timer is the event loop driving push-mode | brainstorming | s4, Architecture Summary |
| Voice output max 2 lines | brainstorming | s2, Core Design Principles |
| Dead time = briefing time | brainstorming | s2, s6 |
| File-backed state for crash recovery | brainstorming | s4, Architecture Summary |
| Five core systems (Protocol, Execution, Sensing, Interface, State) | brainstorming | s4 |
| BMM skill collection pattern (5 commands) | brainstorming | s3 #74, s4 |
| v0.1 cuts: sensors, camera pipeline, scaling, etc. | brainstorming | s5 |
| No culinary skill exists in Anthropic ecosystem | project-idea | s2 |
| Multi-phase recipes require precise coordination | project-idea | s2 |
| MVP scope: SKILL.md, schema, 5 protocols, timers, hooks | project-idea | s3 |
| Agent responsibilities (7 core functions) | project-idea | s4 |
| 4 user journeys (execution, troubleshooting, scaling, substitution) | project-idea | s5 |
| 5 MVP success criteria | project-idea | s6 |
| Bash ±1s timer error = HIGH risk | project-idea | s7 |
| Phase 1 = 4–6 weeks, Phase 2 = 8–12 weeks | project-idea | s9 |
| FDA/USDA temperature minimums (hard-coded) | domain-research | s4, Food Safety |
| EU AI Act = limited/minimal risk, Aug 2026 deadline | domain-research | s4, EU AI Act |
| Apache 2.0 license recommendation | domain-research | s4, Open Source Licensing |
| FireBoard 2 Drive = primary sensor target | domain-research | s5, Best Integration Targets |
| MCP = 97M monthly SDK downloads | domain-research | s5, MCP Ecosystem |
| YAML fills genuine recipe format gap | domain-research | s5, Recipe Standardization |
| Google Gemini for Home (Oct 2025) + Samsung CES 2026 | domain-research | s3, Key Players |
| Gartner: 40% enterprise apps with AI agents by end-2026 | domain-research | s1, Research Significance |
| 25% of adults skip recipes due to lack of confidence | domain-research | s2, Key Growth Drivers |
| Positioning statement | domain-research | s3, Recommended Positioning |
