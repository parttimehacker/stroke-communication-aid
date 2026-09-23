Hackster.io Project Draft

This document contains paste-ready material for the Hackster.io project builder.

Basics

Title

Stroke Communication Aid: A Raspberry Pi Voice

Short description

A Bluetooth keyboard, large HDMI display, and offline speech provide a simpler communication path for a family stroke patient.

Recommended publication settings

Field

Recommendation

Project type

Work in Progress with build instructions

Difficulty

Intermediate

Estimated build time

4–6 hours after Raspberry Pi OS is installed

License

Select before publication; no license is assumed in this draft

Visibility while editing

Private

Change the project to a tutorial only after another person can reproduce the build and the supervised value demonstration has been recorded.

Suggested tags

Raspberry Pi

Accessibility

Assistive Technology

AAC

Bluetooth

Python

Text to Speech

Stroke

Healthcare

HDMI

Things used in this project

Hardware

Quantity

Component

Notes

1

Raspberry Pi 4 Model B

Prototype computer

1

ROADOM 10.1-inch 1024×600 HDMI touchscreen

Primary display and speakers

1

HXMJ Large Print Mini Bluetooth Keyboard

Compact, high-contrast patient input with reduced one-handed reach

1

USB keyboard

Optional recovery input

1

microSD card

Raspberry Pi OS and application

1

Raspberry Pi USB-C power supply

Power the Pi independently

1

ROADOM-compatible power supply

Power the display independently during setup

1

Micro-HDMI-to-HDMI cable

Pi HDMI0 to ROADOM

1

Appropriate USB cable

ROADOM touch connection to Pi

1

Development computer

SSH, Git, and optional PyCharm development

Software

Software

Purpose

Raspberry Pi OS with Desktop

Appliance operating system

Python 3

Application runtime

Tkinter

Full-screen interface

eSpeak NG

Offline text-to-speech

PipeWire / pw-play

HDMI audio playback

BlueZ / bluetoothctl

Bluetooth keyboard management

keyd

Device-specific translation of the HXMJ multifunction Delete key

evtest

Verify the raw and translated Linux key events

Git and GitHub

Source and configuration management

labwc

Desktop-session autostart

Tools

No soldering or fabrication is required for the proof of concept.

Story

Why I built this

This project began after I watched a family stroke patient try to communicate with a handheld whiteboard. The stroke had affected both speech and the ability to hold a marker and write legibly.

That experience led to a simple question: could pressing keys with one or more fingers require less fine motor control than forming letters with a marker?

I wanted to fail fast before designing a polished product. The first goal was to prove that a small dedicated appliance could:

Accept input from a Bluetooth keyboard.

Show the complete message in large, readable text.

Let the user correct mistakes without losing the message.

Speak the message locally.

Start automatically after power-on.

Survive the kind of abrupt power removal that may occur with an appliance.

The result is a working Raspberry Pi proof of concept. It demonstrates technical feasibility, but it has not yet demonstrated that keyboard input is suitable for the intended patient.

Important boundary

This is an experimental assistive communication project. It is not a medical device, diagnostic system, nurse-call system, or emergency-call system. It should not replace evaluation by a speech-language pathologist, occupational therapist, or clinical care team.

Stroke can affect language, vision, attention, coordination, comprehension, and fatigue in different ways. Typing will not be appropriate for every stroke survivor. An approved communication method and nurse-call control must remain available.

The prototype

The current appliance consists of:

A Raspberry Pi 4 running Raspberry Pi OS with Desktop

A ROADOM 10.1-inch, 1024×600 HDMI touchscreen with built-in speakers

An HXMJ Large Print Mini Bluetooth Keyboard

A Python/Tkinter full-screen application

eSpeak NG for offline speech

PipeWire for HDMI audio

Desktop autostart

Read-only root and boot protection

The application keeps only the current message in memory. It does not create an account, call a cloud service, or save a transcript.

How it works

Bluetooth/USB keyboard
          |
          v
 Python/Tkinter application ---> eSpeak NG ---> PipeWire ---> HDMI speakers
          |
          +----> ROADOM large-text display
          |
          +----> Optional second HDMI display in a future test

The patient-facing controls use one key at a time:

Key

Action

Character keys

Type into the message

Backspace

Correct the character before the cursor

Left / Right

