# RoosTx Session 13 Handoff
**Date:** 2026-03-20
**Repo:** github.com/WickedFog/Test_Bench_1 (rename to RoosTx when ready)
**Local:** D:\RoosTx on Lappy

---

## WHAT HAPPENED THIS SESSION

### Session 13A — Research and Notation Verification

**Gemini research completed (all 5 prompts):**
- Confirmed: delay/duration in tenths of a second, FUNC_STICKY andsw hard gate, OVERRIDE_CHANNEL neutral=0
- Corrected: func field uses string names not integers (FUNC_VPOS, FUNC_STICKY etc.) — integers are firmware-only
- Corrected: source notation uses strings (I1, SC2, L1) not integer indexes
- Confirmed: REPL replaces everything above it, lines below still execute (kill must be LAST)
- Confirmed: RGB_LED def format is `"red,1,On"` / `"green,1,On"`

**RCGroups thread scan (55 pages):**
- 12 attachments found — no YML files exist in the thread
- `rcgroups_p21_model07.yml` downloaded — confirms SC/SB toggle patterns, copied to `models/archive/`
- Radiomaster.zip in Downloads = logo files only, not useful

**Working reference model discovered:**
- `C:\Users\WickedFog\Documents\Radiomasater MT12\Drag_Race_v4.etx` — existing working model
- Extracted to YAML — reveals `SD2,SD2` and `SC2` as correct Companion 2.11.4 notation
- Confirmed: `OVERRIDE_CHANNEL def: 1,0,1` works correctly when gated by `!L4`
- Confirmed: `RGB_LED def: red,1,On` correct format (not `red` or `red,0`)
- Copied to `models/archive/Drag_Race_v4_WORKING_REF.etx`

### Session 13B — Repo Cleanup

- Moved misplaced files to correct locations
- Created `models/test/` for verified feature test files
- Created `docs/GUIDES/` for instruction documents
- Deleted junk/empty output files
- Committed all cleanup

### Session 13C — Live Simulator Testing

**Tested in order, all verified working:**

1. **SD2,SD2 self-toggle** — WORKS. SD press arms L1, press again disarms. Red/green LED switches correctly.
2. **SC2 as andsw gate** — WORKS. SC held = L2 fires (transbrake detect). SC released = L2 drops.
3. **OVERRIDE_CHANNEL** — WORKS. `def: 1,0,1` kills CH2 to neutral when !L1.
4. **3-stage launch chain** — WORKS after fixing mix stack order and launch latch gate.
5. **andsw: !SC2 on L4** — WORKS. Prevents 100% throttle spike on SC release. Stage 1 fires immediately.
6. **Stage timers** — WORKS. 0.5s to Stage2, 0.3s to Stage3.

**What failed and was fixed:**
- `SD,SD` (no 2) — does nothing. Fixed to `SD2,SD2`.
- `SC,SC` self-toggle — does nothing. Changed SC to andsw gate pattern.
- Kill mix before stage mixes — stages override kill. Fixed: kill goes LAST.
- No andsw on L4 — 100% spike on launch. Fixed: `andsw: "!SC2"` on L4.

### Session 13D — Documentation

- Created `models/test/Launch_Control_3Stage_REFERENCE.yml` — gold reference file, fully commented
- Created `docs/GUIDES/Advanced_EdgeTX_Staged_Throttle.docx` — full instruction sheet
- Updated `ROOSTX_FILES.md` to Session 13 state

---

## CURRENT STATE OF KEY FILES

| File | State | Notes |
|------|-------|-------|
| `models/test/Launch_Control_3Stage_REFERENCE.yml` | **GOLD** | Verified working. Do not modify. |
| `models/archive/Drag_Race_v4_WORKING_REF.etx` | REFERENCE | Original working file. |
| `roostx_core/drag_race_template.py` | NEEDS REBUILD | Pre-Session 13 — wrong notation throughout |
| `models/Drag_Race_v4.yml` | STALE | Regenerate after template rebuild |
| `docs/GUIDES/Advanced_EdgeTX_Staged_Throttle.docx` | NEW | Full guide for staged throttle |
| `roostx_wizard_v3.html` | LOCKED | Do not touch |
| All Layers 1–3 files | LOCKED | Do not touch |

---

## CONFIRMED NOTATION (LOCKED — verified Session 13)

```
SD2,SD2       = SD self-toggle (arm/disarm)
SC2           = SC pressed/held (as andsw gate)
!SC2          = SC released (as andsw gate)
I1            = Throttle input source in def field
L1..L6        = Logical switch refs (string notation)
def: 1,0,1    = OVERRIDE_CHANNEL CH2 to neutral
def: red,1,On = RGB_LED red continuous
def: green,1,On = RGB_LED green continuous
```

## CONFIRMED BROKEN (do not use)

```
SD,SD         = Does nothing in 2.11.4
SC,SC         = Does nothing (momentary too fast)
Kill mix before stage mixes = stages override kill
No andsw on L4 = 100% spike on launch
GV in delay/duration = Issue #4832 unresolved
GV in speedUp/speedDown = Issue #4832 unresolved
```

---

## LOGICAL SWITCH CHAIN (verified working)

