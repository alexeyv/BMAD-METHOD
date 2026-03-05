---
artifact_type: "brainstorming"
governing_insight: "The sous-chef skill should be a timer-driven, push-mode coaching agent that prevents cooking mistakes primarily through pre-flight briefings during dead time, supported by file-backed state persistence and voice-first interaction, rather than through real-time monitoring or procedural instruction."
key_claims:
  - claim: "Most cooking mistakes are planning failures (forgotten steps, misaligned expectations) rather than technique execution failures, so pre-flight briefings and checklists are the primary error prevention mechanism."
    evidence_strength: anecdotal
    section: "Key Insights & Breakthroughs"
  - claim: "The timer should be the runtime event loop that drives push-mode interaction: it fires to trigger the agent to read state, determine what's next, and push guidance without being asked."
    evidence_strength: moderate
    section: "Architecture Summary"
  - claim: "Voice should be the primary output channel for active cooking, constrained to two short sentences maximum, with screen serving as the glanceable dashboard for detail and reference material."
    evidence_strength: moderate
    section: "Core Design Principles"
  - claim: "File-backed cook state on disk is essential for context-window survival and crash recovery, structured to self-compact as phases complete and always remain small enough to fit in every agent context window."
    evidence_strength: moderate
    section: "Architecture Summary"
  - claim: "Reference photos showing 'what perfect actually looks like' is the number-one unmet need in cooking guidance, solving what words and descriptions cannot adequately convey."
    evidence_strength: anecdotal
    section: "Key Insights & Breakthroughs"
  - claim: "The skill should be built as a BMM-style skill collection with five separate commands (help, research, compile, cook, review) connected by protocol YAML artifacts on the file system rather than a single monolithic agent."
    evidence_strength: moderate
    section: "Architecture Summary"
  - claim: "Science explanations should always be full-depth and native to physics/chemistry language, with every explanation framed as 'here's what goes wrong if...' to support diagnostic reasoning during failure."
    evidence_strength: moderate
    section: "Core Design Principles"
  - claim: "The five core systems required are: Protocol Layer (dual-format, science-rich), Execution Engine (timer-driven, push-mode), Sensing Stack (human-read voice input), Interface Layer (voice-first), and State Manager (file-backed, self-compacting)."
    evidence_strength: strong
    section: "Architecture Summary"
  - claim: "Dead time (idle periods during cooking) should be filled with lookahead briefings covering upcoming phase requirements and Q&A, making the cook prepared before execution begins."
    evidence_strength: moderate
    section: "Core Design Principles"
  - claim: "v0.1 should deliberately exclude sensor hardware integration, camera pipeline, reference photo library, familiarity decay modes, ingredient scaling, multi-recipe coordination, and learning features to stay focused on the core execution engine."
    evidence_strength: strong
    section: "MVP v0.1"

tensions:
  - "Core Design Principle #5 ('Science serves diagnostics') emphasizes full-depth physics/chemistry explanations, but User Model theme (#11) assumes 'single guy kitchen' simplicity — tension between explanatory depth and interface simplicity resolved by pushing science to screen detail while keeping voice summaries to 2 lines."
  - "Theme 1 describes the agent as 'calibrate-your-intuition engine' that teaches users to need it less (#4), but this contradicts the push-mode assumption that the agent owns the timeline indefinitely — generalization to teach independence is explicitly deferred to v-future."
  - "The document emphasizes 'protocol is compact reference card' (#23) yet simultaneously pushes 'full depth, no dimmer switch' (#5), suggesting the human-readable card will be one-page while the agent-layer carries unlimited depth — a possible contradiction in what 'compact' means."
  - "Pre-flight briefings are described as simultaneous error prevention, teaching moments, and technique explainers (#6 in Key Insights), but theme conflict exists: if briefings must serve all three purposes, they risk becoming too long or unfocused for the 'two-line voice discipline' rule."
  - "The skill collection pattern (#74) references 'BMM-style' architecture, but the core runtime loop is timer-driven polling, which differs from typical BMM event-driven patterns — potential architectural mismatch between skill collection metaphor and actual execution model."