Move the cursor

Home / End

Move to the beginning or end

Enter

Speak; press again to stop

Delete, release, Delete

Clear the message

The two-press clear sequence requires a key release, so keyboard auto-repeat cannot erase the message by itself. Any typing key cancels a pending clear.

There is no patient-facing exit command.

Hardware assembly

Power everything off before making connections.

Connect the Pi 4 HDMI0 port—the micro-HDMI port nearest the USB-C power connector—to the ROADOM HDMI input.

Connect the ROADOM touch/data USB port to a USB port on the Pi.

Power the ROADOM through its designated power connection.

Power the Pi using a suitable Pi USB-C power supply.

Insert the prepared microSD card.

Power the display, then boot the Pi.

For initial testing I powered the display and Pi separately. This avoids confusing display problems with Pi undervoltage.

The application does not currently require touch; the USB touch connection is available for future caregiver controls.

Media placeholder: Add a clear photograph of the assembled Pi, ROADOM, keyboard, power connections, HDMI cable, and touch USB cable.

Prepare Raspberry Pi OS

Install Raspberry Pi OS with Desktop and configure a user account, hostname, Wi-Fi or Ethernet, and SSH.

Update the system and install the dependencies:

sudo apt update
sudo apt full-upgrade -y
sudo apt install -y git python3 python3-tk espeak-ng pipewire-bin keyd evtest

Clone the project:

mkdir -p /home/an/projects
cd /home/an/projects
git clone https://github.com/parttimehacker/stroke-communication-aid.git
cd stroke-communication-aid
python3 -m py_compile poc/app.py

Replace /home/an in these instructions if your Pi uses another username.

Pair the Bluetooth keyboard

Put the keyboard into pairing mode, then use SSH to run:

sudo systemctl enable --now bluetooth
sudo rfkill unblock bluetooth
bluetoothctl

At the bluetoothctl prompt:

power on
agent on
default-agent
pairable on
scan on

When the keyboard appears, note its actual Bluetooth address. Replace <ADDRESS> in the commands below:

pair <ADDRESS>
trust <ADDRESS>
connect <ADDRESS>
info <ADDRESS>
scan off
quit

If a pairing code appears, type the code on the Bluetooth keyboard and press its Enter key. Verify that info reports:

Paired: yes
Trusted: yes
Connected: yes

Open a local text editor on the Pi and type with the keyboard. This proves that it is generating local input rather than merely appearing in the device list.

Configure the HXMJ keyboard's Delete key

I selected the HXMJ Large Print Mini Bluetooth Keyboard because its compact width reduces one-handed reach and its high-contrast legends are easier to locate. The keyboard connected to the Pi as a standard Bluetooth HID device, but one key required special handling.

The key intended for clearing the message did not initially generate Linux KEY_DELETE. In the keyboard's Apple-oriented mode it generated KEY_POWER, which started a Pi shutdown. After switching keyboard modes it generated KEY_LEFTMETA plus KEY_L, the standard screen-lock shortcut. Because the intended user must not be required to hold a modifier key, the correction belongs in the appliance configuration rather than in the patient workflow.

First, prevent a raw Bluetooth power-key event from shutting down the appliance if the remapper is ever unavailable:

sudo mkdir -p /etc/systemd/logind.conf.d
sudo nano /etc/systemd/logind.conf.d/awwsome-keyboard.conf

Add:

[Login]
HandlePowerKey=ignore
HandlePowerKeyLongPress=ignore

Reboot, then identify the HXMJ keyboard's actual keyd device ID:

sudo /usr/bin/keyd.rvaiya monitor

Press the problem key once, record the ID shown beside Bluetooth Keyboard, and press Ctrl-C. Do not copy the ID from this project: determine the ID reported for your own keyboard.

Create the device-specific mapping:

sudo nano /etc/keyd/hxmj.conf

Replace <HXMJ_DEVICE_ID> with the ID reported by keyd monitor:

[ids]
<HXMJ_DEVICE_ID>

[main]
leftmeta+l = delete
power = delete

Validate and activate the configuration:

sudo /usr/bin/keyd.rvaiya check /etc/keyd/hxmj.conf
sudo systemctl enable --now keyd
sudo /usr/bin/keyd.rvaiya reload
sudo systemctl restart keyd

