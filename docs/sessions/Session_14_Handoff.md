# RoosTx Session 14 Handoff
**Date:** 2026-03-22
**Repo:** github.com/WickedFog/Test_Bench_1 (rename to RoosTx when ready)
**Local:** D:\RoosTx on Lappy

---

## WHAT HAPPENED THIS SESSION

### Session 14A — Template Rebuild and File Confusion

**Problem at session start:** The Drag_Race.yml file in the project was an old stale version. The real working file is in `models/test/Drag_Race_v4.yml`. The project file should be ignored.

**drag_race_template.py rebuilt** from `Launch_Control_3Stage_REFERENCE.yml` (Session 13 gold reference). All Session 13 verified notation confirmed:
- `SD2,SD2` = SD self-toggle
- `SC2` = SC pressed (andsw gate)
- `!SC2` = SC released
- L1-L6 chain verified clean
- Mix stack order verified: stages → transbrake → kill (LAST)

**24/24 automated checks passed** on rebuilt template output.

### Session 14B — Source Code Access

**EdgeTX repo cloned to D:\edgetx** — full source available for future lookups. Key files confirmed:
- `companion/src/firmwares/edgetx/yaml_rawswitch.cpp` — switch encoding
- `companion/src/firmwares/edgetx/yaml_customfunctiondata.cpp` — SF encoding
- `companion/src/firmwares/boardjson.cpp` — trim/switch names
- `radio/src/boards/hw_defs/mt12.json` — MT12 hardware definition

### Session 14C — Long GV Trim Adjustment Journey

**The problem:** Spent most of the session trying to get T4 trim to adjust GV1 (Stage 1 %) and ST trim to adjust GV2 (Stage 2 %). Multiple failed approaches:

1. FUNC_AND logical switches — crashed Companion
2. Wrong ADJUST_GVAR def format (`0,0` → `T1,0` → various guesses)
3. Wrong gv field in mixes (`gv: GV1` → `gv: 0` → `gv(0)`)
4. Missing enable flag in ADJUST_GVAR def
5. Wrong trim YAML names for T4 (`TrimThrUp` → `TrimAilRight`)
6. Missing GV default values in flightModeData

**What finally worked — all confirmed on physical radio:**

| Item | Correct Syntax |
|------|---------------|
| GV source in mix | `srcRaw: gv(0)` with `weight: 100` |
| ADJUST_GVAR def | `0,IncDec,1,1` (index, mode, amount, **enable flag**) |
| T4 trim (8:30) | `TrimAilRight` / `TrimAilLeft` |
| ST trim (10:30) | `TrimRudRight` / `TrimRudLeft` |
| GV defaults | `flightModeData[0].gvars[0].val: 50` |
| GV min/max | Top-level `gvars` section: `min: 1064, max: 964` (1024+40, 1024-60) |
| Trim decoupling | `trim: {0: {value: 0, mode: 31}}` in DM3 |

**The enable flag was the final missing piece.** ADJUST_GVAR def must end in `,1` to be enabled. Companion writes `,0` by default if you don't check the Enable checkbox.

### Session 14D — MT12 Syntax Reference (from source code + testing)

**Switch positions (confirmed from yaml_rawswitch.cpp + mt12.json):**

| Switch | YAML | Hardware |
|--------|------|----------|
| SA up | `SA0` | 3-pos top |
| SA mid | `SA1` | 3-pos top |
| SA down | `SA2` | 3-pos top |
| SB released | `SB0` | 2-pos momentary |
| SB pressed | `SB2` | 2-pos momentary |
| SC released | `SC0` | 2-pos momentary |
| SC pressed | `SC2` | 2-pos momentary |
| SD released | `SD0` | 2-pos momentary (**SD is 2POS not 3POS**) |
| SD pressed | `SD2` | 2-pos momentary |

**MT12 trim physical map (confirmed on hardware):**

| Physical | Clock | YAML Up/Right | YAML Down/Left |
|----------|-------|---------------|----------------|
| T1 / ST trim | 10:30 | `TrimRudRight` | `TrimRudLeft` |
| T2 / TH trim | 1:30 | `TrimEleUp` (unconfirmed) | `TrimEleDown` (unconfirmed) |
| T3 | 3:30 | Unknown | Unknown |
| T4 | 8:30 | `TrimAilRight` | `TrimAilLeft` |
| T5 | handle | `TrimT5Up` (unconfirmed) | `TrimT5Down` (unconfirmed) |

**Note:** T2, T3, T5 YAML names not yet confirmed on hardware. T1 and T4 confirmed.

**FL1/FL2:** Serialize as `FL1`, `FL2` with position appended. Require S3/S4 set to Switch type in Radio Settings → Hardware.

**FUNC_AND def format:** `L7,TrimAilLeft` (comma-separated, no quotes needed)

