# PROJECT — AWW-Some Blackboard

**Project type:** Raspberry Pi-based stroke communication aid  
**Current platform:** Raspberry Pi 4, ROADOM 10.1-inch HDMI display, and HXMJ Large Print Mini Bluetooth Keyboard  
**Project status:** Working appliance proof of concept; human-centered validation and enclosure work remain  
**Product name:** AWW-Some Blackboard (AWW are the family stroke patient's initials)  
**Last updated:** 2026-09-23

## 1. Project purpose

Create a simple, dependable bedside communication aid for a person who can formulate messages and use one or more fingers to type, but whose speech and handwriting have been impaired by a stroke.

The product will turn physical-keyboard input into large on-screen text and optional synthesized speech. It should help the patient communicate with family, friends, and medical staff while preserving the patient's authorship, privacy, and control.

## 2. Problem statement

Speech impairment after stroke can make even basic needs difficult to express. A whiteboard may help, but it still requires grip, coordinated arm movement, and legible handwriting. Phones and tablets may introduce small targets, gestures, screen timeouts, notifications, and unfamiliar interfaces.

A dedicated appliance with a physical keyboard and an always-visible message area may reduce those barriers for some patients. It will not work for everyone: the person's motor, visual, language, cognitive, and fatigue profile must determine whether keyboard entry is appropriate.

## 3. Product hypothesis

For a patient who can recognize letters and intentionally press keys, a dedicated keyboard connected to a distraction-free, large-text display will enable clearer and less frustrating communication than handwriting alone.

We will consider the hypothesis supported when a user can independently compose, correct, show, speak, and clear a short message with acceptable effort and few accidental actions.

Milestone −1 tested two narrower assertions before further product development:

1. **Constructability:** a Raspberry Pi 4 can accept remotely injected development input and a real Bluetooth keyboard, render a message legibly, and speak it with a small Python application.
2. **Potential value:** a working demonstration is compelling enough that the patient, family, and appropriate clinical staff believe further testing is worthwhile.

Milestone −1 was meant to produce evidence quickly, not production architecture. The construction assertion has now been demonstrated: the Raspberry Pi accepts Bluetooth-keyboard input, displays wrapped large text, and speaks the message locally. A supervised value demonstration with the family stroke patient and appropriate clinical staff remains necessary before claiming patient benefit.

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

### Current working prototype

The project has progressed beyond the original Milestone −1 technical scope. The current appliance:

- Boots Raspberry Pi OS Desktop and launches `poc/app.py` automatically through the desktop session.
- Accepts direct input from the HXMJ Large Print Mini Bluetooth Keyboard.
- Displays large, centered, high-contrast text with automatic multiline wrapping.
- Speaks the complete visible message through the ROADOM display's HDMI speakers.
- Uses a slower speech rate and an audio warm-up to reduce first-utterance clipping.
- Uses single-key patient controls: `Enter` speaks or stops speech, and two presses of `Delete` clear the message.
- Keeps message content in memory rather than creating a transcript.
- Can be maintained over SSH and updated from GitHub using an SSH key.
- Has been rebuilt from a newly imaged SD card, providing an early reproducibility test of the setup instructions.

### Minimum viable prototype (MVP)

- Boot directly into a full-screen communication application
- Accept the paired Bluetooth keyboard, with USB available as a recovery input
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

## 8. Hardware configuration

| Component | MVP choice | Notes |
|---|---|---|
| Computer | Raspberry Pi 4 | Two micro-HDMI outputs; 4 GB RAM is ample |
| POC development input | SSH from a development computer | Fast iteration and simulated text input; not a substitute for physical-keyboard validation |
| Patient input | HXMJ Large Print Mini Bluetooth Keyboard | Compact, high-contrast keyboard selected to reduce one-handed reach |
| MVP fallback input | Compact USB keyboard | Recovery path if Bluetooth fails |
| Primary display | ROADOM 10.1-inch, 1024×600 HDMI touchscreen | Touch is not required; built-in speakers provide HDMI audio |
| Shared display | Room television via second HDMI | Requires hospital permission, compatible input, and safe cable routing |
| Audio | ROADOM HDMI speakers | Working, but available volume should be validated in the intended room |
| Storage | High-quality microSD or SSD | Read-only or resilient configuration should be explored |
| Power | Approved Pi power supply | Facility review may be required |
| Mounting | Planned 3D-printed enclosure with handle | Include a deliberate shutdown control; no front speaker vents are planned |

The Pi can drive two displays, but exact dual-display behavior and TV compatibility should be tested with the intended Raspberry Pi OS release, resolution, adapters, and room hardware.

## 9. Proposed software design

### Components

- **Input controller:** normalizes keyboard events and configurable actions.
- **Message model:** holds current text and an in-memory undo state.
- **Display view:** renders the same message and status on all displays.
- **Speech service:** sends patient-approved text to an offline TTS engine.
- **Settings service:** stores accessibility preferences, not conversations.
- **Health/status service:** reports keyboard, display, audio, and startup state.

### Implemented technical direction

- Milestone −1: network-connected development on the Pi over SSH
- Milestone −1: a deliberately small Python demo with replaceable input, display, and speech boundaries
- Milestone −1: SSH-originated simulated input plus direct Bluetooth keyboard input
- Raspberry Pi OS Desktop, currently based on Debian Trixie
- Python/Tkinter full-screen application in `poc/app.py`
- Local `espeak-ng` text-to-speech
- PipeWire HDMI audio routed to the ROADOM display
- Desktop autologin with a labwc autostart entry for application startup
- Bluetooth keyboard input through the Linux input stack
- `keyd` remapping for a nonstandard HXMJ key, backed by a logind power-key safety rule
- GitHub SSH access for source control without account-password authentication
- Network access is permitted for proof-of-concept development; the MVP has no network dependency
- Automated tests for message editing and commands; hardware-in-the-loop checks for keyboard, displays, and audio

The application source is stored in the `stroke-communication-aid` Git repository. On the current appliance, the working checkout is `/home/an/projects/stroke-communication-aid`, the host name is `awwsome`, and the application path is `poc/app.py`.

## 10. Current interaction

The default screen contains a compact title/help area and one large, centered message area. Controls intentionally avoid combinations such as `Ctrl` plus another key or `Fn` plus a function key.

| Action | Initial control | Design concern |
|---|---|---|
| Type | Letter, number, punctuation keys | Ignore unintended key repeat where appropriate |
| Correct | Backspace | Removes the preceding character |
| Speak | Enter | Speaks the complete visible message |
| Stop speech | Enter while speech is active | Same large, easy-to-find key |
| Repeat speech | Enter after speech completes | Repeats the unchanged message |
| Clear | Delete twice | First press arms clear; second confirms it |

These mappings work in the current POC but remain hypotheses until observed with the intended user. The HXMJ keyboard's nonstandard key reports either `KEY_POWER` or `Left Meta`+`L`, depending on keyboard mode. The appliance uses `keyd` to translate both forms into `Delete`, and configures systemd-logind to ignore power-key events as a fail-safe against accidental shutdown.

The remapping is tied to the stable device ID `04e8:7021:ed42078f`, not `/dev/input/event6`; Linux event numbers can change after reboot or reconnection. On Debian Trixie the packaged executable is `/usr/bin/keyd.rvaiya`, and this version does not provide a `check` command. Configuration is applied with `sudo /usr/bin/keyd.rvaiya reload` and verified through `evtest` on the `keyd virtual keyboard` device.

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
- SSH access to the Pi uses public-key authentication for normal administration. GitHub access uses a separate repository key so interactive account passwords are not stored or entered on the appliance.
- Bluetooth availability and policy vary by facility; USB must remain a fallback.
- Equipment must be cleanable and positioned without obstructing care.
- The project team should obtain advice before describing or deploying the system as a medical device.
- Any future storage, remote access, clinical integration, or cloud speech feature requires a separate privacy and security review.

## 13. Milestones

### Milestone −1 — Fail-fast proof of concept

**Question:** Is a keyboard-to-large-text-to-speech appliance both constructable and plausibly valuable?

The thinnest demonstrable vertical slice has been built:

- Raspberry Pi 4 connected to a development network
- Python demo application launched and observed on the Pi
- SSH used for development, diagnostics, and simulated message input
- Bluetooth keyboard paired and used for direct message entry
- One HDMI display showing large, high-contrast text
- Text-to-speech for the current message
- Minimal correction and clear actions
- Automatic desktop-session startup has also been added after the original construction test

Demonstration status:

1. **Construction demonstration — passed:** enter, correct, display, speak, repeat, stop, and clear a message through the Bluetooth keyboard. Multiline wrapping, automatic startup, and HDMI audio are also working.
2. **Value demonstration — pending:** show the working loop to the family stroke patient and, when feasible, an SLP, OT, nurse, or other appropriate clinician. Ask whether this warrants a supervised patient trial and what would prevent its use.

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

**Current exit decision:** **proceed cautiously** with supervised validation and appliance hardening. Technical feasibility is established. Potential clinical value is plausible but not yet established by a structured patient or clinician evaluation. This does not establish clinical effectiveness, safety, or bedside readiness.

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

**Technical status:** substantially complete on the bench. The required user-supervised exit test remains.

### Milestone 2 — Bedside prototype

- Reliable automatic startup
- Bluetooth keyboard with USB fallback
- Mirrored second HDMI display
- Accessibility settings
- Safe physical placement and cable management
- Clear fault/status indications

**Exit criterion:** repeated bedside rehearsals succeed without developer intervention.

**Current progress:** automatic launch, Bluetooth input, HDMI display, and HDMI speech are working. Remaining work includes power-loss protection, a deliberate shutdown switch, enclosure and cable design, USB recovery testing, second-display validation, and repeated no-developer rehearsals.

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
- Verify `keyd` remapping after boot, keyboard sleep, disconnect, recharge, and reconnection
- Verify that the physical shutdown control cannot be triggered by ordinary typing
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
| HXMJ special key sends a power event or system shortcut | Device-specific `keyd` remap plus logind power-key ignore rule; verify after every rebuild |
| Accidental key presses alter or erase text | Undo, debounce/key-repeat controls, protected clear |
| Patient tires quickly | Adjustable placement, short sessions, minimal actions |
| Message is visible to unintended people | Privacy mode, deliberate screen placement, no history |
| Speech is too quiet or unclear | Volume/speed controls, tested local voices, visible text remains primary |
| TV input is unavailable or prohibited | Treat second display as optional, never required |
| Power loss corrupts the microSD filesystem | Add a deliberate shutdown switch, enable overlay/read-only protection after configuration is stable, and test abrupt-power recovery |
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

## 18. Current implementation increment

**Objective:** Turn the working POC into a repeatable, safer appliance without expanding the communication interface prematurely.

**Near-term work:**

1. Correct the setup documentation so the Trixie `keyd` instructions use the supported `reload` command and do not use the unavailable `check` command.
2. Confirm cold-boot application startup, keyboard reconnection, remapping, audio routing, and first-utterance behavior on the rebuilt Pi.
3. Add and test a clearly labeled physical control that requests a graceful shutdown rather than directly cutting power.
4. After the software and device configuration are stable, evaluate Raspberry Pi overlay/read-only filesystem protection and test recovery from abrupt power removal.
5. Measure the Pi, ROADOM display, connectors, cable bends, and shutdown control before producing a Pi 4 enclosure design with a carry handle and the engraved name “AWW-Some Blackboard.”
6. Run the structured value demonstration with the family stroke patient and seek SLP/OT or other appropriate clinical feedback.

**Validation target:** A caregiver can power on the unit, wait for the communication screen, type and speak a multiline message, clear it deliberately, and shut the unit down safely without SSH or developer intervention.

## 19. Rebuild and configuration record

The Pi has been intentionally reimaged and rebuilt from scratch as an early test of project reproducibility. Important implementation facts that must remain in the setup documentation are:

- Appliance host name: `awwsome` (normally reached as `awwsome.local` when local name resolution is available)
- Application checkout: `/home/an/projects/stroke-communication-aid`
- Application entry point: `poc/app.py`
- Git remote transport: SSH using a dedicated GitHub key such as `~/.ssh/awwsome_github`
- Bluetooth keyboard device ID: `04e8:7021:ed42078f`
- Current keyboard input event path observed during setup: `/dev/input/event6` (diagnostic only; do not encode this changing path in configuration)
- `keyd` executable on the installed Trixie package: `/usr/bin/keyd.rvaiya`
- HXMJ remapping file: `/etc/keyd/hxmj.conf`
- Power-key fail-safe file: `/etc/systemd/logind.conf.d/awwsome-keyboard.conf`
- Audio path: PipeWire to the HDMI sink associated with the ROADOM display

The source repository is the authoritative location for application and documentation changes. Local IDE metadata and host-specific connection files should not be treated as portable project configuration.

## 20. Definition of project success

Success is not the number of features. Success is a patient being able to communicate an intended message more independently, accurately, comfortably, and reliably—while retaining control over what is displayed and spoken.
