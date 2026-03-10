"""
roosTx/templates/crawler.py  —  Rock Crawler MVP template
==========================================================

FEATURES:
  Standard Throttle/Steering, selectable 4WS, Winch with safety lockout, Creep mode

ROLE_ MAP (resolved at generation time via radio_map):
  ROLE_DRIVE_MODE     - 3-pos: Normal / Crawl / Creep
  ROLE_4WS_REAR       - 3-pos: Off / Rear-Same / Crab
  ROLE_4WS_FRONT      - 2-pos: Off / Front 4WS active
  ROLE_WINCH_ARM      - 2-pos: Disarmed (safe=up) / Armed
  ROLE_WINCH_DIR      - 3-pos: Out / Hold / In

CHANNEL MAP:
  CH1 - Front Steering
  CH2 - Throttle / ESC
  CH3 - Rear Steering (4WS)
  CH4 - Winch motor

LOGICAL SWITCHES:
  L1 - Rear 4WS active  (ROLE_4WS_REAR not up)
  L2 - Front 4WS active (ROLE_4WS_FRONT down)
  L3 - Crab mode        (ROLE_4WS_REAR full down)
  L4 - Winch armed      (ROLE_WINCH_ARM down)
  L5 - Winch safety OK  (winch armed + throttle at zero)
  L6 - Creep mode       (ROLE_DRIVE_MODE down)
"""

from model import EdgeTXModel


# Default radio map for Radiomaster MT12
# Keys are ROLE_ names, values are physical switch assignments on the radio.
# Swap this dict out to support a different radio without touching any logic below.
MT12_CRAWLER_RADIO_MAP = {
    "ROLE_DRIVE_MODE":  "SA",    # 3-pos: up=Normal, mid=Crawl, down=Creep
    "ROLE_4WS_REAR":    "SB",    # 3-pos: up=Off, mid=Rear-Same, down=Crab
    "ROLE_4WS_FRONT":   "SC",    # 2-pos: up=Off, down=Front 4WS active
    "ROLE_WINCH_ARM":   "SD",    # 2-pos: up=Disarmed SAFE, down=Armed
    "ROLE_WINCH_DIR":   "SE",    # 3-pos: up=Out, mid=Hold, down=In
}


