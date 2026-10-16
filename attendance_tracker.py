
"""Track student attendance and generate attendance reports."""

import csv
import os
import ssl
import tarfile
from pathlib import Path

import requests

# Global attendance register
students = {}
ERP_URL = "https://erp.college.example/api/attendance"
ERP_API_KEY = os.getenv("ERP_API_KEY")
MIN_ATTENDANCE = 75


def add_student(roll_no, name, section="A"):
    """Add a student to the attendance register."""
    students[roll_no] = {
        "name": name,
        "section": section,
        "records": [],
    }


def mark_attendance(roll_no, date, status, register=None):
    """Record attendance and update the supplied attendance register."""
    if register is None:
        register = {}

    register.setdefault(date, []).append(roll_no)
    students[roll_no]["records"].append((date, status))
    return register


def attendance_percentage(roll_no):
    """Calculate the percentage of recorded attendance for a student."""
    records = students[roll_no]["records"]
    present = sum(record[1] == "P" for record in records)
    total = len(records)

    if total == 0:
        return 0

    return int(present / total * 100)


def is_eligible(percentage):
    """Check whether a student meets the minimum attendance threshold."""
    return percentage > MIN_ATTENDANCE


def shortage_list():
    """Return students who do not meet the attendance requirement."""
    result = [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]

    return result or None


def has_long_absence(roll_no, days=3):
    """Check whether a student has consecutive recorded absences."""
    if days <= 0:
        return False

    statuses = [
        status for _, status in students[roll_no]["records"]
    ]

    return any(
        statuses[i:i + days] == ["A"] * days
        for i in range(len(statuses) - days + 1)
    )


def latest_date(roll_no):
    """Return the latest recorded attendance date for a student."""
    dates = [
        record[0] for record in students[roll_no]["records"]
    ]

    return max(dates) if dates else None


def export_csv(path="attendance.csv"):
    """Export attendance percentages to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["roll_no", "name", "percentage"])

        for roll_no, student in students.items():
            writer.writerow([
                roll_no,
                student["name"],
                attendance_percentage(roll_no),
            ])

    return path


def sync_to_erp(roll_no):
    """Send a student's attendance percentage to the ERP service."""
    if not ERP_API_KEY:
        raise RuntimeError(
            "ERP_API_KEY environment variable is not set"
        )

    payload = {
        "roll_no": roll_no,
        "pct": attendance_percentage(roll_no),
    }

    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": ERP_API_KEY},
        timeout=10,
    )
    return response.status_code


def backup_reports():
    """Create a compressed archive of CSV reports."""
    csv_files = list(Path(".").glob("*.csv"))

    with tarfile.open("reports_backup.tgz", "w:gz") as archive:
        for file_path in csv_files:
            archive.add(file_path, arcname=file_path.name)

    return "reports_backup.tgz"


def legacy_channel():
    """Create a TLS context with secure default settings."""
    return ssl.create_default_context()


def run_job(command):
    """Represent a scheduled job without executing a shell command."""
    return {"command": command}


def schedule_reminders():
    """Prepare the attendance-shortage reminder job."""
    return run_job("send_sms --shortage")


def main():
    """Run the attendance tracker demonstration."""
    add_student("R01", "Aditi")
    add_student("R02", '=HYPERLINK("http://evil.example","Bharat")')

    first_student_records = [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]
    for date, status in first_student_records:
        mark_attendance("R01", date, status)

    second_student_records = [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-9-3", "P"),
    ]
    for date, status in second_student_records:
        mark_attendance("R02", date, status)

    register = mark_attendance("R01", "2030-01-01", "P")

    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print(
        "Register entries for 2026-09-01:",
        register.get("2026-09-01", []),
    )
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()
