import sqlite3
from tkinter import *
from tkinter import ttk

# Crear la base de datos y la tabla de alumnos
conexion = sqlite3.connect("alumnos.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INTEGER NOT NULL
)
""")
conexion.commit()


def agregar_alumno(nombre, apellido, edad):
    cursor.execute("INSERT INTO alumnos (nombre, apellido, edad) VALUES (?, ?, ?)", (nombre, apellido, edad))
    conexion.commit()

def seleccionar_alumno(id_alumno):
    cursor.execute("SELECT * FROM alumnos WHERE id=?", (id_alumno,))
    return cursor.fetchone()

def actualizar_alumno(id_alumno, nombre, apellido, edad):
    cursor.execute("UPDATE alumnos SET nombre=?, apellido=?, edad=? WHERE id=?", (nombre, apellido, edad, id_alumno))
    conexion.commit()

def eliminar_alumno(id_alumno):
    cursor.execute("DELETE FROM alumnos WHERE id=?", (id_alumno,))
    conexion.commit()

root = Tk()

# Crear los elementos de la interfaz (etiquetas, campos de texto y botones)
nombre_label = Label(root, text="Nombre")
nombre_entry = Entry(root)
apellido_label = Label(root, text="Apellido")
apellido_entry = Entry(root)
edad_label = Label(root, text="Edad")
edad_entry = Entry(root)
agregar_button = Button(root, text="Agregar", command=lambda: agregar_alumno(nombre_entry.get(), apellido_entry.get(), int(edad_entry.get())))

# Colocar los elementos en la ventana
nombre_label.grid(row=0, column=0)
nombre_entry.grid(row=0, column=1)
apellido_label.grid(row=1, column=0)
apellido_entry.grid(row=1, column=1)
edad_label.grid(row=2, column=0)
edad_entry.grid(row=2, column=1)
agregar_button.grid(row=3, column=1)

root.mainloop()
