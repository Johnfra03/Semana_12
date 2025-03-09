class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.titulo = titulo
        self.autor = autor  # Tupla con el autor y título
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"ISBN: {self.isbn}, Título: {self.titulo}, Autor: {self.autor}, Categoría: {self.categoria}"


class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario  # ID único para cada usuario
        self.libros = []  # Lista de libros actualmente prestados

    def __str__(self):
        return f"ID: {self.id_usuario}, Nombre: {self.nombre}"

    def listar_libros(self):
        """Listar los libros actualmente prestados a este usuario"""
        if not self.libros:
            return "No tiene libros prestados."
        return "\n".join([libro.titulo for libro in self.libros])


class Biblioteca:
    def __init__(self):
        self.libros = {}  # Diccionario para almacenar libros por ISBN
        self.usuarios = set()  # Conjunto para almacenar IDs de usuarios únicos

    def añadir_libro(self, libro):
        """Añadir un libro a la biblioteca"""
        self.libros[libro.isbn] = libro
        print(f"Libro '{libro.titulo}' añadido a la biblioteca.")

    def quitar_libro(self, isbn):
        """Quitar un libro de la biblioteca"""
        if isbn in self.libros:
            libro = self.libros.pop(isbn)
            print(f"Libro '{libro.titulo}' eliminado de la biblioteca.")
        else:
            print("El libro con ese ISBN no existe en la biblioteca.")

    def registrar_usuario(self, usuario):
        """Registrar un nuevo usuario"""
        if usuario.id_usuario not in [u.id_usuario for u in self.usuarios]:
            self.usuarios.add(usuario)
            print(f"Usuario '{usuario.nombre}' registrado correctamente.")
        else:
            print("El usuario ya está registrado.")

    def dar_baja_usuario(self, id_usuario):
        """Dar de baja a un usuario"""
        usuario_a_borrar = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        if usuario_a_borrar:
            self.usuarios.remove(usuario_a_borrar)
            print(f"Usuario '{usuario_a_borrar.nombre}' dado de baja.")
        else:
            print("El usuario no existe en la biblioteca.")

    def prestar_libro(self, id_usuario, isbn):
        """Prestar un libro a un usuario"""
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        libro = self.libros.get(isbn, None)

        if usuario is None:
            print("El usuario no está registrado.")
        elif libro is None:
            print("El libro con ese ISBN no existe en la biblioteca.")
        elif libro in usuario.libros:
            print(f"El usuario {usuario.nombre} ya tiene el libro '{libro.titulo}' prestado.")
        else:
            usuario.libros.append(libro)
            print(f"Libro '{libro.titulo}' prestado a {usuario.nombre}.")

    def devolver_libro(self, id_usuario, isbn):
        """Devolver un libro por parte de un usuario"""
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        if usuario:
            libro = next((libro for libro in usuario.libros if libro.isbn == isbn), None)
            if libro:
                usuario.libros.remove(libro)
                print(f"Libro '{libro.titulo}' devuelto por {usuario.nombre}.")
            else:
                print(f"El usuario {usuario.nombre} no tiene el libro con ISBN {isbn}.")
        else:
            print("El usuario no está registrado.")

    def buscar_libro(self, criterio, valor):
        """Buscar libros por título, autor o categoría"""
        if criterio == "titulo":
            return [libro for libro in self.libros.values() if valor.lower() in libro.titulo.lower()]
        elif criterio == "autor":
            return [libro for libro in self.libros.values() if valor.lower() in libro.autor[0].lower()]
        elif criterio == "categoria":
            return [libro for libro in self.libros.values() if valor.lower() in libro.categoria.lower()]
        else:
            print("Criterio inválido.")
            return []

    def listar_libros_prestados(self, id_usuario):
        """Listar todos los libros actualmente prestados a un usuario"""
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        if usuario:
            if not usuario.libros:
                print(f"{usuario.nombre} no tiene libros prestados.")
            else:
                print(f"Libros prestados a {usuario.nombre}:")
                for libro in usuario.libros:
                    print(libro.titulo)
        else:
            print("El usuario no está registrado.")

    def listar_libros(self):
        """Listar todos los libros disponibles en la biblioteca"""
        if not self.libros:
            print("No hay libros disponibles en la biblioteca.")
        else:
            print("Libros disponibles en la biblioteca:")
            for libro in self.libros.values():
                print(libro)


def menu():
    biblioteca = Biblioteca()

    while True:
        print("\n*** Menú de la Biblioteca Digital ***")
        print("1. Añadir libro")
        print("2. Quitar libro")
        print("3. Registrar usuario")
        print("4. Dar de baja usuario")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libro")
        print("8. Listar libros prestados")
        print("9. Listar todos los libros")
        print("10. Salir")

        try:
            opcion = int(input("Elige una opción (1-10): "))

            if opcion == 1:
                titulo = input("Título del libro: ")
                autor = input("Autor del libro: ")
                categoria = input("Categoría del libro: ")
                isbn = input("ISBN del libro: ")
                libro = Libro(titulo, (autor,), categoria, isbn)
                biblioteca.añadir_libro(libro)

            elif opcion == 2:
                isbn = input("ISBN del libro a quitar: ")
                biblioteca.quitar_libro(isbn)

            elif opcion == 3:
                nombre = input("Nombre del usuario: ")
                id_usuario = input("ID del usuario: ")
                usuario = Usuario(nombre, id_usuario)
                biblioteca.registrar_usuario(usuario)

            elif opcion == 4:
                id_usuario = input("ID del usuario a dar de baja: ")
                biblioteca.dar_baja_usuario(id_usuario)

            elif opcion == 5:
                id_usuario = input("ID del usuario: ")
                isbn = input("ISBN del libro a prestar: ")
                biblioteca.prestar_libro(id_usuario, isbn)

            elif opcion == 6:
                id_usuario = input("ID del usuario: ")
                isbn = input("ISBN del libro a devolver: ")
                biblioteca.devolver_libro(id_usuario, isbn)

            elif opcion == 7:
                criterio = input("Buscar por (titulo, autor, categoria): ").lower()
                valor = input(f"Ingrese el valor a buscar por {criterio}: ")
                resultados = biblioteca.buscar_libro(criterio, valor)
                if resultados:
                    for libro in resultados:
                        print(libro)
                else:
                    print(f"No se encontraron libros con {criterio} '{valor}'.")

            elif opcion == 8:
                id_usuario = input("ID del usuario para ver sus libros prestados: ")
                biblioteca.listar_libros_prestados(id_usuario)

            elif opcion == 9:
                biblioteca.listar_libros()

            elif opcion == 10:
                print("¡Gracias por usar el sistema de la biblioteca!")
                break

            else:
                print("Opción no válida. Por favor, elige una opción entre 1 y 10.")

        except ValueError:
            print("Por favor, ingresa un número válido.")


# Ejecutar el menú
menu()
