"""
Student Attendance Management System
------------------------------------
A menu-driven, command-line program for keeping a class list and
recording daily attendance (Present / Absent).

Course  : CSE 1021 - Introduction To Problem Solving And Programming
Author  : Aaditya Singh Jhala (26BCE11113)

How the data is stored
    students   : list of dictionaries, e.g. {"name": "Riya Verma", "roll": "102"}
    attendance : dictionary of dictionaries,
                 e.g. {"30-09-2026": {"101": "Present", "102": "Absent"}}
Both are saved to attendance_data.json after every change and loaded again
when the program starts, so nothing is lost when the program is closed.

Run with:  python attendance.py
"""

import csv
import json
import os
from datetime import datetime

# ----------------------------------------------------------------------
# Settings and global data
# ----------------------------------------------------------------------
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_FOLDER, "attendance_data.json")
REPORT_FILE = os.path.join(BASE_FOLDER, "attendance_report.csv")
DATE_FORMAT = "%d-%m-%Y"      # dates are typed and stored as DD-MM-YYYY
MINIMUM_PERCENTAGE = 75       # below this a student gets a warning

students = []
attendance = {}


# ----------------------------------------------------------------------
# Saving and loading
# ----------------------------------------------------------------------
def save_data():
    """Write the students list and attendance dictionary to the JSON file."""
    data = {"students": students, "attendance": attendance}
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=2)
    except OSError:
        print("Warning: could not save data to file.")


def load_data():
    """Read saved data at start-up. If there is no file yet, start empty."""
    global students, attendance

    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        students = data["students"]
        attendance = data["attendance"]
    except (OSError, ValueError, KeyError):
        # A damaged file should not crash the program
        print("Saved data could not be read. Starting with empty records.")
        students = []
        attendance = {}


# ----------------------------------------------------------------------
# Small input helpers
# ----------------------------------------------------------------------
def read_date(prompt):
    """Keep asking until the user types a real date in DD-MM-YYYY format.

    The date is returned in the same format (01-1-2026 becomes 01-01-2026),
    so the same day is never stored under two different spellings.
    """
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, DATE_FORMAT).strftime(DATE_FORMAT)
        except ValueError:
            print("Invalid date. Use DD-MM-YYYY, for example 30-09-2026.")


def read_status(prompt):
    """Keep asking until the user types P or A (capital or small letter)."""
    while True:
        status = input(prompt).strip().upper()
        if status == "P":
            return "Present"
        if status == "A":
            return "Absent"
        print("Enter only P or A.")


def ask_yes_no(prompt):
    """Return True if the user types y or yes, otherwise False."""
    return input(prompt).strip().lower() in ("y", "yes")


def find_student(roll):
    """Return the student dictionary with this roll number, or None."""
    for student in students:
        if student["roll"] == roll:
            return student
    return None


# ----------------------------------------------------------------------
# Student management
# ----------------------------------------------------------------------
def add_student():
    """Add a student after checking for empty values and duplicate rolls."""
    name = input("Enter student name: ").strip()
    roll = input("Enter roll number: ").strip()

    if name == "" or roll == "":
        print("Please enter all details.")
        return

    if find_student(roll) is not None:
        print("Roll number already exists.")
        return

    students.append({"name": name, "roll": roll})
    save_data()
    print("Student added.")


def view_students():
    """Print every student as 'roll - name'."""
    if len(students) == 0:
        print("No students found.")
        return

    print("\nStudent List")
    for student in students:
        print(student["roll"], "-", student["name"])


def delete_student():
    """Delete a student and every attendance entry of that student."""
    roll = input("Enter roll number: ").strip()
    student = find_student(roll)

    if student is None:
        print("Student not found.")
        return

    if not ask_yes_no("Delete " + student["name"] + "? (y/n): "):
        print("Delete cancelled.")
        return

    students.remove(student)

    # Remove the roll number from every date, then drop dates that are
    # now empty so they are not counted as attendance days.
    for date in list(attendance):
        attendance[date].pop(roll, None)
        if len(attendance[date]) == 0:
            del attendance[date]

    save_data()
    print("Student deleted.")


# ----------------------------------------------------------------------
# Attendance management
# ----------------------------------------------------------------------
def mark_attendance():
    """Ask P or A for every student on a chosen date and save the result."""
    if len(students) == 0:
        print("Add students first.")
        return

    date = read_date("Enter date (DD-MM-YYYY): ")

    if date in attendance:
        if not ask_yes_no("Attendance for this date exists. Replace it? (y/n): "):
            print("Nothing changed.")
            return

    record = {}
    for student in students:
        record[student["roll"]] = read_status(
            student["roll"] + " " + student["name"] + " (P/A): "
        )

    attendance[date] = record
    save_data()
    print("Attendance saved.")


