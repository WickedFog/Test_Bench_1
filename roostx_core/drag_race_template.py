# drag_race_template.py
# RoosTx — Drag Race Template
# Rebuilt Session 12 — All Grok audit issues resolved
# Session 13 — Arrow character bug fixed, plain ASCII notation enforced
#
# GROK FIXES APPLIED:
#   Bug 3:  SC2 -> SC (SC2 does not exist; momentary has no positions)
#   Bug 4:  SD2 -> SA2/SA0 (SD2 does not exist; L4 redesigned)
#   Bug 5:  FM names Race/Stage/Burnout, SA0/SA1/SA2 mapping corrected
#   Bug 6:  4 placeholder curves defined (Burnout/Stg1/Stg2/Stg3)
#   Bug 7:  add_input() now populates expoData and inputNames (fixed in model.py)
#   Bug 9:  CustomFn throttle kill trigger chain corrected
#   Bug 10: FM channel map CH1=ST CH2=TH enforced; all swtch refs valid
#
# SESSION 13 FIX:
#   SC_DOWN / SC_UP unicode arrow variables REMOVED entirely.
#   All switch references use plain ASCII only.
#   SC = pressed/held (momentary active state)
#   !SC = released (momentary inactive state)
#   No arrow characters anywhere in this file.
#
# DRIVE MODE MAP (LOCKED):
#   FM0 = Race    (SA up  / SA0) -- default, car is running
#   FM1 = Stage   (SA mid / SA1) -- staging lane, 25% power cap
#   FM2 = Burnout (SA down/ SA2) -- burnout box, ramps to 75%
#
# LOGICAL SWITCH CHAIN:
#   L1 -- Throttle > 0.5% AND transbrake held (SC pressed)
#   L2 -- Stage capture: fires when L1 fires, holds 1.0s, gate=L1
#   L3 -- Confirmed stage: same as L2 but 1.0s delay before firing
#   L4 -- Master arm: set=SA2 (enter Burnout), clear=SA0 (return to Race)
#        !L4 = throttle kill + red LED
#         L4 = launch active + green LED
#
# SAFETY:
#   - CH6/SD is NEVER assigned
#   - !L4 override kills CH2 (throttle) at all times when disarmed
#   - SA must be up (Race) on power-on to clear switch warning
#
# Run command:
#   python drag_race_template.py
#   cp output/Drag_Race_RoosTx.yml ../models/Drag_Race_v4.yml

import sys
import os
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import EdgeTXModel


def build():
    m = EdgeTXModel(name="Drag Race")

    # -- DRIVE MODES ----------------------------------------------------------
    # FM0 = Race    (SA up)   -- default, no switch required
    # FM1 = Stage   (SA mid)  -- staging lane
    # FM2 = Burnout (SA down) -- burnout box / launch prep
    m.add_flight_mode(0, name="Race",    swtch=None)
    m.add_flight_mode(1, name="Stage",   swtch="SA1")
    m.add_flight_mode(2, name="Burnout", swtch="SA2")

    # -- INPUTS ---------------------------------------------------------------
    # Input 0 -- Steering Wheel (ST -> CH1)
    # Input 1 -- Throttle Trigger (TH -> CH2)
    m.add_input(0, src="ST", name="St", chn=0, weight=100, mode=3)
    m.add_input(1, src="TH", name="TH", chn=1, weight=100, mode=3)

    # -- CURVES ---------------------------------------------------------------
    # Straight line placeholders -- Kevin dials in curves after radio test
    m.add_curve(0, name="Burnout", points=[-100, -50, 0, 50, 100])
    m.add_curve(1, name="Stg1",    points=[-100, -50, 0, 50, 100])
    m.add_curve(2, name="Stg2",    points=[-100, -50, 0, 50, 100])
    m.add_curve(3, name="Stg3",    points=[-100, -50, 0, 50, 100])

    # -- MIXES ----------------------------------------------------------------
    # CH1 -- Steering Wheel passthrough, always active
    m.add_mix(destCh=0, srcRaw="I0", weight=100)

    # CH2 -- Throttle Trigger base, always active
    m.add_mix(destCh=1, srcRaw="I1", weight=100)

    # CH2 -- Stage power (25%, 1.0s ramp up)
    #   Active: L2 fired AND in FM1 (Stage mode / SA mid) only
    #   flightModes "101111111" = FM1 active, FM0+FM2 disabled
    m.add_mix(
        destCh=1, srcRaw="MAX", weight=25,
        swtch="L2", mltpx="REPL",
        speedUp=10, speedDown=0, carryTrim=0,
        flightModes="101111111",
        name=""
    )

    # CH2 -- Burnout power (75%, 1.0s ramp up)
    #   Active: L3 fired AND in FM2 (Burnout mode / SA down) only
    #   flightModes "110111111" = FM2 active, FM0+FM1 disabled
    m.add_mix(
        destCh=1, srcRaw="MAX", weight=75,
        swtch="L3", mltpx="REPL",
        speedUp=10, speedDown=0, carryTrim=0,
        flightModes="110111111",
        name=""
    )

    # -- LOGICAL SWITCHES -----------------------------------------------------

    # L1 -- Throttle trigger with transbrake held
    #   FUNC_VPOS: Throttle input (I1) > 5 (~0.5% of -1024 to 1024 range)
    #   andsw="SC" = transbrake held (SC pressed, plain ASCII, no arrows)
    m.add_logical_switch(
        index=0,
        func="FUNC_VPOS",
        v1="I1", v2="5",
        andsw="SC",
        delay=0, duration=0
    )

    # L2 -- Stage capture sticky
    #   Set=L1, Clear=NONE, gate=L1, holds 1.0s
    m.add_logical_switch(
        index=1,
        func="FUNC_STICKY",
        v1="L1", v2="NONE",
        andsw="L1",
        delay=0, duration=10
    )

    # L3 -- Confirmed stage sticky
    #   Same as L2 but 1.0s delay before firing
    m.add_logical_switch(
        index=2,
        func="FUNC_STICKY",
        v1="L1", v2="NONE",
        andsw="L1",
        delay=10, duration=10
    )

    # L4 -- Master arm
    #   Set=SA2 (enter Burnout mode), Clear=SA0 (return to Race)
    #   No gate -- latches until explicitly cleared
    m.add_logical_switch(
        index=3,
        func="FUNC_STICKY",
        v1="SA2", v2="SA0",
        andsw="NONE",
        delay=0, duration=0
    )

    # -- CUSTOM FUNCTIONS -----------------------------------------------------
    # CF0 -- Master throttle block: kill CH2 when disarmed (!L4)
    m.add_custom_fn(swtch="!L4", func="OVERRIDE_CHANNEL", defn="1,0,1")
    # CF1 -- Red LED: system disarmed
    m.add_custom_fn(swtch="!L4", func="RGB_LED", defn="red,1,On")
    # CF2 -- Green LED: system armed / launch active
    m.add_custom_fn(swtch="L4",  func="RGB_LED", defn="green,1,On")

    # -- MISC -----------------------------------------------------------------
    m.set_switch_warning("SA", "up")
    m.set_thr_trace("TH")

    return m.build()


if __name__ == "__main__":
    model_data = build()

    os.makedirs("output", exist_ok=True)
    out_path = "output/Drag_Race_RoosTx.yml"

    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(
            model_data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )

    print(f"[OK] Generated: {out_path}")
