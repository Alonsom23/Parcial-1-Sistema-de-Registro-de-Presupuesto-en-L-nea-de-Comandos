🎯 Objetivo
Desarrollar una aplicación de línea de comandos en Python que permita gestionar artículos dentro de un sistema de registro de presupuesto, incluyendo funcionalidades para registrar, buscar, editar y eliminar artículos.

📝 Contexto
Los usuarios deben poder registrar artículos asociados a un presupuesto, visualizar la lista completa, buscar artículos específicos por nombre o categoría, editar su información o eliminarlos completamente. Esta herramienta será útil para llevar un control detallado de insumos, costos u otros componentes presupuestarios.

📌 Requisitos funcionales
La aplicación debe permitir al usuario realizar las siguientes operaciones:

Registrar un nuevo artículo
➤ Ingresar nombre, categoría, cantidad, precio unitario y descripción.

Buscar artículos
➤ Permitir búsquedas por nombre o categoría.

Editar un artículo existente
➤ Actualizar los campos de un artículo (por ejemplo, cantidad o precio).

Eliminar un artículo
➤ Remover un artículo del sistema por su identificador o nombre.

Listar todos los artículos registrados
➤ Mostrar la lista completa en un formato legible (tabulado o alineado).

💡 Consideraciones técnicas
Usar Python 3 para el desarrollo.

Guardar los artículos en un archivo (por ejemplo, JSON o CSV) o en una base de datos local como SQLite.

Utilizar funciones y estructuras de datos adecuadas para modularizar el código.

Validar entradas del usuario (ej. campos vacíos, datos numéricos correctos).

Incluir manejo de errores y mensajes amigables para el usuario.

El código debe estar documentado con comentarios claros.

El programa debe ejecutarse desde la terminal (python app.py o similar).
