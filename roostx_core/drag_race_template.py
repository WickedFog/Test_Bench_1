"""
roostx_core/drag_race_template.py
----------------------------------
RoosTx Drag Race template — full rebuild.
Based on approved spec: docs/Drag_Race_Spec_v1.md
Approved by Kevin Rowe (WickedFog) — Session 11

DRIVE MODES (SA):
  DM0 (SA up)  = Race    -- default on power-up, full throttle available
  DM1 (SA mid) = Stage   -- creep to staging beams, dual throttle curves
  DM2 (SA dn)  = Burnout -- burnout prep, timed sequence via SC

MASTER SAFETY:
  SD up  = throttle BLOCKED (always enforced via customFn OVERRIDE)
  SD dn  = throttle ARMED / available
  No SA startup warning required -- SD block handles safety at all times.

SC ROLES (changes per DM -- intentional design):
  DM0 Race:    SC held = transbrake (throttle locked at 0), release = launch
  DM1 Stage:   SC held = Throttle Curve 2 (fine creep), release = Curve 1
  DM2 Burnout: SC held + Throttle Trigger > threshold = burnout sequence

BURNOUT SEQUENCE (pure EdgeTX, 0.1s resolution):
  1. SC held + throttle > 80% triggers L1
  2. L1 must hold 2.0s to arm L2 (prevents accidental trigger)
  3. L2 arms -- burnout active at 80% cap -- runs for 7.0s (L3)
  4. L3 clears -- L4 fires after 7.0s delay -- lockout active for 10.0s
  5. L4 lockout clears -- returns to 80% cap

RACE LAUNCH (Lua required for sub-0.1s timing -- STUBBED in this template):
  SC release triggers ramp stages:
  Stage 1: ramp to 50% over 0.5s (default)
  Stage 2: ramp to 75% over 0.3s (default)
  Stage 3: straight ramp to 100%
  Delay box: 0.00-0.50s in 0.01s steps, trim-adjustable

TERMINOLOGY (locked for RoosTx -- never use aircraft terms):
  Steering Wheel (not stick)
  Throttle Trigger (not stick)
  Drive Mode / DM (not Flight Mode / FM)

LOGICAL SWITCH MAP:
  L1 = Burnout trigger    (throttle > threshold AND SC held, DM2)
  L2 = Burnout arm latch  (STICKY, 2.0s arm delay)
  L3 = Burnout run timer  (STICKY, 7.0s duration)
  L4 = Burnout lockout    (STICKY, 7.0s delay then 10.0s lockout)

NOTE ON TIMING VALUES:
  EdgeTX logical switch delay/duration fields store values in tenths of
  a second (0.1s resolution). So delay=20 = 2.0s, duration=70 = 7.0s.
  Verify against radio if behavior is unexpected.
"""

from model import EdgeTXModel


# ── Radio map ────────────────────────────────────────────────────────────────
MT12_DRAG_RADIO_MAP = {
    "ROLE_DRIVE_MODE":  "SA",   # 3-pos: SA up=Race DM0, SA mid=Stage DM1, SA dn=Burnout DM2
    "ROLE_TRANS_BRAKE": "SC",   # momentary: hold=transbrake(Race)/Curve2(Stage)/burnout trigger(Burnout)
    "ROLE_MASTER_SAFE": "SD",   # 2-pos RESERVED: SD up=blocked, SD dn=armed -- NEVER REASSIGN
    "ROLE_CURVE1_KNOB": "S1",   # pot: Stage Throttle Curve 1 level knob
    "ROLE_CURVE2_KNOB": "S2",   # pot: Stage Throttle Curve 2 level knob
}

