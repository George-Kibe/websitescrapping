import sqlite3
import tempfile
import unittest
from pathlib import Path

import openpyxl

from storage import HEADINGS, Entry, save_to_excel, save_to_sqlite

ENTRY = Entry("Ada", "Lovelace", "Ms.", 36, "Europe", "Registered", 3, 2)


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_excel_writes_header_once_and_appends_rows(self):
        path = self.dir / "data.xlsx"
        save_to_excel(ENTRY, path)
        save_to_excel(ENTRY, path)
        rows = list(openpyxl.load_workbook(path).active.values)
        self.assertEqual(list(rows[0]), HEADINGS)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1][:2], ("Ada", "Lovelace"))

    def test_sqlite_creates_table_and_inserts(self):
        path = self.dir / "data.db"
        save_to_sqlite(ENTRY, path)
        save_to_sqlite(ENTRY, path)
        with sqlite3.connect(path) as conn:
            rows = conn.execute("SELECT firstname, age, num_courses FROM student_data").fetchall()
        conn.close()
        self.assertEqual(rows, [("Ada", 36, 3), ("Ada", 36, 3)])


if __name__ == "__main__":
    unittest.main()
