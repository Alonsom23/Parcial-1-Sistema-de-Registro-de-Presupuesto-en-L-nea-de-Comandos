import sqlite3
import os

# Define el nombre de la base de datos
DB_NAME = 'budget.db'

def get_db_connection():
    """
    Establece y devuelve una conexión a la base de datos SQLite.
    Crea la base de datos si no existe.
    """
    conn = sqlite3.connect(DB_NAME)
    # Permite acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """
    Crea la tabla 'items' si no existe.
    La tabla almacenará: id, nombre, categoría, cantidad, precio_unitario, descripción.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            descripcion TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Base de datos '{DB_NAME}' y tabla 'items' aseguradas.")

def add_item(nombre, categoria, cantidad, precio_unitario, descripcion):
    """
    Agrega un nuevo artículo a la base de datos.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO items (nombre, categoria, cantidad, precio_unitario, descripcion)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, categoria, cantidad, precio_unitario, descripcion))
        conn.commit()
        return cursor.lastrowid # Retorna el ID del artículo insertado
    except sqlite3.Error as e:
        print(f"Error al agregar artículo: {e}")
        return None
    finally:
        conn.close()

def get_all_items():
    """
    Obtiene todos los artículos registrados en la base de datos.
    Retorna una lista de diccionarios (o Row objects).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM items ORDER BY nombre")
        items = cursor.fetchall()
        return [dict(item) for item in items] # Convertir Row objects a diccionarios
    except sqlite3.Error as e:
        print(f"Error al obtener artículos: {e}")
        return []
    finally:
        conn.close()

def find_items(query, search_by='nombre'):
    """
    Busca artículos por nombre o categoría.
    `search_by` puede ser 'nombre' o 'categoria'.
    Retorna una lista de diccionarios.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    items = []
    try:
        if search_by == 'nombre':
            cursor.execute("SELECT * FROM items WHERE nombre LIKE ? ORDER BY nombre", ('%' + query + '%',))
        elif search_by == 'categoria':
            cursor.execute("SELECT * FROM items WHERE categoria LIKE ? ORDER BY categoria", ('%' + query + '%',))
        else:
            print("Criterio de búsqueda inválido. Use 'nombre' o 'categoria'.")
            return []

        items = cursor.fetchall()
        return [dict(item) for item in items]
    except sqlite3.Error as e:
        print(f"Error al buscar artículos: {e}")
        return []
    finally:
        conn.close()

def get_item_by_id(item_id):
    """
    Obtiene un artículo por su ID.
    Retorna un diccionario o None si no se encuentra.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        return dict(item) if item else None
    except sqlite3.Error as e:
        print(f"Error al obtener artículo por ID: {e}")
        return None
    finally:
        conn.close()

def update_item(item_id, updates):
    """
    Actualiza los campos de un artículo existente.
    `updates` es un diccionario con los campos a actualizar (ej. {'cantidad': 5, 'precio_unitario': 12.5}).
    Retorna True si la actualización fue exitosa, False en caso contrario.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Construir la parte SET de la consulta SQL dinámicamente
        set_clauses = [f"{key} = ?" for key in updates.keys()]
        query = f"UPDATE items SET {', '.join(set_clauses)} WHERE id = ?"
        values = list(updates.values()) + [item_id]

        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si al menos una fila fue afectada
    except sqlite3.Error as e:
        print(f"Error al actualizar artículo: {e}")
        return False
    finally:
        conn.close()

def delete_item(item_id):
    """
    Elimina un artículo de la base de datos por su ID.
    Retorna True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si al menos una fila fue eliminada
    except sqlite3.Error as e:
        print(f"Error al eliminar artículo: {e}")
        return False
    finally:
        conn.close()

# Si este script se ejecuta directamente, crea la tabla
if __name__ == '__main__':
    create_table()
    print("Módulo de base de datos listo.")