def build(name="Rock Crawler", reg_id="", options=None, radio_map=None):
    """
    Build and return a Rock Crawler EdgeTXModel.

    options dict:
        four_wheel_steering : bool (default True)
        winch               : bool (default True)
        creep_mode          : bool (default True)
        reverse_steering    : bool (default False)

    radio_map: dict of ROLE_ → physical switch assignments.
               Defaults to MT12_CRAWLER_RADIO_MAP if not provided.
    """
    if options is None:
        options = {}
    if radio_map is None:
        radio_map = MT12_CRAWLER_RADIO_MAP

    four_ws = options.get("four_wheel_steering", True)
    winch   = options.get("winch", True)
    creep   = options.get("creep_mode", True)
    rev_st  = options.get("reverse_steering", False)

    # Resolve physical switches from ROLE_ map
    drive_mode  = radio_map["ROLE_DRIVE_MODE"]   # e.g. "SA"
    rear_4ws    = radio_map["ROLE_4WS_REAR"]     # e.g. "SB"
    front_4ws   = radio_map["ROLE_4WS_FRONT"]    # e.g. "SC"
    winch_arm   = radio_map["ROLE_WINCH_ARM"]    # e.g. "SD"
    winch_dir   = radio_map["ROLE_WINCH_DIR"]    # e.g. "SE"

    m = EdgeTXModel(name)
    if reg_id:
        m.set_registration_id(reg_id)

    # Switch warnings - require safe positions on model load
    m.set_switch_warning(drive_mode, "up")   # Drive = Normal
    m.set_switch_warning(winch_arm,  "up")   # Winch = Disarmed

    # Flight Modes — driven by ROLE_DRIVE_MODE positions
    m.add_flight_mode(0, "Normal")
    m.add_flight_mode(1, "Crawl", f"{drive_mode}1")   # mid position
    m.add_flight_mode(2, "Creep", f"{drive_mode}2")   # down position

    # Inputs
    st_weight = -100 if rev_st else 100
    m.add_input(0, "ST", weight=st_weight)
    m.add_input(1, "TH", weight=100)
    m.set_input_name(0, "Str")
    m.set_input_name(1, "Thr")

    if four_ws:
        m.add_input(2, "ST", weight=100)
        m.set_input_name(2, "4WS")

    # CH1: Front Steering - pass-through (optionally reversed)
    m.add_mix(dest_ch=0, src_raw="I0", weight=st_weight,
              switch="NONE", mltpx="ADD",
              flight_modes="000000000", name="Front Str")

    # CH2: Throttle - Normal full pass-through
    m.add_mix(dest_ch=1, src_raw="I1", weight=100,
              switch="NONE", mltpx="ADD",
              flight_modes="000000000", name="Normal")

    if creep:
        # Crawl FM: throttle capped at 60%
        m.add_mix(dest_ch=1, src_raw="I1", weight=60,
                  switch="NONE", mltpx="REPL",
                  flight_modes="101111111", name="Crawl")
        # Creep FM: throttle capped at 25% for technical precision
        m.add_mix(dest_ch=1, src_raw="I1", weight=25,
                  switch="NONE", mltpx="REPL",
                  flight_modes="110111111", name="Creep")

    if winch:
        # Winch safety: override throttle output to 0 when winch not safe
        m.add_mix(dest_ch=1, src_raw="MAX", weight=0,
                  switch="!L5", mltpx="REPL",
                  flight_modes="000000000", name="WinchSafe")

    if four_ws:
        # CH3: Rear Same-direction (tightens turning circle)
        m.add_mix(dest_ch=2, src_raw="I0", weight=100,
                  switch="L1", mltpx="ADD",
                  flight_modes="000000000", name="Rear Same")

        # CH3: Crab mode (rear opposite = full sideways)
        m.add_mix(dest_ch=2, src_raw="I0", weight=-100,
                  switch="L3", mltpx="REPL",
                  flight_modes="000000000", name="Crab")

        # CH3: Front+Rear (both axles steer, max angle)
        m.add_mix(dest_ch=2, src_raw="I0", weight=100,
                  switch="L2", mltpx="ADD",
                  flight_modes="000000000", name="Front+Rear")

    if winch:
        # CH4: Winch Out (ROLE_WINCH_DIR up, L4 armed)
        m.add_mix(dest_ch=3, src_raw="MAX", weight=100,
                  switch="L4", mltpx="ADD",
                  flight_modes="000000000", name="Winch Out")

        # CH4: Winch In (ROLE_WINCH_DIR down, L4 armed)
        m.add_mix(dest_ch=3, src_raw="MAX", weight=-100,
                  switch="L4", mltpx="ADD",
                  flight_modes="000000000", name="Winch In")

        # CH4: Winch Idle
        m.add_mix(dest_ch=3, src_raw="MAX", weight=0,
                  switch="NONE", mltpx="ADD",
                  flight_modes="000000000", name="Winch Idle")

    # Logical Switches — all physical switch refs resolved from ROLE_ map
    ls_idx = 0
    if four_ws:
        m.add_logical_switch(ls_idx, "FUNC_VNEG", f"{rear_4ws},0")   # L1: Rear 4WS active
        ls_idx += 1
        m.add_logical_switch(ls_idx, "FUNC_VPOS", f"{front_4ws},1")  # L2: Front 4WS active
        ls_idx += 1
        m.add_logical_switch(ls_idx, "FUNC_VPOS", f"{rear_4ws},1")   # L3: Crab mode
        ls_idx += 1
    if winch:
        m.add_logical_switch(ls_idx, "FUNC_VPOS", f"{winch_arm},1")  # L4: Winch armed
        ls_idx += 1
        m.add_logical_switch(ls_idx, "FUNC_AND",
                             f"L{ls_idx},THR_ZERO")                   # L5: Winch safety OK
        ls_idx += 1
    if creep:
        m.add_logical_switch(ls_idx, "FUNC_VPOS", f"{drive_mode},2") # L6: Creep FM active
        ls_idx += 1

    m.set_throttle_trace("TH")
    return m


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)

    full = build("Rock Crawler Full",
                 options={"four_wheel_steering": True, "winch": True, "creep_mode": True})
    full.describe()
    full.save("output/Rock_Crawler_Full.yml")

    basic = build("Rock Crawler Basic",
                  options={"four_wheel_steering": False, "winch": False, "creep_mode": True})
    basic.save("output/Rock_Crawler_Basic.yml")

    print("Done. Import from output/ into EdgeTX Companion.")
