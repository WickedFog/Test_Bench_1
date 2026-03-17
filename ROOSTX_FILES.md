# RoosTx - Project File Manifest
**Last Updated: Session 11 | Maintained by: Claude**

Check this file at the start of every session to know exactly where everything stands.

---

## ENGINE FILES (`roostx_core/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `model.py` | v0.6 | FIXED | expoData, inputNames, semver all fixed. Grok verified. |
| `drag_race_template.py` | v1-ROLE | NEEDS FULL REBUILD | Spec now approved (Drag_Race_Spec_v1.md). Ready to rebuild next session. |
| `crawler_template.py` | v1-ROLE | VERIFIED (Grok) | ROLE_ refactor complete |
| `roostx_wizard.py` | v0.2 | RUNNING | Asks radio first, loads switch map, passes to build() |
| `setup_roostx.py` | - | UNREVIEWED | Not yet audited |

---

## MODEL FILES (`models/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `Drag_Race_v2.yml` | v2 | VERIFIED | semver bumped to 2.11.4 Session 11 |
| `Rock_Crawler.yml` | v1 | IN REPO | semver bumped to 2.11.4 Session 11. Not yet Grok-verified. |
| `archive/Drag_Race_v3.yml` | v3 | ARCHIVED | Broken test file from Session 11. Kept for reference. |

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
| `drag_library.json` | DRAFT | Gemini + Grok generated. Pending Grok verification. |

---

## VEHICLE TAXONOMY (`research_database/vehicles/`)

| File | Status | Notes |
|------|--------|-------|
| `taxonomy_research_v1.md` | DRAFT | Basher = style not type. Pending full codebase propagation. |

---

## WIZARD (`wizard/`)

| File | Status | Notes |
|------|--------|-------|
| `roostx_wizard_v3.html` | LOCKED v1 skin | Mean rooster, headbob animation. Do not modify. |

---

## DOCUMENTATION (`docs/`)

| File | Status | Notes |
|------|--------|-------|
| `design-tokens.css` | LOCKED | Full color palette locked Session 8 |
| `Drag_Race_Spec_v1.md` | APPROVED | Full drag race spec. Kevin-approved Session 11. Source of truth for rebuild. |
| `GROK_VERIFICATION_BRIEF.md` | COMPLETE | Session 9 audit complete |
| `roostx_wizard_v4.html` | IN REPO | Live demo linked in README. Needs final design lock. |
| `roostx_engineering_brief.txt` | IN REPO | Engineering reference |
| `surface_control_standard_v1.txt` | IN REPO | Control standard reference |

**Note:** Folder `docs/RoosTx Doocumentation/` has a typo (double-O). Rename when convenient.

---

## REPO ROOT FILES

| File | Status | Notes |
|------|--------|-------|
| `README.md` | DONE | Includes live wizard v4 demo link |
| `CONTRIBUTING.md` | DONE | Rules, constraints, team roles, known issues |
| `LICENSE` | DONE | MIT, Kevin Rowe 2026 |
| `.gitignore` | DONE | Covers pycache, syncthing, zips, output/ |
| `MT12_SWITCH_DESIGN.md` | IN REPO | Hardware reference |
| `ROOSTX_FILES.md` | IN REPO | This file. Single source of truth. |
| `RoosTx_System_Design_v1.1.docx` | IN REPO | At repo root. Consider moving to docs/. |

---

## REFERENCE DOCUMENTS (Local Only - not in repo)

| File | Location | Notes |
|------|----------|-------|
| `RoosTx_Forum_Post.md` | RoosTx Resources | Ready to post |
| `AI_PROJECT_RULES.txt` | RoosTx Resources | Internal team rules |

---

## GROK VERIFICATION RESULTS (Session 9)

