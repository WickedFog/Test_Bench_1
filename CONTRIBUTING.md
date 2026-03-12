# Contributing to RoosTx

RoosTx is a structured, layered project. Before touching anything, read this.

---

## Project Structure

| Layer | Folder | Status | Description |
|-------|--------|--------|-------------|
| 1 | `schemas/` | ✅ LOCKED | Component and pattern schemas |
| 2 | `research_database/patterns/` | ✅ LOCKED | Control patterns (drag, crawler, drift, skid_steer) |
| 3 | `research_database/components/` | ✅ LOCKED | Feature components using ROLE_ abstraction |
| 4 | `roostx_core/` | ⚠️ IN PROGRESS | Engine, templates, model generator |
| 5 | `wizard/` | ⚠️ IN PROGRESS | Web-based setup wizard |
| 6-7 | — | ❌ NOT STARTED | Companion integration, packaging |

**LOCKED means locked.** Layers 1-3 do not change without explicit approval from the project lead.

---

## Hardware Constraints — MT12 (Read This First)

These are hard constraints. Violating them breaks real hardware.

- `CH6 / SD` is the factory standard for throttle lockout. Reassignment requires explicit justification and Grok verification. (Pending: confirm whether lockout activates on button UP or DOWN.)
- `SB`, `SC`, `SD` are **MOMENTARY** switches. They do not have a "2" position.
- `SC2`, `SD2`, `SB2` **do not exist** on the MT12. Do not reference them.
- Channel map: `CH1:ST CH2:TH CH3:SA CH4:SB CH5:SC CH6:SD CH7:S1 CH8:S2 CH9:FL1 CH10:FL2`

---

## Naming Conventions

- Schema files: `lowercase_underscore.schema.json`
- Pattern files: `lowercase_underscore.json`
- Python files: `lowercase_underscore.py`
- Use `ROLE_` prefix for all abstract channel assignments (e.g. `ROLE_DRIVE_MODE`, `ROLE_TRANS_BRAKE`)
- Commit messages: `type: short description` (e.g. `fix: correct semver in model.py`, `feat: add drift pattern`)
- No redundant folder names in filenames. If a file lives in `/drag/`, don't name it `drag_logic.json` — just `logic.json`. Keep filenames as short as possible.

---

## Vehicle Taxonomy

- Vehicle type = **platform** (Monster Truck, SCT, Buggy, Truggy, Touring Car, Crawler, Boat, etc.)
- Driving style = **secondary selector** (Bash, Race, Crawl, Drift)
- **Basher is a driving style, not a vehicle type.** Do not use it as a top-level category.
- This list is not complete. Racing classes (oval, 1/8 buggy, etc.) are planned for addition pre- or post-release.

---

## Design Tokens

UI colors are locked for the initial GUI skin. See `docs/design-tokens.css`. Do not introduce new colors without approval.

> Note: A Winamp-style skinnable/configurable GUI system is being explored pending EdgeTX dev team input. Tokens may evolve into a full theming system.

---

## AI Team Roles

| AI | Role |
|----|------|
| Claude | Architecture lead, code generation, documentation |
| Grok | Verification, bug checking, conformance review, graphic design |
| Gemini | Research |
| Kevin (WickedFog) | Vision, direction, final approval on everything |

No layer gets locked without Kevin's sign-off. No design decision is final until Kevin approves it.

---

## Known Open Issues

1. `model.py` — `expoData` outputs empty `[]`
2. `model.py` — `inputNames` outputs empty `{}`
3. `model.py` — semver shows `2.11.4`, should be `2.11.3`
4. `drag_race_template.py` — needs full redesign
5. Vehicle taxonomy — needs correction throughout codebase

---

## Questions

Open an issue or contact @WickedFog.
