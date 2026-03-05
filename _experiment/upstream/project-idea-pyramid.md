---
artifact_type: "research"
governing_insight: "Create a standardized AI Agent Skill for cooking that transforms recipe protocols into real-time guidance with integrated timers and temperature monitoring, filling a gap in Anthropic's open skills ecosystem."
key_claims:
  - claim: "No culinary/cooking skill exists in Anthropic's open skills ecosystem"
    evidence_strength: strong
    section: "## Problem Statement"
  - claim: "Multi-phase recipes require precise temperature control and sequential logic that humans struggle to coordinate"
    evidence_strength: strong
    section: "## Problem Statement"
  - claim: "Anthropic Agent Skills framework can package cooking knowledge as reusable procedural modules"
    evidence_strength: moderate
    section: "## Problem Statement (Opportunity section)"
  - claim: "MVP scope includes SKILL.md, protocol schema, 5 example protocols, timer scripts, and sensor integration hooks"
    evidence_strength: strong
    section: "## Project Scope"
  - claim: "Timer precision in bash has ±1s error, classified as high risk"
    evidence_strength: strong
    section: "## Risks & Mitigations"
  - claim: "Protocol adoption barrier exists because chefs use free-form text, not structured formats"
    evidence_strength: moderate
    section: "## Risks & Mitigations"
  - claim: "Extended success targets 10+ community-contributed protocols and placement on agentskills.io marketplace"
    evidence_strength: anecdotal
    section: "## Success Metrics"
  - claim: "Skill must teach agents to parse protocols, validate ingredients, guide execution, monitor progress, adjust on-the-fly, manage timers, and log data"
    evidence_strength: strong
    section: "## Technical Architecture"
  - claim: "Project requires 1 lead engineer, 1 culinary consultant, 1 technical writer"
    evidence_strength: moderate
    section: "## Budget & Resources"
  - claim: "Phase 1 timeline is 4-6 weeks; Phase 2 is 8-12 weeks post-MVP"
    evidence_strength: moderate
    section: "## Timeline & Milestones"
tensions:
  - "**Scope balance**: Document declares 'strict MVP scope' and 'phase-based rollout' as mitigation for scope creep risk, yet simultaneously outlines ambitious Phase 2/3 features (ingredient scaling, multi-recipe coordination, video support). The tension between controlled MVP and expansive vision is acknowledged but unresolved."
  - "**Design simplicity vs. sophistication**: Questions section explicitly asks 'How should the skill balance simplicity (beginner cooks) vs. sophistication (chefs)?' — no answer provided. This is a critical design trade-off that could reshape the protocol schema and agent guidance logic."
  - "**Timer precision contradiction**: Document identifies 'bash sleep has ±1s error' as high-risk, yet proposes bash scripts (timer.sh, parse-protocol.sh, validate-protocol.sh) as core implementation. The mitigation suggests 'use system timers' but doesn't clarify if bash is still the primary language or if a switch to Python/compiled language is planned."
  - "**Sensor integration scope**: Phase 1 includes 'Integration Hooks' and 'Hooks for external temperature sensors', but Questions section asks 'What's the minimum viable sensor integration (mock APIs vs. real hardware)?' — indicating the extent of Phase 1 sensor work is not finalized."
  - "**Monetization unresolved**: Project is framed as open-source throughout (GitHub, marketplace, community contributions), but Questions section includes 'Is this open-source only, or are there premium features?' — creating ambiguity about the business model and licensing strategy."
  - "**Recipe source conflict**: Problem statement emphasizes 'recipes and cooking protocols aren't structured in a machine-readable way that agents can parse', yet Phase 3 mentions 'Integration with popular recipe platforms' (AllRecipes, Serious Eats) which currently publish in free-form text. No solution is proposed for translating free-form → structured."
