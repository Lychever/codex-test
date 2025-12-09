"""Desktop GUI for the Chibi Fantasy inspired character creator.

This lightweight Tkinter app is meant for quick local testing and can be
embedded into a larger game launcher while the main game is in development.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from character_creator import (
    ELEMENTS,
    HOMETOWNS,
    JOBS,
    SPECIES,
    STYLES,
    generate_character,
    pick_random_choice,
    random_name,
)


class CharacterCreatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Chibi Fantasy 2 Character Maker")
        self.root.geometry("560x540")

        self.name_var = tk.StringVar()
        self.species_var = tk.StringVar(value=list(SPECIES.keys())[0])
        self.job_var = tk.StringVar(value=list(JOBS.keys())[0])
        self.hometown_var = tk.StringVar(value=list(HOMETOWNS.keys())[0])
        self.style_var = tk.StringVar(value=list(STYLES.keys())[0])
        self.element_var = tk.StringVar(value=ELEMENTS[0])

        self._build_form()
        self._build_buttons()
        self._build_output()

    def _build_form(self) -> None:
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.X)

        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=4)
        ttk.Entry(frame, textvariable=self.name_var, width=30).grid(
            row=0, column=1, columnspan=2, sticky=tk.W, pady=4
        )

        self._add_combobox(frame, "Species", self.species_var, list(SPECIES.keys()), 1)
        self._add_combobox(frame, "Job", self.job_var, list(JOBS.keys()), 2)
        self._add_combobox(
            frame, "Hometown", self.hometown_var, list(HOMETOWNS.keys()), 3
        )
        self._add_combobox(frame, "Style", self.style_var, list(STYLES.keys()), 4)
        self._add_combobox(frame, "Element", self.element_var, ELEMENTS, 5)

    def _build_buttons(self) -> None:
        frame = ttk.Frame(self.root, padding=(10, 0))
        frame.pack(fill=tk.X)

        ttk.Button(frame, text="Fill Random", command=self.fill_random).pack(
            side=tk.LEFT, padx=(0, 10), pady=6
        )
        ttk.Button(frame, text="Generate", command=self.generate).pack(
            side=tk.LEFT, pady=6
        )

    def _build_output(self) -> None:
        output_frame = ttk.LabelFrame(self.root, text="Character Sheet", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))

        self.output = tk.Text(output_frame, height=18, wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.insert(tk.END, "Choose your options and click Generate.")
        self.output.configure(state=tk.DISABLED)

    def _add_combobox(
        self, frame: ttk.Frame, label: str, var: tk.StringVar, values: list[str], row: int
    ) -> None:
        ttk.Label(frame, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Combobox(frame, textvariable=var, values=values, state="readonly", width=30).grid(
            row=row, column=1, columnspan=2, sticky=tk.W, pady=4
        )

    def fill_random(self) -> None:
        if not self.name_var.get():
            self.name_var.set(random_name())
        self.species_var.set(pick_random_choice(SPECIES))
        self.job_var.set(pick_random_choice(JOBS))
        self.hometown_var.set(pick_random_choice(HOMETOWNS))
        self.style_var.set(pick_random_choice(STYLES))
        self.element_var.set(pick_random_choice({el: {} for el in ELEMENTS}))

    def generate(self) -> None:
        try:
            character = generate_character(
                name=self.name_var.get() or random_name(),
                species=self.species_var.get(),
                job=self.job_var.get(),
                hometown=self.hometown_var.get(),
                style=self.style_var.get(),
                element=self.element_var.get(),
            )
        except Exception as exc:  # pragma: no cover - defensive UI handling
            messagebox.showerror("Error", str(exc))
            return

        self._display_character(character.describe())

    def _display_character(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)


def launch_app() -> None:
    root = tk.Tk()
    CharacterCreatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_app()
