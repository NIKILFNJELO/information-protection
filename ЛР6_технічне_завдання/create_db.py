import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS students")

c.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    faculty TEXT,
    gpa INTEGER,
    scholarship INTEGER
)
""")

students = [
    ("Буман Микита", "ФІТ", 82, "2600"),
    ("Марія Коваль", "ФЕМ", 75, "2000"),
    ("Анна Литвин", "ЮФ", 85, "2600"),
    ("Олег Романюк", "ФІТ", 62, "0")
]

c.executemany("INSERT INTO students (name, faculty, gpa, scholarship) VALUES (?, ?, ?, ?)", students)
conn.commit()
conn.close()

print("Database created with updated scholarships!")
