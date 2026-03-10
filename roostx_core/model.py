"""
roosTx/model.py  v0.5  —  Companion-compatible YAML output
"""

import yaml
import copy
import re
from pathlib import Path


# ── Custom Dumper — fixes list indentation to match Companion format ──────────

class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow=flow, indentless=False)


# ── Custom Dumper for bare scalars and flightModes ───────────────────────────

_BARE_RE = re.compile(r'^(?:[01]{9}|OFF|ON|GLOBAL|WARN_OFF|WARN_ON|JOYSTICK|JOYSTICK_EXT|none)$')

class CompanionDumper(yaml.SafeDumper):
    def represent_scalar(self, tag, value, style=None):
        if isinstance(value, str):
            if _BARE_RE.match(value):
                return self.represent_scalar('tag:yaml.org,2002:str', value, style='')
            if value.isdigit() and len(value) <= 4:
                return self.represent_scalar('tag:yaml.org,2002:str', value, style='')
        return super().represent_scalar(tag, value, style)


# Force no quotes on 9-bit flightModes masks
def no_quote_flight_modes(dumper, data):
    if isinstance(data, str) and len(data) == 9 and all(c in '01' for c in data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')
CompanionDumper.add_representer(str, no_quote_flight_modes)


# ── Default model skeleton ────────────────────────────────────────────────────

DEFAULT_MODEL = {
    "semver": "2.11.4",
    "header": {"name": "New Model", "bitmap": "", "labels": ""},
    "noGlobalFunctions": 0, "thrTrim": 0, "trimInc": 0, "displayTrims": 0,
    "ignoreSensorIds": 0, "showInstanceIds": 0, "disableThrottleWarning": 0,
    "enableCustomThrottleWarning": 0, "customThrottleWarningPosition": 0,
    "beepANACenter": 0, "extendedLimits": 0, "extendedTrims": 0,
    "throttleReversed": 0, "checklistInteractive": 0,
    "flightModeData": {}, "mixData": [], "expoData": [],
    "inputNames": {}, "logicalSw": {}, "customFn": {},
    "thrTraceSrc": "TH", "switchWarning": {},
    "thrTrimSw": 0, "potsWarnMode": "WARN_OFF", "potsWarnEnabled": 0,
    "jitterFilter": "GLOBAL", "displayChecklist": 0, "telemetryProtocol": 0,
    "varioData": {"source": "none", "centerSilent": 0, "centerMax": 0,
                  "centerMin": 0, "min": 0, "max": 0},
    "rssiSource": "none",
    "rfAlarms": {"warning": 45, "critical": 42},
    "disableTelemetryWarning": 0,
    "trainerData": {"mode": "OFF", "channelsStart": 0, "channelsCount": -8,
                    "frameLength": 0, "delay": 0, "pulsePol": 0},
    "modelRegistrationID": "",
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
    "modelTelemetryDisabled": "GLOBAL",
}


class EdgeTXModel:
    def __init__(self, name="New Model"):
        self._data = copy.deepcopy(DEFAULT_MODEL)
        self._data["header"]["name"] = name
        self._radio_map = {}  # populated later if needed

    def set_registration_id(self, reg_id):
        self._data["modelRegistrationID"] = reg_id

    def set_switch_warning(self, sw, pos):
        self._data["switchWarning"][sw] = {"pos": pos}

    def add_flight_mode(self, idx, name, switch=""):
        fm = make_flight_mode(name, switch)
        self._data["flightModeData"][str(idx)] = fm

    def add_input(self, idx, src, name=""):
        # Simplified — add to expoData if needed
        pass  # implement if needed for full expo

    def set_input_name(self, idx, name):
        self._data["inputNames"][str(idx)] = name

    def add_mix(self, dest_ch, src_raw, weight=100, switch="NONE", mltpx="ADD",
                flight_modes="000000000", name="", **kwargs):
        mix = {
            "destCh": dest_ch,
            "srcRaw": src_raw,
            "weight": weight,
            "swtch": switch,
            "curve": {"type": 0, "value": 0},
            "delayPrec": 0, "delayUp": 0, "delayDown": 0,
            "speedPrec": 0, "speedUp": 0, "speedDown": 0,
            "carryTrim": 0,
            "mltpx": mltpx,
            "mixWarn": 0,
            "flightModes": flight_modes,
            "offset": 0,
            "name": name,
        }
        mix.update(kwargs)
        self._data["mixData"].append(mix)

    def add_logical_switch(self, idx, func, def1, and_switch="", delay=0, duration=0):
        ls = {
            "func": func,
            "def": def1,
        }
        if and_switch:
            ls["andsw"] = and_switch
        if delay:
            ls["delay"] = delay
        if duration:
            ls["duration"] = duration
        self._data["logicalSw"][str(idx)] = ls

    def add_custom_fn(self, idx, swtch, func, def_str):
        cf = {
            "swtch": swtch,
            "func": func,
            "def": def_str,
        }
        self._data["customFn"][str(idx)] = cf

    def set_throttle_trace(self, src):
        self._data["thrTraceSrc"] = src

    def save(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(
                self._data,
                f,
                Dumper=IndentDumper,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                indent=2,
                width=1000
            )
        print(f"Saved: {path}")

    def describe(self):
        d = self._data
        print(f"{'='*55}")
        print(f"  RoosTx Model: {d['header']['name']} (semver {d['semver']})")
        print(f"{'='*55}")

        fm = d.get("flightModeData", {})
        print(f"\n  Flight Mode ({len(fm)}):")
        for idx, mode in fm.items():
            print(f"    [{idx}] {mode['name']:15s}  switch={mode.get('swtch','DEFAULT')}")

        print(f"\n  Inputs ({len(d.get('expoData',[]))}):")
        for inp in d.get("expoData", []):
            print(f"    CH{inp['chn']+1} <- {inp['srcRaw']:6s}  weight={inp['weight']}%")

        print(f"\n  Mixes ({len(d.get('mixData',[]))}):")
        for m in d.get("mixData", []):
            lbl = f"  ({m['name']})" if m.get("name") else ""
            print(f"    CH{m['destCh']+1} <- {m['srcRaw']:6s} "
                  f"weight={m['weight']:4d}%  sw={m['swtch']:8s}  "
                  f"mltpx={m['mltpx']}{lbl}")

        ls = d.get("logicalSw", {})
        if ls:
            print(f"\n  Logical Switches ({len(ls)}):")
            for idx, sw in ls.items():
                print(f"    L{int(idx)+1}  {sw['func']:22s}  def={sw['def']}")

        cf = d.get("customFn", {})
        if cf:
            print(f"\n  Custom Functions ({len(cf)}):")
            for idx, fn in cf.items():
                print(f"    SF{int(idx)+1}  sw={fn['swtch']:8s}  {fn['func']:25s}  {fn['def']}")

        sw_warn = d.get("switchWarning", {})
        if sw_warn:
            print(f"\n  Switch Warnings:")
            for sw, val in sw_warn.items():
                print(f"    {sw} must be: {val['pos']}")
        print()


# ── Helper factories ──────────────────────────────────────────────────────────

def make_flight_mode(name, switch="", fade_in=0, fade_out=0):
    """Always put swtch BEFORE name — matches Companion field order."""
    fm = {"fadeIn": fade_in, "fadeOut": fade_out}
    if switch and switch != "NONE":
        fm["swtch"] = switch
    fm["name"] = name
    return fm