sections:
  - id: s1
    heading: "## Executive Summary"
    summary: "Comprehensive Sous-Chef Skill enabling AI agents to guide real-time cooking with protocol tracking and multi-modal integration"
  - id: s2
    heading: "## Problem Statement"
    summary: "Five critical gaps in cooking guidance plus opportunity via Anthropic Agent Skills framework"
  - id: s3
    heading: "## Project Scope"
    summary: "Three-phase rollout: MVP (core skill, schemas, examples), extended features (scaling, techniques, video)"
  - id: s4
    heading: "## Technical Architecture"
    summary: "Modular skill structure with protocol parsing, timer management, sensor integration, and agent responsibilities"
  - id: s5
    heading: "## User Journeys"
    summary: "Four scenarios: first-time execution, troubleshooting, scaling, ingredient substitution guidance flows"
  - id: s6
    heading: "## Success Metrics"
    summary: "MVP functionality targets; extended success measures adoption, community, integration, marketplace presence"
  - id: s7
    heading: "## Risks & Mitigations"
    summary: "Five key risks (timer precision, sensor complexity, protocol adoption, cross-platform, scope creep) with mitigation strategies"
  - id: s8
    heading: "## Dependencies & Requirements"
    summary: "Software (Bash, Python, git), standards (Agent Skills spec, YAML, JSON Schema), optional external services"
  - id: s9
    heading: "## Timeline & Milestones"
    summary: "Phase 1: 4-6 weeks (schema, protocols, timers, hooks); Phase 2: 8-12 weeks (scaling, techniques, testing)"
  - id: s10
    heading: "## Deliverables"
    summary: "Code (skill, validation, protocols, timers, sensors); documentation (specs, guides, API refs); community (GitHub, marketplace, blog)"
  - id: s11
    heading: "## Budget & Resources"
    summary: "Three-person team (lead engineer, culinary consultant, technical writer) with free tools and infrastructure"
  - id: s12
    heading: "## Success Criteria for BMAD Planning"
    summary: "Project is BMAD-ready: clear problem, defined solution, measurable impact, phased approach, open standard"
  - id: s13
    heading: "## Questions for Planning Agent"
    summary: "Six unresolved design and strategic questions spanning architecture, protocols, sensors, community, monetization, and scalability"
---

# Sous-Chef Agent Skill — Project Idea Document (Pyramid)

## Governing Insight

Create a standardized AI Agent Skill for cooking that transforms recipe protocols into real-time guidance with integrated timers and temperature monitoring. This skill fills a gap in Anthropic's open skills ecosystem by enabling agents to act as sophisticated kitchen companions, translating complex cooking procedures into actionable steps with multi-modal tracking and sensory guidance.

## Key Claims

1. **No culinary/cooking skill exists in Anthropic's open ecosystem** (evidence: strong) — "Anthropic's open skills ecosystem has document manipulation, code generation, and enterprise tools — but **no culinary/cooking skill**" [s2]

2. **Multi-phase recipes require precise coordination that humans struggle with** (evidence: strong) — "Multi-phase recipes (braises, roasts, stocks) require precise temperature control, timing, and sequential logic that humans struggle to coordinate" [s2]

3. **Anthropic Agent Skills framework can package reusable cooking modules** (evidence: moderate) — Presented as opportunity vehicle but not proven: "Works across multiple LLM platforms (Claude, Gemini, others adopting the skills standard) / Packages cooking knowledge as procedural, reusable modules" [s2]

4. **MVP includes comprehensive skill structure, protocol schema, 5+ examples, timers, and sensor hooks** (evidence: strong) — Detailed Phase 1 deliverables: "SKILL.md with comprehensive instructions / PROTOCOL_FORMAT.md specification / TEMPERATURE_GUIDE.md / scripts/timer.sh and validate-protocol.sh / YAML/JSON schema for cooking protocols / 3-5 example protocols" [s3]

5. **Bash timer implementation carries ±1s error precision risk** (evidence: strong) — "Timer precision (bash sleep has ±1s error)" identified as high impact, mitigation proposes "use system timers, document tolerances, provide visual countdowns" [s7]

6. **Recipe protocol adoption barrier: chefs use free-form text, not structured data** (evidence: moderate) — "Recipe protocol adoption (chefs use free-form text)" marked as medium risk, mitigation suggests "Provide simple YAML template, auto-conversion tools" [s7]

