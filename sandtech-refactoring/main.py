# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import sqlite3

# Clase POJO que representa al cliente:
class Customer:
    def __init__(self, id, name, surname, address):
        self._id = id
        self._name = name
        self._surname = surname
        self._address = address
        
    # PROPERTIES para clase Customers
       
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

# Clase CustomerManager para mapear datos de la clase Customer a la base de datos
# Aplicando el patron DataMapper de Martin Fowler: 
# https://martinfowler.com/eaaCatalog/dataMapper.html
class CustomerManager:
    def __init__(self):
        self._connection = sqlite3.connect("customers.db")
        self._cursor = self._connection.cursor()
        self._create_table()    
    
    def _create_table(self):
        # Solo va a crear la tabla customers si no existe. 
        # Es mejor no permitir valores nulos
        self._cursor.execute("""          
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, 
                surname TEXT NOT NULL,
                address TEXT NOT NULL
            );
        """)
        # Solo va a insertar el valor 99 de id atoincremental
        # para empezar cn código en valor igual a 100 si no 
        # existe la columna name con el valor 'customers',
        # esto significa que solo se insertará la primera
        # vez que se crea la tabla customers.
        self._cursor.execute("""
            INSERT INTO sqlite_sequence (name, seq)
            SELECT 'customers', 99
            WHERE NOT EXISTS (SELECT 1 FROM sqlite_sequence WHERE name = 'customers')
        """)   
        self._connection.commit()
        
    def insert_customer(self, customer):
        self._cursor.execute("""
            INSERT INTO customers (name, surname, address)
            VALUES (?, ?, ?)
        """, (customer.name, customer.surname, customer.address))
        self._connection.commit()
        print("Cliente agregado correctamente.")

    def delete_customer(self, id):
        self._cursor.execute("DELETE FROM customers WHERE id=?", (id,))
        self._connection.commit()
        print("Cliente eliminado correctamente.")

    def update_customer(self, customer):
        self._cursor.execute("""
            UPDATE customers
            SET name=?, surname=?, address=?
            WHERE id=?
        """, (customer.name, customer.surname, customer.address, customer.id))
        self._connection.commit()
        print("Cliente actualizado correctamente.")

    def get_customer(self, id):
        self._cursor.execute("SELECT * FROM customers WHERE id=?", (id,))
        customer_data = self._cursor.fetchone()
        if customer_data:
            id, name, surname, address = customer_data
            return Customer(id, name, surname, address)
        else:
            print("Cliente no encontrado.")
            return None

    def get_all_customers(self):
        self._cursor.execute("SELECT * FROM customers")
        customers_data = self._cursor.fetchall()
        customers = []
        for customer_data in customers_data:
            id, name, surname, address = customer_data
            customer = Customer(id, name, surname, address)
            customers.append(customer)
        return customers

    def close_connection(self):
        self._cursor.close()
        self._connection.close()

