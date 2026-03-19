# RoosTx Session 12 Handoff
**Date:** 2026-03-19
**Repo:** github.com/WickedFog/Test_Bench_1 (rename to RoosTx when ready)
**Local:** D:\RoosTx on Lappy

---

## WHAT HAPPENED THIS SESSION

### Session 12A — Drag Race Model Work (chat: 3435810c)

**Goal:** Fix all Grok-flagged bugs in the drag race YAML, get a working file that loads in Companion.

**Key findings from Gemini research (LOCKED — do not re-research):**
- LS timer delay/duration fields store values in **tenths of a second** (delay=10 = 1.0s)
- FUNC_STICKY `andsw` is a **hard gate** — if the gate goes false, the latch drops immediately
- OVERRIDE_CHANNEL `def` format is `channel_index,value,enable` — channels are **0-indexed**
- Momentary switch notation: SC↓ = pressed, SC↑ = released (arrow characters)

**Unicode arrow character problem (RESOLVED — permanent fix applied):**
- PowerShell FileSystem write tool writes `\u2193` as literal text, not actual UTF-8 bytes
- Companion rejects these as blank/invalid switch references
- **Permanent fix:** Abandon arrow characters entirely. Use plain ASCII notation throughout:
  - `SA1` / `SA2` for 3-way positions
  - `SC` for SC pressed (momentary)
  - `SD` for SD up, `!SD` for SD down

**Drag_Race_Spec_v1.md:** Was discovered corrupted. Restored from git commit `ce10466` using:
```
git checkout ce10466 -- docs/Drag_Race_Spec_v1.md
```

**Logical switch chain (L1–L4):** Was missing entirely from the committed YAML in previous session. Now present.

**Final state of drag race template:** Plain ASCII switch notation in use. No arrow characters anywhere.

---

### Session 12B — File Housekeeping (this chat)

**ROOSTX_FILES.md situation:**
- Was missing from repo root
- Found at: `docs/RoosTx Doocumentation/ROOSTX_FILES.md` (old archived version)
- That old version was committed to repo root — it is **NOT current**
- The copy uploaded to Claude project knowledge is the Session 11 version
- **Action needed next session:** Update ROOSTX_FILES.md at repo root to reflect Session 12 changes, then commit

**The Doocumentation folder typo** (`docs/RoosTx Doocumentation/`) still exists in the repo. Still needs renaming. Still on the list.

---

## CURRENT STATE OF KEY FILES

| File | State | Notes |
|------|-------|-------|
| `drag_race_template.py` | NEEDS VERIFICATION | Plain ASCII notation applied this session |
| `model.py` | v0.6 FIXED | All 4 Grok bugs resolved |
| `ROOSTX_FILES.md` (repo root) | STALE | Old archived version — needs update |
| `docs/Drag_Race_Spec_v1.md` | RESTORED | Recovered from git ce10466 |
| `roostx_wizard_v3.html` | LOCKED | Do not touch |
| All Layers 1–3 files | LOCKED | Do not touch |

---

## HARD RULES — DO NOT FORGET

