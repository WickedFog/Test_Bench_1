# RoosTx — MT12 Switch Design Reference
**Status: LOCKED | Architecture Lead: Claude | Approved by: Kevin**

---

## MT12 Hardware — Physical Controls

| Channel | Control | Type | Notes |
|---------|---------|------|-------|
| CH1 | ST | Steering wheel | Primary steering input |
| CH2 | TH | Trigger | Primary throttle input |
| CH3 | SA | 3-way toggle | Up / Mid / Down positions |
| CH4 | SB | Momentary button | No position 2 — hold/release only |
| CH5 | SC | Momentary button | No position 2 — hold/release only |
| CH6 | SD | Momentary button | No position 2 — hold/release only |
| CH7 | S1 | Knob | Continuous analog |
| CH8 | S2 | Knob | Continuous analog |
| CH9 | FL1 | 2-way toggle | On / Off |
| CH10 | FL2 | 2-way toggle | On / Off |

> **CRITICAL:** SB, SC, and SD are MOMENTARY. They have no "position 2."
> Using SC2 or SD2 in any logic is WRONG. These switches do not have that state.

---

## MT12 Swappable Switch Bay

The MT12 has a swappable switch bay at the base of the radio. Options:
- 2x 2-way switches
- 1x 2-way + 1x 3-way combo
- 2x 3-way switches
- Joystick (potential gimbal cam control)
- GPS sensor module

This means SA is not the only available 3-way input. Any bay config can
provide a 3-way switch for ROLE_DRIVE_MODE.

---

## The ROLE_ System — Why It Exists

Kevin's exact words (Session 1):

> *"There is really no reason to go into this using particular inputs for a feature,
> as you can program about anything with this radio. The research into the inputs
> was more meant to find out the common uses for the inputs for the defaults more
> than anything."*

This is the law. No hardcoded switch names anywhere in logic. Ever.
Physical switch names appear in ONE place only: the radio map dict at the top
of each template/component file.

The user picks what they want to DO. The app figures out which button does it.
Change the radio = change one dict. Nothing else moves.

---

## MT12 Default ROLE Assignments

```python
MT12_DRAG_RADIO_MAP = {
    "ROLE_DRIVE_MODE":      "SA",   # 3-way: Burnout / Staging / Race
    "ROLE_TRANS_BRAKE":     "SC",   # momentary: hold=staged, release=launch
    "ROLE_THROTTLE_SAFETY": "SD",   # RESERVED — factory default, never reassign
    "ROLE_STAGE_SELECT":    "SB",   # momentary: cycle active stage for S1/S2
    "ROLE_THROTTLE_CAP":    "S1",   # knob: power level (contextual per mode)
    "ROLE_RAMP_ADJUST":     "S2",   # knob: ramp time (contextual per mode)
    "ROLE_DELAY_BOX":       "FL1",  # 2-way toggle: delay box enable
}
```

---

## SD — RESERVED (Throttle Safety)

SD is the MT12 factory hardware-level throttle safety switch. It operates at
the radio firmware level. The engine must never assign anything to SD.

It belongs in `mt12.json` as `ROLE_THROTTLE_SAFETY: SD` and is treated as
reserved in all templates.

---

## SC — Trans Brake (ROLE_TRANS_BRAKE)

SC is the trans brake button. Momentary only — hold = throttle locked at zero,
release = launch sequence begins.

SC is the most ergonomic thumb position for a hold-and-release action on the MT12.

Kevin confirmed (Session 1):
> *"The SC button is a momentary switch. Not a two way toggle."*

---

## SA — Drive Mode Selector (ROLE_DRIVE_MODE)

SA is the 3-way toggle. Default mode assignments:

| SA Position | Mode | Flight Mode |
|-------------|------|-------------|
| Up | Burnout | FM0 |
| Mid | Staging | FM1 |
| Down | Race / Launch | FM2 |

Kevin confirmed SA Up=Burnout, Mid=Staging, Down=Race.

---

## S1 / S2 — Contextual Per Flight Mode

Same physical knobs do different things depending on which mode is active.

| Control | Burnout | Staging | Race |
|---------|---------|---------|------|
| S1 | Throttle cap (rev limiter) | Staging throttle cap (5–30%) | Stage 1/2/3 power level |
| S2 | Burnout timer duration | Staging ramp rate | Stage 1/2/3 timing |

In Race mode, SB cycles which stage S1/S2 are currently affecting.

---

## SB — Stage Selector (ROLE_STAGE_SELECT)

In Race mode: momentary press cycles active stage target for S1 and S2.
Radio screen shows which stage is currently being adjusted.

In other modes: TBD / available for other assignment.

---

## FL1 — Delay Box Enable (ROLE_DELAY_BOX)

2-way toggle. Only active in Race mode. Enables the delay box function.
Trim switch controls delay time in ~1ms increments.
Lua script enforces 1ms resolution.

---

## Global Variables — Drag Race

| GV | Purpose |
|----|---------|
| GV1 | Burnout max throttle cap |
| GV2 | Staging max throttle cap |
| GV3 | Stage 1 power level |
| GV4 | Stage 1 ramp time |
| GV5 | Stage 2 power level |
| GV6 | Stage 2 ramp time |

---

## LED State Reference

| Color | State |
|-------|-------|
| Red solid | Disarmed / not ready |
| Yellow | Trans brake held — staged and armed |
| Red flashing | Full throttle against trans brake (wrong) |
| Green | Launch sequence active |

---

## Key Design Decisions (Locked)

1. **ROLE_ abstraction is the law** — no hardcoded switch names in logic
2. **SD is permanently reserved** — factory throttle safety, never assign
3. **SC is trans brake** — momentary hold/release is correct for this function
4. **SA is drive mode** — 3-way gives Burnout / Staging / Race
5. **S1/S2 are contextual** — same knobs do different things per mode
6. **Switches are defaults, not requirements** — any control can be remapped
7. **Momentary switches have no position 2** — SC2/SD2/SB2 do not exist on MT12

---

*RoosTx — Architecture Lead: Claude | Verified: Grok | Break Room: ChatGPT*
