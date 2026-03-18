# model.py
# RoosTx EdgeTX model builder
# Session 12 — add_input implemented, all known bugs resolved

import copy

SEMVER = "2.11.4"

# ── HARDWARE NOTES ───────────────────────────────────────────────────────────
# MT12 channel map (LOCKED):
#   CH1=ST  CH2=TH  CH3=SA  CH4=SB  CH5=SC  CH6=SD(RESERVED)
#   CH7=S1  CH8=S2  CH9=FL1  CH10=FL2
#
# SC2 / SD2 / SB2 DO NOT EXIST — SB, SC, SD are momentary (pos1 only)
# CH6/SD is the factory safety lockout — never assign it
#
# flightModes bitmask in mixes:
#   leftmost char = FM0, rightmost = FM8
#   0 = active in this FM, 1 = disabled in this FM
#   "000000000" = active in all FMs
#   "011111111" = FM0 only
#   "101111111" = FM1 only
#   "110111111" = FM2 only
#
# LS delay/duration are stored in tenths of a second
#   delay=10 = 1.0s,  delay=1 = 0.1s
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_MODEL = {
    "semver": SEMVER,
    "header": {
        "name": "",
        "bitmap": "",
        "labels": ""
    },
    "noGlobalFunctions": 0,
    "thrTrim": 0,
    "trimInc": 0,
    "displayTrims": 0,
    "ignoreSensorIds": 0,
    "showInstanceIds": 0,
    "disableThrottleWarning": 0,
    "enableCustomThrottleWarning": 0,
    "customThrottleWarningPosition": 0,
    "beepANACenter": 0,
    "extendedLimits": 0,
    "extendedTrims": 0,
    "throttleReversed": 0,
    "checklistInteractive": 0,
    "flightModeData": {},
    "mixData": [],
    "expoData": [],
    "inputNames": {},
    "curves": [],
    "logicalSw": {},
    "customFn": [],
    "thrTraceSrc": "TH",
    "switchWarning": {},
    "thrTrimSw": 0,
    "potsWarnMode": "WARN_OFF",
    "potsWarnEnabled": 0,
    "jitterFilter": "GLOBAL",
    "displayChecklist": 0,
    "telemetryProtocol": 0,
    "varioData": {
        "source": "none",
        "centerSilent": 0,
        "centerMax": 0,
        "centerMin": 0,
        "min": 0,
        "max": 0
    },
    "rssiSource": "none",
    "rfAlarms": {
        "warning": 45,
        "critical": 42
    },
    "disableTelemetryWarning": 0,
    "trainerData": {
        "mode": "OFF",
        "channelsStart": 0,
        "channelsCount": -8,
        "frameLength": 0,
        "delay": 0,
        "pulsePol": 0
    },
    "modelRegistrationID": "MT12",
    "hatsMode": "GLOBAL",
    "usbJoystickExtMode": 0,
    "usbJoystickIfMode": "JOYSTICK",
    "usbJoystickCircularCut": 0,
    "radioGFDisabled": "GLOBAL",
    "radioTrainerDisabled": "GLOBAL",
    "modelHeliDisabled": "GLOBAL",
    "modelFMDisabled": "GLOBAL",
    "modelCurvesDisabled": "GLOBAL",
    "modelGVDisabled": "GLOBAL",
    "modelLSDisabled": "GLOBAL",
    "modelSFDisabled": "GLOBAL",
    "modelCustomScriptsDisabled": "GLOBAL",
    "modelTelemetryDisabled": "GLOBAL"
}


