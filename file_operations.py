import json
from tkinter import messagebox

ATTENDANCE_FILE = "attendance.json"

def save_attendance(data):
    try:
        with open(ATTENDANCE_FILE, "r") as file:
            attendance_records = json.load(file)
    except FileNotFoundError:
        attendance_records = []

    attendance_records.append(data)

    with open(ATTENDANCE_FILE, "w") as file:
        json.dump(attendance_records, file, indent=4)
    messagebox.showinfo("Éxito", "Asistencia registrada exitosamente.")

def load_attendance():
    try:
        with open(ATTENDANCE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def update_attendance_file(dni):
    attendance_records = load_attendance()
    updated_records = [record for record in attendance_records if record["dni"] != dni]
    with open(ATTENDANCE_FILE, "w") as file:
        json.dump(updated_records, file, indent=4)
