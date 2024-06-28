import sqlite3

Con = sqlite3.connect("Database.db")
Cur = Con.cursor()

Course = input("Enter course name: ")


Cur.execute("INSERT INTO C(CourseName) VALUES (?)", (Course))

Con.commit()
