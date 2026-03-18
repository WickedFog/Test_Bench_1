# RoosTx - Project File Manifest
**Last Updated: Session 11 (final) | Maintained by: Claude**

Check this file at the start of every session to know exactly where everything stands.

---

## ENGINE FILES (`roostx_core/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `model.py` | v0.7 | UPDATED Session 11 | lsPersist/lsState fixed, semver default 2.11.4, Drive Mode terminology, add_curve() method added |
| `drag_race_template.py` | v2 | REBUILT Session 11 | Full rebuild from approved spec. Curves added (Burnout/Stg1/Stg2/Stg3). Needs radio testing. |
| `crawler_template.py` | v1-ROLE | VERIFIED (Grok) | ROLE_ refactor complete |
| `roostx_wizard.py` | v0.2 | RUNNING | Asks radio first, loads switch map, passes to build() |
| `setup_roostx.py` | - | UNREVIEWED | Not yet audited |

---

## MODEL FILES (`models/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `Drag_Race_v2.yml` | v2 | REFERENCE | semver 2.11.4. Known good logical switch structure. |
| `Drag_Race_v4.yml` | v4 | GENERATED Session 11 | Output of rebuilt template. Needs radio testing. |
| `Rock_Crawler.yml` | v1 | IN REPO | semver 2.11.4. Not yet Grok-verified. |
| `archive/Drag_Race_v3.yml` | v3 | ARCHIVED | Broken test file. Kept for reference. |

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
| `drag_library.json` | DRAFT | Pending Grok verification |

---

## VEHICLE TAXONOMY (`research_database/vehicles/`)

| File | Status | Notes |
|------|--------|-------|
| `taxonomy_research_v1.md` | DRAFT | Basher = style not type. Pending codebase propagation. |

---

## WIZARD (`wizard/`)

| File | Status | Notes |
|------|--------|-------|
| `roostx_wizard_v3.html` | LOCKED v1 skin | Do not modify. |

---

## DOCUMENTATION (`docs/`)

| File | Status | Notes |
|------|--------|-------|
| `design-tokens.css` | LOCKED | Full color palette locked Session 8 |
| `Drag_Race_Spec_v1.md` | APPROVED | Kevin-approved Session 11. Source of truth for rebuild. |
| `Drag_Race_Curves_v1.txt` | DRAFT | Kevin curve ideas. Burnout, Stage 1/2/3. Placeholder straight lines in template, Kevin to dial in sine curves. |
| `GROK_VERIFICATION_BRIEF.md` | COMPLETE | Session 9 audit complete |
| `roostx_wizard_v4.html` | IN REPO | Live demo linked in README. Needs final design lock. |
| `roostx_engineering_brief.txt` | IN REPO | Engineering reference |
| `surface_control_standard_v1.txt` | IN REPO | Control standard reference |
| `RoosTx_Documentation/RoosTx_System_Design_v1.1.pdf` | IN REPO | Typo in folder name fixed Session 11 |
| `sessions/Session_12_Handoff.md` | IN REPO | Session 12 start doc |

---

## REPO ROOT FILES

| File | Status | Notes |
|------|--------|-------|
| `README.md` | DONE | Includes live wizard v4 demo link |
| `CONTRIBUTING.md` | DONE | Needs FM/stick language purge (pending) |
| `LICENSE` | DONE | MIT, Kevin Rowe 2026 |
| `.gitignore` | DONE | Covers pycache, syncthing, zips, output/ |
| `MT12_SWITCH_DESIGN.md` | IN REPO | Hardware reference |
| `ROOSTX_FILES.md` | IN REPO | This file. Single source of truth. |
| `RoosTx_System_Design_v1.1.docx` | IN REPO | At repo root. Consider moving to docs/. |

---

## GROK VERIFICATION RESULTS (Session 9)

