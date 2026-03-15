import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

# --- jouw business logic ---
def verwerk_excel(input_pad):
    df = pd.read_excel(input_pad)

    # voorbeeldbewerking
    df["verwerkt"] = True

    output_pad = os.path.splitext(input_pad)[0] + "_output.xlsx"
    df.to_excel(output_pad, index=False)

    return output_pad


# --- UI ---
class ExcelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Verwerker")
        self.root.geometry("420x180")
        self.root.resizable(False, False)

        self.bestand = None

        tk.Label(root, text="Stap 1: Kies een Excel-bestand").pack(pady=10)

        tk.Button(
            root,
            text="Kies bestand",
            command=self.kies_bestand
        ).pack()

        self.label_bestand = tk.Label(root, text="Nog geen bestand gekozen")
        self.label_bestand.pack(pady=5)

        tk.Button(
            root,
            text="Verwerk",
            command=self.verwerk,
            state="disabled"
        ).pack(pady=15)

        self.verwerk_knop = root.winfo_children()[-1]

    def kies_bestand(self):
        pad = filedialog.askopenfilename(
            title="Kies een Excel-bestand",
            filetypes=[("Excel bestanden", "*.xlsx *.xls")]
        )

        if pad:
            self.bestand = pad
            self.label_bestand.config(text=os.path.basename(pad))
            self.verwerk_knop.config(state="normal")

    def verwerk(self):
        try:
            output = verwerk_excel(self.bestand)
            messagebox.showinfo(
                "Klaar",
                f"Bestand succesvol verwerkt!\n\nOutput:\n{output}"
            )
        except Exception as e:
            messagebox.showerror(
                "Fout",
                f"Er ging iets mis:\n{e}"
            )


# --- start app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelApp(root)
    root.mainloop()