def edit_attendance():
    """Change the status of one student on one date."""
    date = read_date("Enter date (DD-MM-YYYY): ")

    if date not in attendance:
        print("No attendance found.")
        return

    roll = input("Enter roll number: ").strip()
    student = find_student(roll)

    if student is None or roll not in attendance[date]:
        print("No record for this student on that date.")
        return

    print("Current status:", attendance[date][roll])
    attendance[date][roll] = read_status("New status (P/A): ")
    save_data()
    print("Attendance updated.")


def get_attendance(roll):
    """Return (present days, absent days, percentage) for one roll number.

    Only dates on which this student has an entry are counted.
    """
    present = 0
    absent = 0

    for date in attendance:
        if roll in attendance[date]:
            if attendance[date][roll] == "Present":
                present = present + 1
            else:
                absent = absent + 1

    total = present + absent

    # total can be zero for a new student, so check before dividing
    if total > 0:
        percentage = (present / total) * 100
    else:
        percentage = 0.0

    return present, absent, percentage


# ----------------------------------------------------------------------
# Reports
# ----------------------------------------------------------------------
def print_student_summary(student):
    """Print the attendance figures of one student."""
    p, a, per = get_attendance(student["roll"])

    print("Name:", student["name"])
    print("Roll:", student["roll"])
    print("Present:", p)
    print("Absent:", a)
    print("Attendance:", round(per, 1), "%")

    if (p + a) > 0 and per < MINIMUM_PERCENTAGE:
        print("Warning: below", MINIMUM_PERCENTAGE, "% attendance.")


def attendance_report():
    """Print present days, absent days and percentage for every student."""
    if len(students) == 0:
        print("No students found.")
        return

    for student in students:
        print()
        print_student_summary(student)


def search_student():
    """Show every student whose name or roll number contains the text."""
    search = input("Enter name or roll number: ").strip().lower()

    if search == "":
        print("Please enter a name or roll number.")
        return

    found = 0
    for student in students:
        if search in student["name"].lower() or search in student["roll"].lower():
            found = found + 1
            print("\nStudent Found")
            print_student_summary(student)

    if found == 0:
        print("Student not found.")


def daily_report():
    """Print the status of every student on one date."""
    date = read_date("Enter date (DD-MM-YYYY): ")

    if date not in attendance:
        print("No attendance found.")
        return

    print("\nAttendance for", date)

    for student in students:
        roll = student["roll"]
        # a student added after this date has no entry for it
        status = attendance[date].get(roll, "Not Marked")
        print(roll, "-", student["name"], "-", status)


def dashboard():
    """Print overall figures for the whole class."""
    present = 0
    absent = 0

    for date in attendance:
        for roll in attendance[date]:
            if attendance[date][roll] == "Present":
                present = present + 1
            else:
                absent = absent + 1

    total = present + absent

    if total > 0:
        percentage = (present / total) * 100
    else:
        percentage = 0.0

    print("\nDashboard")
    print("Total Students:", len(students))
    print("Total Present:", present)
    print("Total Absent:", absent)
    print("Attendance Rate:", round(percentage, 1), "%")
    print("Total Days:", len(attendance))


def export_csv():
    """Save the attendance report of all students to a CSV file."""
    if len(students) == 0:
        print("No students found.")
        return

    try:
        with open(REPORT_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Roll", "Name", "Present", "Absent", "Percentage"])
            for student in students:
                p, a, per = get_attendance(student["roll"])
                writer.writerow([student["roll"], student["name"], p, a, round(per, 1)])
    except OSError:
        print("Could not write the CSV file.")
        return

    print("Report saved to attendance_report.csv")


# ----------------------------------------------------------------------
# Main menu
# ----------------------------------------------------------------------
def main():
    """Load saved data, then show the menu until the user chooses Exit."""
    load_data()

    while True:
        print("\n===== STUDENT ATTENDANCE SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Mark Attendance")
        print("4. Attendance Report")
        print("5. Search Student")
        print("6. Daily Report")
        print("7. Dashboard")
        print("8. Delete Student")
        print("9. Edit Attendance")
        print("10. Export Report (CSV)")
        print("11. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            mark_attendance()

        elif choice == "4":
            attendance_report()

        elif choice == "5":
            search_student()

        elif choice == "6":
            daily_report()

        elif choice == "7":
            dashboard()

        elif choice == "8":
            delete_student()

        elif choice == "9":
            edit_attendance()

        elif choice == "10":
            export_csv()

        elif choice == "11":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
