import database
from tabulate import tabulate # Para imprimir tablas bonitas

def clear_screen():
    """Limpia la pantalla de la terminal (funciona en la mayoría de los sistemas)."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Muestra el menú principal al usuario."""
    print("\n--- Gestor de Artículos de Presupuesto ---")
    print("1. Registrar nuevo artículo")
    print("2. Listar todos los artículos")
    print("3. Buscar artículos")
    print("4. Editar artículo")
    print("5. Eliminar artículo")
    print("6. Salir")
    print("------------------------------------------")

def register_item():
    """
    Guía al usuario para registrar un nuevo artículo,
    validando las entradas.
    """
    print("\n--- Registrar Nuevo Artículo ---")
    nombre = input("Nombre del artículo: ").strip()
    if not nombre:
        print("❌ El nombre no puede estar vacío.")
        return

    categoria = input("Categoría: ").strip()
    if not categoria:
        print("❌ La categoría no puede estar vacía.")
        return

    try:
        cantidad = int(input("Cantidad: "))
        if cantidad <= 0:
            print("❌ La cantidad debe ser un número entero positivo.")
            return
    except ValueError:
        print("❌ Cantidad inválida. Debe ser un número entero.")
        return

    try:
        precio_unitario = float(input("Precio unitario: "))
        if precio_unitario <= 0:
            print("❌ El precio unitario debe ser un número positivo.")
            return
    except ValueError:
        print("❌ Precio unitario inválido. Debe ser un número.")
        return

    descripcion = input("Descripción (opcional): ").strip()

    item_id = database.add_item(nombre, categoria, cantidad, precio_unitario, descripcion if descripcion else None)
    if item_id:
        print(f"✅ Artículo '{nombre}' (ID: {item_id}) registrado exitosamente.")
    else:
        print("❌ No se pudo registrar el artículo. Consulta el log de errores.")

def list_items():
    """
    Muestra una lista tabulada de todos los artículos.
    """
    print("\n--- Lista de Artículos ---")
    items = database.get_all_items()
    if not items:
        print("No hay artículos registrados.")
        return

    headers = ["ID", "Nombre", "Categoría", "Cantidad", "Precio Unitario", "Total", "Descripción"]
    table_data = []
    for item in items:
        total_cost = item['cantidad'] * item['precio_unitario']
        table_data.append([
            item['id'],
            item['nombre'],
            item['categoria'],
            item['cantidad'],
            f"${item['precio_unitario']:.2f}",
            f"${total_cost:.2f}",
            item['descripcion'] if item['descripcion'] else "N/A"
        ])

    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\nTotal de artículos: {len(items)}")