- **SC2 / SD2 / SB2 DO NOT EXIST.** SB, SC, SD are momentary. No position 2.
- **CH6/SD is RESERVED.** Never assign it to anything.
- **No arrow characters in YAML.** Use SA1, SA2, SC, !SD, SD — plain ASCII only.
- **GVs cannot go in LS delay/duration fields** (uint8_t only)
- **GVs cannot go in mix speedUp/speedDown fields** (Issue #4832, unresolved)
- **Always test in Companion Simulate Radio before writing to the radio.** Kevin bricked his radio once already.
- **Terminology:** Steering Wheel, Throttle Trigger, Drive Mode (DM). Never stick, never Flight Mode.
- **Don't run git autonomously.** Kevin runs all git commands himself in Git Bash.
- **Don't take off on tasks.** Wait for green light.

---

## GIT RULE FOR THIS PROJECT

Always give Kevin individual commands with separate copy points. Never combine into one multi-line block. He has hand tremors and a bad touchpad — multi-line paste is error-prone. Always include `git add` explicitly before commit.

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Update ROOSTX_FILES.md at repo root to Session 12 state, commit | Claude | FIRST ORDER NEXT SESSION |
| 2 | Verify drag_race_template.py output loads cleanly in Companion | Kevin | NEEDS TEST |
| 3 | Fix vehicle taxonomy throughout codebase | Claude | NOT STARTED |
| 4 | Schema/component conformance audit (send files to Grok) | Kevin + Grok | NOT STARTED |
| 5 | Fix SA expansion bay hardcoding (Grok flag) | Claude | NOT STARTED |
| 6 | Grok verify Rock_Crawler.yml | Kevin + Grok | NOT STARTED |
| 7 | Grok verify drag_library.json | Kevin + Grok | NOT STARTED |
| 8 | Expand Drag Racer feature list in wizard | Claude | NOT STARTED |
| 9 | Add 4WS expansion bay prerequisite warning to wizard feature card | Claude | NOT STARTED |
| 10 | Clone repo to HAL9000 | Kevin | NOT STARTED |
| 11 | Remove Syncthing, clean up .st folders | Kevin | NOT STARTED |
| 12 | Rename docs/RoosTx Doocumentation/ (fix typo) | Claude | NOT STARTED |
| 13 | Google Drive setup and sync | Kevin + Claude | NOT STARTED |
| 14 | GUI redesign discussion | Kevin + Claude | NOT STARTED |
| 15 | Final wizard demo lock | Claude + Kevin | NOT STARTED |
| 16 | Reach out to elecpower | Kevin | NOT STARTED |
| 17 | Update CONTRIBUTING.md — purge FM/stick language | Claude | NOT STARTED |
| 18 | Install Python 3.12 on Lappy (no PATH, venv312) | Kevin | NOT STARTED |
| 19 | Install cmake, ninja, msys2, git-lfs on Lappy | Kevin | NOT STARTED |
| 20 | Change MCP filesystem config path from ghost LogiTX folder to D:\RoosTx | Kevin | NOT STARTED |

---

## INFRASTRUCTURE

| Item | Status |
|------|--------|
| Repo | PUBLIC at github.com/WickedFog/Test_Bench_1 |
| Lappy | Windows 10, D:\RoosTx, Python 3.14, Git 2.53, VS Code, Node 22.14.0 |
| HAL9000 | Windows 11, 192.168.50.128, Python 3.12 |
| Companion | 2.11.4 — matches radio firmware |
| Google Drive | Mounted at G: |
| Syncthing | Still active, gitignored |

---

## HOW TO START SESSION 13

Paste this entire document at the top of the new chat.

**Session 13 opens differently — Gemini goes first.**
Before any code work, Gemini delivers the Research Enhancement Brief (see below). Claude reads it, confirms understanding, then work begins.

---

## GEMINI RESEARCH ENHANCEMENT PROJECT

**Purpose:** Give Claude a rock-solid foundation before touching any more drag race code. The Unicode/arrow character mess, the missing logical switch chain, the Companion import failures — all of it traces back to gaps in EdgeTX internals knowledge. Fix the knowledge, fix the code.

**Gemini — research and document the following:**

### 1. EdgeTX YAML Structure — Drag Race Specifics
- Exact YAML schema for `logicalSw` entries in EdgeTX 2.11.4
- Valid values for `func`, `def`, `andsw`, `delay`, `duration` fields
- How FUNC_STICKY behaves: set input, clear input, andsw gate interaction
- How FUNC_VPOS behaves: threshold, input source format
- Confirm: delay/duration units (tenths of a second — verify against source)

### 2. Switch Notation — Plain ASCII
- Confirm exact string values Companion/EdgeTX expects for:
  - SA 3-way: up, mid, down positions
  - SC momentary: pressed vs released
  - SD: up vs down
  - Negation syntax (!SD, !SC, etc.)
- Confirm these are valid with NO arrow characters

### 3. OVERRIDE_CHANNEL Custom Function
- Exact `def` field format: channel index, value, enable flag
- Confirm 0-indexed vs 1-indexed channels
- Confirm valid value range
- How it interacts with mixes — does it completely bypass them?

### 4. Logical Switch Chain for Drag Race (L1–L4)
- Walk through the intended behavior:
  - L1: throttle position threshold — detects trigger pull past X%
  - L2: sticky arm — latches when L1 true
  - L3: staged delay (burnout timer)
  - L4: launch active gate
- Verify the YAML entries that correctly represent this chain
- Flag any known issues with chained FUNC_STICKY in 2.11.x

### 5. Mix Behavior in Drag Race Context
- How REPL vs ADD mltpx interact when multiple mixes target same channel
- How flightModes bitmask controls which Drive Mode a mix is active in
- Confirm bitmask bit order (DM0=bit0, etc.)

### 6. Known EdgeTX 2.11.x Bugs Relevant to This Project
- Issue #4832 (GV in ramp fields) — current status
- Any other open issues affecting logical switches, OVERRIDE_CHANNEL, or YAML import

**Deliverable:** A clean research doc. No fluff. Findings only, with source references where possible. Structured so Claude can read it top to bottom and have everything needed to rebuild drag_race_template.py correctly on the first pass.

---

*Session 12 | Maintained by Claude*

---

*Session 12 | Maintained by Claude*
