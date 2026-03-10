# RoosTx — Project File Manifest
**Last Updated: Session 4 | Maintained by: Claude**

Check this file at the start of every session to know exactly where everything stands.

---

## ENGINE FILES (`roostx_core/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `model.py` | v0.5 | ✅ VERIFIED | YAML output clean, passes diff vs Drag_Race.yml. Known bugs: expoData empty, inputNames empty, semver 2.11.4 should be 2.11.3 |
| `drag_race_template.py` | v1-ROLE | ⚠️ NEEDS REDESIGN | ROLE_ refactor done, but full logic redesign required per new drag race spec |
| `crawler_template.py` | v1-ROLE | ✅ VERIFIED (Grok) | ROLE_ refactor complete |
| `roosTx_wizard.py` | v0.2 | ✅ RUNNING | Asks radio first, loads switch map, passes to build(). Runs on HAL9000 |

---

## SCHEMA FILES (`schemas/`)

| File | Status | Notes |
|------|--------|-------|
| `component.schema.json` | ✅ LOCKED | Verified |
| `pattern.schema.json` | ✅ LOCKED | Rebuilt from scratch, Grok verified |

---

## PATTERN FILES (`research_database/patterns/`)

| File | Status | Notes |
|------|--------|-------|
| `drag.json` | ✅ LOCKED | CH5 launch_trigger fix applied |
| `crawler.json` | ✅ LOCKED | Stray brace fixed |
| `drift.json` | ✅ LOCKED | No changes needed |
| `skid_steer.json` | ✅ LOCKED | No changes needed |

---

## COMPONENT FILES (`research_database/components/`)

All 11 components use ROLE_ abstraction. No hardcoded switch names.

| File | Status |
|------|--------|
| `steering/logic.json` | ✅ LOCKED |
| `dig/logic.json` | ✅ LOCKED |
| `drag/logic.json` | ✅ LOCKED |
| `drive_modes/logic.json` | ✅ LOCKED |
| `gyro/logic.json` | ✅ LOCKED |
| `lighting/logic.json` | ✅ LOCKED |
| `safety/logic.json` | ✅ LOCKED |
| `skid_steer/logic.json` | ✅ LOCKED |
| `telemetry/logic.json` | ✅ LOCKED |
| `ui/logic.json` | ✅ LOCKED |
| `winch/logic.json` | ✅ LOCKED |

---

## REFERENCE DOCUMENTS

| File | Location | Notes |
|------|----------|-------|
| `MT12_SWITCH_DESIGN.md` | outputs / GitHub | Hardware reference, ROLE assignments, design decisions |
| `ROOSTX_FILES.md` | outputs / GitHub | This file — project manifest |
| `RoosTx_System_Design.docx` | outputs / GitHub | Full system design document v1.1 |
| `Intent.txt` | project root | Kevin's original vision document |
| `Drag_Race.yml` | project root | Reference model file from radio |

---

## GENERATED TEST FILES

| File | Notes |
|------|-------|
| `Fukd_Off.yml` | Drag race test model — validated in Companion |
| `2.yml` | Drag race test model |

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Write drag race control system design doc (plain English spec) | Claude | ⏳ NEXT |
| 2 | Build `mt12.json` radio map file | Claude | ❌ NOT STARTED |
| 3 | Rebuild `drag_race_template.py` from scratch per new design | Claude | ❌ NOT STARTED |
| 4 | Build logical switch library (`research_database/logical_switches/`) | Claude | ❌ NOT STARTED |
| 5 | Merge logic (pattern → components → resolve ROLE → generate .yml) | Claude | ❌ NOT STARTED |
| 6 | Fix known bugs in `model.py` (expoData, inputNames, semver) | Claude | ❌ NOT STARTED |
| 7 | Install Companion on Lappy | Kevin | ⏳ PENDING |
| 8 | Upload fresh RoosTx.zip to GitHub | Kevin | ⏳ PENDING |

---

## INFRASTRUCTURE

| Item | Status | Notes |
|------|--------|-------|
| GitHub repo | ✅ LIVE | github.com/WickedFog/RoosTx (private) |
| HAL9000 (Desktop) | ✅ | Windows 11, IP 192.168.50.128, Python 3.12 |
| Lappy (Laptop) | ✅ | Windows 10, 500GB SSD, Python 3.14, Remote Desktop from HAL9000 |
| Google Drive connector | ✅ | Connected via Claude |
| GitHub connector | ✅ | Connected via Claude |

---

## KNOWN ENGINE BUGS (model.py)

1. `expoData` outputs empty `[]` — ST and TH expo not written
2. `inputNames` outputs empty `{}` — input names not written
3. `semver` outputs `2.11.4` — should be `2.11.3`
4. Momentary switch positions wrong — `SC2`/`SD2` used but momentary switches have no position 2

---

## TEAM

| Role | Who |
|------|-----|
| Vision / Direction / Final Approval | Kevin (WickedFog) |
| Architecture Lead / Orchestration | Claude |
| Verification / Validation | Grok |
| Research | Gemini (active) |
| Break Room | ChatGPT (permanent assignment) |

---

*Update this file at the end of every session. It is the single source of truth.*
