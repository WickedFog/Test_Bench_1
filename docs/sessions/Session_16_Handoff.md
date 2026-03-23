# RoosTx Session 16 Handoff
**Date:** 2026-03-23
**Repo:** github.com/WickedFog/Test_Bench_1 (rename to RoosTx pending)
**Local:** D:\RoosTx on Lappy

---

## WHAT HAPPENED THIS SESSION

### Primary Focus: New GUI Design Direction

Session 16 was entirely GUI design exploration. No code was merged to repo. All output files are in `/mnt/user-data/outputs/` on the Claude session machine — NOT in the repo yet.

### Decision: Winamp-Style Hardware Panel

Abandoned the existing `roostx_wizard_v3.html` / `roostx_wizard_v4.html` panel flow entirely for the main window. New direction:

- **Form factor:** Wide landscape hardware panel — white body chassis, physical buttons flanking a central LCD screen, red accent bottom panel. Modeled on the Radiomaster MT12 screen hardware aesthetic.
- **Colorway LOCKED:**
  - Chassis body: `#f0efe9` white with gradient shading
  - Carbon fiber inlays: `#161616` with 4px repeating diagonal weave
  - Candy apple red: `#cc1111` / `#d41515` title bar, `#7d0505` deep shadow
  - LCD background: `#0d0000`
  - LCD active text: `#ff2b00` with glow
  - LCD mid text: `#cc2000`
  - LCD dim text: `#7a1800`
  - LCD border/dividers: `#3a0800`
- **Button style:** Deep mechanical keyboard style — raised cap with highlight sheen, 4px bottom border shadow, CF surround inset. Active state = candy apple red.
- **Concept A** from the session drafts is the chosen direction (CF outer frame, red title bar, deep MX keys).

### Design Tokens File Needed
`wizard/design-tokens.css` contains the OLD cyan wizard palette — do NOT use for new GUI.
New palette needs to be written to `wizard/design-tokens-gui-v1.css` — not done yet. **Do this first next session.**

---

## GUI ARCHITECTURE DECISIONS (LOCKED THIS SESSION)

### Button Layout
- **5 left buttons** — primary navigation satellites
- **5 right buttons** — secondary navigation satellites
- **Bottom right cluster** — 3-4 smaller utility buttons (Display, Setup, etc.)
- **Bottom left** — CF inlay block, decorative only
- All buttons delivered as **blank caps** — text labels overlaid in CSS, not baked into assets

### Left Button Assignments (draft — not locked)
| Button | Target |
|--------|--------|
| Features | Feature toggle satellite |
| Ch Map | Channel map satellite |
| Drive Modes | DM editor satellite |
| Curves | Curve editor satellite |
| Log SW | Logical switch chain satellite |

### Right Button Assignments (draft — not locked)
| Button | Target |
|--------|--------|
| Inputs | Input/expo editor |
| Mixes | Mix stack editor |
| Outputs | Output limits |
| Special Fn | Special functions |
| Output | YAML preview + download |

### Utility Buttons (bottom right, small)
Display, Setup, Telemetry, About — TBD exact count

### Radio Pages Reference (MT12 — 11 total)
Setup, Drive Modes, Inputs, Mixes, Outputs, Curves, Global Variables, Logical Switches, Special Functions, Display, Telemetry.
GVars folds into Drive Modes. Setup lives on main LCD. = 10 buttons covers everything cleanly.

---

## LCD SCREEN LAYOUT (LOCKED THIS SESSION)

Three-column layout inside the LCD:

| Col 1 | Col 2 | Col 3 |
|-------|-------|-------|
| Vehicle image + label | Inputs list | Drive Modes |

**Header:** `// ACTIVE MODEL //` + model name (Orbitron, large, glowing) + VALID badge + FW info

**Inputs list (full — locked):**
ST, TH, SA, SB, SC, SD, S1, S2, FL1, FL2, T1, T2, T3, T4, T5
- ST/TH/SC/SD = bright (primary inputs)
- All others = dim (secondary)
- FL1/FL2 tagged `[EXP]` — expansion bay hardware required

**Drive Modes:** 9 slots (DM0–DM8). Clickable — clicking a slot opens an info box describing that mode. Click again to dismiss.

**Status strip (bottom of LCD):**
Model OK · Telemetry OFF · Radio Unbound · FW Match · YAML Pending

**No internals on screen** — GVars, logical switch numbers, mix counts, semver — none of it. Driver-relevant info only.

**Scanlines:** REMOVED. Looked bad at hi-res. LCD color + vignette does the job.

---

## SIX SKIN THEMES (DECIDED THIS SESSION)

Same chassis shape for ALL skins. Grok textures the mold, Claude composites.

| # | Skin | Aesthetic |
|---|------|-----------|
| 1 | Drag / Street | Slick. White, CF, candy apple red, chrome. Current design. |
| 2 | Dirt / Rock / Crawler | Beaten aluminum. Mud, scratches, chunked corners, rust bleeds. Earth tones. |
| 3 | Construction / Hauler | Industrial. Hex bolt corners, caution stripe, I-beam borders, yellow/black. |
| 4 | Military | OD green or desert tan. Stencil text, camo, battle scarring, field radio. |
| 5 | Race (SCT/Buggy/Truggy) | Motorsport. Sponsor energy, team colors, CF undertray, race number plate. |
| 6 | Marine / Boat | Nautical. Teak texture, brushed aluminum, navy/white, compass rose. |