On Raspberry Pi OS based on Debian Trixie, the Debian package installs this implementation as /usr/bin/keyd.rvaiya, even though the package and service are named keyd.

Verify the translated event:

sudo evtest

Select keyd virtual keyboard, press the physical key once, and confirm that it reports KEY_DELETE. Selecting the original Bluetooth keyboard will still show the raw firmware-generated events.

The mapping is limited to the identified HXMJ keyboard. Other connected recovery keyboards retain their normal mappings. The application can therefore continue to use two separate Delete presses to clear the complete message.

Configure ROADOM HDMI audio

List the available PipeWire sinks:

wpctl status

Find the HDMI sink. Its numerical ID is assigned by the running system and should not be hard-coded.

wpctl set-default <HDMI_SINK_ID>
wpctl set-mute <HDMI_SINK_ID> 0
wpctl set-volume <HDMI_SINK_ID> 1.0

Test the speakers:

pw-play --target <HDMI_SINK_ID> /usr/share/sounds/alsa/Front_Center.wav

The ROADOM also has its own hardware volume. Both the display volume and the Pi volume may need adjustment.

During development I found that the generic ALSA default route did not open correctly on the new Pi, while PipeWire playback worked. The application therefore uses pw-play and follows the selected system output.

The ROADOM also clipped the start of the first speech stream after being idle. The application adds a short silent SSML pre-roll to each eSpeak stream, allowing the HDMI audio path to wake before the first word.

Run the application

From the desktop:

cd /home/an/projects/stroke-communication-aid
python3 poc/app.py

From SSH while the desktop session is active:

cd /home/an/projects/stroke-communication-aid
DISPLAY=:0 python3 poc/app.py

The application should open full-screen. Type:

I need some water

Test the complete loop:

Type the sentence.

Move the cursor and correct a character.

Press Enter and hear the complete message.

Press Enter during speech to stop.

Press Enter again to repeat.

Press and release Delete, then press Delete again.

Type a second sentence and confirm that the first sentence does not reappear or get spoken.

During development, stop the full-screen program from SSH:

pkill -f "/poc/app.py"

Media placeholder: Add a photograph showing “I need some water” centered on the ROADOM.

Start automatically after boot

Use sudo raspi-config to enable:

System Options
  Boot / Auto Login
  Desktop Autologin

Confirm the desktop is using labwc:

pgrep -a labwc

Create or edit:

/home/an/.config/labwc/autostart

Add:

(sleep 3; /usr/bin/python3 /home/an/projects/stroke-communication-aid/poc/app.py >> /home/an/strokecom-startup.log 2>&1) &

The three-second delay allows the display and user PipeWire session to initialize. Reboot and verify that the application appears automatically:

sudo reboot

If it fails to start, inspect:

tail -50 /home/an/strokecom-startup.log

Protect the SD card

The intended user may remove power without performing an operating-system shutdown. I therefore enabled Raspberry Pi OS's overlay filesystem only after the application, Bluetooth, audio, autostart, and Git repository were working.

Before enabling the overlay:

Test a cold boot.

Commit and push all permanent changes.

Confirm that the Git working tree is clean.

Preferably make a known-good microSD image.

Run:

sudo raspi-config

Select:

Performance Options
  Overlay File System

Enable both the root overlay and boot-partition write protection.

Runtime changes are then stored in RAM and disappear at reboot. This substantially reduces filesystem-corruption risk, but it does not protect against every possible SD-card, power-supply, or hardware failure.

To perform maintenance:

Disable overlay and boot protection.

Reboot.

Update and test the system.

Commit and push permanent changes.

Re-enable both protections.

Reboot and repeat the appliance test.

Problems encountered

The keyboard appeared paired but did not connect

The Pi's Bluetooth radio was initially soft-blocked. rfkill unblock bluetooth, followed by pairing, trusting, and connecting the actual device address, resolved the problem.

Earlier text was spoken again

The first interface used an editable text widget with a global key binding. Pressing Enter inserted a hidden newline before the speech handler ran. The visible field appeared cleared, but hidden content remained.

The application now owns an explicit message string and cursor position. The display label renders that model, so hidden widget content cannot be spoken.

Long messages lost their earlier text

A single-line entry control was replaced with a centered label driven by the explicit message model. The label uses word wrapping and can display multiple lines.