sections:
  - id: s1
    heading: "## Session Overview"
    summary: "Brainstorming parameters, context, goals, and approach for sous-chef agent."
  - id: s2
    heading: "## Core Design Principles"
    summary: "Five foundational truths: dead-time learning, push-mode, muscle-memory delivery, voice-first interface."
  - id: s3
    heading: "## Complete Idea Inventory (75 Ideas)"
    summary: "Ten themed categories of 75 concrete ideas for coaching, briefings, science, recovery, voice, camera, protocol, architecture, user model, skill collection."
  - id: s4
    heading: "## Architecture Summary"
    summary: "Five core systems, three-stage pipeline, skill collection pattern, runtime loop."
  - id: s5
    heading: "## MVP v0.1 — Build These Three Things"
    summary: "Smart protocol format, timer-driven execution engine, file-backed state manager."
  - id: s6
    heading: "## Key Insights & Breakthroughs"
    summary: "Six critical lessons: protocol as research output, checklists solve forgetting, reference photos essential."
  - id: s7
    heading: "## Session Reflections"
    summary: "Design grounded in real, concurrent kitchen experience and BMM architectural pattern."

---

# Brainstorming Session Results (Pyramid)

## Governing Insight

The sous-chef skill should be a timer-driven, push-mode coaching agent that prevents cooking mistakes primarily through pre-flight briefings delivered during dead time, supported by file-backed state persistence and voice-first interaction. The core insight is that most cooking mistakes are forgetting steps (planning failures) rather than technique failures, so structured briefings, checklists, and reference photos solve the actual problem better than real-time monitoring or reactive instruction.

## Key Claims

1. **Most cooking mistakes are planning failures, not technique failures** (evidence: anecdotal) — "Most cooking mistakes are forgetting steps, not technique failures. Checklists and briefings fix this, not monitoring." [s6]

2. **The timer is the event loop that drives push-mode guidance** (evidence: moderate) — "Timer fires event → Agent reads state file + protocol → Determines: what phase? what's next? what should user know?" [s4]

3. **Dead time should be filled with pre-flight briefings and preparation, not idle waiting** (evidence: moderate) — "Dead time is learning time. The pre-flight briefing is simultaneously the teaching moment, the error prevention mechanism, and the technique explainer." [s6]

4. **Reference photos showing ideal execution are the number-one unmet need** (evidence: anecdotal) — "'What does perfect look like?' is the #1 unmet need. Reference photos solve what words cannot describe." [s6]

5. **Voice should be constrained to two-line maximum with screen as detail dashboard** (evidence: moderate) — "Hard rule: voice output never more than two short sentences" with "Voice gives 2-line action. Screen has the full science." [s2]

6. **Science should be full-depth and diagnostic, not dumbed-down education** (evidence: moderate) — "Explains collagen kinetics = you can diagnose 'why is beef still tough?'" and "Every science explanation comes with 'so here's what goes wrong if...'" [s3]

7. **File-backed state on disk is essential for context-window survival and crash recovery** (evidence: moderate) — "Single source of truth on disk. Conversation is ephemeral; state is persistent" with "Crash recovery for free. New session reads file, picks up where you left off." [s4]

8. **The five core systems are Protocol Layer, Execution Engine, Sensing Stack, Interface Layer, and State Manager** (evidence: strong) — Architecture diagram and detailed system descriptions provided. [s4]

9. **Skill should follow BMM-style skill collection pattern with five separate commands** (evidence: moderate) — "Sous-Chef as Skill Collection: `/sous-chef help`, `/sous-chef research`, `/sous-chef compile`, `/sous-chef cook`, `/sous-chef review`. BMM pattern." [s3]

10. **v0.1 should exclude sensor integration, camera pipeline, reference library, and learning features** (evidence: strong) — "Deliberately Cut from v0.1" lists eight feature categories deferred to future versions. [s5]

## Tensions & Contradictions

