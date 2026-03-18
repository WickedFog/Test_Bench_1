# RoosTx Drag Race — Full Specification
**Version:** 1.1 DRAFT
**Author:** Kevin Rowe (WickedFog)
**Session:** 11
**Status:** DRAFT — pending Kevin review and approval before any code is written

---

## Overview

A drag racing model for the Radiomaster MT12 using EdgeTX 2.11.4.
Three drive modes controlled by SA. SC is the transbrake in Race mode
and a throttle limiter toggle in Stage mode. Sub-second timing requires
Lua — EdgeTX native resolution is 0.1 seconds minimum.

**Language note:** RoosTx uses surface RC terminology throughout.
"Steering Wheel" and "Throttle Trigger" — never "sticks."

---

## Hardware Assignment

| Channel | Control | Role |
|---------|---------|------|
| CH1 | Steering Wheel | Steering |
| CH2 | Throttle Trigger | Throttle |
| CH3 | SA (3-way) | Drive Mode selector |
| CH4 | SB (momentary) | Unassigned |
| CH5 | SC (momentary) | Transbrake (Race) / Throttle limiter toggle (Stage) |
| CH6 | SD (2-pos) | MASTER THROTTLE BLOCK — RESERVED, never assign |
| CH7 | S1 | Throttle Curve 1 level (Stage) |
| CH8 | S2 | Throttle Curve 2 level (Stage) |

---

## Master Safety — SD Throttle Block

SD is the hardware master safety switch. SD UP = throttle blocked regardless
of drive mode. SD DOWN = throttle armed and available.

Because SD already provides a hard throttle block at all times, the SA
startup switch warning is NOT required. The SD block is always enforced
first. Driver must consciously move SD to armed position before any
throttle is available.

---

## Drive Modes

### DM0 — Race Mode (SA↑)
- Default on power-up.
- SD must be DOWN (armed) for any throttle to be available.
- SC held = transbrake engaged, throttle locked at zero.
- SC released = launch sequence begins.

**Launch sequence (requires Lua for sub-0.1s timing):**
1. Driver holds SC (transbrake) and pulls full Throttle Trigger.
2. Light turns green — driver releases SC.
3. Delay box fires (0.00-0.50s adjustable, set before run).
4. Stage 1 ramp: throttle ramps to **50% (default)** over **0.5 seconds (default)**.
5. Stage 2 ramp: throttle ramps to **75% (default)** over **0.3 seconds (default)**.
6. Stage 3: straight ramp to **100%** — not adjustable.

**Delay box (Lua):**
- Adjustable 0.00 to 0.50 seconds in 0.01 second steps.
- Controlled via MT12 trim switches.
- Displayed on screen for setting purposes — driver sets it before the run,
  not during. Nobody is watching a screen during a 2-second pass.

---

### DM1 — Stage Mode (SA-)
- Used to creep the car up to the staging beams.
- Two independent throttle curves controlled by S1 and S2 knobs.
- **Throttle Curve 1 (S1):** Base throttle cap. Default 50%. Range 0-100%.
- **Throttle Curve 2 (S2):** Secondary cap as a percentage OF Curve 1. Default 50%. Range 0-100%.
- SC released = Curve 1 active.
- SC held = Curve 2 active (drops throttle further for fine creep).

**Examples:**
- Curve 1 = 100%, Curve 2 = 100% → full throttle both ways.
- Curve 1 = 100%, Curve 2 = 50% → 100% normal, drops to 50% with SC held.
- Curve 1 = 50%, Curve 2 = 10% → 50% normal, drops to 5% with SC held.

**Use case:** Driver can set Curve 2 to near zero and creep into the beams
with SC pulses (creep-brake-creep). Most drivers place car by hand but
this feature is in v1.

---

### DM2 — Burnout Mode (SA↓)
- Throttle limited to **80% default**. Adjustable.
- SC held + full Throttle Trigger = burnout sequence begins.

**Burnout sequence:**
1. SC held, Throttle Trigger pulled full.
2. **2 second arm delay** — must hold for 2 seconds to confirm intentional.
3. Throttle armed at set % (default 80%) for **7 seconds (default)**.
4. Throttle **disabled for 10 seconds** — cool-down lockout.
5. Throttle limit removed — returns to 80% cap.

**Note:** All burnout timings are user-adjustable defaults.
Timer resolution is 0.1 seconds (EdgeTX LS native limit).

---

## LED Behavior

| State | LED Color |
|-------|-----------|
| SD up — master block active | Red |
| SD down — armed / launch active | Green |

---

## Global Variables (GV) — planned

| GV | Purpose |
|----|---------|
| GV1 | Burnout throttle cap % |
| GV2 | Stage Throttle Curve 1 % |
| GV3 | Stage Throttle Curve 2 % |
| GV4 | Burnout arm delay (seconds) |
| GV5 | Burnout run time (seconds) |
| GV6 | Burnout lockout time (seconds) |

---

## Lua Requirements

The following features require Lua scripts:

- Delay box (0.00-0.50s in 0.01s steps, trim-adjustable, screen display for setting)
- Stage 1 ramp timing (default 0.5s)
- Stage 2 ramp timing (default 0.3s)

---

## Future Features (not in v1)

- Parachute deployment channel
- Line lock
- Telemetry: drive pack voltage (RxBt), run timer, reaction time display
- Launch light tree display on screen

---

## Terminology (locked for RoosTx)

| RoosTx term | Never use |
|-------------|-----------|
| Steering Wheel | Steering stick |
| Throttle Trigger | Throttle stick |
| Drive Mode (DM) | Flight Mode (FM) |

---

## Notes

- semver target: 2.11.4
- SC role changes depending on active DM — this is intentional
- SD is permanently reserved as master throttle block
- Burnout timers: 0.1s resolution (EdgeTX native)
- Race ramp timers: 0.01s resolution (Lua required)
- All defaults are user-adjustable in the wizard

---

*This document must be reviewed and approved by Kevin before any YAML
or Python code is written. Do not proceed to implementation until Kevin
gives the green light.*
