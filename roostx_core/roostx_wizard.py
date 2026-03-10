"""
roosTx_wizard.py  —  RoosTx EdgeTX Model Wizard v0.2
=====================================================
Run: python roosTx_wizard.py
Requires: pip install pyyaml
"""

import os, sys


# ── Radio Maps ────────────────────────────────────────────────────────────────
# Each entry maps ROLE_ names to the physical switches on that radio.
# Adding a new radio = adding one dict here. Nothing else changes.

RADIO_MAPS = {
    "Radiomaster MT12": {
        "ROLE_DRIVE_MODE":  "SA",
        "ROLE_LAUNCH_ARM":  "SD",
        "ROLE_4WS_REAR":    "SB",
        "ROLE_4WS_FRONT":   "SC",
        "ROLE_WINCH_ARM":   "SD",
        "ROLE_WINCH_DIR":   "SE",
    },
    # Future radios go here — same ROLE_ keys, different switch letters
    # "Radiomaster MT12S": { ... },
    # "Jumper T15": { ... },
}

SUPPORTED_RADIOS = list(RADIO_MAPS.keys())


# ── UI Helpers ────────────────────────────────────────────────────────────────

def header():
    print("""
+======================================================+
|         R O O S T x   W I Z A R D  v0.2             |
|    EdgeTX Model Generator for Surface RC             |
+======================================================+
""")


def ask(prompt, options):
    print(f"\n  {prompt}")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")
    while True:
        c = input("\n  Enter number: ").strip()
        if c.isdigit() and 1 <= int(c) <= len(options):
            return options[int(c) - 1]
        print("  Invalid, try again.")


def ask_yn(prompt):
    while True:
        a = input(f"\n  {prompt} (y/n): ").strip().lower()
        if a in ("y", "yes"):   return True
        if a in ("n", "no"):    return False
        print("  Enter y or n.")


def ask_str(prompt, default):
    v = input(f"\n  {prompt} [{default}]: ").strip()
    return v if v else default


# ── Main Wizard ───────────────────────────────────────────────────────────────

def run():
    header()

    # Radio selection — drives the entire switch map
    radio = ask("Select your radio:", SUPPORTED_RADIOS)
    radio_map = RADIO_MAPS[radio]
    print(f"\n  Radio: {radio}")
    print(f"  Switch map loaded. {len(radio_map)} roles resolved.")

    vehicle = ask("Select vehicle type:", [
        "Rock Crawler",
        "Drag Racer",
        "Basher",
        "Drifter",
        "Boat",
    ])

    print(f"\n  Building: {vehicle}")
    model_name = ask_str("Model name", vehicle)
    options = {}

    if vehicle == "Rock Crawler":
        print("\n  -- Feature Selection --")
        options["four_wheel_steering"] = ask_yn(
            "Include 4WS? (rear, crab, front+rear modes)")
        if options["four_wheel_steering"]:
            print("\n  [WHY] 4WS lets you tighten your turn radius (rear-same),")
            print("  slide sideways onto a ledge (crab), or steer both axles")
            print("  for max angle. Three Logical Switches handle mode selection.")

        options["winch"] = ask_yn("Include Winch with safety lockout?")
        if options["winch"]:
            print("\n  [WHY] The winch safety prevents you from driving and")
            print("  winching at the same time — it overrides throttle to zero")
            print("  whenever the winch is armed. Logical Switch L5 enforces this.")

        options["creep_mode"] = ask_yn("Include Creep/Crawl throttle reduction modes?")
        if options["creep_mode"]:
            print("\n  [WHY] Crawl FM caps throttle at 60%, Creep FM at 25%.")
            print("  Built as Flight Mode mix overrides, not curves, so your")
            print("  stick input stays linear — only the output is scaled.")

        options["reverse_steering"] = ask_yn("Reverse steering direction?")

    elif vehicle == "Drag Racer":
        print("\n  [WHY] Drag uses Sticky Logical Switches for launch control.")
        print("  L1 detects staging. L2/L3 create timed power pulses.")
        print("  L4 arms launch. LED = red until armed, green = go.")

    reg_id = ask_str("Radio registration ID (blank to skip)", "")
    out_dir = ask_str("Output folder", "output")
    os.makedirs(out_dir, exist_ok=True)

    safe = model_name.replace(" ", "_")
    out_path = os.path.join(out_dir, f"{safe}.yml")

    print(f"\n  Building {model_name}...")

    try:
        from model import EdgeTXModel

        if vehicle == "Rock Crawler":
            from crawler_template import build
        elif vehicle == "Drag Racer":
            from drag_race_template import build
        else:
            print(f"\n  [!] {vehicle} template not yet available. Building base model.")
            m = EdgeTXModel(model_name)
            m.add_flight_mode(0, "Normal")
            m.add_input(0, "ST"); m.add_input(1, "TH")
            m.set_input_name(0, "Str"); m.set_input_name(1, "Thr")
            m.add_mix(dest_ch=0, src_raw="I0", weight=100)
            m.add_mix(dest_ch=1, src_raw="I1", weight=100)
            m.save(out_path)
            finish(out_path); return

        # radio_map passed here — this is what connects ROLE_ to physical switches
        model = build(name=model_name, reg_id=reg_id, radio_map=radio_map)

    except ImportError as e:
        print(f"\n  [ERROR] {e}")
        print("  Ensure model.py and template files are in the same folder.")
        sys.exit(1)

    model.describe()
    model.save(out_path)
    finish(out_path)


def finish(path):
    print(f"""
  +======================================================+
  |  Saved: {path:<44s}|
  |                                                      |
  |  Next steps:                                         |
  |  1. Open EdgeTX Companion                            |
  |  2. File > Import Model                              |
  |  3. Select the .yml file above                       |
  |  4. Radio Simulator to test-drive before powering on |
  +======================================================+
""")


if __name__ == "__main__":
    run()
