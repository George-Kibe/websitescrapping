"""
Student data entry form built with Tkinter.

Usage:
    python main.py                    # print entries to the console
    python main.py --storage excel    # append entries to data.xlsx
    python main.py --storage sqlite   # insert entries into data.db
"""

import argparse
import tkinter as tk

from form import DataEntryForm
from storage import BACKENDS


def main() -> None:
    parser = argparse.ArgumentParser(description="Student data entry form.")
    parser.add_argument("--storage", choices=BACKENDS, default="console")
    args = parser.parse_args()

    window = tk.Tk()
    window.title("Data Entry Form")
    DataEntryForm(window, on_submit=BACKENDS[args.storage]).pack()
    window.mainloop()


if __name__ == "__main__":
    main()
