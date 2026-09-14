# PROJECT — Stroke Communication Aid

## 1. Project purpose

Create a simple, dependable bedside communication aid for a person who can formulate messages and use one or more fingers to type, but whose speech and handwriting have been impaired by a stroke.

The product will turn physical-keyboard input into large on-screen text and optional synthesized speech. It should help the patient communicate with family, friends, and medical staff while preserving the patient's authorship, privacy, and control.

## 2. Problem statement

Speech impairment after stroke can make even basic needs difficult to express. A whiteboard may help, but it still requires grip, coordinated arm movement, and legible handwriting. Phones and tablets may introduce small targets, gestures, screen timeouts, notifications, and unfamiliar interfaces.

A dedicated appliance with a physical keyboard and an always-visible message area may reduce those barriers for some patients. It will not work for everyone: the person's motor, visual, language, cognitive, and fatigue profile must determine whether keyboard entry is appropriate.

## 3. Product hypothesis

For a patient who can recognize letters and intentionally press keys, a dedicated keyboard connected to a distraction-free, large-text display will enable clearer and less frustrating communication than handwriting alone.

We will consider the hypothesis supported when a user can independently compose, correct, show, speak, and clear a short message with acceptable effort and few accidental actions.

Before pursuing the full product hypothesis, Milestone −1 will test two narrower assertions:

1. **Constructability:** a Raspberry Pi 4 can accept remotely injected development input and a real Bluetooth keyboard, render a message legibly, and speak it with a small Python application.
2. **Potential value:** a working demonstration is compelling enough that the patient, family, and appropriate clinical staff believe further testing is worthwhile.

Milestone −1 is meant to produce evidence quickly, not production architecture. Development shortcuts are permitted when they are clearly separated from the eventual patient-use path.

## 4. Intended users and stakeholders

### Primary user

- A stroke patient with impaired speech and/or handwriting who retains enough language, vision, attention, and finger control to use a keyboard.

### Communication partners

- Family and friends
- Nurses, physicians, therapists, aides, and other care staff

### Advisors

- Speech-language pathologist (SLP)
- Occupational therapist (OT)
- Physical therapist and nursing staff when positioning or safety is involved
- Hospital accessibility, infection-control, privacy, and biomedical-equipment staff
- Stroke survivors and caregivers

## 5. Product principles

1. **The patient owns the message.** The system must not change meaning without permission.
2. **Communication comes first.** Startup, pairing, settings, and decorative UI must stay out of the way.
3. **Offline is the safe default.** Core communication must not require internet access.
4. **One action, one result.** Controls should be obvious, predictable, and reversible where possible.
5. **Do not erase unexpectedly.** Protect unfinished and completed messages from accidental loss.
6. **Adapt to the person.** Stroke effects vary; font, contrast, keyboard placement, audio, and controls must be adjustable.
7. **Minimize retained data.** Do not save transcripts by default.
8. **Fail visibly and safely.** Loss of speech audio or the second display must not destroy the typed message.

## 6. Scope

### Milestone −1 proof-of-concept scope

- Develop directly on a network-connected Raspberry Pi 4.
- Use SSH for installation, code changes, launching, diagnostics, and simulated text input.
- Feed SSH-originated text into the application as a development input channel; do not claim that SSH emulates a physical USB keyboard.
- Pair and test a lightweight Bluetooth keyboard as the representative patient input device.
- Display a single large, high-contrast message on one HDMI monitor.
- Speak the current message using any readily available local text-to-speech engine.
- Demonstrate basic correction and clearing; production-quality safeguards are not required yet.
- Capture observations and a go/stop decision; do not build settings, automatic startup, enclosure, dual-display behavior, or clinical integrations.

The proof of concept may use networking and developer intervention. Those conveniences are scaffolding and are not evidence of bedside reliability.

### Minimum viable prototype (MVP)

- Boot directly into a full-screen communication application
- Accept USB keyboard input first; support Bluetooth after boot reliability is proven
- Show the current message in large, high-contrast text
- Mirror the interface to both HDMI outputs when a second display is connected
- Permit typing, cursor movement, Backspace, and an Undo action
- Speak the message locally after an intentional command
- Stop/repeat speech using simple controls
- Clear the message only after a deliberate action or confirmation
- Provide an accessible settings screen for text size, color theme, volume, and speech rate
- Run without internet connectivity
- Recover cleanly after power interruption

### Early enhancements

