# Stroke Communication Aid

An offline-first Raspberry Pi communication aid for people whose speech and handwriting have been affected by a stroke.

The patient types with one or more fingers on a lightweight Bluetooth or USB keyboard. The Raspberry Pi displays the message in very large, high-contrast text on its local screen and, when available, mirrors it to a hospital-room television. The completed message can also be spoken aloud using text-to-speech.

> **Project status:** concept and prototype planning. This is an assistive communication tool, not a medical device, diagnostic system, emergency-call system, or replacement for evaluation by a speech-language pathologist (SLP), occupational therapist, or the clinical care team.

## Why this project

A handheld whiteboard may be difficult to use when a stroke affects fine motor control, grip, coordination, language, vision, or attention. A physical keyboard can reduce the precision required to form letters by hand while preserving the patient's ability to compose their own message.

Typing is not suitable for every stroke survivor. Aphasia can affect reading, spelling, word retrieval, or comprehension even when the person's intelligence and ideas are intact. The design must therefore support typing without assuming that typing alone solves every communication need.

## Proposed first version

- Raspberry Pi 4 with Raspberry Pi OS
- Compact Bluetooth keyboard, with USB keyboard fallback
- One local HDMI display
- Optional second HDMI connection to a television
- Full-screen, high-contrast message display
- Large, adjustable text
- Simple keyboard-only controls
- Offline text-to-speech through a speaker or the display audio output
- No account, cloud service, or patient-data collection

## Basic interaction

1. The device starts directly in the communication screen.
2. The patient types a message.
3. Text appears immediately in a large, readable format on both displays.
4. The patient presses a large, easy-to-find key (initially `Enter`) to speak the message.
5. The patient presses another deliberate shortcut to clear the message.

The exact controls must be tested with patients and therapists. Accidental clearing should be difficult, and typing should never require key combinations for normal use.

## Feasibility

The core concept is technically straightforward. A Raspberry Pi 4 can:

- accept Bluetooth and USB keyboard input;
- drive two HDMI displays;
- mirror a full-screen application;
- synthesize speech locally; and
- start the application automatically at boot.

The principal risks are human rather than computational: fatigue, one-handed reach, tremor, visual-field loss, cognitive load, aphasia, accidental keystrokes, keyboard pairing failures, and hospital infection-control requirements. A successful prototype therefore needs early review by an SLP, an occupational therapist, nursing staff, and—most importantly—people with lived stroke experience.

## Suggested prototype architecture

```text
Bluetooth/USB keyboard
          |
          v
 Raspberry Pi application ---> Offline text-to-speech ---> Speaker/HDMI audio
          |
          +----> Local display (mirrored) ----> Room television
```

For the first prototype, a small Python application using a simple full-screen GUI is sufficient. The input and display logic should not depend on a network connection. Speech should use a locally installed engine. Technology choices should remain replaceable until usability testing establishes the actual needs.

## Accessibility principles

- Patient-controlled: never speak or clear a message without an intentional action.
- Low effort: ordinary message entry should require only single-key presses.
- Forgiving: support Backspace, Undo, and protection against accidental clearing.
- Legible: adjustable text size, high contrast, generous spacing, and minimal clutter.
- Private: show only the current message by default; do not retain transcripts by default.
- Reliable: operate offline and accept a wired keyboard when Bluetooth is unavailable.
- Adaptable: allow left- or right-side keyboard placement and future alternative inputs.
- Respectful: do not infer, rewrite, or “correct” the patient's meaning without consent.

## Safety and privacy boundaries

- Do not rely on the device for urgent calls to staff or emergency services.
- Keep an established nurse-call method accessible.
- Do not store conversation history in the first version.
- Avoid cloud speech or AI services unless later versions add explicit consent and appropriate privacy safeguards.
- Confirm that cables, stands, power supplies, and keyboard placement do not create fall, entanglement, or care-access hazards.
- Follow the facility's cleaning, electrical-equipment, wireless-device, and infection-control policies.

## Repository direction

```text
stroke-communication-aid/
├── README.md
├── PROJECT.md
├── app/
├── tests/
├── scripts/
├── docs/
└── hardware/
```

No application code has been selected or created yet. See [PROJECT.md](PROJECT.md) for the product definition, scope, milestones, risks, and validation plan.

## Immediate next step

Build a tabletop proof of concept using a Pi, one keyboard, one monitor, and a speaker. Validate only the essential loop: **type → read → speak → correct → clear**. Before expanding it, observe whether a potential user can complete that loop comfortably and reliably.

## Working name

“Stroke Communication Aid” is a descriptive placeholder. A future name should emphasize the person's voice and agency rather than their diagnosis.
