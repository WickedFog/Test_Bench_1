"""
roosTx/templates/drag_race.py
------------------------------
Drag Racing template for RoosTx.
Recreates Drag_Race.yml programmatically to validate the engine.

ROLE_ MAP (resolved at generation time via radio_map):
  ROLE_DRIVE_MODE     - 3-pos switch: controls flight mode staging
  ROLE_LAUNCH_ARM     - 2-pos switch: master arm (safe=up, armed=down)
"""

from model import EdgeTXModel


# Default radio map for Radiomaster MT12
MT12_DRAG_RADIO_MAP = {
    "ROLE_DRIVE_MODE": "SA",     # 3-pos: up=Launch, mid=Stage, down=WarmUp
    "ROLE_LAUNCH_ARM": "SD",     # 2-pos: up=Disarmed/safe, down=Armed
}


def build(name="Drag Race", reg_id="MT12", radio_map=None):
    if radio_map is None:
        radio_map = MT12_DRAG_RADIO_MAP

    m = EdgeTXModel(name)
    if reg_id:
        m.set_registration_id(reg_id)

    # SA must be UP (Launch) on load
    m.set_switch_warning(radio_map["ROLE_DRIVE_MODE"], "up")

    # Flight Modes
    drive_mode = radio_map["ROLE_DRIVE_MODE"]
    m.add_flight_mode(0, "Launch")
    m.add_flight_mode(1, "Stage", f"{drive_mode}1")
    m.add_flight_mode(2, "WarmUp", f"{drive_mode}2")

    # Inputs
    m.add_input(0, "ST", name="Str")
    m.add_input(1, "TH", name="Thr")

    # Basic mixes
    m.add_mix(dest_ch=0, src_raw="I0", weight=100, name="Steering")
    m.add_mix(dest_ch=1, src_raw="I1", weight=100, name="Throttle")

    # Launch sequence mixes
    m.add_mix(dest_ch=1, src_raw="MAX", weight=25,
              switch="L2", mltpx="REPL", flight_modes="000000000", name="Stage Pulse")
    m.add_mix(dest_ch=1, src_raw="MAX", weight=75,
              switch="L3", mltpx="REPL", flight_modes="011111111", name="Prep Pulse")
    m.add_mix(dest_ch=1, src_raw="MAX", weight=70,
              switch="L3", mltpx="REPL", flight_modes="101111111", name="WarmUp Cap")
    m.add_mix(dest_ch=1, src_raw="MAX", weight=15,
              switch="L3", mltpx="REPL", flight_modes="110111111", name="Stage Cap")

    # Logical Switches
    launch_arm = radio_map["ROLE_LAUNCH_ARM"]
    m.add_logical_switch(0, "FUNC_VPOS", "I1,5", and_switch="SC2")  # L1: staged detect
    m.add_logical_switch(1, "FUNC_STICKY", "L1,NONE", delay=0, duration=10, and_switch="L1")  # L2: first pulse
    m.add_logical_switch(2, "FUNC_STICKY", "L1,NONE", delay=10, duration=10, and_switch="L1")  # L3: second pulse
    m.add_logical_switch(3, "FUNC_STICKY", f"{launch_arm}2,{launch_arm}2")  # L4: arm sticky

    # Custom Functions
    m.add_custom_fn(0, "!L4", "OVERRIDE_CHANNEL", "1,0,1")  # throttle kill
    m.add_custom_fn(1, "!L4", "RGB_LED", "red,1,On")
    m.add_custom_fn(2, "L4", "RGB_LED", "green,1,On")

    m.set_throttle_trace("TH")
    return m


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    model = build()
    model.describe()
    model.save("output/Drag_Race_RoosTx.yml")
    print("Done. Import output/Drag_Race_RoosTx.yml into Companion to verify.")