- On-screen status indicators for keyboard, audio, and second display
- Optional word prediction that never overwrites patient text
- Patient-approved quick phrases such as “I am in pain” or “Please call my family”
- Customizable key bindings and one-handed layouts
- Scan-and-select input for users who cannot type reliably
- Multilingual display and speech voices
- A privacy mode that temporarily hides the display from visitors

### Explicitly out of scope for the MVP

- Medical diagnosis or clinical decision support
- Emergency or nurse-call replacement
- Automatic interpretation of unclear messages
- Generative-AI rewriting
- Cloud accounts, remote access, analytics, or transcript synchronization
- Electronic health record integration
- Camera or microphone monitoring
- Claims that the prototype is a regulated medical device

## 7. Core user stories

- As a patient, I can begin typing immediately after the device starts.
- As a patient, I can see every character clearly from my normal position.
- As a patient, I can correct mistakes without losing the rest of my message.
- As a patient, I can intentionally have my message spoken aloud.
- As a patient, I can repeat a message without retyping it.
- As a patient, I control when my message is cleared.
- As a communication partner, I can read the same message without crowding the patient.
- As a caregiver, I can tell whether the keyboard, audio, and second display are working.
- As a therapist, I can adjust the interface to the patient's motor and visual needs.

## 8. Proposed hardware

| Component | MVP choice | Notes |
|---|---|---|
| Computer | Raspberry Pi 4 | Two micro-HDMI outputs; 4 GB RAM is ample |
| POC development input | SSH from a development computer | Fast iteration and simulated text input; not a substitute for physical-keyboard validation |
| POC patient input | Lightweight Bluetooth keyboard | Validates the intended wireless input path early |
| MVP fallback input | Compact USB keyboard | Recovery path if Bluetooth fails |
| Primary display | Portable HDMI monitor | Size and mounting depend on bedside position and vision |
| Shared display | Room television via second HDMI | Requires hospital permission, compatible input, and safe cable routing |
| Audio | Powered speaker or HDMI audio | Must be understandable at limited volume |
| Storage | High-quality microSD or SSD | Read-only or resilient configuration should be explored |
| Power | Approved Pi power supply | Facility review may be required |
| Mounting | Stable, cleanable stand/tray | Must not interfere with treatment or create a hazard |

The Pi can drive two displays, but exact dual-display behavior and TV compatibility should be tested with the intended Raspberry Pi OS release, resolution, adapters, and room hardware.

## 9. Proposed software design

### Components

- **Input controller:** normalizes keyboard events and configurable actions.
- **Message model:** holds current text and an in-memory undo state.
- **Display view:** renders the same message and status on all displays.
- **Speech service:** sends patient-approved text to an offline TTS engine.
- **Settings service:** stores accessibility preferences, not conversations.
- **Health/status service:** reports keyboard, display, audio, and startup state.

### Initial technical direction

- Milestone −1: network-connected development on the Pi over SSH
- Milestone −1: a deliberately small Python demo with replaceable input, display, and speech boundaries
- Milestone −1: SSH-originated simulated input plus direct Bluetooth keyboard input
- Raspberry Pi OS with automatic login into a restricted application session
- Python application with a lightweight full-screen GUI
- Local text-to-speech engine behind an interface so it can be replaced
- `systemd` service for automatic startup and restart
- Network access is permitted for proof-of-concept development; the MVP has no network dependency
- Automated tests for message editing and commands; hardware-in-the-loop checks for keyboard, displays, and audio

The implementation language and GUI toolkit are provisional. Usability and startup reliability should drive the choice.

## 10. Interaction proposal

The default screen contains one large message area and a small status strip. The patient types normally. Proposed controls for the first test:

| Action | Initial control | Design concern |
|---|---|---|
| Type | Letter, number, punctuation keys | Ignore unintended key repeat where appropriate |
| Correct | Backspace and arrow keys | Make cursor visually prominent |
| Speak | Enter | Prevent accidental activation during multiline entry |
| Repeat speech | F5 or configurable large key | Needs a label or key cover |
| Stop speech | Escape | Must respond immediately |
| Clear | Hold a designated key, then confirm | Never use a single easy-to-hit key |
| Increase/decrease text | Dedicated keys or caregiver settings | Avoid complex shortcuts for the patient |

These mappings are hypotheses, not settled requirements. Observe actual use before finalizing them. A keyboard with large-print key stickers, keyguard, reduced key set, or programmable external buttons may be more effective than a standard compact keyboard.

