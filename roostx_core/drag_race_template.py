# drag_race_template.py
# RoosTx — Drag Race Template
# Rebuilt Session 12 — All Grok audit issues resolved
# Session 13A — Arrow character bug fixed, plain ASCII notation enforced
# Session 13B — Logic bugs fixed:
#   Fix 1: L1 andsw SC -> !SC (fire when transbrake RELEASED, not held)
#   Fix 2: L4 clear SA0 -> SB (SA0 is persistent level, clears L4 instantly on
#           return to Race; SB is momentary = deliberate disarm only)
#   Fix 3: OVERRIDE_CHANNEL removed, replaced with REPL mix on CH2
#           (OVERRIDE_CHANNEL enable=1 in def was holding CH2 dead permanently)
#
# DRIVE MODE MAP (LOCKED):
#   FM0 = Race    (SA up  / SA0) -- default, car is running
#   FM1 = Stage   (SA mid / SA1) -- staging lane, 25% power cap
#   FM2 = Burnout (SA down/ SA2) -- burnout box, ramps to 75%
#
# LOGICAL SWITCH CHAIN:
#   L1 -- Throttle > 0.5% AND transbrake RELEASED (!SC)
#          Gate drops L1 if SC is re-engaged mid-run
#   L2 -- Stage capture: fires when L1 fires, holds 1.0s, gate=L1
#   L3 -- Confirmed stage: same as L2 but 1.0s delay before firing
#   L4 -- Master arm: set=SA2 (enter Burnout), clear=SB (deliberate disarm)
#          Latches across SA positions — only SB press clears it
#         !L4 = throttle kill (REPL mix zeros CH2) + red LED
#          L4 = launch active + green LED
#
# SAFETY:
#   - CH6/SD is NEVER assigned
#   - !L4 REPL mix zeros CH2 at all times when disarmed
#   - SA must be up (Race) on power-on to clear switch warning
#   - Press SB to disarm / reset after a run
#
# Run command:
#   python drag_race_template.py

import sys
import os
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import EdgeTXModel


def build():
    m = EdgeTXModel(name="Drag Race")

    # -- DRIVE MODES ----------------------------------------------------------
    m.add_flight_mode(0, name="Race",    swtch=None)
    m.add_flight_mode(1, name="Stage",   swtch="SA1")
    m.add_flight_mode(2, name="Burnout", swtch="SA2")

    # -- INPUTS ---------------------------------------------------------------
    m.add_input(0, src="ST", name="St", chn=0, weight=100, mode=3)
    m.add_input(1, src="TH", name="TH", chn=1, weight=100, mode=3)

    # -- CURVES ---------------------------------------------------------------
    m.add_curve(0, name="Burnout", points=[-100, -50, 0, 50, 100])
    m.add_curve(1, name="Stg1",    points=[-100, -50, 0, 50, 100])
    m.add_curve(2, name="Stg2",    points=[-100, -50, 0, 50, 100])
    m.add_curve(3, name="Stg3",    points=[-100, -50, 0, 50, 100])

    # -- MIXES ----------------------------------------------------------------
    # CH1 -- Steering passthrough, always active
    m.add_mix(destCh=0, srcRaw="I0", weight=100)

    # CH2 -- KILL mix: zero throttle when L4 not armed
    #   REPL, always active in all FMs, swtch=!L4
    #   When !L4 is true (disarmed), this replaces all CH2 mixes with 0
    #   When L4 is true (armed), this mix is inactive, normal mixes take over
    m.add_mix(
        destCh=1, srcRaw="MAX", weight=0,
        swtch="!L4", mltpx="REPL",
        flightModes="000000000",
        name="Kill !L4"
    )

    # CH2 -- Throttle base, active in all FMs
    m.add_mix(destCh=1, srcRaw="I1", weight=100, name="TH base")

    # CH2 -- Stage power cap (25%, 1.0s ramp up)
    #   Active: L2 fired AND FM1 only
    m.add_mix(
        destCh=1, srcRaw="MAX", weight=25,
        swtch="L2", mltpx="REPL",
        speedUp=10, speedDown=0, carryTrim=0,
        flightModes="101111111",
        name="Stage cap"
    )

    # CH2 -- Burnout power (75%, 1.0s ramp up)
    #   Active: L3 fired AND FM2 only
    m.add_mix(
        destCh=1, srcRaw="MAX", weight=75,
        swtch="L3", mltpx="REPL",
        speedUp=10, speedDown=0, carryTrim=0,
        flightModes="110111111",
        name="Burnout cap"
    )

    # -- LOGICAL SWITCHES -----------------------------------------------------

    # L1 -- Throttle > 0.5% AND transbrake RELEASED
    #   andsw="!SC" = gate is open only when SC is NOT held
    #   Fires when trigger pulled after releasing transbrake button
    m.add_logical_switch(
        index=0,
        func="FUNC_VPOS",
        v1="I1", v2="5",
        andsw="!SC",
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
    #   1.0s delay before firing
    m.add_logical_switch(
        index=2,
        func="FUNC_STICKY",
        v1="L1", v2="NONE",
        andsw="L1",
        delay=10, duration=10
    )

    # L4 -- Master arm
    #   Set=SA2 (flip to Burnout mode to arm)
    #   Clear=SB (press SB to disarm — deliberate action only)
    #   No andsw gate — latches across all SA positions
    m.add_logical_switch(
        index=3,
        func="FUNC_STICKY",
        v1="SA2", v2="SB",
        andsw="NONE",
        delay=0, duration=0
    )

    # -- CUSTOM FUNCTIONS -----------------------------------------------------
    # CF0 -- Red LED: system disarmed
    m.add_custom_fn(swtch="!L4", func="RGB_LED", defn="red,1,On")
    # CF1 -- Green LED: system armed / launch active
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