**Selection screen:** User picks vehicle class on launch — correct skin loads. The selection screen tiles are already styled in their own theme so you know what you're picking before you click it.

---

## LCD PROFILE VARIANTS (per skin group)

Same three-column structure, content swaps by class:

| Group | Col 1 | Col 2 | Col 3 |
|-------|-------|-------|-------|
| Drag/Street | Car image | Inputs | Drive Modes |
| Crawler/Trail | Car image | Inputs | Terrain Modes |
| SCT/Buggy | Car image | Inputs | Handling Modes |
| Construction/Scale | Channel map | Systems | Status |

Scale/semi/32ch builds get a **table mode** — channel map IS the main content, no car image, scrollable list.

---

## GROK PROJECT: GUI Development for RoosTx

### Project Sources to Upload
1. Screenshot of Concept A chassis (CF outer frame, red titlebar — best one from session)
2. Screenshot of the LCD PNG (`roostx_lcd.png` from outputs)
3. The Gemini LCD screenshot Kevin saved
4. Hardware panel reference photo (white panel with flanking buttons)
5. RCTalk Mustang line art PNG — reference for drag car asset
6. Kevin's style reference images (whatever he has)
7. `docs/RoosTx_Documentation/RoosTx_System_Design_v1.2.docx` — project context
8. New `wizard/design-tokens-gui-v1.css` once written next session

### Grok First Prompt (asset request — no code)
```
Do not write any code. Image assets only, PNG with transparent backgrounds.

Priority 1 — Drag/Street skin assets:
1. Blank button cap — resting state (white body, CF surround, deep MX-style shadow)
2. Blank button cap — hover state (red border glow)
3. Blank button cap — active/selected state (candy apple red, lit)
4. Bottom utility button — smaller variant, same family
5. Chassis body texture tile — white with subtle panel line shading
6. LCD bezel frame — dark, inset, slight red ambient glow

All assets must fit this chassis shape: [attach Concept A screenshot]
Colorway: white #f0efe9, CF #161616, candy apple red #cc1111, LCD bg #0d0000, LCD active #ff2b00
```

---

## OUTPUT FILES FROM THIS SESSION
(in Claude outputs, NOT in repo — copy manually if needed)
- `roostx_concepts.html` — first three concept drafts (A/B/C)
- `roostx_panel_concept.html` — hardware panel form factor v1
- `roostx_v2_drafts.html` — three variants with deeper buttons, CF, car attempts
- `roostx_lcd_v3.html` — interactive LCD with clickable DMs
- `roostx_v3_final.html` — Concept A with embedded Mustang photo (filtered)
- `roostx_lcd.png` — rendered LCD PNG with Mustang, no scanlines

---

## PENDING WORK (Priority Order)

| # | Task | Who | Status |
|---|------|-----|--------|
| 1 | Write `wizard/design-tokens-gui-v1.css` and push | Claude | NEXT |
| 2 | Build final chassis HTML — Concept A, production quality | Claude | NEXT after tokens |
| 3 | Get Grok button/skin assets | Kevin + Grok | IN PROGRESS |
| 4 | Composite Grok assets into chassis HTML | Claude | Waiting on Grok |
| 5 | Build selection screen (skin picker) | Claude | NOT STARTED |
| 6 | Build remaining 5 skin themes | Claude + Grok | NOT STARTED |
| 7 | Wire drag_race_template.py into wizard | Claude | BLOCKED (GUI first) |
| 8 | Confirm T2, T3, T5 trim YAML names on hardware | Kevin | NOT STARTED |
| 9 | Fix vehicle taxonomy throughout codebase | Claude | NOT STARTED |
| 10 | Expand Drag Racer feature list in wizard | Claude | NOT STARTED |
| 11 | Add 4WS expansion bay prerequisite warning | Claude | NOT STARTED |
| 12 | Purge FM/stick language from CONTRIBUTING.md | Claude | NOT STARTED |
| 13 | Google Drive full sync with D:\RoosTx | Kevin | NOT STARTED |
| 14 | Clone repo to HAL9000 | Kevin | NOT STARTED |
| 15 | Remove Syncthing, clean .st folders | Kevin | NOT STARTED |
| 16 | Rename repo from Test_Bench_1 to RoosTx | Kevin | NOT STARTED |

---

## HARD RULES — CARRY FORWARD

- **Drive Mode (DM)** always. Never Flight Mode, never FM.
- **Steering Wheel / Throttle Trigger** — locked terminology.
- **Don't run git autonomously.** Kevin runs all git in Git Bash.
- **Test in Companion Simulate Radio** before writing to physical radio.
- **One command at a time** — shaky hands, bad touchpad.
- **Never delete files.** Backup before replacing.
- **wizard/design-tokens.css** = OLD cyan skin. Do not use for new GUI.

---

## HOW TO START SESSION 17

Paste this document at the top of the new chat.

**Session 17 opens with:**
1. Write and push `wizard/design-tokens-gui-v1.css` with the new palette
2. Build the clean Concept A chassis HTML — production quality, no drafts
3. Drop in whatever Grok assets Kevin has by then

Read `D:\RoosTx\wizard\roostx_wizard_v3.html` for reference on what the old wizard did — but do NOT modify it. Frozen until new GUI is locked.

---

*Session 16 | Maintained by Claude*