| Item | Result |
|------|--------|
| SC2/SD2 invalid references | FIXED |
| expoData empty | FIXED |
| inputNames empty | FIXED |
| semver | FIXED - now 2.11.4 |
| GV in delay field | NOT PRESENT |
| GV ramp limitation | NOT PRESENT |
| SD/CH6 lockout direction | CONFIRMED - DOWN = active |
| Telemetry voltage field | CONFIRMED - RxBt |
| Schema conformance (Layers 1-3) | NOT YET AUDITED |
| Basher taxonomy violations | NOT YET AUDITED |
| Expansion bay SA hardcoding | FLAGGED |

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Test Drag_Race_v4.yml on radio — verify SD block, DM switching, burnout LS chain | Kevin + Claude | NEXT UP |
| 2 | Wire curves to correct mixes in template | Claude | NEXT UP |
| 3 | Fix vehicle taxonomy throughout codebase | Claude | NOT STARTED |
| 4 | Schema/component conformance audit | Kevin + Grok | NOT STARTED |
| 5 | Fix SA expansion bay hardcoding | Claude | NOT STARTED |
| 6 | Grok verify Rock_Crawler.yml | Kevin + Grok | NOT STARTED |
| 7 | Grok verify drag_library.json | Kevin + Grok | NOT STARTED |
| 8 | Expand Drag Racer feature list in wizard | Claude | NOT STARTED |
| 9 | Add 4WS expansion bay prerequisite warning | Claude | NOT STARTED |
| 10 | Clone repo to HAL9000 | Kevin | NOT STARTED |
| 11 | Remove Syncthing, clean up .st folders | Kevin | NOT STARTED |
| 12 | Purge FM/stick language from CONTRIBUTING.md | Claude | NOT STARTED |
| 13 | Google Drive setup and sync | Kevin + Claude | NOT STARTED |
| 14 | GUI redesign discussion | Kevin + Claude | NOT STARTED |
| 15 | Final wizard demo lock | Claude + Kevin | NOT STARTED |
| 16 | Reach out to elecpower | Kevin | NOT STARTED |
| 17 | Install cmake, ninja, msys2, git-lfs on Lappy | Kevin | NOT STARTED |

---

## INFRASTRUCTURE

| Item | Status | Notes |
|------|--------|-------|
| GitHub repo | PUBLIC (temp name) | github.com/WickedFog/Test_Bench_1 - rename to RoosTx when ready |
| Node.js | INSTALLED Session 11 | v22.14.0 on Lappy |
| Python | INSTALLED Session 11 | 3.12.9 on Lappy - use this, not 3.14 (corrupt) |
| pyyaml | INSTALLED Session 11 | In Python 3.12 environment |
| Companion | UPDATED Session 11 | 2.11.4 - matches radio |
| HAL9000 (Desktop) | OK | Windows 11, IP 192.168.50.128, Python 3.12 |
| Lappy (Laptop) | OK | Windows 10, D: drive, Python 3.12.9, Git 2.53, VS Code, Node 22 |
| Remote Desktop | OK | HAL9000 to Lappy via TeamViewer |
| Google Drive (G:) | MOUNTED | Drive letter G: confirmed |
| Syncthing | ACTIVE | Still running - gitignored but active. Remove when convenient. |
| MCP filesystem | WORKAROUND | LogiTX folder created as placeholder. Change to D:\RoosTx via Settings > Developer. |

---

## DESIGN DECISIONS (LOCKED)

| Decision | Value |
|----------|-------|
| Drag race DM0 | Race (SA up) - default on power-up |
| Drag race DM1 | Stage (SA mid) |
| Drag race DM2 | Burnout (SA dn) |
| Trans brake switch | SC - momentary |
| Master throttle block | SD - always enforced via customFn OVERRIDE |
| LED | Red = SD up (blocked), Green = SD down (armed) |
| SB | Parachute deploy |
| Telemetry voltage | RxBt |
| All controls | Suggested defaults, user-overridable in wizard |
| Wizard skin v1 | Claude V1 - roostx_wizard_v3.html LOCKED |
| Canonical wizard width | 480px |
| semver | 2.11.4 |

---

## TERMINOLOGY (LOCKED)

| Use this | Never use this |
|----------|----------------|
| Steering Wheel | Steering stick |
| Throttle Trigger | Throttle stick |
| Drive Mode (DM) | Flight Mode (FM) |

---

## RUN TEMPLATE COMMAND

```
cd /d/RoosTx/roostx_core
C:/Users/WickedFog/AppData/Local/Programs/Python/Python312/python.exe drag_race_template.py
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
