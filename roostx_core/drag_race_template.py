# drag_race_template.py
# RoosTx — Drag Race model template
# Updated Session 15 — synced to Drag_Race_v4.yml (hardware-verified Session 14)
#
# NOTATION (locked — Sessions 13+14):
#   SD2,SD2   = SD self-toggle (arm/disarm)
#   SC2       = SC pressed/held (andsw gate)
#   !SC2      = SC released (andsw gate)
#   SB2       = SB pressed
#   I1        = Throttle input source
#   L1..L7    = Logical switch refs
#   gv(0)     = GV1 as mix srcRaw (Stage 1 %)
#   gv(1)     = GV2 as mix srcRaw (Stage 2 %)
#
# DRIVE MODES:
#   DM0 = Race    (SA up, default)
#   DM1 = Stage   (SA1, mid)
#   DM2 = Burnout (SA2, down)
#   DM3 = TH Adj  (L7 toggle via SB — trims decoupled)
#   DM4 = Ramp Adj (reserved, NONE switch)
#
# GV DEFAULTS (in DM0):
#   GV1 (gv(0)) = 50  — Stage 1 throttle %
#   GV2 (gv(1)) = 75  — Stage 2 throttle %
#
# GV MIN/MAX (top-level gvars):
#   GV1: min=1064 (1024+40=40%), max=964 (1024-60=60%)
#   GV2: min=1089 (1024+65=65%), max=939 (1024-85=85%)
#
# LS CHAIN:
#   L1 = FUNC_STICKY  SD2,SD2             Master arm toggle
#   L2 = FUNC_VPOS    I1>5  andsw:SC2     Throttle up while SC held
#   L3 = FUNC_STICKY  L2,SD2              Was-staged latch
#   L4 = FUNC_STICKY  L3,SD2 andsw:!SC2  Launch latch (fires on SC release, no spike)
#   L5 = FUNC_STICKY  L4,SD2 delay:5     Stage 2 — 0.5s after launch
#   L6 = FUNC_STICKY  L5,SD2 delay:3     Stage 3 — 0.3s after Stage 2
#   L7 = FUNC_STICKY  SB2,SB2            Race <-> TH Adj mode toggle
#
# MIX STACK ORDER (critical — order determines priority):
#   1. ST base    : I0,    ADD,  all DMs
#   2. TH base    : I1,    ADD,  all DMs
#   3. Stage1     : gv(0), REPL, swtch=L4, speedUp=5  (GV1 default 50%)
#   4. Stage2     : gv(1), REPL, swtch=L5, speedUp=3  (GV2 default 75%)
#   5. Stage3     : I1,    REPL, swtch=L6, speedUp=3
#   6. Transbrake : MAX 0%, REPL, swtch=SC2   <- AFTER stages
#   7. Kill       : MAX 0%, REPL, swtch=!L1   <- LAST
#
# SPECIAL FUNCTIONS:
#   SF0: OVERRIDE_CHANNEL — CH2 held at 0 when disarmed (!L1)
#   SF1: RGB_LED red   — disarmed
#   SF2: RGB_LED green — armed (L1)
#   SF3: RGB_LED yellow — TH Adj mode (L7)
#   SF4: ADJUST_GVAR GV1 +1 (TrimAilRight / T4+)
#   SF5: ADJUST_GVAR GV1 -1 (TrimAilLeft  / T4-)
#   SF6: ADJUST_GVAR GV2 +1 (TrimRudRight / ST trim+)
#   SF7: ADJUST_GVAR GV2 -1 (TrimRudLeft  / ST trim-)

import yaml
from model import CompanionDumper, _companion_fixup


