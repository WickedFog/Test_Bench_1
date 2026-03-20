# RoosTx - Project File Manifest
**Last Updated: Session 13 | Maintained by: Claude**

Check this file at the start of every session to know exactly where everything stands.

---

## ENGINE FILES (`roostx_core/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `model.py` | v0.7 | STABLE | lsPersist/lsState fixed, semver default 2.11.4, Drive Mode terminology, add_curve() method added |
| `drag_race_template.py` | v3 | NEEDS REBUILD Session 13 | Current output is broken — uses wrong switch notation pre-Session 13 discoveries. Rebuild required before wizard wire-up. |
| `crawler_template.py` | v1-ROLE | VERIFIED (Grok) | ROLE_ refactor complete |
| `roostx_wizard.py` | v0.2 | RUNNING | Asks radio first, loads switch map, passes to build() |
| `setup_roostx.py` | - | UNREVIEWED | Not yet audited |

---

## MODEL FILES (`models/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `Drag_Race_v4.yml` | v4 | STALE — needs regen | Generated pre-Session 13. Wrong switch notation. Regenerate from rebuilt template. |

### `models/archive/`

| File | Status | Notes |
|------|--------|-------|
| `Drag_Car_v4.yml` | ARCHIVED | Old test file |
| `Drag_Race_v2.yml` | REFERENCE | Known good LS structure reference |
| `Drag_Race_v3.yml` | ARCHIVED | Broken test file |
| `Drag_Race_v4_BACKUP.yml` | ARCHIVED | Pre-Session 13 backup |
| `Drag_Race_v4_WORKING_REF.etx` | REFERENCE | Working .etx from Documents folder. SD toggle confirmed working. Source of truth for SD2/SC2 notation. |
| `rcgroups_p21_model07.yml` | REFERENCE | Real user model from RCGroups thread. Confirms SC/SB toggle patterns. |
| `Rock_Crawler.yml` | PENDING | Not yet Grok-verified |
| `archive/scratch/` | SCRATCH | Throwaway test files |

### `models/test/` — Session 13 verified test files

| File | Status | Notes |
|------|--------|-------|
| `Launch_Control_3Stage_REFERENCE.yml` | **GOLD — DO NOT MODIFY** | Fully verified 3-stage launch control. All notation confirmed. Full comments inside. |
| `SD_Toggle_Test.yml` | VERIFIED | SD2,SD2 toggle working |
| `SD_SC_Test.yml` | VERIFIED | SD toggle + SC transbrake gate working |
| `SC_Transbrake_Test.yml` | SUPERSEDED | Earlier attempt, replaced by SD_SC_Test |
| `Stage_Test.yml` | WORKING | Current stage test file — matches REFERENCE |
| `LED_Test.yml` | VERIFIED | All 3 RGB_LED def formats accepted by Companion |

---

## SCHEMA FILES (`schemas/`)

| File | Status | Notes |
|------|--------|-------|
| `component.schema.json` | LOCKED | Verified |
| `pattern.schema.json` | LOCKED | Grok verified |

---

## PATTERN FILES (`research_database/patterns/`)

| File | Status | Notes |
|------|--------|-------|
| `drag.json` | LOCKED | CH5 launch_trigger fix applied |
| `crawler.json` | LOCKED | Stray brace fixed |
| `drift.json` | LOCKED | No changes needed |
| `skid_steer.json` | LOCKED | No changes needed |

---

## COMPONENT FILES (`research_database/components/`)

All 11 components use ROLE_ abstraction. No hardcoded switch names.

| File | Status |
|------|--------|
| `steering/logic.json` | LOCKED |
| `dig/logic.json` | LOCKED |
| `drag/logic.json` | LOCKED |
| `drive_modes/logic.json` | LOCKED |
| `gyro/logic.json` | LOCKED |
| `lighting/logic.json` | LOCKED |
| `safety/logic.json` | LOCKED |
| `skid_steer/logic.json` | LOCKED |
| `telemetry/logic.json` | LOCKED |
| `ui/logic.json` | LOCKED |
| `winch/logic.json` | LOCKED |

---

## LOGICAL SWITCH LIBRARY (`research_database/logical_switches/`)

| File | Status | Notes |
|------|--------|-------|
| `drag_library.json` | DRAFT | Pending Grok verification. Some entries pre-date Session 13 notation fixes — audit needed. |

---

## VEHICLE TAXONOMY (`research_database/vehicles/`)

| File | Status | Notes |
|------|--------|-------|
| `taxonomy_research_v1.md` | DRAFT | Basher = style not type. Pending codebase propagation. |

---

## WIZARD (`wizard/`)

| File | Status | Notes |
|------|--------|-------|
| `roostx_wizard_v3.html` | LOCKED v1 skin | Do not modify |
| `roostx_wizard_v4.html` | IN REPO | Live demo. Needs final design lock. |
| `design-tokens.css` | LOCKED | Full color palette locked Session 8 |