Function-key and modifier commands were unsuitable

The intended user may type with one finger. Controls such as Fn+F5 or Ctrl+L were removed. Normal communication now uses one key at a time.

The HXMJ Delete key requested shutdown or screen lock

The compact HXMJ keyboard uses an Apple/mobile-oriented multifunction layout. Linux evtest showed that its Delete-position key emitted KEY_POWER in one mode and KEY_LEFTMETA plus KEY_L in another. The first event requested shutdown; the second requested screen lock.

A device-specific keyd configuration now translates either sequence into KEY_DELETE. A systemd-logind override ignores raw keyboard power events as a fail-safe. This preserves the single-key patient interface without changing other paired keyboards.

The first spoken message was clipped

Increasing PipeWire latency did not solve the problem. Adding actual silence at the start of the same speech stream gave the HDMI audio path time to wake.

Abrupt power removal could corrupt the SD card

The stable build now uses a RAM overlay with read-only root and boot storage. Persistent maintenance requires deliberately leaving appliance mode.

Current results

The construction demonstration passes:

The Pi boots into the communication screen.

The Bluetooth keyboard enters and edits text.

The compact HXMJ large-print keyboard reconnects and its remapped Clear key generates KEY_DELETE without requesting shutdown or screen lock.

Long messages wrap across multiple centered lines.

The message is spoken offline through ROADOM HDMI audio.

Speech can be stopped and repeated.

Clearing requires two deliberate Delete presses.

A new message does not contain hidden text from an earlier message.

Root and boot storage are protected during appliance operation.

The value demonstration remains pending. The prototype has not yet established that the intended patient can use it comfortably, independently, or more effectively than available alternatives.

Next step

The next step is not another feature. It is a supervised observation with the intended user, family, and—when feasible—an SLP, OT, nurse, or other appropriate clinician.

I want to learn:

Can the person locate and press the needed keys?

Is the display readable from the normal position?

Are correction, Speak, Stop, and Clear understandable?

How much time, effort, and fatigue are involved?

Does the device offer an advantage over the whiteboard or other AAC?

Should the project proceed, pivot, or stop?

Safety and privacy

Do not use this prototype as an emergency or nurse-call system.

Keep an approved call control and another communication method available.

Do not assume that typing performance establishes comprehension or decision-making capacity.

Do not store patient conversations by default.

Position the screen to limit unintended viewing.

Review cables, stands, cleaning, electrical power, Bluetooth policy, and infection control with the facility.

Obtain clinical guidance before patient use.

Code

Source repository:

https://github.com/parttimehacker/stroke-communication-aid

Primary application:

poc/app.py

Supporting documentation:

README.md

PROJECT.md

Schematics and connection documentation

No custom circuit board or electronic schematic is required. The project uses standard HDMI, USB, and power connections.

Create one uploadable connection diagram showing:

Pi USB-C power supply → Raspberry Pi 4

Raspberry Pi HDMI0 → ROADOM HDMI input

Raspberry Pi USB → ROADOM touch/data port

ROADOM power supply → ROADOM power input

Bluetooth keyboard ⇢ Raspberry Pi

Media checklist before publication

Do not include the patient's face, name, medical chart, room number, hospital identifiers, or private messages.

Cover image: Pi, ROADOM, and keyboard together with a neutral sample message.

Connection image: Rear or side view showing labeled cables.

Screen image: Large centered “I need some water” message.

Command image: Header showing Speak/Stop, Correct, and Clear.

Short demonstration video: Power-on → type → correct → speak → stop → repeat → clear.

Optional comparison image: Whiteboard and appliance without identifying a patient.

Optional screenshot: GitHub repository or simplified architecture diagram.

Upload the demonstration video to YouTube or Vimeo, public or unlisted, and embed its link in the Hackster story.

Final publication checklist

Exact Bluetooth keyboard brand and model added: HXMJ Large Print Mini Bluetooth Keyboard

Raspberry Pi RAM size recorded

Raspberry Pi OS version recorded

Photographs added with useful captions

Demonstration video embedded

Source repository is public and current

README and PROJECT documentation are current

License decision recorded

Build time confirmed

Difficulty selected

Tags selected

Work in Progress status selected

No identifying patient information included

Safety boundary appears near the beginning

Supervised value demonstration clearly marked pending