def search_items():
    """
    Permite al usuario buscar artículos por nombre o categoría.
    """
    print("\n--- Buscar Artículos ---")
    search_by = input("Buscar por (nombre/categoria): ").strip().lower()
    if search_by not in ['nombre', 'categoria']:
        print("❌ Criterio de búsqueda inválido. Por favor, use 'nombre' o 'categoria'.")
        return

    query = input(f"Ingrese el texto a buscar por {search_by}: ").strip()
    if not query:
        print("❌ La búsqueda no puede estar vacía.")
        return

    found_items = database.find_items(query, search_by)

    if not found_items:
        print(f"No se encontraron artículos que coincidan con '{query}' en '{search_by}'.")
        return

    headers = ["ID", "Nombre", "Categoría", "Cantidad", "Precio Unitario", "Total", "Descripción"]
    table_data = []
    for item in found_items:
        total_cost = item['cantidad'] * item['precio_unitario']
        table_data.append([
            item['id'],
            item['nombre'],
            item['categoria'],
            item['cantidad'],
            f"${item['precio_unitario']:.2f}",
            f"${total_cost:.2f}",
            item['descripcion'] if item['descripcion'] else "N/A"
        ])

    print(f"\nArtículos encontrados que coinciden con '{query}':")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def edit_item():
    """
    Permite al usuario editar un artículo existente por su ID.
    """
    print("\n--- Editar Artículo ---")
    try:
        item_id = int(input("Ingrese el ID del artículo a editar: "))
    except ValueError:
        print("❌ ID inválido. Debe ser un número entero.")
        return

    item = database.get_item_by_id(item_id)
    if not item:
        print(f"❌ No se encontró ningún artículo con ID {item_id}.")
        return

    print(f"Editando artículo: ID {item['id']} - Nombre: {item['nombre']}")
    updates = {}

    # Solicitar nuevos valores, permitiendo dejar en blanco para no cambiar
    new_nombre = input(f"Nuevo nombre (actual: {item['nombre']}): ").strip()
    if new_nombre:
        updates['nombre'] = new_nombre

    new_categoria = input(f"Nueva categoría (actual: {item['categoria']}): ").strip()
    if new_categoria:
        updates['categoria'] = new_categoria

    new_cantidad_str = input(f"Nueva cantidad (actual: {item['cantidad']}): ").strip()
    if new_cantidad_str:
        try:
            new_cantidad = int(new_cantidad_str)
            if new_cantidad <= 0:
                print("❌ La cantidad debe ser un número entero positivo. No se actualizará la cantidad.")
            else:
                updates['cantidad'] = new_cantidad
        except ValueError:
            print("❌ Cantidad inválida. Debe ser un número entero. No se actualizará la cantidad.")

    new_precio_str = input(f"Nuevo precio unitario (actual: {item['precio_unitario']:.2f}): ").strip()
    if new_precio_str:
        try:
            new_precio = float(new_precio_str)
            if new_precio <= 0:
                print("❌ El precio unitario debe ser un número positivo. No se actualizará el precio.")
            else:
                updates['precio_unitario'] = new_precio
        except ValueError:
            print("❌ Precio unitario inválido. Debe ser un número. No se actualizará el precio.")

    new_descripcion = input(f"Nueva descripción (actual: {item['descripcion'] if item['descripcion'] else 'N/A'}): ").strip()
    # Si la descripción se deja vacía, se puede interpretar como borrarla o dejarla como está.
    # Aquí la actualizaremos si se provee o si se quiere borrar explícitamente con un espacio.
    # Podríamos añadir una opción para 'borrar descripción'. Por simplicidad, si no es vacía, la actualiza.
    # Si se deja en blanco y antes tenía algo, no la cambia. Si se pone 'N/A' o similar, la actualiza.
    # Para forzar el borrado de una descripción: el usuario debería quizás escribir "borrar"
    if new_descripcion:
        updates['descripcion'] = new_descripcion
    elif new_descripcion == '': # Si se deja en blanco, y antes tenía algo, no se actualiza a None
         pass # Si se deja vacía, no se incluye en los updates a menos que sea un campo que deba ser nulo.

    # Una forma explícita de borrar la descripción
    clear_desc = input("¿Desea eliminar la descripción? (s/N): ").strip().lower()
    if clear_desc == 's':
        updates['descripcion'] = None

    if not updates:
        print("ℹ️ No se detectaron cambios para actualizar.")
        return

    if database.update_item(item_id, updates):
        print(f"✅ Artículo (ID: {item_id}) actualizado exitosamente.")
    else:
        print(f"❌ No se pudo actualizar el artículo (ID: {item_id}).")


def delete_item():
    """
    Permite al usuario eliminar un artículo por su ID.
    """
    print("\n--- Eliminar Artículo ---")
    try:
        item_id = int(input("Ingrese el ID del artículo a eliminar: "))
    except ValueError:
        print("❌ ID inválido. Debe ser un número entero.")
        return

    item = database.get_item_by_id(item_id)
    if not item:
        print(f"❌ No se encontró ningún artículo con ID {item_id}.")
        return

    confirm = input(f"¿Está seguro de que desea eliminar '{item['nombre']}' (ID: {item_id})? (s/N): ").strip().lower()
    if confirm == 's':
        if database.delete_item(item_id):
            print(f"✅ Artículo '{item['nombre']}' (ID: {item_id}) eliminado exitosamente.")
        else:
            print(f"❌ No se pudo eliminar el artículo (ID: {item_id}).")
    else:
        print("Operación de eliminación cancelada.")

def main():
    """
    Función principal de la aplicación CLI.
    """
    database.create_table() # Asegura que la tabla exista al iniciar

    while True:
        display_menu()
        choice = input("Seleccione una opción: ").strip()

        if choice == '1':
            register_item()
        elif choice == '2':
            list_items()
        elif choice == '3':
            search_items()
        elif choice == '4':
            edit_item()
        elif choice == '5':
            delete_item()
        elif choice == '6':
            print("👋 Saliendo del Gestor de Artículos de Presupuesto. ¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida. Por favor, intente de nuevo.")

        # Pausa para que el usuario pueda leer la salida antes de limpiar la pantalla
        input("\nPresiona Enter para continuar...")
        clear_screen()

if __name__ == "__main__":
    main()