---

## DOCUMENTATION (`docs/`)

| File | Status | Notes |
|------|--------|-------|
| `Drag_Race_Spec_v1.md` | APPROVED | Kevin-approved Session 11. Source of truth for spec. |
| `Drag_Race_Curves_v1.txt` | DRAFT | Kevin curve ideas. Placeholder straight lines in template. Kevin to dial in sine curves. |
| `GROK_VERIFICATION_BRIEF.md` | COMPLETE | Session 9 audit complete |
| `MT12_SWITCH_DESIGN.md` | IN REPO | Hardware reference |
| `RoosTx_Documentation/RoosTx_System_Design_v1.1.pdf` | IN REPO | System design reference |
| `sessions/Session_12_Handoff.md` | IN REPO | Session 12 handoff |
| `GUIDES/Advanced_EdgeTX_Staged_Throttle.docx` | NEW Session 13 | Full verified instruction sheet for 3-stage launch control. Covers notation, LS chain, mix stack, YAML, limitations, test sequence. |

---

## REPO ROOT FILES

| File | Status | Notes |
|------|--------|-------|
| `README.md` | DONE | Includes live wizard v4 demo link |
| `CONTRIBUTING.md` | PENDING | Needs FM/stick language purge |
| `LICENSE` | DONE | MIT, Kevin Rowe 2026 |
| `.gitignore` | DONE | Covers pycache, syncthing, zips, output/ |
| `ROOSTX_FILES.md` | THIS FILE | Single source of truth |
| `RoosTx_System_Design_v1.1.docx` | IN REPO | Consider moving to docs/ |

---

## SESSION 13 — KEY DISCOVERIES (LOCKED KNOWLEDGE)

### Switch Notation (Companion 2.11.4 YAML)

| What you want | Correct notation | Broken — do not use |
|---|---|---|
| SD pressed / active state | `SD2` | `SD` (does nothing in sticky) |
| SD self-toggle | `def: SD2,SD2` | `def: SD,SD` (no effect) |
| SC pressed (as gate) | `SC2` | `SC`, `SC1` (invalid) |
| SC NOT pressed | `!SC2` (in andsw field) | `!SC` |
| Throttle input source | `I1` (string) | `100` (integer, firmware-only) |

### RGB_LED def format (confirmed working)
```
def: red,1,On
def: green,1,On
```

### OVERRIDE_CHANNEL (confirmed working)
```
def: 1,0,1   # CH2, neutral (0=1500us), enabled
```
Must be in customFn gated by switch. Runs after all mixes.

### Mix stack order rule (CRITICAL)
```
1. TH base (ADD)
2. Stage 1 cap (REPL, swtch=L4)
3. Stage 2 cap (REPL, swtch=L5)
4. Stage 3 full (REPL, swtch=L6)
5. Transbrake kill (REPL, swtch=SC2)  ← MUST be after stages
6. Master kill (REPL, swtch=!L1)      ← MUST be last
```

### Launch latch gate (CRITICAL — prevents 100% spike)
```yaml
L4: func: FUNC_STICKY, def: L3,SD2, andsw: "!SC2"
```
L3's rising edge sets latch while SC held. Output masked until SC releases. Zero gap — Stage 1 fires immediately on SC release.

### What doesn't work (confirmed broken)
- `SD,SD` self-toggle — does nothing
- `SC,SC` self-toggle — does nothing (spring-return too fast)
- REPL kill mix placed before stage mixes — stages override kill
- GVs in delay/duration fields — Issue #4832, still unresolved
- GVs in speedUp/speedDown fields — Issue #4832, still unresolved

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Rebuild `drag_race_template.py` from Launch_Control_3Stage_REFERENCE.yml | Claude | FIRST ORDER |
| 2 | Regenerate Drag_Race_v4.yml from rebuilt template | Claude | AFTER #1 |
| 3 | Wire rebuilt template into wizard — verify wizard output matches reference | Claude + Kevin | AFTER #2 |
| 4 | Add GV trim adjustment (T1=Stage1%, T2=Stage2%) to template | Claude | AFTER #3 |
| 5 | Add burnout mode LS chain to drag race template | Claude | NOT STARTED |
| 6 | Add stage mode (DM1) throttle curves to template | Claude | NOT STARTED |
| 7 | Fix vehicle taxonomy throughout codebase | Claude | NOT STARTED |
| 8 | Schema/component conformance audit (send files to Grok) | Kevin + Grok | NOT STARTED |
| 9 | Fix SA expansion bay hardcoding (Grok flag) | Claude | NOT STARTED |
| 10 | Grok verify Rock_Crawler.yml | Kevin + Grok | NOT STARTED |
| 11 | Grok verify drag_library.json (some entries pre-date Session 13 fixes) | Kevin + Grok | NOT STARTED |
| 12 | Expand Drag Racer feature list in wizard | Claude | NOT STARTED |
| 13 | Add 4WS expansion bay prerequisite warning to wizard feature card | Claude | NOT STARTED |
| 14 | Clone repo to HAL9000 | Kevin | NOT STARTED |
| 15 | Remove Syncthing, clean up .st folders | Kevin | NOT STARTED |
| 16 | Rename docs/RoosTx Doocumentation/ (fix typo) — note: folder may still exist | Claude | NOT STARTED |
| 17 | Change MCP filesystem config path from ghost LogiTX folder to D:\RoosTx | Kevin | NOT STARTED |
| 18 | Purge FM/stick language from CONTRIBUTING.md | Claude | NOT STARTED |
| 19 | Google Drive setup and sync | Kevin + Claude | NOT STARTED |
| 20 | GUI redesign discussion | Kevin + Claude | NOT STARTED |
| 21 | Final wizard demo lock | Claude + Kevin | NOT STARTED |
| 22 | Reach out to elecpower | Kevin | NOT STARTED |
| 23 | Install cmake, ninja, msys2, git-lfs on Lappy | Kevin | NOT STARTED |

