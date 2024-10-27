import tkinter as tk
from tkinter import messagebox
import os

def execute_other_script():
    # Llama al otro script de Python
    os.system('python other_script.py')  # Ajusta la ruta si es necesario

# Crear la ventana principal
root = tk.Tk()
root.title("Mi Aplicación Tkinter")

# Establecer el icono (ajusta la ruta al icono)
#root.iconbitmap("icono.ico")

# Establecer el tamaño de la ventana para que sea un cuarto de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 2  # Un cuarto de ancho
window_height = screen_height // 2  # Un cuarto de alto
root.geometry(f"{window_width}x{window_height}")

# Establecer color de fondo verde claro
root.configure(bg="lightgreen")

# Configurar las fuentes
label_font = ("Tahoma", 12)

# Labels
label1 = tk.Label(root, text="Primera Opción:", font=label_font, bg="lightgreen")
label2 = tk.Label(root, text="Segunda Opción:", font=label_font, bg="lightgreen")

# Variables de selección para los RadioButtons
option = tk.IntVar()

# Radio Buttons
radio1 = tk.Radiobutton(root, text="Opción 1", variable=option, value=1, font=label_font, bg="lightgreen")
radio2 = tk.Radiobutton(root, text="Opción 2", variable=option, value=2, font=label_font, bg="lightgreen")

# Botón para ejecutar otro programa
button = tk.Button(root, text="Ejecutar Otro Programa", font=("Tahoma", 12), command=execute_other_script)

# Posicionamiento usando grid()
label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
radio1.grid(row=0, column=1, padx=10, pady=10)

label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
radio2.grid(row=1, column=1, padx=10, pady=10)

button.grid(row=2, column=0, columnspan=2, pady=20)

# Iniciar el loop principal de la aplicación
root.mainloop()

