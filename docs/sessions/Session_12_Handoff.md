# RoosTx Session 12 Handoff
**Date:** 2026-03-18
**Repo:** https://github.com/WickedFog/Test_Bench_1
**Cloned to:** D:\RoosTx on Lappy

---

## Session 11 Completed

- Node.js v22.14.0 installed on Lappy
- Python 3.12.9 installed on Lappy (3.14 was corrupt -- use 3.12)
- pyyaml installed in Python 3.12 environment
- Companion updated to 2.11.4 -- matches radio firmware
- Companion Radio Profile: Lua ticked, backup folder set, Int Module corrected
- Radio hardware labels set: STR/THR/TL1/TL2/DM/TRB/THL
- ROOSTX_FILES.md fully rebuilt
- Drag Race spec written and Kevin-approved (docs/Drag_Race_Spec_v1.md)
- Drag Race curve ideas captured (docs/Drag_Race_Curves_v1.txt)
- Terminology locked -- DM / Steering Wheel / Throttle Trigger everywhere
- semver bumped to 2.11.4 across all YMLs
- Broken Drag_Race_v3 archived to models/archive/
- README live demo link added
- drag_race_template.py fully rebuilt from approved spec
- model.py fixed -- lsPersist/lsState in all logical switches
- model.py fixed -- semver default 2.11.4
- model.py fixed -- Drive Mode terminology
- model.py -- add_curve() method added
- drag_race_template.py -- 4 placeholder curves added (Burnout/Stg1/Stg2/Stg3)
- Drag_Race_v4.yml generated and committed
- docs/RoosTx_Documentation folder typo fixed (was Doocumentation)
- SB assigned to Parachute deploy

---

## Where We Left Off

Template rebuilt and generating correct output. Curves added as straight line
placeholders -- Kevin will dial in sine curves later. Model NOT yet tested on
radio. That is Session 12 priority #1.

---

## Run Template Command

```
cd /d/RoosTx/roostx_core
C:/Users/WickedFog/AppData/Local/Programs/Python/Python312/python.exe drag_race_template.py
cp output/Drag_Race_RoosTx.yml ../models/Drag_Race_v4.yml
```

---

## Session 12 Priority Order

| # | Task |
|---|------|
| 1 | Load Drag_Race_v4.yml in Companion, test on radio |
| 2 | Verify SD master block kills throttle when up |
| 3 | Verify DM switching works correctly |
| 4 | Verify burnout LS chain fires |
| 5 | Wire curves to correct mixes in template |
| 6 | Update ROOSTX_FILES.md, commit, push |

---

## Key Constraints (never forget)

- SC2/SD2/SB2 DO NOT EXIST -- momentary switches only have position 1
- SD is RESERVED master throttle block -- never assign anything to it
- semver: 2.11.4
- DM0=Race(SA up), DM1=Stage(SA mid), DM2=Burnout(SA down)
- Steering Wheel / Throttle Trigger -- never "stick"
- Drive Mode (DM) -- never Flight Mode (FM)
- GV cannot be used in LS delay/duration fields
- EdgeTX LS timer resolution: 0.1s native, Lua needed for 0.01s
- Python to use: C:/Users/WickedFog/AppData/Local/Programs/Python/Python312/python.exe
