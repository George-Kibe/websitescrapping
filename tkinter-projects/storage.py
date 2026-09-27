"""Where submitted form entries are saved."""

import sqlite3
from dataclasses import astuple, dataclass, fields
from pathlib import Path

import openpyxl

DATA_DIR = Path(__file__).parent


@dataclass
class Entry:
    firstname: str
    lastname: str
    title: str
    age: int
    nationality: str
    registration_status: str
    num_courses: int
    num_semesters: int


HEADINGS = ["First Name", "Last Name", "Title", "Age", "Nationality",
            "Registration status", "# Courses", "# Semesters"]


def save_to_console(entry: Entry) -> None:
    for heading, value in zip(HEADINGS, astuple(entry), strict=True):
        print(f"{heading}: {value}")
    print("-" * 40)


def save_to_excel(entry: Entry, path: Path = DATA_DIR / "data.xlsx") -> None:
    if path.exists():
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(HEADINGS)
    sheet.append(list(astuple(entry)))
    workbook.save(path)


def save_to_sqlite(entry: Entry, path: Path = DATA_DIR / "data.db") -> None:
    columns = [f.name for f in fields(Entry)]
    with sqlite3.connect(path) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS student_data (
                firstname TEXT, lastname TEXT, title TEXT, age INTEGER, nationality TEXT,
                registration_status TEXT, num_courses INTEGER, num_semesters INTEGER)"""
        )
        conn.execute(
            f"INSERT INTO student_data ({', '.join(columns)}) VALUES ({', '.join('?' * len(columns))})",
            astuple(entry),
        )
    conn.close()


BACKENDS = {"console": save_to_console, "excel": save_to_excel, "sqlite": save_to_sqlite}