class EdgeTXModel:

    def __init__(self, name=""):
        self._model = copy.deepcopy(DEFAULT_MODEL)
        self._model["header"]["name"] = name

    # ── DRIVE MODES ──────────────────────────────────────────────────────────
    def add_flight_mode(self, index, name, swtch=None, fadeIn=0, fadeOut=0):
        """
        Add a Drive Mode (EdgeTX flight mode).
        FM0 = Race    (SA up, default, no switch)
        FM1 = Stage   (SA1 = SA mid)
        FM2 = Burnout (SA2 = SA down)
        """
        fm = {"name": name, "fadeIn": fadeIn, "fadeOut": fadeOut}
        if swtch:
            fm["swtch"] = swtch
        self._model["flightModeData"][index] = fm

    # ── INPUTS ───────────────────────────────────────────────────────────────
    def add_input(self, index, src, name, chn, weight=100, mode=3,
                  offset=0, curve_type=1, curve_value=0,
                  flightModes="000000000", trim_source=0):
        """
        Populate expoData entry and inputNames entry.
        Previously a no-op (pass). Now fully implemented.

        src:        "ST" or "TH"
        name:       display name for inputNames ("St", "TH")
        chn:        channel index (0=ST, 1=TH)
        weight:     100 = full, no scaling
        mode:       3 = both directions
        curve_type: 1 = custom (type 1, value 0 = no expo applied)
        """
        self._model["expoData"].append({
            "srcRaw": src,
            "scale": 0,
            "mode": mode,
            "chn": chn,
            "swtch": "NONE",
            "flightModes": flightModes,
            "weight": weight,
            "offset": offset,
            "curve": {
                "type": curve_type,
                "value": curve_value
            },
            "trimSource": trim_source,
            "name": ""
        })
        self._model["inputNames"][index] = {"val": name}

    # ── MIXES ────────────────────────────────────────────────────────────────
    def add_mix(self, destCh, srcRaw, weight=100, swtch="NONE",
                curve_type=0, curve_value=0,
                delayUp=0, delayDown=0,
                speedUp=0, speedDown=0,
                carryTrim=0, mltpx="ADD",
                mixWarn=0, flightModes="000000000",
                offset=0, name=""):
        """
        Add a mix line.

        flightModes bitmask (9 chars):
          leftmost = FM0, rightmost = FM8
          0 = mix active in this FM
          1 = mix disabled in this FM
          "000000000" = active in all FMs (default)
          "011111111" = FM0 only
          "101111111" = FM1 only
          "110111111" = FM2 only

        speedUp/speedDown: tenths of a second (10 = 1.0s ramp)
        mltpx: "ADD" for base mixes, "REPL" for override mixes
        """
        self._model["mixData"].append({
            "destCh": destCh,
            "srcRaw": srcRaw,
            "weight": weight,
            "swtch": swtch,
            "curve": {"type": curve_type, "value": curve_value},
            "delayPrec": 0,
            "delayUp": delayUp,
            "delayDown": delayDown,
            "speedPrec": 0,
            "speedUp": speedUp,
            "speedDown": speedDown,
            "carryTrim": carryTrim,
            "mltpx": mltpx,
            "mixWarn": mixWarn,
            "flightModes": flightModes,
            "offset": offset,
            "name": name
        })

    # ── LOGICAL SWITCHES ─────────────────────────────────────────────────────
    def add_logical_switch(self, index, func, v1, v2,
                           andsw="NONE", delay=0, duration=0):
        """
        Add a logical switch.

        delay/duration: tenths of a second (10 = 1.0s, 1 = 0.1s)

        FUNC_VPOS:   v1=source, v2=threshold (e.g. I1, 5 = throttle > 0.5%)
        FUNC_STICKY: v1=set_trigger, v2=clear_trigger
          - andsw on FUNC_STICKY is a HARD GATE
          - if gate goes false while latched, output drops immediately

        NEVER use SC2/SD2/SB2 — use SC1/SD1/SB1 (momentary = pos1 only)
        GVs cannot be used in delay/duration fields (uint8_t integers only)
        """
        self._model["logicalSw"][index] = {
            "func": func,
            "def": f"{v1},{v2}",
            "delay": delay,
            "duration": duration,
            "andsw": andsw,
            "lsPersist": 0,
            "lsState": 0
        }

    # ── CUSTOM FUNCTIONS ─────────────────────────────────────────────────────
    def add_custom_fn(self, swtch, func, defn):
        """
        Add a custom function.

        OVERRIDE_CHANNEL defn format: "channel_index,value,enable"
          channel_index: 0-indexed (0=CH1, 1=CH2)
          value:         -1024 to 1024  (0 = zero output / kill)
          enable:        1 = active
          Example: "1,0,1" = kill CH2 (throttle)

        RGB_LED defn format: "color,led_index,state"
          Example: "red,1,On" / "green,1,On"
        """
        self._model["customFn"].append({
            "swtch": swtch,
            "func": func,
            "def": defn
        })

    # ── CURVES ───────────────────────────────────────────────────────────────
    def add_curve(self, index, name, points):
        """
        Add a point-based curve.
        Straight line placeholder: [-100, -50, 0, 50, 100]
        Point values: -100 to 100.
        To reference in a mix: curve_type=1, curve_value=<this index>

        TODO: Kevin dials in actual sine curves after radio testing.
        """
        while len(self._model["curves"]) <= index:
            self._model["curves"].append(None)
        self._model["curves"][index] = {
            "name": name,
            "type": 0,
            "smooth": 0,
            "points": points
        }

    # ── MISC ─────────────────────────────────────────────────────────────────
    def set_switch_warning(self, switch, pos):
        self._model["switchWarning"][switch] = {"pos": pos}

    def set_thr_trace(self, src):
        self._model["thrTraceSrc"] = src

    def build(self):
        return copy.deepcopy(self._model)
