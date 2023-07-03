import tkinter as tk
import sqlite3
from tkinter import messagebox

connection = sqlite3.connect('clientes.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL);
""")

class Cliente:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

class Interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title('Gestión de Clientes')

        # Lista de clientes
        self.clientes_list = tk.Listbox(ventana)
        self.clientes_list.grid(row=0, column=0, columnspan=2)      
        
        # Botones de acción
        tk.Button(ventana, text='Agregar Cliente', command=self.agregar_cliente).grid(row=1, column=0, columnspan=2)
        tk.Button(ventana, text='Modificar', command=self.modificar).grid(row=2, column=0)
        tk.Button(ventana, text='Borrar', command=self.borrar).grid(row=2, column=1)
        tk.Button(ventana, text='Buscar', command=self.buscar).grid(row=3, column=0, columnspan=2)

        self.actualizar_lista()

    def actualizar_lista(self):
        # Vaciar la lista de clientes
        self.clientes_list.delete(0, tk.END)

        # Consulta a la base de datos
        rows = cursor.execute("SELECT * FROM clientes").fetchall()

        # Rellenar la lista
        for row in rows:
            self.clientes_list.insert(tk.END, str(row[0]) + " - " + row[1] + " " + row[2])

    def agregar_cliente(self):
        # Muestra un nuevo cuadro de dialogo para agregar un cliente
        AgregarClienteDialog(self)
        
    def modificar(self):
        id_cliente = int(self.clientes_list.get(self.clientes_list.curselection()).split(" - ")[0])
        cliente_data = cursor.execute("SELECT * FROM clientes WHERE id=?", (id_cliente,)).fetchone()

        # Muestra el cuadro de dialogo de modificación
        ModificarClienteDialog(self, cliente_data)

    def borrar(self):
        id_cliente = int(self.clientes_list.get(self.clientes_list.curselection()).split(" - ")[0])
        cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
        connection.commit()
        
        self.actualizar_lista()

    def buscar(self):
        BusquedaClienteDialog(self)

class AgregarClienteDialog:
    def __init__(self, parent):
        self.parent = parent  
        self.top = tk.Toplevel(parent.ventana)
        
        # Entry widgets y labels
        tk.Label(self.top, text='Nombre:').grid(row=0, column=0)
        self.nombre = tk.Entry(self.top)
        self.nombre.grid(row=0, column=1)

        tk.Label(self.top, text='Apellido:').grid(row=1, column=0)
        self.apellido = tk.Entry(self.top)
        self.apellido.grid(row=1, column=1)
        
        # Botón de guardar
        tk.Button(self.top, text='Guardar', command=self.guardar).grid(row=2, column=0, columnspan=2)
    
    def guardar(self):      
        cursor.execute("INSERT INTO clientes (nombre, apellido) VALUES (?, ?)", (self.nombre.get(), self.apellido.get()))
        connection.commit()
        
        # Cerrar el dialogo y actualizar la lista
        self.top.destroy()
        self.parent.actualizar_lista()

class ModificarClienteDialog:
    def __init__(self, parent, cliente_data):
        self.top = tk.Toplevel(parent.ventana)
        self.parent = parent
        
        # Entry widgets y labels
        tk.Label(self.top, text='Nombre:').grid(row=0, column=0)
        self.nombre = tk.Entry(self.top)
        self.nombre.insert(tk.END, cliente_data[1])
        self.nombre.grid(row=0, column=1)

        tk.Label(self.top, text='Apellido:').grid(row=1, column=0)
        self.apellido = tk.Entry(self.top)
        self.apellido.insert(tk.END, cliente_data[2])
        self.apellido.grid(row=1, column=1)
        
        # Botón de guardar
        tk.Button(self.top, text='Guardar cambios', command=lambda: self.guardar(cliente_data[0])).grid(row=2, column=0, columnspan=2)
    
    def guardar(self, id_cliente):      
        cursor.execute("UPDATE clientes SET nombre=?, apellido=? WHERE id=?", (self.nombre.get(), self.apellido.get(), id_cliente))
        connection.commit()

        # Cerrar el dialogo y actualizar la lista
        self.top.destroy()
        self.parent.actualizar_lista()

class BusquedaClienteDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent.ventana)
        
        # Entry widget y label
        tk.Label(self.top, text='Nombre/Apellido:').grid(row=0, column=0)
        self.nombre_apellido = tk.Entry(self.top)
        self.nombre_apellido.grid(row=0, column=1)
        
        # Botón de buscar
        tk.Button(self.top, text='Buscar', command=self.buscar).grid(row=1, column=0, columnspan=2)
        
        # Lista de resultados
        self.resultados = tk.Listbox(self.top)
        self.resultados.grid(row=2, column=0, columnspan=2)
    
    def buscar(self):
        # Vaciar la lista de resultados
        self.resultados.delete(0, tk.END)

        # Consulta a la base de datos
        rows = cursor.execute("SELECT * FROM clientes WHERE nombre LIKE ? OR apellido LIKE ?", ('%'+self.nombre_apellido.get()+'%', '%'+self.nombre_apellido.get()+'%')).fetchall()
        
        # Rellena el listbox con los resultados
        for row in rows:
            self.resultados.insert(tk.END, str(row[0]) + " - " + row[1] + " " + row[2])


ventana = tk.Tk()
interfaz = Interfaz(ventana)
ventana.mainloop()
