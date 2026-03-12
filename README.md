# RoosTx

**A guided setup wizard for surface RC vehicles in EdgeTX Companion.**

---

## The Problem

EdgeTX and Companion were built for aircraft. Surface RC vehicles — cars, trucks, crawlers, drag racers — have completely different control logic, and Companion is just beginning to explore surface RC support — without yet having a dedicated setup wizard to guide users through the process. For most surface RC users, setting up a model file from scratch means hours of trial and error, digging through forums, and hoping you got it right before you fry something at the track.

## What RoosTx Does

RoosTx adds a step-by-step setup wizard to Companion that walks the user through configuring a surface RC model file based on their vehicle type and how they run it. It asks plain-language questions, handles the logic behind the scenes, and outputs a ready-to-load model file.

No YAML knowledge required. No manual channel mapping. No guessing.

## Current Status

- **Active development** — pre-release
- Wizard UI: functional demo (v3)
- Supported patterns: Drag Race, Crawler, Drift, Skid Steer
- Target radio: Radiomaster MT12
- Target platform: EdgeTX Companion 2.11

## Repo Structure

```
roostx_core/          — Core engine, templates, model generator
schemas/              — Component and pattern schemas
research_database/    — Component logic, vehicle patterns, research
radio_maps/           — Hardware definitions (MT12)
docs/                 — System design, engineering brief, design tokens
wizard/               — Web-based setup wizard (HTML, offline)
```

## Documentation

Full system design, architecture, and technical specification:
[RoosTx_System_Design_v1.1.docx](RoosTx_System_Design_v1.1.docx)

---

*Built by Kevin Rowe (@WickedFog) with the RoosTx AI development team.*