def build():
    model = {
        'semver': '2.11.4',
        'header': {
            'name': 'Drag Race',
            'bitmap': '',
            'labels': ''
        },
        'noGlobalFunctions': 0,
        'thrTrim': 0,
        'trimInc': 0,
        'displayTrims': 0,
        'ignoreSensorIds': 0,
        'showInstanceIds': 0,
        'disableThrottleWarning': 1,
        'enableCustomThrottleWarning': 0,
        'customThrottleWarningPosition': 0,
        'beepANACenter': 0,
        'extendedLimits': 0,
        'extendedTrims': 0,
        'throttleReversed': 0,
        'checklistInteractive': 0,

        # -- Drive Modes -------------------------------------------------------
        # DM0 = Race (default, SA up) — GV defaults live here
        # DM3 = TH Adj: trims decoupled (mode:31) so T4/ST trim only adjust GVs
        'flightModeData': {
            0: {
                'name': 'Race',
                'fadeIn': 0,
                'fadeOut': 0,
                'gvars': {
                    0: {'val': 50},   # GV1 — Stage 1 throttle %
                    1: {'val': 75},   # GV2 — Stage 2 throttle %
                },
            },
            1: {'swtch': 'SA1', 'name': 'Stage',    'fadeIn': 0, 'fadeOut': 0},
            2: {'swtch': 'SA2', 'name': 'Burnout',  'fadeIn': 0, 'fadeOut': 0},
            3: {
                'trim': {
                    0: {'value': 0, 'mode': 31},  # ST trim decoupled
                    1: {'value': 0, 'mode': 31},  # TH trim decoupled
                },
                'swtch': 'L7',
                'name': 'TH Adj',
                'fadeIn': 0,
                'fadeOut': 0,
            },
            4: {'swtch': 'NONE', 'name': 'Ramp Adj', 'fadeIn': 0, 'fadeOut': 0},
        },

        # -- Mix Stack ---------------------------------------------------------
        # ORDER IS CRITICAL. Later REPL overrides earlier REPL.
        # Kill must be absolute last.
        'mixData': [
            # 1. Steering base
            {
                'destCh': 0, 'srcRaw': 'I0', 'weight': 100, 'swtch': 'NONE',
                'curve': {'type': 0, 'value': 0},
                'delayPrec': 0, 'delayUp': 0, 'delayDown': 0,
                'speedPrec': 0, 'speedUp': 0, 'speedDown': 0,
                'carryTrim': 0, 'mltpx': 'ADD', 'mixWarn': 0,
                'flightModes': '000000000', 'offset': 0, 'name': 'Steering'
            },
            # 2. Throttle base
            {
                'destCh': 1, 'srcRaw': 'I1', 'weight': 100, 'swtch': 'NONE',
                'curve': {'type': 0, 'value': 0},
                'delayPrec': 0, 'delayUp': 0, 'delayDown': 0,
                'speedPrec': 0, 'speedUp': 0, 'speedDown': 0,
                'carryTrim': 0, 'mltpx': 'ADD', 'mixWarn': 0,
                'flightModes': '000000000', 'offset': 0, 'name': 'TH base'
            },
            # 3. Stage 1 — GV1 (default 50%), L4 fires on SC release
            {
                'destCh': 1, 'srcRaw': 'gv(0)', 'weight': 100, 'swtch': 'L4',
                'curve': {'type': 0, 'value': 0},
                'delayPrec': 0, 'delayUp': 0, 'delayDown': 0,
                'speedPrec': 0, 'speedUp': 5, 'speedDown': 0,
                'carryTrim': 0, 'mltpx': 'REPL', 'mixWarn': 0,
                'flightModes': '000000000', 'offset': 0, 'name': 'Stage1 GV1'
            },
            # 4. Stage 2 — GV2 (default 75%), 0.5s after Stage 1
            {
                'destCh': 1, 'srcRaw': 'gv(1)', 'weight': 100, 'swtch': 'L5',
                'curve': {'type': 0, 'value': 0},
                'delayPrec': 0, 'delayUp': 0, 'delayDown': 0,
                'speedPrec': 0, 'speedUp': 3, 'speedDown': 0,
                'carryTrim': 0, 'mltpx': 'REPL', 'mixWarn': 0,
                'flightModes': '000000000', 'offset': 0, 'name': 'Stage2 GV2'
            },
            # 5. Stage 3 — full trigger, 0.3s after Stage 2
            {
                'destCh': 1, 'srcRaw': 'I1', 'weight': 100, 'swtch': 'L6',
                'curve': {'type': 0, 'value': 0},
                'delayPrec': 0, 'delayUp': 0, 'delayDown': 0,
                'speedPrec': 0, 'speedUp': 3, 'speedDown': 0,
                'carryTrim': 0, 'mltpx': 'REPL', 'mixWarn': 0,
                'flightModes': '000000000', 'offset': 0, 'name': 'Stage3 100pct'
            },
            # 6. Transbrake — kills CH2 while SC held (AFTER stages)
            {
                'destCh': 1, 'srcRaw': 'MAX', 'weight': 0, 'swtch': 'SC2',
                'curve': {'type': 0, 'value': 0},
                'delayPrec': 0, 'delayUp': 0, 'delayDown': 0,
                'speedPrec': 0, 'speedUp': 0, 'speedDown': 0,
                'carryTrim': 0, 'mltpx': 'REPL', 'mixWarn': 0,
                'flightModes': '000000000', 'offset': 0, 'name': 'Transbrake SC2'
            },
            # 7. Master kill — kills CH2 when disarmed (MUST BE LAST)
            {
                'destCh': 1, 'srcRaw': 'MAX', 'weight': 0, 'swtch': '!L1',
                'curve': {'type': 0, 'value': 0},
                'delayPrec': 0, 'delayUp': 0, 'delayDown': 0,
                'speedPrec': 0, 'speedUp': 0, 'speedDown': 0,
                'carryTrim': 0, 'mltpx': 'REPL', 'mixWarn': 0,
                'flightModes': '000000000', 'offset': 0, 'name': 'Kill !L1'
            },
        ],

        # -- Inputs ------------------------------------------------------------
        'expoData': [
            {
                'srcRaw': 'ST', 'scale': 0, 'mode': 3, 'chn': 0,
                'swtch': 'NONE', 'flightModes': '000000000',
                'weight': 100, 'offset': 0,
                'curve': {'type': 1, 'value': 0},
                'trimSource': 0, 'name': ''
            },
            {
                'srcRaw': 'TH', 'scale': 0, 'mode': 3, 'chn': 1,
                'swtch': 'NONE', 'flightModes': '000000000',
                'weight': 100, 'offset': 0,
                'curve': {'type': 1, 'value': 0},
                'trimSource': 0, 'name': ''
            },
        ],

        'inputNames': {
            0: {'val': 'St'},
            1: {'val': 'TH'},
        },

        # -- Logical Switch Chain ----------------------------------------------
        'logicalSw': {
            0: {  # L1 — Master arm toggle (SD press/press)
                'func': 'FUNC_STICKY',
                'def': 'SD2,SD2',
                'delay': 0, 'duration': 0,
                'andsw': 'NONE',
                'lsPersist': 0, 'lsState': 0,
            },
            1: {  # L2 — Throttle up while SC held
                'func': 'FUNC_VPOS',
                'def': 'I1,5',
                'delay': 0, 'duration': 0,
                'andsw': 'SC2',
                'lsPersist': 0, 'lsState': 0,
            },
            2: {  # L3 — Was-staged latch
                'func': 'FUNC_STICKY',
                'def': 'L2,SD2',
                'delay': 0, 'duration': 0,
                'andsw': 'NONE',
                'lsPersist': 0, 'lsState': 0,
            },
            3: {  # L4 — Launch latch (opens on SC release, zero throttle spike)
                'func': 'FUNC_STICKY',
                'def': 'L3,SD2',
                'delay': 0, 'duration': 0,
                'andsw': '!SC2',
                'lsPersist': 0, 'lsState': 0,
            },
            4: {  # L5 — Stage 2, 0.5s after launch
                'func': 'FUNC_STICKY',
                'def': 'L4,SD2',
                'delay': 5, 'duration': 0,
                'andsw': 'NONE',
                'lsPersist': 0, 'lsState': 0,
            },
            5: {  # L6 — Stage 3, 0.3s after Stage 2
                'func': 'FUNC_STICKY',
                'def': 'L5,SD2',
                'delay': 3, 'duration': 0,
                'andsw': 'NONE',
                'lsPersist': 0, 'lsState': 0,
            },
            6: {  # L7 — SB toggle: Race <-> TH Adj mode
                'func': 'FUNC_STICKY',
                'def': 'SB2,SB2',
                'delay': 0, 'duration': 0,
                'andsw': 'NONE',
                'lsPersist': 0, 'lsState': 0,
            },
        },

        # -- Special Functions -------------------------------------------------
        'customFn': {
            0: {'swtch': '!L1',          'func': 'OVERRIDE_CHANNEL', 'def': '1,0,1'},
            1: {'swtch': '!L1',          'func': 'RGB_LED',          'def': 'red,1,On'},
            2: {'swtch':  'L1',          'func': 'RGB_LED',          'def': 'green,1,On'},
            3: {'swtch':  'L7',          'func': 'RGB_LED',          'def': 'yellow,1,On'},
            4: {'swtch': 'TrimAilRight', 'func': 'ADJUST_GVAR',      'def': '0,IncDec,1,1'},
            5: {'swtch': 'TrimAilLeft',  'func': 'ADJUST_GVAR',      'def': '0,IncDec,-1,1'},
            6: {'swtch': 'TrimRudRight', 'func': 'ADJUST_GVAR',      'def': '1,IncDec,1,1'},
            7: {'swtch': 'TrimRudLeft',  'func': 'ADJUST_GVAR',      'def': '1,IncDec,-1,1'},
        },

        'thrTraceSrc': 'TH',
        'switchWarning': {'SA': {'pos': 'up'}},
        'thrTrimSw': 0,
        'potsWarnMode': 'WARN_OFF',
        'potsWarnEnabled': 0,
        'jitterFilter': 'GLOBAL',
        'displayChecklist': 0,

        # -- Global Variables --------------------------------------------------
        # min/max use 1024-offset format:
        #   GV1: 40-60%  -> min=1064 (1024+40), max=964 (1024-60)
        #   GV2: 65-85%  -> min=1089 (1024+65), max=939 (1024-85)
        'gvars': {
            0: {'name': 'ST1', 'min': 1064, 'max': 964, 'popup': 0, 'prec': 0, 'unit': 0},
            1: {'name': 'ST2', 'min': 1089, 'max': 939, 'popup': 0, 'prec': 0, 'unit': 0},
        },

        'telemetryProtocol': 0,
        'varioData': {
            'source': 'none',
            'centerSilent': 0, 'centerMax': 0, 'centerMin': 0,
            'min': 0, 'max': 0,
        },
        'rssiSource': 'none',
        'rfAlarms': {'warning': 45, 'critical': 42},
        'disableTelemetryWarning': 0,
        'trainerData': {
            'mode': 'OFF', 'channelsStart': 0, 'channelsCount': -8,
            'frameLength': 0, 'delay': 0, 'pulsePol': 0,
        },
        'modelRegistrationID': 'MT12',
        'hatsMode': 'GLOBAL',
        'usbJoystickExtMode': 0,
        'usbJoystickIfMode': 'JOYSTICK',
        'usbJoystickCircularCut': 0,
        'radioGFDisabled': 'GLOBAL',
        'radioTrainerDisabled': 'GLOBAL',
        'modelHeliDisabled': 'GLOBAL',
        'modelFMDisabled': 'GLOBAL',
        'modelCurvesDisabled': 'GLOBAL',
        'modelGVDisabled': 'GLOBAL',
        'modelLSDisabled': 'GLOBAL',
        'modelSFDisabled': 'GLOBAL',
        'modelCustomScriptsDisabled': 'GLOBAL',
        'modelTelemetryDisabled': 'GLOBAL',
    }
    raw = yaml.dump(model, Dumper=CompanionDumper, default_flow_style=False,
                     sort_keys=False, allow_unicode=True, indent=2, width=1000)
    return _companion_fixup(raw)


if __name__ == '__main__':
    import os
    os.makedirs('output', exist_ok=True)
    output = build()
    with open('output/Drag_Race_v4.yml', 'w') as f:
        f.write(output)
    print("Written: output/Drag_Race_v4.yml")