```
L1 = FUNC_STICKY  def: SD2,SD2           Master safety toggle
L2 = FUNC_VPOS    def: I1,5  andsw: SC2  Throttle > 0.5% while SC held
L3 = FUNC_STICKY  def: L2,SD2            Was-staged latch
L4 = FUNC_STICKY  def: L3,SD2  andsw: !SC2  Launch latch (opens on SC release, zero gap)
L5 = FUNC_STICKY  def: L4,SD2  delay: 5  Stage 2 — 0.5s after launch
L6 = FUNC_STICKY  def: L5,SD2  delay: 3  Stage 3 — 0.3s after Stage 2
```

## MIX STACK ORDER (verified — order is critical)

```
1. TH base: I1, ADD, always active
2. Stage1: MAX, 50%, REPL, swtch=L4, speedUp=5
3. Stage2: MAX, 75%, REPL, swtch=L5, speedUp=3
4. Stage3: I1, 100%, REPL, swtch=L6, speedUp=3
5. Transbrake: MAX, 0%, REPL, swtch=SC2    ← AFTER stages
6. Master kill: MAX, 0%, REPL, swtch=!L1   ← LAST
```

---

## HARD RULES — DO NOT FORGET

- **SC2 / SD2 / SB2 DO NOT EXIST as physical positions** but DO EXIST as Companion YAML notation for pressed state.
- **CH6/SD is RESERVED.** SD is used as the safety toggle via logical switch only — never assign CH6 directly.
- **GVs cannot go in LS delay/duration fields** — Issue #4832, unresolved.
- **GVs cannot go in mix speedUp/speedDown fields** — Issue #4832, unresolved.
- **Kill mix must be LAST in the CH2 stack.** Any REPL after it will override the kill.
- **andsw: !SC2 on L4 is mandatory.** Without it, 100% throttle fires on SC release.
- **Always test in Companion Simulate Radio before writing to the radio.** Kevin bricked his radio once already.
- **Terminology:** Steering Wheel, Throttle Trigger, Drive Mode (DM). Never stick, never Flight Mode.
- **Don't run git autonomously.** Kevin runs all git commands himself in Git Bash.
- **Don't take off on tasks.** Wait for green light.

---

## GIT RULE FOR THIS PROJECT

Always give Kevin individual commands with separate copy points. Never combine into one multi-line block. He has hand tremors and a bad touchpad — multi-line paste is error-prone. Always include `git add` explicitly before commit.

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Rebuild drag_race_template.py from Launch_Control_3Stage_REFERENCE.yml | Claude | FIRST ORDER |
| 2 | Regenerate Drag_Race_v4.yml from rebuilt template | Claude | AFTER #1 |
| 3 | Wire rebuilt template into wizard — verify output matches reference | Claude + Kevin | AFTER #2 |
| 4 | Add GV trim adjustment (T1=Stage1%, T2=Stage2%) to template | Claude | AFTER #3 |
| 5 | Add burnout mode LS chain to drag race template | Claude | NOT STARTED |
| 6 | Add stage mode (DM1) throttle curves to template | Claude | NOT STARTED |
| 7 | Fix vehicle taxonomy throughout codebase | Claude | NOT STARTED |
| 8 | Schema/component conformance audit (send files to Grok) | Kevin + Grok | NOT STARTED |
| 9 | Fix SA expansion bay hardcoding (Grok flag) | Claude | NOT STARTED |
| 10 | Grok verify Rock_Crawler.yml | Kevin + Grok | NOT STARTED |
| 11 | Grok verify drag_library.json | Kevin + Grok | NOT STARTED |
| 12 | Expand Drag Racer feature list in wizard | Claude | NOT STARTED |
| 13 | Add 4WS expansion bay prerequisite warning | Claude | NOT STARTED |
| 14 | Clone repo to HAL9000 | Kevin | NOT STARTED |
| 15 | Remove Syncthing, clean up .st folders | Kevin | NOT STARTED |
| 16 | Change MCP filesystem config path to D:\RoosTx | Kevin | NOT STARTED |
| 17 | Purge FM/stick language from CONTRIBUTING.md | Claude | NOT STARTED |
| 18 | Google Drive setup and sync | Kevin + Claude | NOT STARTED |
| 19 | GUI redesign discussion | Kevin + Claude | NOT STARTED |
| 20 | Final wizard demo lock | Claude + Kevin | NOT STARTED |
| 21 | Reach out to elecpower | Kevin | NOT STARTED |
| 22 | Install cmake, ninja, msys2, git-lfs on Lappy | Kevin | NOT STARTED |

---

## INFRASTRUCTURE

| Item | Status |
|------|--------|
| Repo | PUBLIC at github.com/WickedFog/Test_Bench_1 |
| Lappy | Windows 10, D:\RoosTx, Python 3.12.9, Git 2.53, VS Code, Node 22.14.0 |
| HAL9000 | Windows 11, 192.168.50.128, Python 3.12 |
| Companion | 2.11.4 — matches radio firmware |
| Google Drive | Mounted at G: |
| Syncthing | Still active, gitignored |
| Gemini GEM | "Radiomaster MT12 Research Database" — EdgeTX/MT12 knowledge base |

---

## HOW TO START SESSION 14

Paste this entire document at the top of the new chat.

**Session 14 opens with template rebuild.** Read `models/test/Launch_Control_3Stage_REFERENCE.yml` first — it is the source of truth for the new `drag_race_template.py`. Do not start coding until you have read it fully.

---

*Session 13 | Maintained by Claude*
