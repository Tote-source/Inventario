import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class Producto:
    def __init__(self, nombre, categoria, precio, cantidad):
        self.__nombre = nombre
        self.__categoria = categoria
        self.set_precio(precio)
        self.set_cantidad(cantidad)

    def get_nombre(self):
        return self.__nombre

    def get_categoria(self):
        return self.__categoria

    def get_precio(self):
        return self.__precio

    def get_cantidad(self):
        return self.__cantidad

    def set_precio(self, precio):
        if precio > 0:
            self.__precio = precio
        else:
            raise ValueError("El precio debe ser mayor que 0.")

    def set_cantidad(self, cantidad):
        if cantidad >= 0:
            self.__cantidad = cantidad
        else:
            raise ValueError("La cantidad debe ser mayor o igual a 0.")

    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "categoria": self.__categoria,
            "precio": self.__precio,
            "cantidad": self.__cantidad
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["nombre"], data["categoria"], data["precio"], data["cantidad"])

    def __str__(self):
        return f"{self.__nombre} (Categoría: {self.__categoria}, Precio: {self.__precio}, Cantidad: {self.__cantidad})"


class Almacenamiento:
    def __init__(self, archivo='inventario.json'):
        self.archivo = archivo

    def cargar_datos(self):
        if os.path.isfile(self.archivo):
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                return [Producto.from_dict(item) for item in datos]
        return []

    def guardar_datos(self, productos):
        with open(self.archivo, 'w') as f:
            json.dump([producto.to_dict() for producto in productos], f, indent=4)


class Inventario:
    def __init__(self, almacenamiento):
        self.almacenamiento = almacenamiento
        self.__productos = self.almacenamiento.cargar_datos()

    def agregar_producto(self, producto):
        if not self.buscar_producto(producto.get_nombre()):
            self.__productos.append(producto)
            self.almacenamiento.guardar_datos(self.__productos)
            return f"Producto '{producto.get_nombre()}' agregado al inventario."
        else:
            return "El producto ya existe en el inventario."

    def actualizar_producto(self, nombre, nuevo_precio=None, nueva_cantidad=None):
        producto = self.buscar_producto(nombre)
        if producto:
            if nuevo_precio is not None:
                producto.set_precio(nuevo_precio)
            if nueva_cantidad is not None:
                producto.set_cantidad(nueva_cantidad)
            self.almacenamiento.guardar_datos(self.__productos)
            return f"Producto '{nombre}' actualizado."
        return f"Producto '{nombre}' no encontrado en el inventario."

    def eliminar_producto(self, nombre):
        producto = self.buscar_producto(nombre)
        if producto:
            self.__productos.remove(producto)
            self.almacenamiento.guardar_datos(self.__productos)
            return f"Producto '{nombre}' eliminado del inventario."
        return f"Producto '{nombre}' no encontrado en el inventario."

    def buscar_producto(self, nombre):
        for producto in self.__productos:
            if producto.get_nombre() == nombre:
                return producto
        return None

    def mostrar_inventario(self):
        return "\n".join(str(producto) for producto in self.__productos) if self.__productos else "El inventario está vacío."


class App(tk.Tk):
    def __init__(self, inventario):
        super().__init__()
        self.inventario = inventario
        self.title("Gestión de Inventario")
        self.geometry("500x400")

        tk.Label(self, text="Gestión de Inventario", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Agregar producto", command=self.agregar_producto).pack(fill="x", pady=5)
        tk.Button(self, text="Actualizar producto", command=self.actualizar_producto).pack(fill="x", pady=5)
        tk.Button(self, text="Eliminar producto", command=self.eliminar_producto).pack(fill="x", pady=5)
        tk.Button(self, text="Mostrar inventario", command=self.mostrar_inventario).pack(fill="x", pady=5)
        tk.Button(self, text="Buscar producto", command=self.buscar_producto).pack(fill="x", pady=5)

    def agregar_producto(self):
        nombre = simpledialog.askstring("Nombre", "Nombre del producto:")
        if nombre:
            categoria = simpledialog.askstring("Categoría", "Categoría del producto:")
            try:
                precio = float(simpledialog.askstring("Precio", "Precio del producto:"))
                cantidad = int(simpledialog.askstring("Cantidad", "Cantidad del producto:"))
                producto = Producto(nombre, categoria, precio, cantidad)
                mensaje = self.inventario.agregar_producto(producto)
                messagebox.showinfo("Resultado", mensaje)
            except ValueError:
                messagebox.showerror("Error", "Precio o cantidad inválidos.")

    def actualizar_producto(self):
        nombre = simpledialog.askstring("Actualizar", "Nombre del producto a actualizar:")
        if nombre:
            nuevo_precio = simpledialog.askstring("Precio", "Nuevo precio (dejar en blanco para no cambiar):")
            nueva_cantidad = simpledialog.askstring("Cantidad", "Nueva cantidad (dejar en blanco para no cambiar):")

            try:
                nuevo_precio = float(nuevo_precio) if nuevo_precio else None
                nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else None
                mensaje = self.inventario.actualizar_producto(nombre, nuevo_precio, nueva_cantidad)
                messagebox.showinfo("Resultado", mensaje)
            except ValueError:
                messagebox.showerror("Error", "Precio o cantidad inválidos.")

    def eliminar_producto(self):
        nombre = simpledialog.askstring("Eliminar", "Nombre del producto a eliminar:")
        if nombre:
            mensaje = self.inventario.eliminar_producto(nombre)
            messagebox.showinfo("Resultado", mensaje)

    def mostrar_inventario(self):
        inventario = self.inventario.mostrar_inventario()
        messagebox.showinfo("Inventario", inventario)

    def buscar_producto(self):
        nombre = simpledialog.askstring("Buscar", "Nombre del producto a buscar:")
        if nombre:
            producto = self.inventario.buscar_producto(nombre)
            if producto:
                messagebox.showinfo("Producto encontrado", str(producto))
            else:
                messagebox.showinfo("Resultado", "Producto no encontrado.")


if __name__ == "__main__":
    almacenamiento = Almacenamiento()
    inventario = Inventario(almacenamiento)
    app = App(inventario)
    app.mainloop()
