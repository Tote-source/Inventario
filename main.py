import json
import os

class Producto:
    def __init__(self, nombre, categoria, precio, cantidad):
        self.__nombre = nombre
        self.__categoria = categoria
        self.set_precio(precio)
        self.set_cantidad(cantidad)

    # Getters
    def get_nombre(self):
        return self.__nombre

    def get_categoria(self):
        return self.__categoria

    def get_precio(self):
        return self.__precio

    def get_cantidad(self):
        return self.__cantidad

    # Setters
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
        """Convierte el objeto Producto a un diccionario para guardar en JSON."""
        return {
            "nombre": self.__nombre,
            "categoria": self.__categoria,
            "precio": self.__precio,
            "cantidad": self.__cantidad
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Producto desde un diccionario."""
        return cls(data["nombre"], data["categoria"], data["precio"], data["cantidad"])

    def __str__(self):
        return f"{self.__nombre} (Categoría: {self.__categoria}, Precio: {self.__precio}, Cantidad: {self.__cantidad})"


class Almacenamiento:
    def __init__(self, archivo='inventario.json'):
        self.archivo = archivo

    def cargar_datos(self):
        """Carga los productos desde un archivo JSON, si existe."""
        if os.path.isfile(self.archivo):
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                return [Producto.from_dict(item) for item in datos]
        return []

    def guardar_datos(self, productos):
        """Guarda los productos en un archivo JSON."""
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
            print(f"Producto '{producto.get_nombre()}' agregado al inventario.")
        else:
            print("El producto ya existe en el inventario.")

    def actualizar_producto(self, nombre, nuevo_precio=None, nueva_cantidad=None):
        producto = self.buscar_producto(nombre)
        if producto:
            if nuevo_precio is not None:
                producto.set_precio(nuevo_precio)
            if nueva_cantidad is not None:
                producto.set_cantidad(nueva_cantidad)
            self.almacenamiento.guardar_datos(self.__productos)
            print(f"Producto '{nombre}' actualizado.")
        else:
            print(f"Producto '{nombre}' no encontrado en el inventario.")

    def eliminar_producto(self, nombre):
        producto = self.buscar_producto(nombre)
        if producto:
            self.__productos.remove(producto)
            self.almacenamiento.guardar_datos(self.__productos)
            print(f"Producto '{nombre}' eliminado del inventario.")
        else:
            print(f"Producto '{nombre}' no encontrado en el inventario.")

    def buscar_producto(self, nombre):
        for producto in self.__productos:
            if producto.get_nombre() == nombre:
                return producto
        return None

    def mostrar_inventario(self):
        if self.__productos:
            print("Inventario:")
            for producto in self.__productos:
                print(producto)
        else:
            print("El inventario está vacío.")


def menu():
    print("\n--- Menú de Gestión de Inventario ---")
    print("1. Agregar producto")
    print("2. Actualizar producto")
    print("3. Eliminar producto")
    print("4. Mostrar inventario")
    print("5. Buscar producto")
    print("6. Salir")
    return input("Seleccione una opción: ")


def main():
    almacenamiento = Almacenamiento()
    inventario = Inventario(almacenamiento)

    while True:
        opcion = menu()
        
        if opcion == "1":
            try:
                nombre = input("Nombre del producto: ")
                categoria = input("Categoría: ")
                precio = float(input("Precio: "))
                cantidad = int(input("Cantidad: "))
                nuevo_producto = Producto(nombre, categoria, precio, cantidad)
                inventario.agregar_producto(nuevo_producto)
            except ValueError as e:
                print("Error:", e)

        elif opcion == "2":
            nombre = input("Nombre del producto a actualizar: ")
            nuevo_precio = input("Nuevo precio (dejar en blanco para no cambiar): ")
            nueva_cantidad = input("Nueva cantidad (dejar en blanco para no cambiar): ")

            try:
                nuevo_precio = float(nuevo_precio) if nuevo_precio else None
                nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else None
                inventario.actualizar_producto(nombre, nuevo_precio, nueva_cantidad)
            except ValueError as e:
                print("Error:", e)

        elif opcion == "3":
            nombre = input("Nombre del producto a eliminar: ")
            inventario.eliminar_producto(nombre)

        elif opcion == "4":
            inventario.mostrar_inventario()

        elif opcion == "5":
            nombre = input("Nombre del producto a buscar: ")
            producto = inventario.buscar_producto(nombre)
            if producto:
                print("Producto encontrado:", producto)
            else:
                print("Producto no encontrado.")

        elif opcion == "6":
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()