**ADJUST_GVAR def format:** `gvar_index,IncDec,±amount,enable_flag`
- Example: `0,IncDec,1,1` = GV1 increment by 1, enabled

### Session 14E — Drag Race Model Verified Working

**`models/test/Drag_Race_v4.yml`** committed and pushed. Confirmed on physical MT12:
- SD arm/disarm working
- SC transbrake working
- 3-stage launch chain working
- SB toggle → TH Adj mode (yellow LED)
- T4 trim adjusts GV1 (Stage 1 %) within 40-60% range
- ST trim adjusts GV2 (Stage 2 %) within 65-85% range
- GV defaults: GV1=50, GV2=75

### Session 14F — elecpower Contact

elecpower responded positively. Key points:
- Called the wizard "nice and simple"
- Raised valid concern about user understanding
- Will not officially endorse as EdgeTX project (standard for third-party tools)
- Invited Kevin to comment on Companion UI redesign when it happens
- Asked to see the design document (original send failed — file never attached)

**RoosTx_System_Design_v1.2.docx** updated and sent:
- Added learning platform intent to Section 1
- Fixed Drive Mode order (DM0=Race, DM1=Stage, DM2=Burnout)
- Removed S1/S2 knob references (marked as TBD)
- Updated Section 4.6 to reflect T4/ST trim adjustment and SB mode toggle
- Saved to: `D:\RoosTx\docs\RoosTx_Documentation\RoosTx_System_Design_v1.2.docx`
- Copied to: `G:\My Drive\Projects Folder\RoosTx\docs\`

---

## CURRENT STATE OF KEY FILES

| File | State | Notes |
|------|-------|-------|
| `models/test/Drag_Race_v4.yml` | **VERIFIED WORKING** | Confirmed on hardware. Do not modify without testing. |
| `models/test/MT12_Syntax_Test.yml` | REFERENCE | Contains confirmed Companion syntax for trims, GVs, FL1/FL2 |
| `models/test/Stage_Simple.yml` | REFERENCE | Minimal GV mix test — shows gv(0) syntax |
| `models/test/GV1_and_2_Working_SAVED_From_Companion.yml` | REFERENCE | Radio-exported version of working model |
| `models/test/Launch_Control_3Stage_REFERENCE.yml` | **GOLD** | Session 13 verified. Do not modify. |
| `roostx_core/drag_race_template.py` | REBUILT | Clean rebuild Session 14. Generates verified YAML. |
| `docs/RoosTx_Documentation/RoosTx_System_Design_v1.2.docx` | CURRENT | Updated with learning intent + correct DM order |
| `docs/sessions/Session_13_Handoff.md` | REFERENCE | Contains full Session 13 verified notation |

---

## CONFIRMED NOTATION (LOCKED — verified Sessions 13+14)

```
SD2,SD2         = SD self-toggle (arm/disarm)
SC2             = SC pressed/held (andsw gate)
!SC2            = SC released (andsw gate)
SA0/SA1/SA2     = SA up/mid/down
SB0/SB2         = SB released/pressed (2POS)
SD0/SD2         = SD released/pressed (2POS — NOT 3POS)
L1..L7          = Logical switch refs
gv(0)/gv(1)     = GV1/GV2 as mix srcRaw
TrimAilRight    = T4+ (8:30 on wheel)
TrimAilLeft     = T4- (8:30 on wheel)
TrimRudRight    = T1/ST+ (10:30 on wheel)
TrimRudLeft     = T1/ST- (10:30 on wheel)
ADJUST_GVAR def = index,IncDec,±amount,1  (last field = enable flag, must be 1)
FUNC_AND def    = V1,V2 (comma separated)
FL1/FL2         = Expansion bay switches (S3/S4 must be set to Switch in radio hardware)
```

## CONFIRMED BROKEN

```
SD,SD           = Does nothing in 2.11.4
SC,SC           = Does nothing (momentary too fast)
Kill mix before stage mixes = stages override kill
No andsw on L4  = 100% spike on launch
ADJUST_GVAR def ending in ,0 = function disabled
gv: GV1 in mixData = WRONG (use srcRaw: gv(0))
weight: "GV1" in mixData = WRONG
TrimThrUp/Down for T4 = WRONG (use TrimAilRight/Left)
GVs in LS delay/duration = Issue #4832 unresolved
```

---

## LOGICAL SWITCH CHAIN (verified working)

```
L1 = FUNC_STICKY  def: SD2,SD2            Master arm toggle
L2 = FUNC_VPOS    def: I1,5  andsw: SC2   Throttle up while SC held
L3 = FUNC_STICKY  def: L2,SD2             Was-staged latch
L4 = FUNC_STICKY  def: L3,SD2  andsw: !SC2  Launch latch (no spike)
L5 = FUNC_STICKY  def: L4,SD2  delay: 5   Stage 2 — 0.5s after launch
L6 = FUNC_STICKY  def: L5,SD2  delay: 3   Stage 3 — 0.3s after Stage 2
L7 = FUNC_STICKY  def: SB2,SB2            Race <-> TH Adjust mode toggle
```

## MIX STACK ORDER (verified — order is critical)

```
1. ST base    : I0,  ADD,  always active
2. TH base    : I1,  ADD,  always active
3. Stage1     : gv(0), REPL, swtch=L4, speedUp=5  ← GV1 default 50%
4. Stage2     : gv(1), REPL, swtch=L5, speedUp=3  ← GV2 default 75%
5. Stage3     : I1,  REPL, swtch=L6, speedUp=3
6. Transbrake : MAX, 0%,  REPL, swtch=SC2         ← AFTER stages
7. Kill       : MAX, 0%,  REPL, swtch=!L1         ← LAST
```

---

## HARD RULES — DO NOT FORGET

- **ADJUST_GVAR enable flag is mandatory.** def must end in `,1` or the function is disabled.
- **gv(0) not GV1.** Mix srcRaw for GV source is `gv(0)`, `gv(1)` etc.
- **GV defaults go in flightModeData[0].gvars.** Without defaults, GVs start at 0.
- **GV min/max go in top-level gvars section.** Format: `min: 1064` = 1024+40, `max: 964` = 1024-60.
- **SD is 2POS on MT12.** Not 3POS. SD2 = pressed. There is no SD1 middle position.
- **Kill mix must be LAST.** Any REPL after it overrides the kill.
- **andsw: !SC2 on L4 is mandatory.** Without it, 100% throttle spike on SC release.
- **Always test in Companion Simulate Radio before writing to radio.**
- **Don't run git autonomously.** Kevin runs all git commands himself in Git Bash.
- **Drive Mode terminology only.** Never say Flight Mode. Never say stick. Never say FM.
- **Give Kevin one command at a time** — shaky hands, bad touchpad, no multi-line paste.

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Confirm T2, T3, T5 trim YAML names on hardware | Kevin | NOT STARTED |
| 2 | Wire drag_race_template.py into wizard — verify output matches Drag_Race_v4.yml | Claude | NOT STARTED |
| 3 | Add GV trim adjustment to drag_race_template.py | Claude | NOT STARTED |
| 4 | Add burnout mode LS chain to template | Claude | NOT STARTED |
| 5 | Add stage mode (DM1) throttle curves | Claude | NOT STARTED |
| 6 | Google Drive full sync with D:\RoosTx | Kevin + Claude | NOT STARTED |
| 7 | Fix vehicle taxonomy throughout codebase | Claude | NOT STARTED |
| 8 | Schema/component conformance audit (Grok) | Kevin + Grok | NOT STARTED |
| 9 | Expand Drag Racer feature list in wizard | Claude | NOT STARTED |
| 10 | Add 4WS expansion bay prerequisite warning | Claude | NOT STARTED |
| 11 | Purge FM/stick language from CONTRIBUTING.md | Claude | NOT STARTED |
| 12 | Write MT12 YAML reference doc from source code | Claude | NOT STARTED |
| 13 | Lua launch timer integration | Claude | STUBBED |
| 14 | Clone repo to HAL9000 | Kevin | NOT STARTED |
| 15 | Remove Syncthing, clean .st folders | Kevin | NOT STARTED |
| 16 | Change MCP filesystem config to D:\RoosTx | Kevin | NOT STARTED |
| 17 | Reach out to elecpower — send v1.2 doc | Kevin | DONE ✅ |
| 18 | GUI redesign discussion | Kevin + Claude | NOT STARTED |
| 19 | Final wizard demo lock | Claude + Kevin | NOT STARTED |

---

## INFRASTRUCTURE

| Item | Status |
|------|--------|
| Repo | PUBLIC at github.com/WickedFog/Test_Bench_1 |
| Lappy | Windows 10, D:\RoosTx, Python 3.12.9, Git 2.53, VS Code, Node 22.14.0 |
| HAL9000 | Windows 11, 192.168.50.128, Python 3.12 |
| Companion | 2.11.4 — matches radio firmware |
| Google Drive | Mounted at G:\ — needs full sync with D:\RoosTx |
| EdgeTX source | Cloned to D:\edgetx — use for syntax lookups |
| Syncthing | Still active, gitignored |
| Gemini GEM | "Radiomaster MT12 Research Database" |

---

## HOW TO START SESSION 15

Paste this entire document at the top of the new chat.

**Session 15 opens with template wiring.** The verified `Drag_Race_v4.yml` is the ground truth. The goal is to update `drag_race_template.py` so running it generates output that matches that file exactly, then wire it into the wizard.

Before touching the template, read `models/test/Drag_Race_v4.yml` and `roostx_core/drag_race_template.py` to compare current output against verified target.

---

*Session 14 | Maintained by Claude*