7. **Extended success targets 10+ community protocols and marketplace presence** (evidence: anecdotal) — "10+ community-contributed protocols (recipes) in library" and "Skill is featured on agentskills.io marketplace" listed as extended success measures without prior evidence of adoption demand [s6]

8. **Agents must execute seven core responsibilities in cooking guidance** (evidence: strong) — "Parse Protocols / Validate Ingredients / Guide Execution / Monitor Progress / Adjust on Fly / Manage Timers / Log & Audit" [s4]

9. **Three-person team required: lead engineer, culinary consultant, technical writer** (evidence: moderate) — Team composition stated without justification for skill distribution or workload sizing [s11]

10. **Phase 1 requires 4-6 weeks; Phase 2 requires 8-12 weeks** (evidence: moderate) — Milestone timeline provided without breakdown of historical reference or complexity estimation [s9]

## Tensions & Contradictions

- **Scope balance unresolved**: Document declares "Strict MVP scope, phase-based rollout" as mitigation for scope creep (high risk), yet Phase 2 and Phase 3 outline extensive features: ingredient scaling, substitution guidance, culinary technique library, multi-recipe coordination, video/image support, and fail-safe recovery. The tension between controlled MVP and expansive vision is acknowledged but left unresolved in design.

- **Beginner vs. chef simplicity trade-off**: Questions section explicitly asks "How should the skill balance simplicity (beginner cooks) vs. sophistication (chefs)?" — this is a critical architectural choice that could reshape the protocol schema, agent guidance verbosity, and sensor integration depth. No design decision is documented.

- **Timer precision contradiction**: Document identifies "bash sleep has ±1s error" as **high** impact risk, yet proposes bash scripts (timer.sh, parse-protocol.sh, validate-protocol.sh, sensor-reader.sh) as core implementation. Mitigation suggests "use system timers" without clarifying whether the primary language remains bash or shifts to Python/compiled language.

- **Sensor integration scope undefined**: Phase 1 includes both "Integration Hooks" for external sensors and "Hooks for external temperature sensors (thermocouples, IR guns)", but Questions section asks "What's the minimum viable sensor integration (mock APIs vs. real hardware)?" — indicating Phase 1 scope for sensor work is not finalized at the time of writing.

- **Monetization strategy unresolved**: Project is framed as open-source throughout (GitHub, Anthropic skills repository, agentskills.io marketplace, community contributions), yet Questions section includes "Is this open-source only, or are there premium features?" — creating ambiguity about business model, licensing, and commercial viability.

- **Recipe source standardization unsolved**: Problem statement emphasizes "Recipes and cooking protocols aren't structured in a machine-readable way that agents can parse, validate, and execute." Phase 3 mentions "Integration with popular recipe platforms (AllRecipes, Serious Eats, Chef's standards)" which publish content in free-form text. No solution is proposed for bridging this gap or building the "auto-conversion tools" mentioned as mitigation.

---

## [s1] Executive Summary

Create a comprehensive **Sous-Chef Agent Skill** that enables AI agents (Claude, other compatible LLMs) to act as sophisticated kitchen companions. The skill transforms recipe protocols into actionable, real-time cooking guidance with multi-modal tracking (timers, temperature monitoring, step progression, ingredient management). This skill is designed to be open-source, reusable, and compatible with the Anthropic Agent Skills standard.

---

## [s2] Problem Statement

### Current Gaps

1. **Recipe Execution Friction**: Home cooks and professional chefs lack AI-guided, real-time support that understands cooking protocols deeply.
2. **Protocol Complexity**: Multi-phase recipes (braises, roasts, stocks) require precise temperature control, timing, and sequential logic that humans struggle to coordinate.
3. **No Standard Skill Exists**: Anthropic's open skills ecosystem has document manipulation, code generation, and enterprise tools — but **no culinary/cooking skill**.
4. **Timer/Tracking is Manual**: Cooks must manage separate timers, temperature probes, and step checklists without AI integration.
5. **Protocol Portability**: Recipes and cooking protocols aren't structured in a machine-readable way that agents can parse, validate, and execute.