## 11. Clinical and usability considerations

Testing should assess:

- Which hand and fingers the person can use reliably
- Reach, posture, fatigue, tremor, and unintended repeated presses
- Ability to recognize keys, spell, read, and find words
- Aphasia, apraxia of speech, dysarthria, neglect, and visual-field limitations
- Font size, contrast, line length, and viewing distance
- Whether synthesized speech is comprehensible and comfortable
- Whether typing frustrates or tires the patient
- Whether low-tech alternatives and picture/phrase boards should remain alongside the device

The care team should use reliable yes/no verification and supported-conversation techniques when meaning is uncertain. The system should never treat slow, misspelled, or incomplete typing as lack of understanding.

## 12. Privacy, safety, and regulatory questions

- The screen may expose sensitive health or family information to roommates, visitors, or passersby.
- Transcripts should remain only in memory and disappear on clear or shutdown unless the patient explicitly requests future saving.
- Network and SSH are permitted during development, with access limited to the developer-controlled network and credentials. They should be disabled or explicitly reviewed before bedside use.
- Bluetooth availability and policy vary by facility; USB must remain a fallback.
- Equipment must be cleanable and positioned without obstructing care.
- The project team should obtain advice before describing or deploying the system as a medical device.
- Any future storage, remote access, clinical integration, or cloud speech feature requires a separate privacy and security review.

## 13. Milestones

### Milestone −1 — Fail-fast proof of concept

**Question:** Is a keyboard-to-large-text-to-speech appliance both constructable and plausibly valuable?

Build the thinnest demonstrable vertical slice:

- Raspberry Pi 4 connected to a development network
- Python demo application launched and observed on the Pi
- SSH used for development, diagnostics, and simulated message input
- Bluetooth keyboard paired and used for direct message entry
- One HDMI display showing large, high-contrast text
- Text-to-speech for the current message
- Minimal correction and clear actions
- No automatic startup, dual-display work, polished settings, enclosure, transcript storage, or reliability engineering

Run two demonstrations:

1. **Construction demonstration:** enter, correct, display, speak, and clear “I need some water” through SSH and then through the Bluetooth keyboard.
2. **Value demonstration:** show the working loop to the patient, family, and—when feasible—an SLP, OT, nurse, or other appropriate clinician. Ask whether this warrants a supervised patient trial and what would prevent its use.

Record:

- Pi model, OS version, keyboard model, display, speaker, and speech engine
- Setup time and failures
- Input-to-display responsiveness
- Bluetooth pairing and reconnection behavior
- Whether the spoken message is understandable
- Stakeholder reactions, limitations, and proposed changes

**Pass criteria:**

- Both SSH-simulated and Bluetooth-keyboard input can complete the full message loop.
- Text is immediately readable and speech is understandable in a quiet-room demonstration.
- At least one intended stakeholder judges the concept valuable enough for a supervised next test.
- No discovered constraint makes the concept clearly inappropriate for the intended patient.

**Stop or pivot criteria:**

- The intended patient cannot reliably use keyboard-based input, even with reasonable adaptations.
- A language, visual, cognitive, positioning, policy, or safety barrier makes this form of interaction unsuitable.
- The demonstration provides no meaningful advantage over available low-tech or tablet-based AAC.
- Construction or operation is disproportionately complex for the benefit observed.

**Exit decision:** explicitly choose **proceed**, **pivot**, or **stop**, with the evidence behind the decision. Passing Milestone −1 proves feasibility and potential value only; it does not establish clinical effectiveness, safety, or bedside readiness.

### Milestone 0 — Needs validation

- Interview the patient and family about the communication problem.
- Ask an SLP and OT whether keyboard input is appropriate.
- Observe one-handed typing with a standard keyboard and at least one accessible alternative.
- Define measurable comfort and success criteria.

**Exit criterion:** advisors agree that a keyboard-based experiment is safe and worth testing for the intended user.

### Milestone 1 — Tabletop proof of concept

- One Pi, USB keyboard, monitor, and speaker
- Full-screen large-text entry
- Correct, speak, repeat, stop, and protected-clear actions
- Fully offline operation

**Exit criterion:** a user can complete the type → read → speak → correct → clear loop during a supervised session.

### Milestone 2 — Bedside prototype

- Reliable automatic startup
- Bluetooth keyboard with USB fallback
- Mirrored second HDMI display
- Accessibility settings
- Safe physical placement and cable management
- Clear fault/status indications