| Item | Result |
|------|--------|
| SC2/SD2 invalid references | FIXED |
| expoData empty | FIXED |
| inputNames empty | FIXED |
| semver | FIXED - now 2.11.4 (radio is running 2.11.4) |
| GV in delay field | NOT PRESENT |
| GV ramp limitation | NOT PRESENT - ramps hardcoded 0 |
| SD/CH6 lockout direction | CONFIRMED - DOWN = active |
| Telemetry voltage field | CONFIRMED - RxBt |
| Schema conformance (Layers 1-3) | NOT YET AUDITED |
| Basher taxonomy violations | NOT YET AUDITED |
| Expansion bay SA hardcoding | FLAGGED - SA must not be hardcoded as 3-way |

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Rebuild `drag_race_template.py` from scratch using approved spec | Claude | READY - spec approved |
| 2 | Fix vehicle taxonomy throughout codebase | Claude | NOT STARTED |
| 3 | Schema/component conformance audit (send files to Grok) | Kevin + Grok | NOT STARTED |
| 4 | Fix SA expansion bay hardcoding (Grok flag) | Claude | NOT STARTED |
| 5 | Grok verify `Rock_Crawler.yml` | Kevin + Grok | NOT STARTED |
| 6 | Grok verify `drag_library.json` | Kevin + Grok | NOT STARTED |
| 7 | Expand Drag Racer feature list in wizard | Claude | NOT STARTED |
| 8 | Add 4WS expansion bay prerequisite warning to wizard feature card | Claude | NOT STARTED |
| 9 | Clone repo to HAL9000 | Kevin | NOT STARTED |
| 10 | Remove Syncthing, clean up .st folders | Kevin | NOT STARTED |
| 11 | Rename `docs/RoosTx Doocumentation/` (fix typo) | Claude | NOT STARTED |
| 12 | Google Drive setup and sync | Kevin + Claude | NOT STARTED |
| 13 | GUI redesign discussion (Kevin vision) | Kevin + Claude | NOT STARTED |
| 14 | Final wizard demo lock | Claude + Kevin | NOT STARTED |
| 15 | Reach out to elecpower | Kevin | NOT STARTED |
| 16 | Update CONTRIBUTING.md - purge all FM/stick language, add DM/Steering Wheel/Throttle Trigger | Claude | NOT STARTED |
| 17 | Install Python 3.12 on Lappy (no PATH, venv312) | Kevin | NOT STARTED |
| 18 | Install cmake, ninja, msys2, git-lfs on Lappy | Kevin | NOT STARTED |

---

## INFRASTRUCTURE

| Item | Status | Notes |
|------|--------|-------|
| GitHub repo | PUBLIC (temp name) | github.com/WickedFog/Test_Bench_1 - rename to RoosTx when ready |
| Node.js | INSTALLED Session 11 | v22.14.0 on Lappy - fixes MCP filesystem npx error |
| Companion | UPDATED Session 11 | Now 2.11.4 - matches radio firmware |
| HAL9000 (Desktop) | OK | Windows 11, IP 192.168.50.128, Python 3.12 |
| Lappy (Laptop) | OK | Windows 10, D: drive, Python 3.14, Git 2.53, VS Code, Node 22 |
| Remote Desktop | OK | HAL9000 to Lappy via TeamViewer |
| Google Drive (G:) | MOUNTED | Drive letter G: confirmed in Explorer |
| Syncthing | ACTIVE | Still running against D:\RoosTx - gitignored but active. Remove when convenient. |
| MCP filesystem config | FIXED Session 11 | Was pointing at ghost LogiTX folder. Created folder as workaround. Change path to D:\RoosTx via Settings > Developer when convenient. |

---

## DESIGN DECISIONS (LOCKED)

| Decision | Value |
|----------|-------|
| Drag race DM0 | Race (SA up) - default on power-up |
| Drag race DM1 | Stage (SA mid) |
| Drag race DM2 | Burnout (SA down) |
| Trans brake switch | SC - momentary hold=engaged, release=launch |
| Master throttle block | SD down = armed, SD up = blocked. Always enforced. |
| LED | Red = disarmed, Green = armed |
| Telemetry voltage field | RxBt |
| All controls | Suggested defaults, all user-overridable in wizard |
| Wizard skin v1 | Claude V1 - roostx_wizard_v3.html LOCKED |
| Canonical wizard width | 480px |
| semver | 2.11.4 |
| Terminology | Steering Wheel, Throttle Trigger, Drive Mode (DM) - never stick/flight mode |

---

## TERMINOLOGY (LOCKED)

| Use this | Never use this |
|----------|----------------|
| Steering Wheel | Steering stick |
| Throttle Trigger | Throttle stick |
| Drive Mode (DM) | Flight Mode (FM) |

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