### Opportunity

The Anthropic Agent Skills framework provides the perfect vehicle to create a reusable, standardized sous-chef capability that:
- Works across multiple LLM platforms (Claude, Gemini, others adopting the skills standard)
- Packages cooking knowledge as procedural, reusable modules
- Integrates timers, temperature probes, ingredient tracking, and step progression
- Can be extended to any recipe protocol (sauces, pasta, baking, sous-vide, etc.)

---

## [s3] Project Scope

### Phase 1: Core Sous-Chef Skill (MVP)

**Deliverables:**
1. **Sous-Chef Agent Skill** (following Anthropic Agent Skills spec)
   - `SKILL.md` with comprehensive instructions for agents
   - `references/PROTOCOL_FORMAT.md` — specification for cooking protocols
   - `references/TEMPERATURE_GUIDE.md` — temperature targets for common techniques
   - `scripts/timer.sh` — background timer with progress updates
   - `scripts/validate-protocol.sh` — validates recipe protocols against schema

2. **Protocol Schema & Examples**
   - YAML/JSON schema for cooking protocols (phases, steps, timers, temps)
   - 3-5 example protocols: beef stew, chicken stock, risotto, sauce béarnaise, roasted vegetables
   - Protocol validation tool

3. **Timer Skill Enhancement**
   - Sophisticated timer system (multi-stage, progress callbacks)
   - Temperature probe integration hooks (read TC/IR sensor data)
   - Alert system (audio, visual, voice)

