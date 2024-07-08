import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from api import get_dni_data
from file_operations import save_attendance, load_attendance, update_attendance_file

def register_attendance(dni, nombres=None, apellido_paterno=None, apellido_materno=None):
    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attendance_data = {
        "dni": dni,
        "nombres": nombres,
        "apellidoPaterno": apellido_paterno,
        "apellidoMaterno": apellido_materno,
        "fechaRegistro": fecha_registro
    }
    save_attendance(attendance_data)

def on_search(dni_entry):
    dni = dni_entry.get()
    dni_data = get_dni_data(dni)

    if dni_data:
        register_attendance(dni, dni_data["nombres"], dni_data["apellidoPaterno"], dni_data["apellidoMaterno"])
        messagebox.showinfo("Éxito", "Asistencia registrada exitosamente.")
    else:
        messagebox.showwarning("No encontrado", "DNI no encontrado en la API. Por favor, ingrese los datos manualmente.")
        open_manual_registration(dni)

def open_manual_registration(dni):
    manual_window = tk.Toplevel()
    manual_window.title("Registro Manual")

    tk.Label(manual_window, text="DNI:").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(manual_window, textvariable=tk.StringVar(value=dni), state='readonly').grid(row=0, column=1, padx=10, pady=5)

    tk.Label(manual_window, text="Nombres:").grid(row=1, column=0, padx=10, pady=5)
    nombres_var = tk.StringVar()
    tk.Entry(manual_window, textvariable=nombres_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(manual_window, text="Apellido Paterno:").grid(row=2, column=0, padx=10, pady=5)
    apellido_paterno_var = tk.StringVar()
    tk.Entry(manual_window, textvariable=apellido_paterno_var).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(manual_window, text="Apellido Materno:").grid(row=3, column=0, padx=10, pady=5)
    apellido_materno_var = tk.StringVar()
    tk.Entry(manual_window, textvariable=apellido_materno_var).grid(row=3, column=1, padx=10, pady=5)

    def on_manual_register():
        register_attendance(dni, nombres_var.get(), apellido_paterno_var.get(), apellido_materno_var.get())
        manual_window.destroy()

    tk.Button(manual_window, text="Registrar", command=on_manual_register).grid(row=4, column=0, columnspan=2, pady=10)

def view_attendance():
    attendance_records = load_attendance()
    view_window = tk.Toplevel()
    view_window.title("Registros de Asistencia")

    columns = ("DNI", "Nombres", "Apellido Paterno", "Apellido Materno", "Fecha de Registro")
    tree = ttk.Treeview(view_window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for record in attendance_records:
        tree.insert("", tk.END, values=(record["dni"], record["nombres"], record["apellidoPaterno"], record["apellidoMaterno"], record["fechaRegistro"]))

    tree.pack(expand=True, fill='both')

    def delete_record(event):
        if not tree.selection():
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")
            return

        item = tree.selection()[0]
        values = tree.item(item, "values")
        dni_to_delete = values[0]
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el registro del DNI {dni_to_delete}?")
        if confirm:
            tree.delete(item)
            update_attendance_file(dni_to_delete)

    menu = tk.Menu(view_window, tearoff=0)
    menu.add_command(label="Eliminar", command=lambda: delete_record(None))
    tree.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))
