# RoosTx — Grok Verification Brief
**Branch:** master
**Requested by:** WickedFog (Kevin Rowe)
**Claude Session:** 9

---

## Your Role

You are the verification lead for the RoosTx project. Your job is to audit the repo for bugs, schema conformance, hardware constraint violations, and logical errors. You are NOT here to redesign anything. Layers 1-3 are LOCKED. Flag issues, don't fix them without approval.

---

## Priority 1 — Known Bugs in model.py

These bugs have been identified but not yet fixed. Confirm each one and provide the exact fix:

1. `expoData` outputs empty `[]` — should contain expo values
2. `inputNames` outputs empty `{}` — should contain named input mappings
3. `semver` outputs `2.11.4` — correct value is `2.11.3`
4. `SC2` and `SD2` are referenced in the code — these switches **do not exist** on the MT12 hardware. Identify every instance and flag for removal.

---

## Priority 2 — Hardware Constraint Audit

Review all files in `roostx_core/`, `research_database/`, and `schemas/` for any violation of these hard MT12 constraints:

**Channel map:**
`CH1:ST CH2:TH CH3:SA CH4:SB CH5:SC CH6:SD CH7:S1 CH8:S2 CH9:FL1 CH10:FL2`

**Switch constraints:**
- `SB`, `SC`, `SD` are MOMENTARY — they have no "2" position
- `SC2`, `SD2`, `SB2` do not exist — flag every reference
- `CH6/SD` is the factory throttle lockout standard — flag any assignment of it without justification

**Verify this specific question:**
Does the EdgeTX throttle lockout on SD/CH6 activate on button UP or button DOWN? This is needed to understand safety logic timing — SD is NOT being considered for transbrake assignment. The wizard will suggest SC as the default transbrake button but allow the user to select any available switch.

---

## Priority 3 — Schema Conformance (Layers 1-3)

Audit all files in `schemas/` and `research_database/` against these locked rules:

- All component files must use `ROLE_` abstraction for channel assignments
- No hardcoded channel numbers in component logic
- Pattern files must reference components by role, not by channel
- Filenames must be `lowercase_underscore` — no spaces, no camelCase
- No redundant folder names in filenames (e.g. a file in `/drag/` should not be named `drag_logic.json`)

Report every violation with file path and line number where possible.

---

## Priority 4 — GV Field Verification

The drag race template uses GV (Global Variable) fields for the following:
- GV1: burnout throttle cap
- GV2: staging throttle cap
- GV3: stage 1 power
- GV4: stage 2 power
- GV5: stage 3 power
- GV6: ramp time

**Verify:**
1. Is storing a GV value in the `delay` field of a special function the correct EdgeTX 2.11.x method?
2. Is there a GV ramp/rate limitation in EdgeTX 2.11.x that would affect the drag race template?
3. What is the correct telemetry field name for the MT12 drive pack battery voltage?

---

## Priority 5 — Vehicle Taxonomy Audit

The current codebase incorrectly uses "Basher" as a vehicle type in some places.

**Rule:** Vehicle type = platform (Monster Truck, SCT, Buggy, Truggy, Touring Car, Crawler, Boat, etc.). Driving style = secondary selector (Bash, Race, Crawl, Drift).

Identify every file where "Basher" or "basher" appears as a vehicle type and flag for correction.

---

## Deliverable Format

Please return your findings as a structured report with:
- Section per priority
- File path + line number for each issue
- Severity: BLOCKER / WARNING / NOTE
- Recommended fix where applicable

---

## Reference Documents

- `CONTRIBUTING.md` — full project rules and constraints
- `docs/RoosTx_System_Design_v1.1.docx` (or PDF in docs folder) — full architecture
- `MT12_SWITCH_DESIGN.md` — switch layout reference