---

## INFRASTRUCTURE

| Item | Status | Notes |
|------|--------|-------|
| GitHub repo | PUBLIC (temp name) | github.com/WickedFog/Test_Bench_1 — rename to RoosTx when ready |
| Node.js | INSTALLED | v22.14.0 on Lappy |
| Python | INSTALLED | 3.12.9 on Lappy — use this, not 3.14 (corrupt) |
| pyyaml | INSTALLED | In Python 3.12 environment |
| Companion | 2.11.4 | Matches radio firmware |
| HAL9000 (Desktop) | OK | Windows 11, IP 192.168.50.128, Python 3.12 |
| Lappy (Laptop) | OK | Windows 10, D:\RoosTx, Python 3.12.9, Git 2.53, VS Code, Node 22 |
| Google Drive (G:) | MOUNTED | Drive letter G: confirmed |
| Syncthing | ACTIVE | Still running — gitignored but active. Remove when convenient. |
| MCP filesystem | WORKAROUND | Change to D:\RoosTx via Settings > Developer when convenient |
| Gemini GEM | ACTIVE | "Radiomaster MT12 Research Database" — EdgeTX/MT12 knowledge base. Has EdgeTX user manual, README, SUMMARY, summary_of_changes, translated user manual in knowledge base. |

---

## DESIGN DECISIONS (LOCKED)

| Decision | Value |
|----------|-------|
| Drag race DM0 | Race (SA up / SA0) — default on power-up |
| Drag race DM1 | Stage (SA mid / SA1) — staging lane |
| Drag race DM2 | Burnout (SA down / SA2) — burnout box |
| Master safety switch | SD — SD2,SD2 self-toggle via FUNC_STICKY |
| Transbrake switch | SC — SC2 as andsw gate (not self-toggle) |
| LED armed | Green (`green,1,On`) |
| LED disarmed | Red (`red,1,On`) |
| LED trigger | OVERRIDE_CHANNEL + RGB_LED in customFn, gated by L1/!L1 |
| SB | Parachute deploy (reserved) |
| Telemetry voltage | RxBt |
| Delay box (free tier) | Hardcoded at 0 (instant) — Issue #4832 prevents GV adjustment |
| Delay box (Pro Mod) | Lua script, 0.00–0.50s in 0.01s steps |
| Stage timers (free tier) | Hardcoded — Stage1=0.5s, Stage2=0.3s |
| Stage timers (Pro Mod) | Lua script, adjustable in 0.01s steps |
| Stage % (free tier) | GV1/GV2, adjustable via T1/T2 trims |
| Canonical wizard width | 480px |
| semver | 2.11.4 |

---

## FOLDER NAMING CONVENTION

Per Gemini suggestion: use ALL CAPS for folder names to match EdgeTX SD card convention.
- New folders: `GUIDES`, `MODELS`, `SCRIPTS` etc.
- Existing folders: rename when convenient, not urgently

---

## TERMINOLOGY (LOCKED)

| Use this | Never use this |
|----------|----------------|
| Steering Wheel | Steering stick |
| Throttle Trigger | Throttle stick |
| Drive Mode (DM) | Flight Mode (FM) |
| Transbrake | Transbrake stick / brake |

---

## RUN TEMPLATE COMMAND

```
cd /d/RoosTx/roostx_core
python drag_race_template.py
cp output/Drag_Race_RoosTx.yml ../models/Drag_Race_v4.yml
```

---

## TEAM

| Role | Who |
|------|-----|
| Vision / Direction / Final Approval | Kevin (WickedFog) |
| Architecture Lead / Code / Docs | Claude |
| Verification / Validation / Graphic Design | Grok |
| Research | Gemini |
| Break Room | ChatGPT (permanent assignment) |

---

*Update this file at the end of every session. It is the single source of truth.*
