import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# Crear las tablas de la base de datos si no existen aún
con = sqlite3.connect('clientes.db')
cur = con.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL)
''')
con.commit()

class Cliente:
    def __init__(self, con):
        self.con = con

    def agregar(self, nombre, apellido):
        cur = self.con.cursor()
        cur.execute("INSERT INTO clientes (nombre, apellido) VALUES (?, ?)",
                    (nombre, apellido))
        self.con.commit()

    def eliminar(self, id):
        with self.con:
            self.con.execute("DELETE FROM clientes WHERE id = ?", (id,))


        
    def buscar(self, id):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM clientes WHERE id = ?", (id, ))
        result = cur.fetchall()
        return result

    def actualizar(self, id, nombre, apellido):
        cur = self.con.cursor()
        cur.execute("UPDATE clientes SET nombre = ?, apellido = ? WHERE id = ?",
                    (nombre, apellido, id))
        self.con.commit()

    def obtener(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM clientes")
        result = cur.fetchall()
        return result

    def modificar(self, id, nombre, apellido):
        cur = self.con.cursor()
        cur.execute("UPDATE clientes SET nombre = ?, apellido = ? WHERE id = ?", (nombre, apellido, id))
        self.con.commit()



class ClienteUI:
    def __init__(self, cliente):
        self.cliente = cliente
        self.root = tk.Tk()
        self.root.title("Sandtech")
        self.id = tk.StringVar()
        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        #self.id_Entry = tk.Entry(self.root, textvariable=tk.StringVar())
        #self.id_Entry.pack() 
        self.id_busqueda = tk.StringVar()

    def mostrar(self):
        #self._crear_formulario()
        self._crear_botonera()
        self._crear_tabla()
        self._refrescar_tabla()
        self.root.mainloop()
        
    def _crear_botonera(self):
        tk.Button(self.root, text='Agregar', command=self._agregar_cliente).grid(row=1, column=2)
        tk.Button(self.root, text='Eliminar', command=self._eliminar_cliente).grid(row=2, column=2)
        tk.Button(self.root, text='Buscar', command=self._buscar_cliente).grid(row=5, column=2)

        


    def _buscar_cliente(self):
        id = simpledialog.askstring("Buscar", "Ingrese el ID del cliente:")
        if id:
            self.lista.delete(0, tk.END)
            cliente = self.cliente.buscar(id)
            if cliente:
                for c in cliente:
                    self.lista.insert(tk.END, c)
            else:
                messagebox.showinfo("Error", "Lo siento, no se encontró ningún cliente con ese ID.")
                self._refrescar_tabla()

    def _crear_formulario(self):
        tk.Label(self.root, text="Nombre").grid(row=0)
        tk.Label(self.root, text="Apellido").grid(row=1)

        tk.Entry(self.root, textvariable=self.nombre).grid(row=0, column=1)
        tk.Entry(self.root, textvariable=self.apellido).grid(row=1, column=1)

    def _crear_botonera(self):
        tk.Button(self.root, text='Agregar', command=self._agregar_cliente).grid(row=2, column=0)
        tk.Button(self.root, text='Eliminar', command=self._eliminar_cliente).grid(row=2, column=1)
        tk.Button(
            self.root, 
            text="Modificar cliente", 
            command=self._modificar_cliente
        ).grid(row=2, column=2)


    def _generar_id(self):
        if not hasattr(self, '_ultimo_id'):
            self._ultimo_id = 100
        else:
            self._ultimo_id += 1
        return self._ultimo_id

    def _crear_tabla(self):
        self.lista = tk.Listbox(self.root)
        self.lista.grid(row=3, column=0, columnspan=3)

    def _agregar_cliente(self):
        id = self._generar_id()  # debes definir cómo generar un id
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        
        self.cliente.agregar(nombre, apellido)
        self._refrescar_tabla()
        self.formulario.destroy()  # cerrar el formulario
        self.nombre.set('')  # limpiar campos del formulario
        self.apellido.set('')



    def _eliminar_cliente(self):
        seleccionados = self.lista.curselection()
        if seleccionados:
            item = self.lista.get(seleccionados[0])
            if item:  # Verificar si el item no está vacío
                id = item[0]
                self.cliente.eliminar(id)
                self._refrescar_tabla()
        else:
            messagebox.showinfo("Error", "Por favor, selecciona un cliente para eliminar.")
    
    def _actualizar_cliente(self):
        seleccionados = self.lista.curselection()
        if seleccionados:
            _, id, _, _ = self.lista.get(seleccionados[0]).split(' ')
            nombre = self.nombre.get()
            apellido = self.apellido.get()

            if nombre and apellido:
                self.cliente.actualizar(id, nombre, apellido)
                self._refrescar_tabla()
            else:
                messagebox.showinfo(message="Todos los campos son requeridos", title="Error de validación")

    def _refrescar_tabla(self):
        self.lista.delete(0, tk.END)
        clientes = self.cliente.obtener()
        for cliente in clientes:
            self.lista.insert(tk.END, cliente)

    def _modificar_cliente(self):
        seleccionados = self.lista.curselection()
        if seleccionados:
            item = self.lista.get(seleccionados[0])
            if item:  # Verificar si el item no está vacío
                id = item[0]
                nuevo_nombre = self.nombre.get()
                nuevo_apellido = self.apellido.get()
                if nuevo_nombre and nuevo_apellido:
                    self.cliente.modificar(id, nuevo_nombre, nuevo_apellido)
                    self._refrescar_tabla()
                else:
                    messagebox.showinfo(
                        "Error", "Por favor, completa los campos de nombre y apellido."
                    )
        else:
            messagebox.showinfo("Error", "Por favor, selecciona un cliente para modificar.")
    



cliente = Cliente(con)
ui = ClienteUI(cliente)
ui.mostrar()
