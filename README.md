# Student Attendance Management System

A menu-driven Python command-line application for maintaining a class list, recording daily attendance, and generating student and class reports. Student details and attendance records are saved in a JSON file so they remain available after the program closes.

## Features

- Add, view, search, and delete students
- Prevent duplicate roll numbers and reject empty student details
- Mark attendance as Present or Absent for a selected date
- Replace an existing day's attendance after confirmation
- Edit an individual student's attendance record
- View per-student summaries, including attendance percentage and a warning below 75%
- View the attendance status for a selected date
- See class-wide totals and overall attendance rate on the dashboard
- Export a student attendance summary to CSV
- Save data automatically in `attendance_data.json`

## Requirements

- Python 3.8 or newer (uses only Python standard-library modules)
- A terminal or command prompt

## Run

Save the program as `attendance.py`, open a terminal in its folder, and run:

```bash
python attendance.py
```

On some systems, use `python3 attendance.py` instead.

## Menu

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

## Data files

- `attendance_data.json` stores the student list and date-wise attendance. It is created beside the Python file when data is saved.
- `attendance_report.csv` is created beside the Python file when the CSV export option is used.
- Dates use the `DD-MM-YYYY` format. Attendance is recorded using `P` for Present and `A` for Absent (uppercase or lowercase).

The CSV contains one row per student with roll number, name, present days, absent days, and attendance percentage. Attendance percentage is calculated from the dates on which that student has a saved status. A student with no recorded attendance has a percentage of 0.0%.

## Course project

- **Course:** CSE 1021 - Introduction To Problem Solving And Programming
- **Author:** Aaditya Singh Jhala (26BCE11113)
