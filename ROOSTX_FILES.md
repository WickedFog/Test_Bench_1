# RoosTx — Project File Manifest
**Last Updated: Session 9 | Maintained by: Claude**

Check this file at the start of every session to know exactly where everything stands.

---

## ENGINE FILES (`roostx_core/`)

| File | Version | Status | Notes |
|------|---------|--------|-------|
| `model.py` | v0.6 | ✅ FIXED | expoData, inputNames, semver all fixed. Grok verified. |
| `drag_race_template.py` | v1-ROLE | ⚠️ NEEDS REDESIGN | SC2/SD2 fixed to SC1/SD1. Full logic redesign still required. |
| `crawler_template.py` | v1-ROLE | ✅ VERIFIED (Grok) | ROLE_ refactor complete |
| `roostx_wizard.py` | v0.2 | ✅ RUNNING | Asks radio first, loads switch map, passes to build() |
| `setup_roostx.py` | — | ⚠️ UNREVIEWED | Not yet audited |

---

## SCHEMA FILES (`schemas/`)

| File | Status | Notes |
|------|--------|-------|
| `component.schema.json` | ✅ LOCKED | Verified |
| `pattern.schema.json` | ✅ LOCKED | Grok verified |

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

## WIZARD (`wizard/`)

| File | Status | Notes |
|------|--------|-------|
| `roostx_wizard_v3.html` | ✅ IN REPO | Claude V1 skin. Mean rooster, headbob animation, fixed panels, offline. Needs final design lock. |

---

## DOCUMENTATION (`docs/`)

| File | Status | Notes |
|------|--------|-------|
| `design-tokens.css` | ✅ LOCKED | Full color palette locked Session 8 |
| `GROK_VERIFICATION_BRIEF.md` | ✅ COMPLETE | Session 9 audit complete |
| `RoosTx_System_Design_v1.1.docx` | ✅ READY | Ready to send to elecpower |
| `roostx_engineering_brief.txt` | ✅ IN REPO | Engineering reference |
| `surface_control_standard_v1.txt` | ✅ IN REPO | Control standard reference |

---

## REPO ROOT FILES

| File | Status | Notes |
|------|--------|-------|
| `README.md` | ✅ DONE | User-facing pitch, Session 9 rewrite |
| `CONTRIBUTING.md` | ✅ DONE | Rules, constraints, team roles, known issues |
| `LICENSE` | ✅ DONE | MIT, Kevin Rowe 2026 |
| `.gitignore` | ✅ DONE | Covers pycache, syncthing, zips, output/ |
| `MT12_SWITCH_DESIGN.md` | ✅ IN REPO | Hardware reference |

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
| SC2/SD2 invalid references | ✅ FIXED — SC1/SD1 |
| expoData empty | ✅ FIXED |
| inputNames empty | ✅ FIXED |
| semver 2.11.4 | ✅ FIXED — 2.11.3 |
| GV in delay field | ✅ NOT PRESENT in current code |
| GV ramp limitation | ✅ NOT PRESENT — ramps hardcoded 0 |
| SD/CH6 lockout direction | ✅ CONFIRMED — DOWN = active |
| Telemetry field for drive pack voltage | ✅ CONFIRMED — RxBt |
| Schema conformance (Layers 1-3) | ⚠️ NOT YET AUDITED — needs file contents |
| Basher taxonomy violations | ⚠️ NOT YET AUDITED — needs file contents |
| Expansion bay SA hardcoding | ⚠️ FLAGGED — SA must not be hardcoded as 3-way |

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Rebuild `drag_race_template.py` from scratch | Claude | ❌ NOT STARTED |
| 2 | Fix vehicle taxonomy throughout codebase | Claude | ❌ NOT STARTED |
| 3 | Schema/component conformance audit (send files to Grok) | Kevin + Grok | ❌ NOT STARTED |
| 4 | Fix SA expansion bay hardcoding (Grok flag) | Claude | ❌ NOT STARTED |
| 5 | Build logical switch library (`research_database/logical_switches/`) | Claude | ❌ NOT STARTED |
| 6 | Google Drive setup and sync | Kevin + Claude | ❌ NOT STARTED |
| 7 | GUI redesign discussion (Kevin's vision) | Kevin + Claude | ❌ NOT STARTED |
| 8 | Final wizard demo lock | Claude + Kevin | ❌ NOT STARTED |
| 9 | Reach out to elecpower | Kevin | ❌ NOT STARTED |
| 10 | Install Python 3.12 on Lappy (no PATH, venv312) | Kevin | ❌ NOT STARTED |
| 11 | Install cmake, ninja, msys2, git-lfs on Lappy | Kevin | ❌ NOT STARTED |

---

## INFRASTRUCTURE

| Item | Status | Notes |
|------|--------|-------|
| GitHub repo | ✅ PUBLIC (temp name) | github.com/WickedFog/Test_Bench_1 — rename to RoosTx when ready |
| HAL9000 (Desktop) | ✅ | Windows 11, IP 192.168.50.128, Python 3.12 |
| Lappy (Laptop) | ✅ | Windows 10, D: drive, Python 3.14, Git 2.53, VS Code |
| Remote Desktop | ✅ | HAL9000 → Lappy working |
| Google Drive (G:) | ✅ MOUNTED | Drive letter G: confirmed in Explorer |
| Syncthing | ⚠️ | Still running against D:\RoosTx — gitignored but active |

---

## DESIGN DECISIONS (LOCKED)

| Decision | Value |
|----------|-------|
| Drag race drive mode switch | SA (3-way: Launch/Stage/WarmUp) |
| Trans brake switch | SC default, user-overridable |
| Launch arm | SD (down = armed) — SD1 = armed state |
| Throttle lockout | SD/CH6, DOWN = active |
| Telemetry voltage field | RxBt |
| All controls | Suggested defaults, all user-overridable in wizard |

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

