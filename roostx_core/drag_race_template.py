# drag_race_template.py
# RoosTx — Drag Race Template
# Rebuilt Session 12 — All Grok audit issues resolved
#
# GROK FIXES APPLIED:
#   Bug 3:  SC2 → SC1  (SC2 does not exist on MT12)
#   Bug 4:  SD2 → SA2/SA0 (SD2 does not exist; L4 redesigned)
#   Bug 5:  FM names Race/Stage/Burnout, SA0/SA1/SA2 mapping corrected
#   Bug 6:  4 placeholder curves defined (Burnout/Stg1/Stg2/Stg3)
#   Bug 7:  add_input() now populates expoData and inputNames (fixed in model.py)
#   Bug 9:  CustomFn throttle kill trigger chain corrected
#   Bug 10: FM channel map CH1=ST CH2=TH enforced; all swtch refs valid
#
# DRIVE MODE MAP (LOCKED):
#   FM0 = Race    (SA up  / SA0) — default, car is running
#   FM1 = Stage   (SA mid / SA1) — staging lane, 25% power cap
#   FM2 = Burnout (SA down/ SA2) — burnout box, ramps to 75%
#
# LOGICAL SWITCH CHAIN:
#   L1 — Throttle > 0.5% AND transbrake held (SC1)
#   L2 — Stage capture: fires when L1 fires, holds 1.0s, gate=L1
#   L3 — Confirmed stage: same as L2 but 1.0s delay before firing
#   L4 — Master arm: set=SA2 (enter Burnout), clear=SA0 (return to Race)
#        !L4 = throttle kill + red LED
#         L4 = launch active + green LED
#
# SAFETY:
#   - CH6/SD is NEVER assigned
#   - !L4 override kills CH2 (throttle) at all times when disarmed
#   - SA must be up (Race) on power-on to clear switch warning
#
# Run command:
#   C:/Users/WickedFog/AppData/Local/Programs/Python/Python312/python.exe drag_race_template.py
#   cp output/Drag_Race_RoosTx.yml ../models/Drag_Race_v4.yml

import sys
import os
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import EdgeTXModel


