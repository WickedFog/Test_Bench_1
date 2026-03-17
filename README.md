# RoosTx

**A guided setup wizard for surface RC vehicles in EdgeTX Companion.**

---

## The Problem

EdgeTX and Companion were built for aircraft. Surface RC vehicles â€” cars, trucks, crawlers, drag racers â€” have completely different control logic, and Companion is just beginning to explore surface RC support â€” without yet having a dedicated setup wizard to guide users through the process. For most surface RC users, setting up a model file from scratch means hours of trial and error, digging through forums, and hoping you got it right before you fry something at the track.

## What RoosTx Does

RoosTx adds a step-by-step setup wizard to Companion that walks the user through configuring a surface RC model file based on their vehicle type and how they run it. It asks plain-language questions, handles the logic behind the scenes, and outputs a ready-to-load model file.

No YAML knowledge required. No manual channel mapping. No guessing.

## Current Status

- **Active development** â€” pre-release
- Wizard UI: **[Live demo (v4)](https://wickedfog.github.io/Test_Bench_1/docs/roostx_wizard_v4.html)**
- Supported patterns: Drag Race, Crawler, Drift, Skid Steer
- Target radio: Radiomaster MT12
- Target platform: EdgeTX Companion 2.11

## Repo Structure

```
roostx_core/          â€” Core engine, templates, model generator
schemas/              â€” Component and pattern schemas
research_database/    â€” Component logic, vehicle patterns, research
radio_maps/           â€” Hardware definitions (MT12)
docs/                 â€” System design, engineering brief, design tokens
wizard/               â€” Web-based setup wizard (HTML, offline)
```

## Documentation

Full system design, architecture, and technical specification:
[RoosTx_System_Design_v1.1.docx](RoosTx_System_Design_v1.1.docx)

---

*Built by Kevin Rowe (@WickedFog) with the RoosTx AI development team.*