- **Science depth vs. interface simplicity:** Core Design Principle #5 emphasizes "full depth, no dimmer switch" for physics/chemistry explanations, but User Model assumes "single guy kitchen" simplicity. Resolved by keeping voice to 2 lines while pushing full science to screen detail, though the actual implementation complexity of this split is unaddressed.

- **Teaching independence vs. persistent push-mode:** Idea #4 ("Calibrate-Your-Intuition Engine") describes teaching users to need the skill less over time, but the entire design assumes the agent owns the timeline indefinitely. This contradiction is deferred to "v-future" without resolving how these capabilities coexist.

- **Compact protocol vs. full-depth science:** Theme 7 states "Protocol as Compact Reference Card" fits "on one page," yet Theme 3 demands "maximum explanatory depth" in the protocol itself. The document doesn't clarify whether the one-page constraint applies to the human-readable card only or also to the agent-layer protocol YAML.

- **Pre-flight briefings as triple-duty mechanism:** Idea #61 ("Combine Briefing + Teaching") and Key Insight #6 claim briefings simultaneously serve as error prevention, teaching moments, and technique explainers. Tension with two-line voice discipline (#44) — it's unclear how one briefing can accomplish all three within the constraint.

- **BMM architectural metaphor vs. timer-driven runtime:** The skill collection pattern (#74) references "BMM-style" architecture with an orchestrator, but the actual core runtime is timer-driven polling and event loops. This differs from typical BMM workflows and may indicate a mismatch between the organizational pattern and the execution model.

---

# [s1] Session Overview

**Facilitator:** Alex
**Date:** 2026-02-16
**Ideas Generated:** 75
**Duration:** ~50 minutes

**Topic:** Sous-Chef Agent Skill — built for Alex, by Alex. A personal kitchen companion for executing cooking protocols.

**Goals:** Identify the features, interactions, and workflow that solve Alex's actual friction points in the kitchen. Build for one user first, generalize later.

**Out of Scope:** Community features, marketplace, multi-platform, configurability for other users, monetization.

**Approach:** Progressive Technique Flow (What If Scenarios → Mind Mapping → SCAMPER → Resource Constraints)

### Context

Session conducted while Alex was mid-cook (beef stew, Phase 4 braise in progress). Brainstorming informed by the real, lived experience of using an ad hoc Claude session as a cooking companion — including its friction points and gaps.

---

# [s2] Core Design Principles

These emerged as the foundational truths of the entire session:

1. **Use dead time to eliminate live confusion** — Pre-flight briefings during wait periods prevent mistakes and reduce cognitive load during active cooking.
2. **Push-mode, not pull-mode** — The agent owns the timeline and proactively delivers guidance. The cook should never have to ask "what's next?"
3. **The agent IS your missing muscle memory** — The protocol exists, you've read it, but you haven't memorized it. The agent drip-feeds it to you at the right moment.
4. **Voice is the headline, screen is the article** — Two-line voice summaries for hands-free cooking; full text + science + photos on screen for when you need more.
5. **Science serves diagnostics, not education** — Full physics/chemistry depth because understanding the process gives you the power to reason about failures.

---

# [s3] Complete Idea Inventory (75 Ideas)

### Theme 1: Coaching Model & Interaction Design
_The skill is a real-time perfection coach, not a recipe reader._

- **#1 Real-Time Perfection Coach** — Shifts from procedural instruction to sensory coaching. "Here's what right looks like."
- **#4 Calibrate-Your-Intuition Engine** — Teaches your senses so you need the skill less over time (v-future).
- **#10 Push-Mode by Default** — Agent owns timeline, pushes guidance without being asked.
- **#12 One Thing At A Time, But Never Nothing** — Never overloads; never leaves you idle without telling you why.
- **#33 The Agent IS Your Missing Muscle Memory** — The protocol is the knowledge; the agent is the live delivery mechanism.
- **#34 Step-at-a-Time Drip Feed** — One instruction, one action, one confirmation, next instruction.
- **#65 Skill Interviews YOU** — At key moments, asks what you observe to train your senses.
- **#71 Every Long Wait Has a Purpose** — Polls sensors, delivers briefings, or explicitly says "relax."
- **#72 Permission to Walk Away** — Explicitly tells you when you can leave the kitchen and promises to call you back.
- **#73 Periodic Lid-Lift Check-Ins** — Every 15-20 min during long holds, nudges you to peek and verify.

### Theme 2: Pre-Flight Briefings & Error Prevention
_The primary mistake prevention mechanism: understanding before execution._

- **#7 Parallel Task Pipelining** — Understands the dependency graph, fills idle time with upcoming prep info.
- **#8 Lookahead Briefings** — At start of each phase, 15-second brief of what's coming and what needs to be ready.
- **#9 Dead Time Alerts** — Identifies windows and fills them with useful prep nudges.
- **#13 No Surprises Guarantee** — You never reach a step and realize you don't have something ready.
- **#14 Phase Transition Preview** — Plain facts, just in time: "In 5 minutes you'll need X, Y, Z."
- **#15 Pre-Flight Briefing Window** — Dead time is for understanding the next play, not for doing.
- **#16 Clarification Window Before Execution** — Q&A before heat is on. Hash out confusion while you have time.
- **#19 Step Completion Tracking** — Checklist: "Beef in? Mushrooms in? Carrots in? Stock in? Go."
- **#21 Pre-Briefing IS the Error Prevention** — Most cooking mistakes are planning failures. Briefings fix that.
- **#62 Aviation Checklist Discipline** — Quick verbal roll call before every phase transition.

### Theme 3: Science & Teaching
_Full depth always. Science as diagnostic power, not trivia._

- **#3 Science-Native Coaching Language** — Speaks in physics and chemistry by default. Not dumbed down.
- **#5 Full Depth, No Dimmer Switch** — V0.1 always maximum explanatory depth. User self-filters.
- **#35 Contextual Recall** — Connects live execution back to the protocol you already scanned.
- **#36 Technique Explainers On Demand** — "How do I dice an onion?" → full mechanical how-to, no judgment.
- **#37 Assumed Ignorance, No Shame** — Assumes you might not know any physical technique. Normalizes asking.
- **#41 Science as Debugging Framework** — Understanding collagen kinetics = you can diagnose "why is beef still tough?"
- **#42 Explain-to-Diagnose, Not Explain-to-Educate** — Every science explanation comes with "so here's what goes wrong if..."
- **#61 Combine Briefing + Teaching** — The briefing IS the teaching moment. One system, not two.

### Theme 4: Error Recovery
_You report mistakes; the skill recalculates forward._

- **#17 Mistake-Forward Adaptation** — No failure states, only forks in the road. Immediate path recalculation.
- **#18 Consequence Transparency** — Honest about impact: "2 out of 10 on the final dish. Here's how we compensate."
- **#20 Forgotten Ingredient Recovery** — "Carrots aren't in? They can go in now. We'll extend by 5 minutes."

### Theme 5: Voice-First Interface
_Hands are busy. Voice in, voice out. Screen is backup._

- **#38 Voice-First Interaction** — STT in, TTS out. No screen required during active cooking.
- **#39 TTS as Primary Output** — `say` command is the main channel, not a nice-to-have.
- **#40 Conversational Pacing** — Short sentences, pauses between steps. Kitchen cadence.
- **#43 Voice as Summary, Text as Detail** — Voice gives 2-line action. Screen has the full science.
- **#44 Two-Line Voice Discipline** — Hard rule: voice output never more than two short sentences.
- **#45 Glanceable Screen** — Current step bolded, timer visible, key numbers prominent. Instrument panel, not chat log.

### Theme 6: Visual References & Camera
_"What does perfect actually look like?"_

- **#2 Camera + Thermometer as Agent Eyes** — Phone camera as a visual sensor alongside TC and IR.
- **#46 Science as Rich Media** — Diagrams, reaction pathways, thermal diffusion curves on screen.
- **#47 Visual Reference Library** — Reference images per step showing target state.
- **#48 Reference Photo Library** — Every technique step has photos showing what "right" looks like. The #1 identified need.
- **#49 Build Your Own Reference Library** — Prompted to take photos during cooks. Personal library grows over time.
- **#50 Camera as Input** — Snap a photo, "does this look right?" Agent evaluates against the science.
- **#51 Camera-In Is Free** — No integration needed for v0.1. Photo in chat, LLM evaluates. Zero infrastructure.
- **#52 Three-Sensor Kitchen** — TC (internal), IR (surface), camera (visual). All already owned.
- **#53 Level 1: Show Me The Target** — Reference photos from cookbooks, food science sources.
- **#54 Level 2: Evaluate Mine** — Agent sees your photo and gives calibrated feedback.
- **#55 Level 3: Disaster Detection** — "That's carbonized. Scrape, re-oil, start over. 8 minutes lost."
- **#56 Camera Integration Spectrum** — From drag-and-drop (v0.1) to watched folder to continuous feed (v-later).

### Theme 7: Protocol Format & Pipeline
_Dual-format protocols. Research → Compile → Execute._

- **#22 Dual-Format Protocols** — Human-readable reference card + agent-rich execution layer. Same source of truth.
- **#23 Protocol as Compact Reference Card** — Human version fits on one page. Everything else is agent-layer.
- **#57 Smart Protocol, Simple Agent** — Push intelligence into the protocol. Agent is a reader, not a reasoner.
- **#58 The Real Pipeline** — Curiosity → Research → Understanding → Protocol → Execution.
- **#59 Research Agent ≠ Execution Agent** — Different capabilities, different models. Protocol is the handoff.
- **#60 Protocol Compiler** — Unstructured science knowledge → structured executable protocol format.

### Theme 8: Architecture & State Management
_File-backed state. Context-window survival. Timer as event loop._

- **#24 Context Window Survival Architecture** — Treats context window as first-class engineering constraint.
- **#25 Phase-Scoped Context Management** — Each phase starts with critical data front-loaded. Never lost in middle.
- **#26 Running State Block** — Every response ends with compact state summary. Self-healing context.
- **#27 File-Backed Cook State** — Single source of truth on disk. Conversation is ephemeral; state is persistent.
- **#28 Self-Compacting State File** — Completed phases collapse to one-line summaries. Always small, always current.
- **#29 State File as Session Resume Point** — Crash recovery for free. New session reads file, picks up where you left off.
- **#32 Task List as Cook State is Too Thin** — State needs observations and deviations, not just phase completion.
- **#66 Keep the Timer — It's the Push-Mode Engine** — Timer drives push-mode. Without it, agent is passive.
- **#67 Timer as Event Loop** — Timer fires → agent reads state → pushes guidance → updates state → loop.
- **#69 Timer-Driven Sensor Polling** — Timer fires, agent asks for TC reading, you say the number, it gives feedback.
- **#70 Adaptive Polling Rate** — Frequent during dynamic phases, infrequent during stable holds.

### Theme 9: User Model & Simplicity
_Single guy kitchen. Keep it simple. Generalize later._

- **#6 Familiarity Decay** — After 3-10 cooks, compress explanations. V-future, not v0.1.
- **#11 Single Guy Kitchen Assumptions** — One pan, one pot, one cutting board, one pair of hands.
- **#68 Sensors Are Human-Read, Voice-In** — No hardware integration. You read the display, you say the number.

### Theme 10: Skill Collection Architecture
_BMM-style skill family with orchestrator._

- **#30 Ad Hoc Session = Protocol Generator + Dumb Task Runner** — The gap: protocol quality is good, execution intelligence is missing.
- **#31 Calibration Data Should Be Inline** — Always speak in "what your display should show" language.
- **#74 Sous-Chef as Skill Collection** — `/sous-chef help`, `/sous-chef research`, `/sous-chef compile`, `/sous-chef cook`, `/sous-chef review`. BMM pattern.
- **#75 Protocol as Handoff Artifact** — Protocol YAML is the contract between skills. File system is the integration layer.

---

# [s4] Architecture Summary

### Five Core Systems

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

1. **Protocol Layer** — Dual-format (human + agent). Science-rich. Calibration-aware. Carries briefings, voice summaries, reference photo links.
2. **Execution Engine** — Timer-driven event loop. Push-mode. Pre-flight briefings. Aviation checklists. One instruction at a time.
3. **Sensing Stack** — TC, IR, camera. All human-read via voice. Agent does calibration math. Camera via photo-in-chat.
4. **Interface Layer** — Voice-first (2-line TTS out, STT in). Screen as glanceable dashboard with full detail.
5. **State Manager** — File-backed on disk. Self-compacting. Crash-recoverable. Context-window immune.

### Three-Stage Pipeline

```
Research (any LLM) → Compile (protocol YAML) → Execute (sous-chef skill)
```

### Skill Collection (BMM Pattern)

- `/sous-chef help` — Orchestrator, routes to right workflow
- `/sous-chef research` — Deep science dive on a dish
- `/sous-chef compile` — Research/recipe → structured protocol
- `/sous-chef cook` — Real-time execution engine
- `/sous-chef review` — Post-cook debrief (v-future)

### Core Runtime Loop

```
Timer fires event
    → Agent reads state file + protocol
    → Determines: what phase? what's next? what should user know?
    → Pushes voice summary (2 lines) + screen detail
    → Polls sensors if needed ("TC reading?")
    → Updates state file
    → Timer continues
```

---

# [s5] MVP v0.1 — Build These Three Things

### 1. Smart Protocol Format + Compiler
The YAML format that carries: phases, steps, calibrated sensor targets, voice summaries, briefing text, reference photo links. Plus a compile step that turns research/recipes into this format.

### 2. Timer-Driven Execution Engine with Push-Mode
The event loop. Timer fires → agent reads protocol + state → pushes voice summary + screen detail. Pre-flight briefings during dead time. Aviation checklists at phase transitions. Sensor polling via voice.

### 3. File-Backed State Manager
Cook state on disk. Self-compacting. Crash-recoverable. Carries phase, elapsed time, temperatures, deviations. Agent reads this instead of relying on conversation middle.

### Deliberately Cut from v0.1
- Sensor hardware integration (voice-in is fine)
- Camera pipeline (drag-and-drop photo is fine)
- Reference photo library (describe in text for now)
- Familiarity decay / depth modes
- Ingredient scaling / substitution
- Multi-recipe coordination
- Learning from past cooks
- `/sous-chef review` (post-cook debrief)

---

# [s6] Key Insights & Breakthroughs

1. **The protocol isn't the starting point** — It's the output of a research rabbit hole driven by curiosity ("I've been frying eggs for 50 years and still don't know how to do it right").
2. **Most cooking mistakes are forgetting steps, not technique failures** — Checklists and briefings fix this, not monitoring.
3. **"What does perfect look like?" is the #1 unmet need** — Reference photos solve what words cannot describe.
4. **The timer is the event loop** — Not a utility; the core runtime that drives push-mode interaction.
5. **The human is the sensor bus** — Voice-in for TC/IR readings. Camera via photo-in-chat. No hardware integration needed.
6. **Dead time is learning time** — The pre-flight briefing is simultaneously the teaching moment, the error prevention mechanism, and the technique explainer.

---

# [s7] Session Reflections

This session was uniquely informed by real, concurrent experience — Alex was mid-braise while brainstorming the tool that would have made that braise smoother. Every idea was tested against "would this have helped me 90 minutes ago?" The result is a design that's deeply grounded in actual kitchen friction rather than imagined user stories.

The BMM architectural pattern provides a proven, familiar structure. The sous-chef skill collection is essentially BMAD for the kitchen — a family of workflows connected by artifacts on disk, with an orchestrator that routes you to the right one.