**Exit criterion:** repeated bedside rehearsals succeed without developer intervention.

### Milestone 3 — Guided pilot

- Written setup, cleaning, privacy, and troubleshooting instructions
- Review by relevant clinical and facility staff
- Structured feedback from patient and communication partners
- Logged technical failures without storing message content

**Exit criterion:** evidence supports continued development and identifies which input/accessibility modes matter.

## 14. MVP acceptance criteria

These criteria apply after Milestone −1. The fail-fast proof of concept uses its own narrower pass and stop criteria above.

- The application is ready for typing within 30 seconds of power-on.
- Core features work with networking disabled.
- Keystrokes appear with no distracting perceptible delay.
- Unplugging the second display does not interrupt input or lose the message.
- Speech failure leaves the full message visible and editable.
- Accidental single-key input cannot erase the whole message.
- Restart after power loss returns to a usable blank screen without exposing an earlier message.
- A caregiver can connect a USB keyboard and recover basic communication without technical expertise.
- Font and contrast settings remain after restart; message content does not.

Targets should be revised after observation with the intended user and clinical advisors.

## 15. Test strategy

### Automated tests

- Character insertion, deletion, cursor movement, and undo
- Key-repeat filtering and shortcut handling
- Speak, stop, repeat, and clear state transitions
- Settings persistence
- No transcript persistence
- Recovery from speech-service and display errors

### Hardware tests

- SSH-originated simulated input during Milestone −1 only
- Supported USB and Bluetooth keyboards
- Bluetooth disconnect/reconnect behavior
- One and two HDMI displays at common resolutions
- HDMI and external-speaker audio
- Cold boot, repeated reboot, and abrupt power interruption
- Operation with all networking disabled

### Human-centered validation

- Time and effort to produce a short message
- Correction rate and accidental activation rate
- Readability for patient and communication partners
- Fatigue over a realistic session
- Ability to recover from confusion or an error
- Patient preference compared with whiteboard, tablet, and low-tech AAC options

## 16. Key risks and mitigations

| Risk | Initial mitigation |
|---|---|
| Typing is impaired or language formulation is difficult | Evaluate with SLP/OT; support other AAC methods |
| Bluetooth fails or keyboard battery dies | Keep a cleanable USB keyboard available |
| Accidental key presses alter or erase text | Undo, debounce/key-repeat controls, protected clear |
| Patient tires quickly | Adjustable placement, short sessions, minimal actions |
| Message is visible to unintended people | Privacy mode, deliberate screen placement, no history |
| Speech is too quiet or unclear | Volume/speed controls, tested local voices, visible text remains primary |
| TV input is unavailable or prohibited | Treat second display as optional, never required |
| Power loss corrupts the device | Resilient filesystem, tested recovery, controlled shutdown where possible |
| Prototype is mistaken for a nurse-call system | Prominent boundary and continued access to approved call controls |

## 17. Open questions

1. Can the intended patient identify and press keys reliably with the available hand?
2. Is spelling/typing preserved enough to express needs, or are phrases, pictures, or scanning also needed?
3. What keyboard size, force, spacing, labeling, and placement work best?
4. Does the patient need a keyguard or a programmable reduced-key keyboard?
5. What display size, distance, font, and contrast accommodate vision and neglect?
6. Should `Enter` speak, insert a new line, or be configurable?
7. How should the patient intentionally clear text with minimal effort but little accident risk?
8. What voices, volume, and speech rate are most understandable?
9. Will the hospital permit the Pi, Bluetooth, external power, speakers, and TV connection?
10. What communication method remains available if the device fails?

## 18. First implementation increment

**Objective:** Complete Milestone −1 on a network-connected Raspberry Pi 4. Build the smallest Python application that accepts SSH-originated simulated input and direct Bluetooth-keyboard input, displays the message in large high-contrast text on one HDMI screen, and speaks it on command.

**Design check:** Keep SSH input, physical keyboard input, display, and speech as separate boundaries, even if their first implementations are minimal. This prevents development scaffolding from becoming an accidental product dependency.

**Validation target:** Demonstrate “I need some water” end to end through SSH and again through the Bluetooth keyboard. Record construction results and stakeholder reaction, then make an explicit proceed, pivot, or stop decision before adding features.

## 19. Definition of project success

Success is not the number of features. Success is a patient being able to communicate an intended message more independently, accurately, comfortably, and reliably—while retaining control over what is displayed and spoken.