# Clase Application para implementar la vista con Tkinter, observar la herencia:
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Clientes")
        self.geometry("1024x768")

        self.customer_manager = CustomerManager()

        self.create_menu()
        self.create_table_view()

        # Cuando inicia la aplicación refresca la tabla clientes
        self.refresh_table()
        
    # Método que crea el menú:
    def create_menu(self):
        self.menu_bar = tk.Menu(self)

        # Opciones del menú
        customers_menu = tk.Menu(self.menu_bar, tearoff=0)
        customers_menu.add_command(
            label="Dar de alta", command=self.add_customer)
        customers_menu.add_command(
            label="Modificar", command=self.update_customer)
        customers_menu.add_command(
            label="Eliminar", command=self.delete_customer)
        customers_menu.add_command(
            label="Listar todos", command=self.list_all_customers)

        self.menu_bar.add_cascade(label="Clientes", menu=customers_menu)
        self.config(menu=self.menu_bar)

    # Método que crea la vista en tabla para listar todos los clientes.
    def create_table_view(self):
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(padx=10, pady=10)

        self.table = ttk.Treeview(self.table_frame, columns=(
            "id", "name", "surname", "address"))
        self.table.heading("id", text="Código")
        self.table.heading("name", text="Nombre")
        self.table.heading("surname", text="Apellido")
        self.table.heading("address", text="Dirección")
        self.table.pack()

    # Método que refresca la tabla para mostrar los datos de los clientes guardados
    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        customers = self.customer_manager.get_all_customers()
        if customers:
            for customer in customers:
                self.table.insert("", "end", values=(
                    customer.id, customer.name, customer.surname, customer.address))
        else:
            self.table.insert("", "end", values=(
                "No hay clientes cargados.", "", "", ""))
            
    # Método de vista para mostrar el formulario de inserción de un cliente
    def add_customer(self):
        add_window = tk.Toplevel(self)
        add_window.title("Agregar un cliente")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Nombre:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Apellido:").pack()
        surname_entry = tk.Entry(add_window)
        surname_entry.pack()

        tk.Label(add_window, text="Dirección:").pack()
        address_entry = tk.Entry(add_window)
        address_entry.pack()

        def save_customer():
            name = name_entry.get()
            surname = surname_entry.get()
            address = address_entry.get()

            customer = Customer(id, name, surname, address)
            self.customer_manager.insert_customer(customer)
            add_window.destroy()
            self.refresh_table()

        tk.Button(add_window, text="Guardar", command=save_customer).pack()

    # Método de vista para mostrar el formulario de borrado de un cliente
    def delete_customer(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Eliminar un cliente")
        delete_window.geometry("200x100")

        tk.Label(delete_window, text="Código:").pack()
        id_entry = tk.Entry(delete_window)
        id_entry.pack()

        def delete():
            id = int(id_entry.get())
            self.customer_manager.delete_customer(id)
            delete_window.destroy()
            self.refresh_table()

        tk.Button(delete_window, text="Eliminar", command=delete).pack()

    # Método de vista para mostrar el formulario de modificación de un cliente
    def update_customer(self):
        update_window = tk.Toplevel(self)
        update_window.title("Modificar un cliente")
        update_window.geometry("300x200")

        tk.Label(update_window, text="Código:").pack()
        id_entry = tk.Entry(update_window)
        id_entry.pack()

        tk.Label(update_window, text="Nombre:").pack()
        name_entry = tk.Entry(update_window)
        name_entry.pack()

        tk.Label(update_window, text="Apellido:").pack()
        surname_entry = tk.Entry(update_window)
        surname_entry.pack()

        tk.Label(update_window, text="Dirección:").pack()
        address_entry = tk.Entry(update_window)
        address_entry.pack()

        def update():
            id = int(id_entry.get())
            customer = self.customer_manager.get_customer(id)
            if customer:
                customer.name = name_entry.get()
                customer.surname = surname_entry.get()
                customer.address = address_entry.get()
                self.customer_manager.update_customer(customer)
                update_window.destroy()
                self.refresh_table()

        tk.Button(update_window, text="Modificar", command=update).pack()

    # Método de vista para mostrar los clientes en la tabla y por consola
    def list_all_customers(self):
        # Refrescar el listado de clientes en la tabla de Tkinter
        self.refresh_table()
        
        # Listar los clientes por consola para ver salida de la transacción
        customers = self.customer_manager.get_all_customers()
        if customers:
            for customer in customers:
                print(f"Código: {customer.id}")
                print(f"Nombre: {customer.name}")
                print(f"Apellido: {customer.surname}")
                print(f"Dirección: {customer.address}")
                print("-------------------")
        else:
            print("No se encontraron clientes.")

    def quit(self):
        self.customer_manager.close_connection()
        self.destroy()

##Iniciar la aplicación:
if __name__ == "__main__":
    app = Application()
    app.mainloop()
