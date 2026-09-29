import subprocess
import tkinter as tk
import html


BACKGROUND = "#101418"
FOREGROUND = "#FFFFFF"
STATUS_COLOR = "#B8C2CC"
WARNING_COLOR = "#FFCC80"
HEADER_BACKGROUND = "#202830"
PANEL_BACKGROUND = "#2B3640"

FONT_FAMILY = "DejaVu Sans"
MESSAGE_FONT_SIZE = 48
SPEECH_RATE = 120

AUDIO_DEVICE = "pipewire"


class CommunicationApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        self.message = ""
        self.cursor_position = 0

        self.clear_pending = False
        self.delete_released = True
        self.help_visible = False

        self.espeak_process = None
        self.aplay_process = None

        root.title("Stroke Communication Aid")
        root.configure(
            background=BACKGROUND,
            cursor="none",
        )
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.focus_force()

        root.grid_rowconfigure(0, weight=0)
        root.grid_rowconfigure(1, weight=0)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.create_header()
        self.create_status()
        self.create_message_display()
        self.create_help_display()

        root.bind("<Escape>", self.show_help)

        root.bind_all(
            "<KeyPress>",
            self.handle_keypress,
        )

        root.bind_all(
            "<KeyRelease-Delete>",
            self.handle_delete_release,
        )

        self.update_message_display()

    def create_header(self) -> None:
        header = tk.Frame(
            self.root,
            background=HEADER_BACKGROUND,
            padx=12,
            pady=10,
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        for column in range(3):
            header.grid_columnconfigure(
                column,
                weight=1,
            )

        title = tk.Label(
            header,
            text="Stroke Communication Aid",
            background=HEADER_BACKGROUND,
            foreground=FOREGROUND,
            font=(FONT_FAMILY, 18, "bold"),
            pady=4,
        )
        title.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
        )

        help_label = tk.Label(
            header,
            text=(
                "ENTER: Speak / Stop     "
                "BACKSPACE: Correct     "
                "DELETE twice: Clear"
            ),
            background=HEADER_BACKGROUND,
            foreground="#DCE6EE",
            font=(FONT_FAMILY, 14),
            pady=6,
        )
        help_label.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
        )

        self.create_command_panel(
            parent=header,
            column=0,
            key_name="ENTER",
            action="SPEAK / STOP",
            color="#B9F6CA",
        )

        self.create_command_panel(
            parent=header,
            column=1,
            key_name="BACKSPACE",
            action="CORRECT",
            color="#FFF59D",
        )

        self.create_command_panel(
            parent=header,
            column=2,
            key_name="DELETE TWICE",
            action="CLEAR",
            color="#FFAB91",
        )

    def create_command_panel(
        self,
        parent: tk.Frame,
        column: int,
        key_name: str,
        action: str,
        color: str,
    ) -> None:
        panel = tk.Frame(
            parent,
            background=PANEL_BACKGROUND,
            padx=10,
            pady=8,
        )
        panel.grid(
            row=2,
            column=column,
            sticky="nsew",
            padx=6,
        )

        action_label = tk.Label(
            panel,
            text=action,
            background=PANEL_BACKGROUND,
            foreground=color,
            font=(FONT_FAMILY, 14, "bold"),
        )
        action_label.pack()

        key_label = tk.Label(
            panel,
            text=key_name,
            background=PANEL_BACKGROUND,
            foreground=FOREGROUND,
            font=(FONT_FAMILY, 14),
        )
        key_label.pack(pady=(3, 0))

    def create_status(self) -> None:
        self.status = tk.Label(
            self.root,
            text="Ready",
            background=BACKGROUND,
            foreground=STATUS_COLOR,
            font=(FONT_FAMILY, 18),
            pady=8,
        )
        self.status.grid(
            row=1,
            column=0,
            sticky="ew",
        )

    def create_message_display(self) -> None:
        self.message_label = tk.Label(
            self.root,
            text="",
            background=BACKGROUND,
            foreground=FOREGROUND,
            font=(
                FONT_FAMILY,
                MESSAGE_FONT_SIZE,
                "bold",
            ),
            justify="center",
            anchor="center",
            padx=50,
            pady=30,
        )
        self.message_label.grid(
            row=2,
            column=0,
            sticky="nsew",
        )

        self.message_label.bind(
            "<Configure>",
            self.resize_message_wrap,
        )

    def create_help_display(self) -> None:
        self.help_frame = tk.Frame(
            self.root,
            background=BACKGROUND,
            padx=18,
            pady=12,
        )

        for column in range(3):
            self.help_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="help",
            )

        self.help_frame.grid_rowconfigure(
            2,
            weight=1,
        )

        title = tk.Label(
            self.help_frame,
            text="Commands and Troubleshooting",
            background=BACKGROUND,
            foreground=FOREGROUND,
            font=(FONT_FAMILY, 18, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(0, 2),
        )

        subtitle = tk.Label(
            self.help_frame,
            text="( AWW-Some Blackboard )",
            background=BACKGROUND,
            foreground=STATUS_COLOR,
            font=(FONT_FAMILY, 14),
        )
        subtitle.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(0, 12),
        )

        edit_panel = self.create_help_panel(
            column=0,
            title="EDIT COMMANDS",
        )

        self.add_help_item(
            edit_panel,
            "BACKSPACE",
            "Correct the previous character",
        )

        self.add_help_item(
            edit_panel,
            "Arrows  ←  →",
            "Move through the message",
        )

        self.add_help_item(
            edit_panel,
            "DELETE twice",
            "Clear the complete message",
        )

        speech_panel = self.create_help_panel(
            column=1,
            title="SPEECH CONTROLS",
        )

        self.add_help_item(
            speech_panel,
            "ENTER",
            "Speak / Stop / Repeat",
        )

        self.add_help_item(
            speech_panel,
            "F10",
            "Mute / Unmute",
        )

        self.add_help_item(
            speech_panel,
            "F11 / F12",
            "Volume down / up",
        )

        troubleshooting_panel = self.create_help_panel(
            column=2,
            title="TROUBLESHOOTING",
        )

        self.add_help_item(
            troubleshooting_panel,
            "HELP",
            "Press ESC to return",
        )

        self.add_help_item(
            troubleshooting_panel,
            "KEYBOARD NOT WORKING",
            (
                "1. Turn the keyboard off\n"
                "2. Wait 5 seconds\n"
                "3. Turn the keyboard on\n"
                "4. Wait for it to reconnect\n"
                "5. Type to get attention"
            ),
        )

        self.add_help_item(
            troubleshooting_panel,
            "BLACKBOARD NOT WORKING",
            (
                "1. Unplug the power cord\n"
                "2. Wait 5 seconds\n"
                "3. Plug the power cord back in\n"
                "4. Wait for the device to start"
            ),
        )

        # Build the help display at startup, but keep it
        # hidden until the patient presses ESC.
        self.help_frame.grid_remove()

    def create_help_panel(
        self,
        column: int,
        title: str,
    ) -> tk.Frame:
        panel = tk.Frame(
            self.help_frame,
            background=PANEL_BACKGROUND,
            padx=16,
            pady=14,
        )

        panel.grid(
            row=2,
            column=column,
            sticky="nsew",
            padx=6,
        )

        heading = tk.Label(
            panel,
            text=title,
            background=PANEL_BACKGROUND,
            foreground=FOREGROUND,
            font=(FONT_FAMILY, 18, "bold"),
            anchor="w",
            justify="left",
        )
        heading.pack(
            anchor="w",
            pady=(0, 14),
        )

        return panel

    def add_help_item(
        self,
        panel: tk.Frame,
        key_name: str,
        description: str,
    ) -> None:
        key_label = tk.Label(
            panel,
            text=key_name,
            background=PANEL_BACKGROUND,
            foreground=FOREGROUND,
            font=(FONT_FAMILY, 14, "bold"),
            anchor="w",
            justify="left",
        )
        key_label.pack(
            anchor="w",
        )

        description_label = tk.Label(
            panel,
            text=description,
            background=PANEL_BACKGROUND,
            foreground="#DCE6EE",
            font=(FONT_FAMILY, 14),
            anchor="w",
            justify="left",
            wraplength=330,
        )
        description_label.pack(
            anchor="w",
            fill="x",
            pady=(2, 14),
        )

    def resize_message_wrap(
        self,
        event: tk.Event,
    ) -> None:
        self.message_label.configure(
            wraplength=max(
                200,
                event.width - 100,
            )
        )

    def show_help(self) -> None:
        """Display help without changing the patient's message."""
        self.help_visible = True

        self.message_label.grid_remove()
        self.status.grid_remove()

        self.help_frame.grid(
            row=1,
            column=0,
            rowspan=2,
            sticky="nsew",
        )

    def hide_help(self) -> None:
        """Return to the patient's message."""
        self.help_visible = False

        self.help_frame.grid_remove()

        self.status.grid()
        self.message_label.grid()

        self.update_message_display()
        self.set_default_status()

    def toggle_help(self) -> None:
        if self.help_visible:
            self.hide_help()
        else:
            self.show_help()

    def handle_keypress(
        self,
        event: tk.Event,
    ) -> str:
        key = event.keysym

        if key in {"XF86HomePage", "Escape"}:
            self.toggle_help()
            return "break"

        if self.help_visible:
            return "break"

        if key == "Delete":
            self.handle_delete()
            return "break"

        if self.clear_pending:
            self.cancel_clear()

        if key in {"Return", "KP_Enter"}:
            self.toggle_speech()
            return "break"

        if key == "BackSpace":
            self.backspace()
            return "break"

        if key == "Left":
            self.cursor_position = max(
                0,
                self.cursor_position - 1,
            )
            self.update_message_display()
            return "break"

        if key == "Right":
            self.cursor_position = min(
                len(self.message),
                self.cursor_position + 1,
            )
            self.update_message_display()
            return "break"

        if key == "Home":
            self.cursor_position = 0
            self.update_message_display()
            return "break"

        if key == "End":
            self.cursor_position = len(
                self.message
            )
            self.update_message_display()
            return "break"

        if (
            event.char
            and event.char.isprintable()
        ):
            self.insert_character(
                event.char
            )

        return "break"

    def insert_character(
        self,
        character: str,
    ) -> None:
        self.message = (
            self.message[
                : self.cursor_position
            ]
            + character
            + self.message[
                self.cursor_position :
            ]
        )

        self.cursor_position += len(
            character
        )

        self.update_message_display()

    def backspace(self) -> None:
        if self.cursor_position == 0:
            return

        self.message = (
            self.message[
                : self.cursor_position - 1
            ]
            + self.message[
                self.cursor_position :
            ]
        )

        self.cursor_position -= 1
        self.update_message_display()

    def update_message_display(self) -> None:
        displayed_message = (
            self.message[
                : self.cursor_position
            ]
            + "▌"
            + self.message[
                self.cursor_position :
            ]
        )

        self.message_label.configure(
            text=displayed_message
        )

    def toggle_speech(self) -> None:
        if self.speech_is_running():
            self.stop_speech()
        else:
            self.speak_message()

    def speak_message(self) -> None:
        message = self.message.strip()

        spoken_message = (
            '<speak><break time="750ms"/>'
            + html.escape(message)
            + "</speak>"
        )

        if not message:
            self.set_status(
                "Type a message before speaking."
            )
            return

        self.stop_speech(
            show_default_status=False
        )

        self.set_status(
            "Speaking — press ENTER to stop"
        )

        try:
            self.espeak_process = (
                subprocess.Popen(
                    [
                        "espeak-ng",
                        "-m",
                        "-s",
                        str(SPEECH_RATE),
                        "--stdout",
                        spoken_message,
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                )
            )

            self.aplay_process = (
                subprocess.Popen(
                    [
                        "pw-play",
                        "--latency=500ms",
                        "-",
                    ],
                    stdin=(
                        self.espeak_process.stdout
                    ),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            )

            if (
                self.espeak_process.stdout
                is not None
            ):
                self.espeak_process.stdout.close()

            self.root.after(
                200,
                self.check_speech_status,
            )

        except OSError as error:
            self.stop_speech(
                show_default_status=False
            )

            self.set_status(
                f"Speech error: {error}"
            )

    def speech_is_running(self) -> bool:
        return (
            self.aplay_process is not None
            and self.aplay_process.poll()
            is None
        )

    def check_speech_status(self) -> None:
        if self.aplay_process is None:
            return

        if self.aplay_process.poll() is None:
            self.root.after(
                200,
                self.check_speech_status,
            )
            return

        self.cleanup_speech_processes()
        self.set_default_status()

    def stop_speech(
        self,
        show_default_status: bool = True,
    ) -> None:
        for process in (
            self.aplay_process,
            self.espeak_process,
        ):
            if (
                process is not None
                and process.poll() is None
            ):
                process.terminate()

        self.cleanup_speech_processes()

        if show_default_status:
            self.set_default_status()

    def cleanup_speech_processes(
        self,
    ) -> None:
        for process in (
            self.aplay_process,
            self.espeak_process,
        ):
            if process is None:
                continue

            try:
                process.wait(timeout=0.2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

        self.aplay_process = None
        self.espeak_process = None

    def handle_delete(self) -> None:
        if not self.clear_pending:
            self.clear_pending = True
            self.delete_released = False

            self.stop_speech(
                show_default_status=False
            )

            self.status.configure(
                text=(
                    "Clear this message? "
                    "Press DELETE again "
                    "to confirm. "
                    "Press any typing key "
                    "to cancel."
                ),
                foreground=WARNING_COLOR,
            )
            return

        if self.delete_released:
            self.clear_message()

    def handle_delete_release(
        self,
        _event=None,
    ) -> None:
        if self.clear_pending:
            self.delete_released = True

    def clear_message(self) -> None:
        self.stop_speech(
            show_default_status=False
        )

        self.message = ""
        self.cursor_position = 0
        self.clear_pending = False
        self.delete_released = True

        self.update_message_display()

        self.set_status(
            "Message cleared — begin typing"
        )

    def cancel_clear(self) -> None:
        self.clear_pending = False
        self.delete_released = True
        self.set_default_status()

    def set_status(
        self,
        message: str,
    ) -> None:
        self.status.configure(
            text=message,
            foreground=STATUS_COLOR,
        )

    def set_default_status(self) -> None:
        self.set_status("Ready")


def main() -> None:
    root = tk.Tk()
    CommunicationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()