def build():
    m = EdgeTXModel(name="Drag Race")

    # ── DRIVE MODES ──────────────────────────────────────────────────────────
    # FM0 = Race    (SA up)   — default, no switch required
    # FM1 = Stage   (SA mid)  — staging lane
    # FM2 = Burnout (SA down) — burnout box / launch prep
    m.add_flight_mode(0, name="Race",    swtch=None)
    m.add_flight_mode(1, name="Stage",   swtch="SA1")
    m.add_flight_mode(2, name="Burnout", swtch="SA2")

    # ── INPUTS ───────────────────────────────────────────────────────────────
    # Input 0 — Steering Wheel (ST → CH1)
    # Input 1 — Throttle Trigger (TH → CH2)
    m.add_input(0, src="ST", name="St", chn=0, weight=100, mode=3)
    m.add_input(1, src="TH", name="TH", chn=1, weight=100, mode=3)

    # ── CURVES ───────────────────────────────────────────────────────────────
    # Straight line placeholders — Kevin dials in sine curves after radio test
    # To wire to a mix: curve_type=1, curve_value=<index below>
    #   Index 0 = Burnout   (CH2 override in FM2)
    #   Index 1 = Stg1      (placeholder)
    #   Index 2 = Stg2      (placeholder)
    #   Index 3 = Stg3      (placeholder)
    # TODO: replace points with tuned sine curves after on-radio verification
    m.add_curve(0, name="Burnout", points=[-100, -50, 0, 50, 100])
    m.add_curve(1, name="Stg1",    points=[-100, -50, 0, 50, 100])
    m.add_curve(2, name="Stg2",    points=[-100, -50, 0, 50, 100])
    m.add_curve(3, name="Stg3",    points=[-100, -50, 0, 50, 100])

    # ── MIXES ────────────────────────────────────────────────────────────────
    # CH1 — Steering Wheel passthrough, always active
    m.add_mix(destCh=0, srcRaw="I0", weight=100)

    # CH2 — Throttle Trigger base, always active
    m.add_mix(destCh=1, srcRaw="I1", weight=100)

    # CH2 — Stage power (25%, 1.0s ramp up)
    #   Active: L2 fired AND in FM1 (Stage mode / SA mid) only
    #   flightModes "101111111" = FM1 active, FM0+FM2 disabled
    #   Replaces base throttle with limited staging power
    #   speedUp=10 = 1.0s ramp (tenths of a second)
    #   Curves: wired after radio verification (curve_type=0 for now)
    m.add_mix(
        destCh=1, srcRaw="MAX", weight=25,
        swtch="L2", mltpx="REPL",
        speedUp=10, speedDown=0, carryTrim=0,
        flightModes="101111111",
        name=""
    )

    # CH2 — Burnout power (75%, 1.0s ramp up)
    #   Active: L3 fired AND in FM2 (Burnout mode / SA down) only
    #   flightModes "110111111" = FM2 active, FM0+FM1 disabled
    #   Replaces base throttle with burnout-level power
    m.add_mix(
        destCh=1, srcRaw="MAX", weight=75,
        swtch="L3", mltpx="REPL",
        speedUp=10, speedDown=0, carryTrim=0,
        flightModes="110111111",
        name=""
    )

    # ── LOGICAL SWITCHES ─────────────────────────────────────────────────────

    # L1 — Throttle trigger with transbrake held
    #   FUNC_VPOS: Throttle input (I1) > 5 (~0.5% of -1024 to 1024 range)
    #   andsw=SC1: only evaluates while transbrake (SC) is held
    #   SC2 DOES NOT EXIST — SC1 only (momentary switch)
    m.add_logical_switch(
        index=0,
        func="FUNC_VPOS",
        v1="I1", v2="5",
        andsw="SC1",
        delay=0, duration=0
    )

    # L2 — Stage capture sticky
    #   Set:      L1 rising edge (throttle + transbrake fires)
    #   Clear:    none (NONE = no explicit clear signal)
    #   Gate:     L1 (hard gate — if throttle or SC released, L2 drops immediately)
    #   Duration: 10 = 1.0s auto-hold
    #   Feeds: CH2 25% stage power mix
    m.add_logical_switch(
        index=1,
        func="FUNC_STICKY",
        v1="L1", v2="NONE",
        andsw="L1",
        delay=0, duration=10
    )

    # L3 — Confirmed stage sticky
    #   Same gate as L2 (L1 must stay active)
    #   Delay: 10 = 1.0s delay before firing (driver must hold 1.0s to confirm)
    #   Duration: 10 = 1.0s hold after firing
    #   Feeds: CH2 75% burnout power mix
    m.add_logical_switch(
        index=2,
        func="FUNC_STICKY",
        v1="L1", v2="NONE",
        andsw="L1",
        delay=10, duration=10
    )

    # L4 — Master arm
    #   Set:   SA2 (driver moves SA to down = enters Burnout mode = armed)
    #   Clear: SA0 (driver moves SA to up = returns to Race = disarmed)
    #   Gate:  NONE (holds state independently)
    #
    #   !L4 = system disarmed → throttle killed + red LED
    #    L4 = system armed    → throttle live + green LED
    #
    #   SD2 DOES NOT EXIST — original bug fixed
    #   SA2 and SA0 are valid 3-way switch positions
    m.add_logical_switch(
        index=3,
        func="FUNC_STICKY",
        v1="SA2", v2="SA0",
        andsw="NONE",
        delay=0, duration=0
    )

    # ── CUSTOM FUNCTIONS ─────────────────────────────────────────────────────

    # CF0 — Master throttle block
    #   When NOT armed (!L4): override CH2 to zero
    #   def "1,0,1" = channel_index=1(CH2), value=0(kill), enable=1
    #   This is a hardware-level override, bypasses mixer entirely
    m.add_custom_fn(swtch="!L4", func="OVERRIDE_CHANNEL", defn="1,0,1")

    # CF1 — Red LED: system disarmed
    m.add_custom_fn(swtch="!L4", func="RGB_LED", defn="red,1,On")

    # CF2 — Green LED: system armed / launch active
    m.add_custom_fn(swtch="L4",  func="RGB_LED", defn="green,1,On")

    # ── MISC ─────────────────────────────────────────────────────────────────
    # SA must be up (Race) on power-on — warns driver if not in safe state
    m.set_switch_warning("SA", "up")
    m.set_thr_trace("TH")

    return m.build()


if __name__ == "__main__":
    model_data = build()

    os.makedirs("output", exist_ok=True)
    out_path = "output/Drag_Race_RoosTx.yml"

    with open(out_path, "w") as f:
        yaml.dump(
            model_data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"[OK] Generated: {out_path}")
