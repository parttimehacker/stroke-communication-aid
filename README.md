# Stroke Communication Aid

An offline-first Raspberry Pi communication aid for people whose speech
and handwriting have been affected by a stroke.

The current appliance uses a **Raspberry Pi 4**, **JUNEBOX 8-inch
1280×800 HDMI touchscreen with built-in speakers**, and **HXMJ Large
Print Mini Bluetooth Keyboard**. The patient types a message, sees it in
large high-contrast text, and can have it spoken locally with eSpeak NG.

> **Status:** working communication appliance under active hardening and
> validation. It is not a medical device, diagnostic system,
> emergency-call system, or replacement for an SLP, OT, nurse-call
> system, or clinical care team.

## Current patient controls

  Control          Action
  ---------------- ----------------------------
  Character keys   Type
  Backspace        Correct previous character
  Left / Right     Move cursor
  Enter            Speak / stop / repeat
  Delete twice     Clear message
  Esc/Homepage     Toggle Help
  F10              Mute / unmute
  F11 / F12        Volume down / up

The Help screen uses three large panels: **Edit Commands**, **Speech
Controls**, and **Troubleshooting**. It includes keyboard reconnection
and power-cycle recovery instructions.

## Hardware

-   Raspberry Pi 4
-   JUNEBOX 8-inch 1280×800 HDMI touchscreen
-   HXMJ Large Print Mini Bluetooth Keyboard
-   microSD card
-   HDMI and USB touch/data connections
-   Suitable power supply arrangement
-   Optional USB keyboard for recovery

The JUNEBOX touchscreen appears as `TSTP MTouch`. Normal communication
does not require touch, but touch remains available for setup and
caregiver recovery.

## Software

-   Raspberry Pi OS Desktop / Debian Trixie
-   Python 3 + Tkinter
-   eSpeak NG
-   PipeWire / `pw-play`
-   BlueZ / `bluetoothctl`
-   `keyd` / `/usr/bin/keyd.rvaiya`
-   `evtest`
-   labwc desktop autostart
-   Git/GitHub

Application entry point:

``` text
poc/app.py
```

## HXMJ keyboard normalization

The HXMJ multifunction Delete-position key has been observed to emit
several raw events. The tested appliance uses:

``` ini
[ids]
04e8:7021

[main]
leftmeta+l = delete
coffee = delete
power = delete
sysrq = noop
```

On this Trixie `keyd.rvaiya` build, Linux `KEY_SCREENLOCK` is named
`coffee`. F4 emits `KEY_SYSRQ`, so `sysrq = noop` prevents a screenshot
popup. F10/F11/F12 remain useful audio controls.

Restricting `keyd` to `04e8:7021` is important: an unrestricted
configuration can interfere with the JUNEBOX `TSTP MTouch` touchscreen.

If the Bluetooth keyboard sleeps and does not reconnect, switch it off,
wait about five seconds, and switch it back on.

## Run

From the Pi desktop:

``` bash
python3 poc/app.py
```

From SSH while the graphical desktop is active:

``` bash
DISPLAY=:0 python3 poc/app.py
```

Check syntax first with:

``` bash
python3 -m py_compile poc/app.py
```

## Automatic startup

The appliance uses Desktop Autologin and labwc. The autostart entry is:

``` bash
(sleep 3; /usr/bin/python3 /home/an/projects/stroke-communication-aid/poc/app.py >> /home/an/strokecom-startup.log 2>&1) &
```

The delay allows the display and user PipeWire session to initialize.

## Audio

The JUNEBOX speakers work through Pi HDMI0. During diagnosis, ALSA card
0 was the working HDMI path. The application uses eSpeak NG piped to
`pw-play`; system/display volume may both need adjustment.

## Power and recovery

After Linux shutdown, the JUNEBOX power button does not reliably
cold-start the halted Pi. The tested recovery is:

1.  Unplug external power.
2.  Wait about 5 seconds.
3.  Reconnect power.
4.  Wait for Stroke Communication Aid to start.

Overlay/read-only root and boot protection is the next
filesystem-hardening step after the current configuration and
documentation are committed and cold-boot tested.

## Repository

-   `README.md` --- quick current-state overview
-   `PROJECT.md` --- product definition, design decisions, milestones,
    risks, and rebuild record
-   `HACKSTER.md` --- build-story/tutorial draft
-   `poc/app.py` --- current application
-   `art/` --- screenshots and project images

Core communication is offline and message text is kept in memory rather
than stored as a transcript by default.

## Safety boundary

Do not use this device as an emergency or nurse-call system. Keep an
approved call control and another communication method available.
Keyboard suitability and interface choices must be validated with the
individual user and appropriate clinical staff.
