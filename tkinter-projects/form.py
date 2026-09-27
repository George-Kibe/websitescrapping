"""The data entry form window."""

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk

from storage import Entry

TITLES = ["", "Mr.", "Ms.", "Dr."]
CONTINENTS = ["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"]


class DataEntryForm(ttk.Frame):
    def __init__(self, master: tk.Misc, on_submit: Callable[[Entry], None]):
        super().__init__(master, padding=10)
        self.on_submit = on_submit
        self._build_user_info()
        self._build_course_info()
        self._build_terms()
        ttk.Button(self, text="Enter data", command=self.submit).grid(
            row=3, column=0, sticky="news", padx=20, pady=10
        )

    def _build_user_info(self) -> None:
        frame = ttk.LabelFrame(self, text="User Information")
        frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        self.first_name = ttk.Entry(frame)
        self.last_name = ttk.Entry(frame)
        self.title_combo = ttk.Combobox(frame, values=TITLES, state="readonly")
        self.age = ttk.Spinbox(frame, from_=18, to=110)
        self.age.set(18)
        self.nationality = ttk.Combobox(frame, values=CONTINENTS, state="readonly")

        for column, (label, widget) in enumerate(
            [("First Name", self.first_name), ("Last Name", self.last_name), ("Title", self.title_combo)]
        ):
            ttk.Label(frame, text=label).grid(row=0, column=column)
            widget.grid(row=1, column=column)
        for column, (label, widget) in enumerate([("Age", self.age), ("Nationality", self.nationality)]):
            ttk.Label(frame, text=label).grid(row=2, column=column)
            widget.grid(row=3, column=column)

        for widget in frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    def _build_course_info(self) -> None:
        frame = ttk.LabelFrame(self, text="Courses")
        frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

        self.registered = tk.BooleanVar(value=False)
        self.num_courses = ttk.Spinbox(frame, from_=0, to=100)
        self.num_semesters = ttk.Spinbox(frame, from_=0, to=100)
        self.num_courses.set(0)
        self.num_semesters.set(0)

        ttk.Label(frame, text="Registration Status").grid(row=0, column=0)
        ttk.Checkbutton(frame, text="Currently Registered", variable=self.registered).grid(row=1, column=0)
        ttk.Label(frame, text="# Completed Courses").grid(row=0, column=1)
        self.num_courses.grid(row=1, column=1)
        ttk.Label(frame, text="# Semesters").grid(row=0, column=2)
        self.num_semesters.grid(row=1, column=2)

        for widget in frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    def _build_terms(self) -> None:
        frame = ttk.LabelFrame(self, text="Terms & Conditions")
        frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)
        self.accepted = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="I accept the terms and conditions.", variable=self.accepted).grid(
            row=0, column=0, padx=10, pady=5
        )

    def read_entry(self) -> Entry:
        """Validate the form and return its values; raises ValueError with a user-facing message."""
        if not self.accepted.get():
            raise ValueError("You have not accepted the terms.")
        firstname, lastname = self.first_name.get().strip(), self.last_name.get().strip()
        if not (firstname and lastname):
            raise ValueError("First name and last name are required.")
        try:
            age = int(self.age.get())
            num_courses = int(self.num_courses.get())
            num_semesters = int(self.num_semesters.get())
        except ValueError:
            raise ValueError("Age, courses and semesters must be whole numbers.") from None
        return Entry(
            firstname=firstname,
            lastname=lastname,
            title=self.title_combo.get(),
            age=age,
            nationality=self.nationality.get(),
            registration_status="Registered" if self.registered.get() else "Not registered",
            num_courses=num_courses,
            num_semesters=num_semesters,
        )

    def submit(self) -> None:
        try:
            entry = self.read_entry()
        except ValueError as error:
            messagebox.showwarning(title="Error", message=str(error))
            return
        try:
            self.on_submit(entry)
        except Exception as error:  # e.g. the Excel file is open in another program
            messagebox.showerror(title="Could not save", message=str(error))
            return
        messagebox.showinfo(title="Saved", message=f"Saved {entry.firstname} {entry.lastname}.")