# ── Burnout sequence timing defaults (values in tenths of seconds) ────────────
# 0.1s resolution -- EdgeTX logical switch native limit
BURNOUT = {
    "cap":            80,    # % max throttle cap in burnout mode
    "trigger_pct":    80,    # throttle % threshold to trigger sequence
    "arm_delay":      20,    # 2.0s -- must hold SC + throttle to confirm intentional
    "run_duration":   70,    # 7.0s -- burnout active window
    "lockout_delay":  70,    # 7.0s -- delay before lockout fires (matches run_duration)
    "lockout_dur":   100,    # 10.0s -- cool-down lockout window
}

# ── Stage mode throttle defaults (%) ─────────────────────────────────────────
STAGE = {
    "curve1_cap":  50,   # Curve 1 cap (SC released) -- S1 knob overrides in wizard
    "curve2_cap":  25,   # Curve 2 cap (SC held) -- percentage of Curve 1 effectively
}


def build(name="Drag Race", reg_id="MT12", radio_map=None):
    if radio_map is None:
        radio_map = MT12_DRAG_RADIO_MAP

    m = EdgeTXModel(name)
    m._data["semver"] = "2.11.4"
    if reg_id:
        m.set_registration_id(reg_id)

    dm = radio_map["ROLE_DRIVE_MODE"]   # SA
    tb = radio_map["ROLE_TRANS_BRAKE"]  # SC
    ms = radio_map["ROLE_MASTER_SAFE"]  # SD

    # ── Drive Modes ───────────────────────────────────────────────────────────
    # DM0 = Race (SA up) -- default, no switch condition
    # DM1 = Stage (SA mid)
    # DM2 = Burnout (SA dn)
    # SD master block enforces safety -- no SA startup warning needed
    m.add_flight_mode(0, "Race")
    m.add_flight_mode(1, "Stage",   f"{dm}1")
    m.add_flight_mode(2, "Burnout", f"{dm}2")

    # SD must be UP (safe/blocked) on startup
    m.set_switch_warning(ms, "up")

    # ── Inputs ────────────────────────────────────────────────────────────────
    m.add_input(0, "ST", name="Whl",  weight=100, offset=0, curve_type=1, curve_value=0)   # Steering Wheel - straight ramp
    m.add_input(1, "TH", name="Trig", weight=100, offset=0, curve_type=1, curve_value=0)  # Throttle Trigger - straight ramp

    # ── Mixes ─────────────────────────────────────────────────────────────────
    # flightModes bitmask: 9 digits, position 0=DM0 / 1=DM1 / 2=DM2 / rest=unused
    # 0 = mix IS active in that DM, 1 = mix is NOT active
    # Active DM0 only: 011111111
    # Active DM1 only: 101111111
    # Active DM2 only: 110111111
    # Active all DMs:  000000000

    # CH1: Steering Wheel -- straight pass-through all drive modes
    m.add_mix(dest_ch=0, src_raw="I0", weight=100,
              flight_modes="000000000", name="Steering Wheel")

    # CH2: Throttle Trigger -- base pass-through (overridden by mode logic below)
    m.add_mix(dest_ch=1, src_raw="I1", weight=100,
              flight_modes="000000000", name="Throttle Trigger")

    # DM0 Race: SC held = transbrake -- replace throttle with 0 while SC pressed
    m.add_mix(dest_ch=1, src_raw="MAX", weight=0,
              switch=f"{tb}1", mltpx="REPL",
              flight_modes="011111111", name="Transbrake")

    # DM1 Stage: SC released = Throttle Curve 1 cap (S1 knob -- default 50%)
    m.add_mix(dest_ch=1, src_raw="MAX", weight=STAGE["curve1_cap"],
              switch=f"!{tb}1", mltpx="REPL",
              flight_modes="101111111", name="Stage Curve 1")

    # DM1 Stage: SC held = Throttle Curve 2 cap (S2 knob -- default 25%)
    # Fine creep for staging beam approach -- creep/brake/creep with SC pulses
    m.add_mix(dest_ch=1, src_raw="MAX", weight=STAGE["curve2_cap"],
              switch=f"{tb}1", mltpx="REPL",
              flight_modes="101111111", name="Stage Curve 2")

    # DM2 Burnout: base throttle cap (80% default)
    # Overridden to 0 by L4 lockout customFn when cool-down is active
    m.add_mix(dest_ch=1, src_raw="MAX", weight=BURNOUT["cap"],
              mltpx="REPL",
              flight_modes="110111111", name="Burnout Cap")

    # ── Logical Switches ──────────────────────────────────────────────────────
    # BURNOUT SEQUENCE (L1-L4):
    #   L1: Trigger  -- throttle > threshold AND SC held
    #   L2: Arm      -- STICKY, 2.0s hold required before arming
    #   L3: Run      -- STICKY, active for 7.0s (burnout window)
    #   L4: Lockout  -- STICKY, fires 7.0s after arm, active 10.0s (cool-down)

    # L1: Burnout trigger -- throttle above threshold AND SC held
    m.add_logical_switch(0, "FUNC_VPOS",
                         f"I1,{BURNOUT['trigger_pct']}",
                         and_switch=f"{tb}1")

    # L2: Arm latch -- sticky, sets on L1, requires 2.0s continuous hold
    m.add_logical_switch(1, "FUNC_STICKY", "L1,NONE",
                         delay=BURNOUT["arm_delay"],
                         duration=0,
                         and_switch="L1")

    # L3: Burnout run timer -- sticky, active for 7.0s then self-clears
    m.add_logical_switch(2, "FUNC_STICKY", "L2,NONE",
                         delay=0,
                         duration=BURNOUT["run_duration"],
                         and_switch="L2")

    # L4: Lockout -- sticky, fires 7.0s after L2 arms, active for 10.0s cool-down
    # Delay matches run_duration so lockout starts exactly when burnout ends
    m.add_logical_switch(3, "FUNC_STICKY", "L2,NONE",
                         delay=BURNOUT["lockout_delay"],
                         duration=BURNOUT["lockout_dur"],
                         and_switch="NONE")

    # ── Custom Functions ───────────────────────────────────────────────────────
    # Master safety block -- SD up = throttle forced to 0 at all times
    m.add_custom_fn(0, f"!{ms}1", "OVERRIDE_CHANNEL", "1,0,1")

    # Burnout lockout -- L4 active = throttle forced to 0 (cool-down)
    m.add_custom_fn(1, "L4", "OVERRIDE_CHANNEL", "1,0,1")

    # LED: Red = SD up (blocked/disarmed)
    m.add_custom_fn(2, f"!{ms}1", "RGB_LED", "red,1,On")

    # LED: Green = SD dn (armed)
    m.add_custom_fn(3, f"{ms}1", "RGB_LED", "green,1,On")

    # ── Curves (straight line placeholders -- Kevin to dial in sine curves) ──
    # 2-point curves: [y at x=-100, y at x=+100]
    # Throttle context: x=-100=no input, x=+100=full trigger
    m.add_curve(0, "Burnout",  [-100, 60,  80])   # starts 60%, ramps to 80%
    m.add_curve(1, "Stg1",    [-100,  0,  50])    # 0% to Stage 2 start (50%)
    m.add_curve(2, "Stg2",    [-100, 50,  75])    # 50% to Stage 3 start (75%)
    m.add_curve(3, "Stg3",    [-100, 75, 100])    # 75% to full

    # ── Throttle trace ─────────────────────────────────────────────────────────
    m.set_throttle_trace("TH")

    # ── Lua stubs (not yet implemented) ───────────────────────────────────────
    # TODO: delay_box.lua  -- 0.00-0.50s delay, 0.01s steps, trim-adjustable
    # TODO: launch_ramp.lua -- Stage 1: 50% over 0.5s, Stage 2: 75% over 0.3s, Stage 3: 100%

    return m


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    model = build()
    model.describe()
    model.save("output/Drag_Race_RoosTx.yml")
    print("Done. Import output/Drag_Race_RoosTx.yml into Companion to verify.")



