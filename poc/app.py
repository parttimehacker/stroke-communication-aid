import tkinter as tk


BACKGROUND = "#101418"
FOREGROUND = "#FFFFFF"
FONT = ("DejaVu Sans", 52)


class CommunicationApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        root.title("Stroke Communication Aid — POC")
        root.configure(bg=BACKGROUND)
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", self.close)

        self.message = tk.StringVar(value="I need some water")

        message_label = tk.Label(
            root,
            textvariable=self.message,
            background=BACKGROUND,
            foreground=FOREGROUND,
            font=FONT,
            wraplength=1100,
            justify="center",
        )
        message_label.pack(
            expand=True,
            fill="both",
            padx=60,
            pady=60,
        )

    def close(self, _event=None) -> None:
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    CommunicationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
