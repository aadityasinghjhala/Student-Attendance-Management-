# Student Attendance Management System

A menu-driven Python command-line application for maintaining a class roster, recording daily attendance, and reviewing student and class reports. Student records and attendance are saved locally in JSON so they are available when the program is started again.

## Features

- Add, view, search, and delete students
- Reject empty student details and duplicate roll numbers
- Mark each student's status as Present or Absent for a chosen date
- Replace an existing day's attendance after confirmation
- Edit a student's status for a saved date
- View individual attendance totals and percentages, with a warning below 75%
- View a date-wise report and a class dashboard
- Export a student summary as CSV
- Persist records in `attendance_data.json`

## Technologies and tools

- Python 3.8 or newer
- Python standard library: `csv`, `json`, `os`, and `datetime`
- Terminal or command prompt
- JSON for local data storage and CSV for report export

## Installation and run

1. Install Python 3.8 or newer.
2. Place the program source in a file named `attendance.py`.
3. Open a terminal in the folder containing `attendance.py`.
4. Start the program:

```bash
python attendance.py
```

On systems where Python is invoked as `python3`, use `python3 attendance.py`.

## How to use

Choose an option from the menu:

| Option | Action |
| --- | --- |
| 1 | Add Student |
| 2 | View Students |
| 3 | Mark Attendance |
| 4 | Attendance Report |
| 5 | Search Student |
| 6 | Daily Report |
| 7 | Dashboard |
| 8 | Delete Student |
| 9 | Edit Attendance |
| 10 | Export Report (CSV) |
| 11 | Exit |

Dates must be entered as `DD-MM-YYYY`. For each student, enter `P` for Present or `A` for Absent; lowercase letters are also accepted.

## Data files

- `attendance_data.json` is created beside `attendance.py` when records are saved. It contains the roster and date-wise attendance.
- `attendance_report.csv` is created in the same folder when option 10 is selected. It includes each student's roll number, name, present days, absent days, and attendance percentage.

Attendance percentage is calculated from the dates on which a student has a saved status. A student without attendance records has a percentage of 0.0%.

## Instructions for testing

Run `python attendance.py` and perform this manual check using sample data:

1. Add a student with a name and roll number, then try adding the same roll number again. The second entry should be rejected.
2. Add another student, mark attendance for a valid date using `P` and `A`, and view the attendance report and daily report.
3. Enter an invalid date and an invalid status to confirm the program asks for valid input.
4. Edit a saved status and check that the individual summary and dashboard reflect the change.
5. Export the CSV and confirm `attendance_report.csv` contains the expected student rows and totals.
6. Exit and start the program again; confirm the roster and attendance are still present.

These are manual usage checks; no automated test suite is included.

## Course project

- **Course:** CSE 1021 - Introduction To Problem Solving And Programming
- **Author:** Aaditya Singh Jhala (26BCE11113)
