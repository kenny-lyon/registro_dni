import tkinter as tk
from ui import on_search, view_attendance

root = tk.Tk()
root.title("Registro de Asistencia")

tk.Label(root, text="DNI:").grid(row=0, column=0, padx=10, pady=5)
dni_entry = tk.Entry(root)
dni_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Button(root, text="Buscar", command=lambda: on_search(dni_entry)).grid(row=0, column=2, padx=10, pady=5)
tk.Button(root, text="Ver Registros", command=view_attendance).grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
