## Documentación del Proyecto: Aplicación de Venta de Purinas

# 1. Introducción

Esta aplicación de escritorio fue desarrollada como un proyecto académico con el objetivo de facilitar la gestión de ventas de productos de purinas.
A través de una interfaz gráfica amigable, los usuarios pueden registrarse, iniciar sesión, explorar productos disponibles, realizar compras y consultar su historial.
La aplicación también lleva el control del inventario, permitiendo simular una tienda funcional a nivel básico.

# 2. Requisitos

Para ejecutar correctamente la aplicación, es necesario tener instalado lo siguiente:

- Python 3.x
- Librerías utilizadas:
  - tkinter (incluida con Python)
  - PIL o Pillow (para manejar imágenes)
  - datetime (incluida con Python)
  - json (incluida con Python)

---

# 3. Instalación

1. Descargar o clonar el repositorio desde GitHub.
2. Verificar que la carpeta contenga los siguientes archivos y directorios:

proyecto

- main.py
- data.json
- historial_compras.json
- productos.json
- imagenes

3. Abrir una terminal en la carpeta del proyecto y ejecutar:

```bash
python main.py

4. Instrucciones de uso
Inicio de sesión y registro
-Al abrir la aplicación, el usuario puede registrarse o iniciar sesión con su correo y contraseña.
-Los datos se guardan en el archivo data.json.

Navegación por productos
-Después de iniciar sesión, se muestra la lista de productos disponibles.

Cada producto tiene una imagen, nombre, precio y cantidad disponible.

Carrito de compras
-Los usuarios pueden agregar productos al carrito.
-Al finalizar la compra, el sistema actualiza el stock y registra la transacción en el historial.

Historial de compras
-Cada compra realizada queda registrada con fecha, productos, cantidad y total.
-El historial se almacena en historial_compras.json.

5. Estructura de datos
Estructura de data.json

[
  {
    "usuario": "kevin",
    "correo": "kevin@mail.com",
    "clave": "1234"
  }
]

Estructura de productos.json

[
  {
    "id": 1,
    "nombre": "Purina Perros Adultos",
    "precio": 45000,
    "stock": 20,
    "imagen": "imagenes/perros_adultos.png"
  }
]

Estructura de historial_compras.json

[
  {
    "usuario": "kevin",
    "fecha": "2025-07-16 13:45:00",
    "productos": [
      {"nombre": "Purina Perros Adultos", "cantidad": 2, "precio_unitario": 45000}
    ],
    "total": 90000
  }
]

6. Organización del código
-main.py: archivo principal que contiene la lógica general del programa, desde la interfaz gráfica hasta el manejo de datos.
-data.json: archivo donde se registran los usuarios.
-productos.json: contiene los productos, precios y stock disponible.
-historial_compras.json: guarda los registros de compras con fecha y usuario.
-imagenes: carpeta que almacena las imágenes de los productos.

7. Posibles mejoras
Reemplazar los archivos .json por una base de datos.
-Añadir un panel para administración (crear, editar y eliminar productos).
-Agregar filtros o búsqueda de productos.
-Generar reportes automáticos en Excel o PDF.
-Incluir integración con métodos de pago reales (simulados por ahora).
-Mejorar el sistema de seguridad para las contraseñas.

8. Conclusión
Este proyecto demuestra la integración de conceptos básicos de programación en Python, manejo de archivos, estructuras de datos y diseño de interfaces gráficas.
Fue desarrollado como parte de un proceso de aprendizaje y cumple con funcionalidades esenciales para la venta de productos desde una aplicación local y sencilla.