4. **Integration Hooks**
   - Hooks for external temperature sensors (thermocouples, IR guns)
   - Support for recipe databases (AllRecipes, Serious Eats, Chef's standards)
   - Logging/audit trail for reproducible cooking

### Phase 2: Extended Features (Post-MVP)

- **Ingredient Scaling**: Adjust recipes for different portions (e.g., 900g → 2kg)
- **Substitution Guidance**: "You don't have Cremini mushrooms? Try button mushrooms instead"
- **Culinary Technique Library**: Deep knowledge of Maillard reactions, collagen gelatinization, emulsification, etc.
- **Multi-Recipe Coordination**: Guide timing for complex meals (soup + main + sides simultaneously)
- **Video/Image Support**: Parse recipe images, provide step-by-step visual guidance
- **Fail-Safe Recovery**: Detect when things go wrong (burnt onions, broken sauce) and suggest fixes

### Phase 3: Ecosystem & Contribution

- Open-source publication to GitHub (anthropics/skills or independent repo)
- Skills marketplace submission (agentskills.io)
- Community protocol contributions (crowdsourced recipes)
- Integration with popular recipe platforms

---

## [s4] Technical Architecture

### Core Components

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
│   └── technique-reference.md        # Maillard, gelatin, etc.
└── README.md                         # Getting started guide
```

### Agent Responsibilities

The Sous-Chef Skill teaches agents to:

1. **Parse Protocols**: Read a recipe protocol, extract phases, steps, timers, temperatures
2. **Validate Ingredients**: Cross-check user's ingredients against protocol requirements
3. **Guide Execution**: Walk the user through each step with timing, temperature guidance, sensory cues
4. **Monitor Progress**: Track elapsed time, temperature stability, sensory checkpoints (color, texture, aroma)
5. **Adjust on Fly**: Scale ingredients, suggest substitutions, troubleshoot failures
6. **Manage Timers**: Set background timers with progress callbacks (every 1 minute or 10% interval, whichever is less)
7. **Log & Audit**: Record cooking data for reproducibility and learning

### Key Interfaces

#### Protocol Format (YAML Example)

```yaml
name: Precision Beef & Potato Stew
description: Collagen-based braise with IR/TC monitoring
serves: 4
duration: 180m

phases:
  - id: prep
    name: Geometric Processing
    duration: 15m
    steps:
      - action: cube_beef
        size: "3.0 cm"
        quantity: 900g
        expected_yield: 30_pieces
      - action: cube_potato
        size: "2.5 cm"
        quantity: 700-900g
      - action: pat_dry
        target: beef
        description: "Completely dry surface for Maillard"

  - id: sear
    name: Maillard Phase
    duration: 20m
    steps:
      - action: preheat
        target: pan
        temp_surface: "210-230°C"
        sensor: ir_thermometer
      - action: sear_batch
        batch: 1
        quantity: 15_cubes
        sides: [120s, 90s]
        internal_temp_check: "<50°C"
        sensor: thermocouple

  - id: braise
    name: Braise (Collagen Conversion)
    duration: 90-120m
    temp_target: "90°C ± 2°C"
    sensor: thermocouple
    steps:
      - action: combine
        ingredients: [beef, mushrooms, onions, stock]
        liquid_coverage: "90%"
      - action: monitor
        metric: liquid_temperature
        target: "90°C ± 2°C"
        duration: "90-120m"
        alerts: [every_10m]

  - id: integrate_veg
    name: Potato & Carrot Integration
    duration: 25-30m
    steps:
      - action: test_beef
        temp_probe: internal
        target: "90°C"
        texture: "soft butter"
      - action: add_vegetables
        ingredients: [potato, carrot]
      - action: monitor
        metric: potato_core_temp
        target: "90-92°C"
        duration: "25-30m"

  - id: finishing
    name: Rest & Season
    duration: 15m
    steps:
      - action: rest
        duration: 15m
        reason: "Pressure equalization in meat fibers"
      - action: season
        salt: "to taste"
        pepper: "to taste"
        notes: "Calgary hard water — use less salt"
```

#### Timer Interface

```bash
# Simple timer
timer 90m "Braise: Collagen Conversion"

# Timer with progress callbacks (every minute or 10%)
timer 90m "Braise" --progress-interval 1m

# Timer with sensor data collection
timer 90m "Braise" --monitor-temp tc:90:2
```

#### Sensor Integration

```bash
# Read thermocouple data
read-sensor tc

# Read IR thermometer
read-sensor ir

# Both
read-sensor all
```

---

## [s5] User Journeys

### Journey 1: First-Time Execution

1. User provides recipe protocol (or selects from library)
2. Sous-Chef agent loads the protocol, validates it
3. Agent checks user's ingredients against requirements
4. Agent guides through prep phase with precise cutting dimensions
5. Agent sets timers for each phase, monitors progress via voice/text
6. Agent probes temperature milestones and adjusts guidance accordingly
7. User receives real-time feedback ("Your onions are at 115°C, perfect — 2 more minutes")
8. Final dish is executed with confidence

### Journey 2: Troubleshooting

1. User mentions "The onions are burning"
2. Sous-Chef recognizes failure mode, suggests immediate recovery
3. Agent adjusts timing, suggests alternative techniques
4. Dish is salvaged with minimal loss

### Journey 3: Scaling & Adaptation

1. User wants to cook for 8 people instead of 4
2. Sous-Chef scales all ingredient quantities proportionally
3. Agent adjusts cooking times (larger volumes = longer heat diffusion)
4. Execution proceeds with scaled protocol

### Journey 4: Ingredient Substitution

1. User lacks an ingredient
2. Sous-Chef suggests compatible substitutes
3. Agent explains flavor/texture impact
4. User proceeds with confidence

---

## [s6] Success Metrics

### MVP Success

1. **Functionality**: Skill successfully guides a user through a complete cooking protocol (soup to nuts)
2. **Accuracy**: Temperature targets met, timing honored, sensory cues validated
3. **Usability**: Agent provides clear, contextual guidance at each step
4. **Reliability**: Timers work correctly, sensor reads are accurate
5. **Documentation**: Protocol schema is clear, examples are complete

### Extended Success

1. **Adoption**: Skill is used across multiple platforms (Claude, Gemini, Cursor, etc.)
2. **Community**: 10+ community-contributed protocols (recipes) in library
3. **Integration**: Real sensor data (TC/IR) is successfully integrated
4. **Marketplace**: Skill is featured on agentskills.io marketplace
5. **Citations**: Referenced in cooking blogs, professional chef communities

---

## [s7] Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Timer precision (bash sleep has ±1s error) | High | Use system timers, document tolerances, provide visual countdowns |
| Sensor integration complexity | Medium | Start with mock sensor APIs, provide clear integration docs |
| Recipe protocol adoption (chefs use free-form text) | Medium | Provide simple YAML template, auto-conversion tools |
| Cross-platform compatibility (macOS `say`, Linux `espeak`) | Low | Abstract TTS layer, support multiple backends |
| Scope creep (too many features) | High | Strict MVP scope, phase-based rollout |

---

## [s8] Dependencies & Requirements

### Software
- Bash (for scripts)
- Python 3.8+ (optional, for validation tools)
- git (version control)
- macOS or Linux (sensor integrations vary)

### Standards
- Anthropic Agent Skills specification (SKILL.md format)
- YAML 1.2 (protocol definition)
- JSON Schema (validation)

### External Services
- Optional: Temperature sensor APIs (if integrating with smart kitchen devices)
- Optional: Recipe database APIs (AllRecipes, etc.)

---

## [s9] Timeline & Milestones

### Phase 1 (4-6 weeks)

- **Week 1-2**: Protocol schema design, SKILL.md core structure
- **Week 2-3**: Timer implementation, 5 example protocols, validation scripts
- **Week 3-4**: Agent guidance logic, sensor integration hooks
- **Week 4-5**: Documentation, testing, refinement
- **Week 5-6**: Beta release, community feedback

### Phase 2 (8-12 weeks post-MVP)

- **Weeks 1-4**: Ingredient scaling, substitution logic
- **Weeks 5-8**: Technique library expansion, multi-recipe coordination
- **Weeks 9-12**: Integration testing, marketplace submission

---

## [s10] Deliverables

### Code
- [ ] Complete Sous-Chef Agent Skill (SKILL.md, scripts, assets)
- [ ] Protocol validation tool
- [ ] 5+ example cooking protocols
- [ ] Timer scripts (simple + advanced)
- [ ] Sensor integration hooks

### Documentation
- [ ] Protocol format specification
- [ ] Agent implementation guide
- [ ] Getting started guide for cooks
- [ ] API reference for sensor integrations
- [ ] Example walkthrough (beef stew execution)

### Community
- [ ] GitHub repository (public)
- [ ] Submission to Anthropic skills repository
- [ ] Submission to agentskills.io marketplace
- [ ] Blog post: "Building a Sous-Chef AI"

---

## [s11] Budget & Resources

### Team
- 1 Lead Engineer (agent/skill architecture)
- 1 Culinary Consultant (recipe protocols, techniques)
- 1 Technical Writer (documentation)

### Tools
- GitHub (free)
- Anthropic Agent Skills SDK (free, open-source)
- Testing infrastructure (local, free)

---

## [s12] Success Criteria for BMAD Planning

This project is ready for **BMAD (Business Model, Architecture, Design) planning** because:

1. **Clear Problem**: Cooking protocols lack standardized AI guidance
2. **Defined Solution**: Anthropic Agent Skill + protocol schema + execution guidance
3. **Measurable Impact**: Adoption metrics, community contributions, marketplace presence
4. **Phased Approach**: MVP → Extended Features → Ecosystem
5. **Open Standard**: Leverages public Anthropic specifications, not proprietary tech

---

## [s13] Questions for Planning Agent

1. **Architecture**: How should the skill balance simplicity (beginner cooks) vs. sophistication (chefs)?
2. **Protocols**: Should we build a protocol compiler that translates free-form recipes → structured YAML?
3. **Sensors**: What's the minimum viable sensor integration (mock APIs vs. real hardware)?
4. **Community**: How do we incentivize recipe contributions?
5. **Monetization**: Is this open-source only, or are there premium features?
6. **Scalability**: Can this model extend beyond cooking (cocktails, bakery, food science)?
