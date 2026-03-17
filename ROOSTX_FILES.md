# RoosTx — Project File Manifest
**Last Updated: Session 11 | Maintained by: Claude**

Check this file at the start of every session to know exactly where everything stands.

---

## ENGINE FILES (`roostx_core/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `model.py` | v0.6 | FIXED | expoData, inputNames, semver all fixed. Grok verified. |
| `drag_race_template.py` | v1-ROLE | NEEDS FULL REBUILD | SC2/SD2 fixed but full logic redesign still required. Priority #1. |
| `crawler_template.py` | v1-ROLE | VERIFIED (Grok) | ROLE_ refactor complete |
| `roostx_wizard.py` | v0.2 | RUNNING | Asks radio first, loads switch map, passes to build() |
| `setup_roostx.py` | — | UNREVIEWED | Not yet audited |

**Note:** `roostx_core/output/` contains test output YMLs (2.yml, drag.yml, Fukd_Off.yml, grockcrawer.yml). These are wizard run artifacts. Confirm they are gitignored.

---

## MODEL FILES (`models/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `Drag_Race_v2.yml` | v2 | VERIFIED | All 4 bugs fixed. Correct semver, expoData, inputNames, SC1/L2+SA0. |
| `Rock_Crawler.yml` | v1 | IN REPO | Built Session 10. Not yet Grok-verified. |

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
| `drag_library.json` | DRAFT | Gemini + Grok generated. Pending Grok verification. Covers FUNC_STICKY, FUNC_VPOS, FUNC_EDGE, FUNC_EQUAL + drag-specific constraints (GV ramp limitation, andsw hard-gate behavior). |

---

## VEHICLE TAXONOMY (`research_database/vehicles/`)

| File | Status | Notes |
|------|--------|-------|
| `taxonomy_research_v1.md` | DRAFT | Gemini research + WickedFog review. Platform = vehicle type, Driving style = secondary. Basher = style not type. Pending full codebase propagation. |

---

## WIZARD (`wizard/`)

| File | Status | Notes |
|------|--------|-------|
| `roostx_wizard_v3.html` | LOCKED v1 skin | Mean rooster, headbob animation, fixed 540px panels, offline-embedded fonts, pinned footer nav. Designated locked v1 skin — do not modify. |

---

## DOCUMENTATION (`docs/`)

| File | Status | Notes |
|------|--------|-------|
| `design-tokens.css` | LOCKED | Full color palette locked Session 8 |
| `GROK_VERIFICATION_BRIEF.md` | COMPLETE | Session 9 audit complete |
| `roostx_wizard_v4.html` | IN REPO | Hardware violations fixed Session 10. Needs final design lock. |
| `roostx_engineering_brief.txt` | IN REPO | Engineering reference |
| `surface_control_standard_v1.txt` | IN REPO | Control standard reference |

**Note:** Folder `docs/RoosTx Doocumentation/` has a typo (double-O). Contains `RoosTx_System_Design_v1.1.pdf`. Rename to `docs/RoosTx_Documentation/` when convenient.

---

## REPO ROOT FILES

| File | Status | Notes |
|------|--------|-------|
| `README.md` | DONE | User-facing pitch, Session 9 rewrite |
| `CONTRIBUTING.md` | DONE | Rules, constraints, team roles, known issues |
| `LICENSE` | DONE | MIT, Kevin Rowe 2026 |
| `.gitignore` | DONE | Covers pycache, syncthing, zips, output/ |
| `MT12_SWITCH_DESIGN.md` | IN REPO | Hardware reference |
| `ROOSTX_FILES.md` | IN REPO | This file. Single source of truth. |
| `RoosTx_System_Design_v1.1.docx` | IN REPO | At repo root. Consider moving to docs/. |

---

## REFERENCE DOCUMENTS (Local Only — not in repo)

| File | Location | Notes |
|------|----------|-------|
| `RoosTx_Forum_Post.md` | RoosTx Resources | Ready to post |
| `AI_PROJECT_RULES.txt` | RoosTx Resources | Internal team rules |

---

## GROK VERIFICATION RESULTS (Session 9)

| Item | Result |
|------|--------|
| SC2/SD2 invalid references | FIXED — SC1/SD1 |
| expoData empty | FIXED |
| inputNames empty | FIXED |
| semver 2.11.4 | FIXED — 2.11.3 |
| GV in delay field | NOT PRESENT in current code |
| GV ramp limitation | NOT PRESENT — ramps hardcoded 0 |
| SD/CH6 lockout direction | CONFIRMED — DOWN = active |
| Telemetry field for drive pack voltage | CONFIRMED — RxBt |
| Schema conformance (Layers 1-3) | NOT YET AUDITED — needs file contents |
| Basher taxonomy violations | NOT YET AUDITED — needs file contents |
| Expansion bay SA hardcoding | FLAGGED — SA must not be hardcoded as 3-way |

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Rebuild `drag_race_template.py` from scratch | Claude | NOT STARTED |
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
| 12 | Confirm `roostx_core/output/` is gitignored | Claude | NOT STARTED |
| 13 | Google Drive setup and sync | Kevin + Claude | NOT STARTED |
| 14 | GUI redesign discussion (Kevin vision) | Kevin + Claude | NOT STARTED |
| 15 | Final wizard demo lock | Claude + Kevin | NOT STARTED |
| 16 | Reach out to elecpower | Kevin | NOT STARTED |
| 17 | Install Python 3.12 on Lappy (no PATH, venv312) | Kevin | NOT STARTED |
| 18 | Install cmake, ninja, msys2, git-lfs on Lappy | Kevin | NOT STARTED |

---

## INFRASTRUCTURE

| Item | Status | Notes |
|------|--------|-------|
| GitHub repo | PUBLIC (temp name) | github.com/WickedFog/Test_Bench_1 — rename to RoosTx when ready |
| Node.js | INSTALLED Session 11 | v22.14.0 on Lappy — fixes MCP filesystem npx error |
| HAL9000 (Desktop) | OK | Windows 11, IP 192.168.50.128, Python 3.12 |
| Lappy (Laptop) | OK | Windows 10, D: drive, Python 3.14, Git 2.53, VS Code, Node 22 |
| Remote Desktop | OK | HAL9000 to Lappy via TeamViewer |
| Google Drive (G:) | MOUNTED | Drive letter G: confirmed in Explorer |
| Syncthing | ACTIVE | Still running against D:\RoosTx — gitignored but active. Remove when convenient. |

---

## DESIGN DECISIONS (LOCKED)

| Decision | Value |
|----------|-------|
| Drag race drive mode switch | SA (3-way: Burnout/Stage/Race = SA0/SA1/SA2) |
| Trans brake switch | SC default, user-overridable |
| Launch arm latch | L4 sticky — sets on L2, clears when SA returns to SA0 |
| Throttle lockout | L4 gate — !L4 forces CH2 to 0 via customFn OVERRIDE |
| LED | Red = !L4 (disarmed), Green = L4 (armed/launch active) |
| Telemetry voltage field | RxBt |
| All controls | Suggested defaults, all user-overridable in wizard |
| Wizard skin v1 | Claude V1 — roostx_wizard_v3.html LOCKED |
| Canonical wizard width | 480px |

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
