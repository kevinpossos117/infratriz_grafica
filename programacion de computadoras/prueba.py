import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from datetime import datetime

# --- Configuración de Archivos ---
USUARIOS_FILE = "usuarios.json"
PRODUCTOS_FILE = "productos.json"
HISTORIAL_COMPRAS_FILE = "historial_compras.json"

# --- Funciones de Utilidad para JSON ---
def cargar_json(filename):
    """Carga datos desde un archivo JSON. Retorna lista vacía si el archivo no existe o está vacío/corrupto."""
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        messagebox.showerror("Error de Carga", f"El archivo {filename} está corrupto. Se reiniciará con datos vacíos.")
        return []
    except Exception as e:
        messagebox.showerror("Error de Carga", f"Error al cargar {filename}: {e}")
        return []

def guardar_json(data, filename):
    """Guarda datos en un archivo JSON."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error al Guardar", f"No se pudo guardar en {filename}: {e}")

# --- Clase Principal de la Aplicación de Tienda ---
class TiendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi Tienda Online")
        self.root.geometry("1000x800")
        self.root.withdraw()  # Oculta la ventana principal hasta la autenticación

        self.usuario_actual = None
        self.carrito_compras = []

        # Asegurarse de que los archivos JSON existan
        self._inicializar_archivos()

        # Cargar datos iniciales
        self.usuarios = cargar_json(USUARIOS_FILE)
        self.productos = cargar_json(PRODUCTOS_FILE)
        self.historial_compras = cargar_json(HISTORIAL_COMPRAS_FILE)

        # Si no hay productos, cargar algunos predeterminados
        if not self.productos:
            self._cargar_productos_predeterminados()

        # Cargar iconos
        self._cargar_iconos()

        # Configurar la interfaz principal
        self._setup_main_ui()

        # Iniciar el proceso de autenticación
        self.iniciar_autenticacion()

    def _inicializar_archivos(self):
        """Crea los archivos JSON si no existen."""
        if not os.path.exists(USUARIOS_FILE):
            guardar_json([], USUARIOS_FILE)
        if not os.path.exists(PRODUCTOS_FILE):
            guardar_json([], PRODUCTOS_FILE)
        if not os.path.exists(HISTORIAL_COMPRAS_FILE):
            guardar_json([], HISTORIAL_COMPRAS_FILE)

    def _cargar_productos_predeterminados(self):
        """Carga productos predeterminados si el archivo de productos está vacío."""
        default_products = [
            {"id": "P001", "nombre": "Teclado Mecánico RGB", "descripcion": "Teclado de alta respuesta para gaming.", "precio": 75.99, "stock": 50},
            {"id": "P002", "nombre": "Mouse Gamer Inalámbrico", "descripcion": "Precisión y velocidad para tus partidas.", "precio": 35.50, "stock": 100},
            {"id": "P003", "nombre": "Monitor Curvo 27'' QHD", "descripcion": "Experiencia inmersiva con alta resolución.", "precio": 299.99, "stock": 20},
            {"id": "P004", "nombre": "Auriculares con Micrófono", "descripcion": "Sonido envolvente y comunicación clara.", "precio": 49.00, "stock": 75},
            {"id": "P005", "nombre": "Webcam Full HD 1080p", "descripcion": "Ideal para streaming y videollamadas.", "precio": 59.99, "stock": 30}
        ]
        self.productos = default_products
        guardar_json(self.productos, PRODUCTOS_FILE)
        messagebox.showinfo("Productos Iniciales", "Se han cargado productos predeterminados.")


    def _cargar_iconos(self):
        """Carga los iconos de la aplicación. Crea iconos dummy si los archivos no se encuentran."""
        self.icons = {}
        icon_names = ["home", "search", "user", "cart", "admin", "add", "edit", "delete"]
        for name in icon_names:
            try:
                # Intenta cargar el icono y redimensionarlo
                self.icons[name] = tk.PhotoImage(file=f"icons/{name}.png").subsample(2, 2)
            except tk.TclError:
                print(f"Advertencia: No se pudo cargar el icono 'icons/{name}.png'. Usando icono dummy.")
                # Crea una imagen transparente si el icono no se encuentra
                self.icons[name] = tk.PhotoImage(width=32, height=32)

    def _setup_main_ui(self):
        """Configura los frames y la barra de navegación principal."""
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)

        self.frames = {}
        # Aquí puedes definir tus frames para cada sección (inicio, buscar, etc.)
        # Por simplicidad, solo mostramos el frame de inicio por ahora
        self.frames["inicio"] = tk.Frame(self.main_frame, bg="white")
        self.frames["buscar"] = tk.Frame(self.main_frame, bg="white")
        self.frames["mi_perfil"] = tk.Frame(self.main_frame, bg="white")
        self.frames["carrito"] = tk.Frame(self.main_frame, bg="white")
        self.frames["admin_panel"] = tk.Frame(self.main_frame, bg="white") # Este frame será para el panel de admin

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self._setup_navbar()

    def _setup_navbar(self):
        """Configura la barra de navegación en la parte inferior."""
        nav_frame = tk.Frame(self.root, bg="#e0e0e0", bd=2, relief="raised")
        nav_frame.pack(side="bottom", fill="x")

        # Botones de navegación
        tk.Button(nav_frame, image=self.icons["home"], text="Inicio", compound="top",
                  command=self.mostrar_inicio, bg="#e0e0e0", fg="black", bd=0, padx=10, pady=5).pack(side="left", expand=True)
        tk.Button(nav_frame, image=self.icons["search"], text="Buscar", compound="top",
                  command=self.mostrar_buscar, bg="#e0e0e0", fg="black", bd=0, padx=10, pady=5).pack(side="left", expand=True)
        tk.Button(nav_frame, image=self.icons["user"], text="Mi Perfil", compound="top",
                  command=self.mostrar_perfil, bg="#e0e0e0", fg="black", bd=0, padx=10, pady=5).pack(side="left", expand=True)
        tk.Button(nav_frame, image=self.icons["cart"], text="Carrito", compound="top",
                  command=self.mostrar_carrito, bg="#e0e0e0", fg="black", bd=0, padx=10, pady=5).pack(side="left", expand=True)
        tk.Button(nav_frame, image=self.icons["admin"], text="Admin", compound="top",
                  command=self.mostrar_panel_admin, bg="#e0e0e0", fg="black", bd=0, padx=10, pady=5).pack(side="left", expand=True)

    def mostrar_frame(self, frame_name):
        """Muestra el frame especificado y oculta los demás."""
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
            print(f"Mostrando: {frame_name}") # Para depuración

    def mostrar_inicio(self):
        self.mostrar_frame("inicio")
        self._cargar_productos_en_inicio()

    def mostrar_buscar(self):
        self.mostrar_frame("buscar")
        tk.Label(self.frames["buscar"], text="Funcionalidad de Búsqueda (en construcción)", font=("Helvetica", 14), bg="white").pack(pady=20)

    def mostrar_perfil(self):
        self.mostrar_frame("mi_perfil")
        tk.Label(self.frames["mi_perfil"], text=f"Bienvenido, {self.usuario_actual['usuario']}", font=("Helvetica", 14), bg="white").pack(pady=20)
        tk.Button(self.frames["mi_perfil"], text="Cerrar Sesión", command=self.cerrar_sesion, bg="#ff6b6b").pack(pady=10)

    def mostrar_carrito(self):
        self.mostrar_frame("carrito")
        for widget in self.frames["carrito"].winfo_children(): # Limpiar antes de mostrar
            widget.destroy()

        tk.Label(self.frames["carrito"], text="Tu Carrito de Compras", font=("Helvetica", 16, "bold"), bg="white", fg="#333").pack(pady=10)

        if not self.carrito_compras:
            tk.Label(self.frames["carrito"], text="El carrito está vacío.", bg="white").pack(pady=20)
            return

        carrito_frame = tk.Frame(self.frames["carrito"], bg="#f9f9f9", bd=2, relief="groove")
        carrito_frame.pack(pady=10, padx=20, fill="both", expand=True)

        total_carrito = 0
        for i, item in enumerate(self.carrito_compras):
            subtotal = item['precio'] * item['cantidad']
            tk.Label(carrito_frame, text=f"{item['nombre']} x {item['cantidad']} - ${item['precio']:.2f} c/u = ${subtotal:.2f}",
                     bg="#f9f9f9", anchor="w").grid(row=i, column=0, sticky="ew", padx=5, pady=2)
            total_carrito += subtotal

        tk.Label(carrito_frame, text=f"Total: ${total_carrito:.2f}", font=("Helvetica", 12, "bold"), bg="#f9f9f9", anchor="e").grid(row=len(self.carrito_compras), column=0, sticky="ew", padx=5, pady=5)

        tk.Button(self.frames["carrito"], text="Proceder al Pago", command=lambda: self.procesar_pago(total_carrito), bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold")).pack(pady=10)


    def _cargar_productos_en_inicio(self):
        """Muestra los productos disponibles en la sección de inicio."""
        for widget in self.frames["inicio"].winfo_children():
            widget.destroy() # Limpiar antes de recargar

        tk.Label(self.frames["inicio"], text="Productos Disponibles", font=("Helvetica", 16, "bold"), bg="white", fg="#333").pack(pady=10)

        if not self.productos:
            tk.Label(self.frames["inicio"], text="No hay productos disponibles.", bg="white").pack(pady=20)
            return

        # Frame para la lista de productos
        productos_list_frame = tk.Frame(self.frames["inicio"], bg="white")
        productos_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for prod in self.productos:
            prod_frame = tk.Frame(productos_list_frame, bd=1, relief="solid", padx=10, pady=5, bg="#f5f5f5")
            prod_frame.pack(fill="x", pady=5)

            tk.Label(prod_frame, text=f"[{prod['id']}] {prod['nombre']}", font=("Helvetica", 12, "bold"), bg="#f5f5f5").pack(anchor="w")
            tk.Label(prod_frame, text=f"Descripción: {prod['descripcion']}", bg="#f5f5f5").pack(anchor="w")
            tk.Label(prod_frame, text=f"Precio: ${prod['precio']:.2f}", bg="#f5f5f5").pack(anchor="w")
            tk.Label(prod_frame, text=f"Stock: {prod['stock']}", bg="#f5f5f5").pack(anchor="w")

            if prod['stock'] > 0:
                tk.Button(prod_frame, text="Añadir al Carrito", command=lambda p=prod: self.anadir_al_carrito(p), bg="#8BC34A", fg="white").pack(pady=5, anchor="e")
            else:
                tk.Label(prod_frame, text="Agotado", fg="red", bg="#f5f5f5").pack(pady=5, anchor="e")

    def anadir_al_carrito(self, producto):
        """Añade un producto al carrito de compras."""
        cantidad = simpledialog.askinteger("Cantidad", f"¿Cuántas unidades de '{producto['nombre']}' quieres añadir al carrito?",
                                            parent=self.root, minvalue=1, maxvalue=producto['stock'])
        if cantidad is not None:
            # Verificar si el producto ya está en el carrito
            found = False
            for item in self.carrito_compras:
                if item['id'] == producto['id']:
                    if item['cantidad'] + cantidad <= producto['stock']:
                        item['cantidad'] += cantidad
                        messagebox.showinfo("Carrito", f"{cantidad} unidades de {producto['nombre']} añadidas al carrito.")
                    else:
                        messagebox.showwarning("Error", f"No hay suficiente stock para añadir {cantidad} unidades de {producto['nombre']}. Stock disponible: {producto['stock'] - item['cantidad']}")
                    found = True
                    break
            if not found:
                # Añadir nuevo producto al carrito
                self.carrito_compras.append({
                    "id": producto['id'],
                    "nombre": producto['nombre'],
                    "precio": producto['precio'],
                    "cantidad": cantidad
                })
                messagebox.showinfo("Carrito", f"{cantidad} unidades de {producto['nombre']} añadidas al carrito.")
        self.mostrar_carrito() # Actualizar vista del carrito

    def procesar_pago(self, total):
        """Simula el proceso de pago y actualiza el stock y el historial de compras."""
        if not self.carrito_compras:
            messagebox.showwarning("Pago", "El carrito está vacío.")
            return

        metodo_pago = simpledialog.askstring("Método de Pago", "¿Cómo deseas pagar? (Tarjeta/PayPal/Efectivo)", parent=self.root)
        if metodo_pago:
            confirm = messagebox.askyesno("Confirmar Compra", f"Confirmas la compra por ${total:.2f} usando {metodo_pago}?", parent=self.root)
            if confirm:
                # Generar ID de transacción
                id_transaccion = f"TR{len(self.historial_compras) + 1:05d}"
                fecha_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                productos_comprados_detalle = []
                for item_carrito in self.carrito_compras:
                    # Actualizar stock del producto
                    for prod_tienda in self.productos:
                        if prod_tienda['id'] == item_carrito['id']:
                            prod_tienda['stock'] -= item_carrito['cantidad']
                            break
                    productos_comprados_detalle.append({
                        "nombre": item_carrito['nombre'],
                        "precio_unitario": item_carrito['precio'],
                        "cantidad": item_carrito['cantidad']
                    })

                # Registrar la compra en el historial
                self.historial_compras.append({
                    "id_transaccion": id_transaccion,
                    "usuario": self.usuario_actual['usuario'],
                    "fecha": fecha_compra,
                    "total_pagado": total,
                    "metodo_pago": metodo_pago,
                    "productos": productos_comprados_detalle
                })

                # Guardar cambios
                guardar_json(self.productos, PRODUCTOS_FILE)
                guardar_json(self.historial_compras, HISTORIAL_COMPRAS_FILE)

                self.carrito_compras = [] # Vaciar carrito
                messagebox.showinfo("Pago Exitoso", f"Compra realizada con éxito! ID de Transacción: {id_transaccion}")
                self.mostrar_inicio() # Volver a mostrar productos con stock actualizado
            else:
                messagebox.showinfo("Pago Cancelado", "La compra ha sido cancelada.")
        else:
            messagebox.showwarning("Método de Pago", "Por favor, ingresa un método de pago.")

    # --- Métodos de Autenticación ---
    def iniciar_autenticacion(self):
        """Muestra la ventana de autenticación (login/registro)."""
        auth_window = tk.Toplevel(self.root)
        auth_window.title("Autenticación")
        auth_window.geometry("400x300")
        auth_window.grab_set()  # Hacerla modal
        auth_window.protocol("WM_DELETE_WINDOW", self.root.quit) # Cierra la app si se cierra esta ventana

        auth_frame = tk.Frame(auth_window, padx=20, pady=20, bg="#e0e0e0")
        auth_frame.pack(expand=True, fill="both")

        tk.Label(auth_frame, text="Usuario:", bg="#e0e0e0").pack(pady=5)
        self.user_entry = tk.Entry(auth_frame)
        self.user_entry.pack(pady=5)

        tk.Label(auth_frame, text="Contraseña:", bg="#e0e0e0").pack(pady=5)
        self.pass_entry = tk.Entry(auth_frame, show="*")
        self.pass_entry.pack(pady=5)

        login_button = tk.Button(auth_frame, text="Iniciar Sesión", command=self._login)
        login_button.pack(pady=10)

        register_button = tk.Button(auth_frame, text="Registrarse", command=self._register)
        register_button.pack(pady=5)

        self.auth_window = auth_window # Guardar referencia para destruirla

    def _login(self):
        """Intenta iniciar sesión con las credenciales proporcionadas."""
        username = self.user_entry.get()
        password = self.pass_entry.get()

        for user in self.usuarios:
            if user['usuario'] == username and user['password'] == password:
                self.usuario_actual = user
                messagebox.showinfo("Login Exitoso", f"¡Bienvenido, {username}!")
                self.auth_window.destroy()
                self.root.deiconify()  # Mostrar la ventana principal
                self.mostrar_inicio() # Cargar la vista de inicio
                return
        messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")

    def _register(self):
        """Registra un nuevo usuario si no existe."""
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if not username or not password:
            messagebox.showwarning("Registro", "Por favor, ingresa un usuario y una contraseña.")
            return

        for user in self.usuarios:
            if user['usuario'] == username:
                messagebox.showwarning("Registro", "El nombre de usuario ya existe.")
                return

        self.usuarios.append({"usuario": username, "password": password, "rol": "cliente"})
        guardar_json(self.usuarios, USUARIOS_FILE)
        messagebox.showinfo("Registro Exitoso", "Usuario registrado. Ya puedes iniciar sesión.")
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def cerrar_sesion(self):
        """Cierra la sesión actual y regresa a la pantalla de autenticación."""
        self.usuario_actual = None
        self.carrito_compras = [] # Vaciar carrito al cerrar sesión
        messagebox.showinfo("Sesión", "Sesión cerrada con éxito.")
        self.root.withdraw() # Oculta la ventana principal
        self.iniciar_autenticacion() # Vuelve a la pantalla de login

    # --- Panel de Administración ---
    def mostrar_panel_admin(self):
        """Muestra el panel de administración para gestionar productos y ver estadísticas."""
        if not self.usuario_actual or self.usuario_actual.get('rol') != 'admin':
            # Nota: para este ejemplo, podrías hacer que el primer usuario registrado sea admin o crearlo manualmente
            # Por simplicidad, asumiremos que "admin" es el usuario admin si existe.
            # Puedes modificar esto para tener un rol 'admin' explícito en tu JSON de usuarios.
            if self.usuario_actual and self.usuario_actual['usuario'] == 'admin': # Asumir 'admin' es el admin
                 pass
            else:
                messagebox.showwarning("Acceso Denegado", "Solo los administradores pueden acceder a esta sección.")
                return

        # Destruir widgets anteriores en el frame de admin si los hay
        for widget in self.frames["admin_panel"].winfo_children():
            widget.destroy()

        self.mostrar_frame("admin_panel")
        tk.Label(self.frames["admin_panel"], text="Panel de Administración", font=("Helvetica", 16, "bold"), bg="white", fg="#0056b3").pack(pady=15)

        # Botones de gestión
        tk.Button(self.frames["admin_panel"], text="Gestionar Productos", command=self._gestion_productos,
                  bg="#17a2b8", fg="white", font=("Helvetica", 12)).pack(pady=10, ipadx=20, ipady=10)
        tk.Button(self.frames["admin_panel"], text="Ver Estadísticas", command=self._mostrar_estadisticas,
                  bg="#28a745", fg="white", font=("Helvetica", 12)).pack(pady=10, ipadx=20, ipady=10)

    def _gestion_productos(self):
        """Abre una nueva ventana para la gestión de productos."""
        gestion_window = tk.Toplevel(self.root)
        gestion_window.title("Gestión de Productos")
        gestion_window.geometry("800x600")
        gestion_window.grab_set()

        gestion_frame = tk.Frame(gestion_window, bg="white", padx=10, pady=10)
        gestion_frame.pack(fill="both", expand=True)

        tk.Label(gestion_frame, text="Administrar Productos", font=("Helvetica", 16, "bold"), bg="white", fg="#007bff").pack(pady=10)

        # Treeview para mostrar productos
        self.productos_tree = ttk.Treeview(gestion_frame, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
        self.productos_tree.heading("ID", text="ID")
        self.productos_tree.heading("Nombre", text="Nombre")
        self.productos_tree.heading("Precio", text="Precio")
        self.productos_tree.heading("Stock", text="Stock")

        self.productos_tree.column("ID", width=70, anchor="center")
        self.productos_tree.column("Nombre", width=250)
        self.productos_tree.column("Precio", width=100, anchor="e")
        self.productos_tree.column("Stock", width=80, anchor="center")
        self.productos_tree.pack(pady=10, fill="both", expand=True)

        self._cargar_productos_treeview() # Cargar productos al Treeview

        # Controles de gestión (añadir, editar, eliminar)
        control_frame = tk.Frame(gestion_frame, bg="white")
        control_frame.pack(pady=10)

        tk.Button(control_frame, image=self.icons["add"], text="Añadir Producto", compound="left",
                  command=self._anadir_producto, bg="#28a745", fg="white").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(control_frame, image=self.icons["edit"], text="Editar Producto", compound="left",
                  command=self._editar_producto, bg="#ffc107", fg="black").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(control_frame, image=self.icons["delete"], text="Eliminar Producto", compound="left",
                  command=self._eliminar_producto, bg="#dc3545", fg="white").grid(row=0, column=2, padx=5, pady=5)

        gestion_window.wait_window() # Esperar a que esta ventana se cierre

    def _cargar_productos_treeview(self):
        """Carga los productos en el Treeview de gestión."""
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        for prod in self.productos:
            self.productos_tree.insert("", "end", values=(prod['id'], prod['nombre'], f"${prod['precio']:.2f}", prod['stock']))

    def _anadir_producto(self):
        """Añade un nuevo producto."""
        dialog = ProductDialog(self.root, "Añadir Nuevo Producto")
        if dialog.result:
            new_prod_id = f"P{len(self.productos) + 1:03d}"
            new_product = {
                "id": new_prod_id,
                "nombre": dialog.result['nombre'],
                "descripcion": dialog.result['descripcion'],
                "precio": dialog.result['precio'],
                "stock": dialog.result['stock']
            }
            self.productos.append(new_product)
            guardar_json(self.productos, PRODUCTOS_FILE)
            self._cargar_productos_treeview()
            self._cargar_productos_en_inicio() # Actualizar vista de productos
            messagebox.showinfo("Éxito", "Producto añadido correctamente.")

    def _editar_producto(self):
        """Edita un producto existente."""
        selected_item = self.productos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Editar Producto", "Por favor, selecciona un producto para editar.")
            return

        item_values = self.productos_tree.item(selected_item, 'values')
        prod_id = item_values[0]
        
        # Encontrar el producto en la lista
        product_to_edit = next((p for p in self.productos if p['id'] == prod_id), None)
        if product_to_edit:
            dialog = ProductDialog(self.root, "Editar Producto", product_to_edit)
            if dialog.result:
                product_to_edit['nombre'] = dialog.result['nombre']
                product_to_edit['descripcion'] = dialog.result['descripcion']
                product_to_edit['precio'] = dialog.result['precio']
                product_to_edit['stock'] = dialog.result['stock']
                guardar_json(self.productos, PRODUCTOS_FILE)
                self._cargar_productos_treeview()
                self._cargar_productos_en_inicio() # Actualizar vista de productos
                messagebox.showinfo("Éxito", "Producto editado correctamente.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def _eliminar_producto(self):
        """Elimina un producto seleccionado."""
        selected_item = self.productos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Eliminar Producto", "Por favor, selecciona un producto para eliminar.")
            return

        item_values = self.productos_tree.item(selected_item, 'values')
        prod_id = item_values[0]

        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar el producto '{item_values[1]} (ID: {prod_id})'?", parent=self.root)
        if confirm:
            self.productos = [p for p in self.productos if p['id'] != prod_id]
            guardar_json(self.productos, PRODUCTOS_FILE)
            self._cargar_productos_treeview()
            self._cargar_productos_en_inicio() # Actualizar vista de productos
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")

    # --- Ventana de Estadísticas (Tu código principal) ---
    def _mostrar_estadisticas(self):
        """Muestra la ventana de estadísticas con gráficos."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas de Compras")
        stats_window.geometry("900x700")
        stats_window.transient(self.root)
        stats_window.grab_set()

        stats_frame = tk.Frame(stats_window, bg="white", padx=10, pady=10)
        stats_frame.pack(fill="both", expand=True)

        tk.Label(stats_frame, text="Análisis de Estadísticas de Compras", font=("Helvetica", 16, "bold"), bg="white", fg="#4CAF50").pack(pady=10)

        # Convertir historial de compras a DataFrame
        df_compras = pd.DataFrame(self.historial_compras)

        # Convertir a tipos numéricos y de fecha
        if not df_compras.empty:
            df_compras['total_pagado'] = pd.to_numeric(df_compras['total_pagado'], errors='coerce')
            df_compras['fecha'] = pd.to_datetime(df_compras['fecha'], errors='coerce')
            df_compras.dropna(subset=['total_pagado', 'fecha'], inplace=True) # Eliminar filas con valores nulos

        # Desglosar productos comprados para análisis detallado
        productos_comprados_list = []
        if not df_compras.empty:
            for _, row in df_compras.iterrows():
                fecha = row['fecha']
                usuario = row['usuario']
                metodo_pago = row['metodo_pago']
                id_transaccion = row['id_transaccion']
                if isinstance(row['productos'], list):
                    for prod in row['productos']:
                        productos_comprados_list.append({
                            'fecha': fecha,
                            'usuario': usuario,
                            'metodo_pago': metodo_pago,
                            'nombre_producto': prod['nombre'],
                            'precio_unitario': prod['precio_unitario'],
                            'cantidad': prod['cantidad'],
                            'subtotal': prod['precio_unitario'] * prod['cantidad'],
                            'id_transaccion': id_transaccion
                        })
        df_productos_detallado = pd.DataFrame(productos_comprados_list)

        if df_compras.empty or df_productos_detallado.empty:
            tk.Label(stats_frame, text="¡No hay datos válidos para generar estadísticas!", bg="white", fg="gray").pack(pady=20)
            tk.Button(stats_frame, text="Volver al Panel de Administración", command=stats_window.destroy, bg="lightgray").pack(pady=10)
            stats_window.wait_window()
            return

        # --- Variables disponibles para ambos ejes ---
        available_variables = {
            "Fecha (Diario)": {"df": df_compras, "column_or_logic": lambda df: df['fecha'].dt.date, "type": "temporal", "display_name": "Fecha"},
            "Fecha (Mensual)": {"df": df_compras, "column_or_logic": lambda df: df['fecha'].dt.to_period('M').astype(str), "type": "temporal", "display_name": "Fecha"},
            "Producto": {"df": df_productos_detallado, "column_or_logic": 'nombre_producto', "type": "categorical", "display_name": "Producto"},
            "Usuario": {"df": df_compras, "column_or_logic": 'usuario', "type": "categorical", "display_name": "Usuario"},
            "Método de Pago": {"df": df_compras, "column_or_logic": 'metodo_pago', "type": "categorical", "display_name": "Método de Pago"},
            "Total Pagado": {"df": df_compras, "column_or_logic": 'total_pagado', "type": "numerical", "display_name": "Total Pagado"},
            "Número de Transacciones": {"df": df_compras, "column_or_logic": 'id_transaccion', "type": "numerical_count", "display_name": "Número de Transacciones"},
            "Cantidad Vendida": {"df": df_productos_detallado, "column_or_logic": 'cantidad', "type": "numerical", "display_name": "Cantidad Vendida"}
        }

        all_axis_options = list(available_variables.keys())

        controls_frame = tk.LabelFrame(stats_frame, text="Personaliza tu Gráfica", bg="white", padx=10, pady=10)
        controls_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(controls_frame, text="Tipo de Gráfica:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        chart_type_options = ["Barras", "Líneas", "Pastel"]
        chart_type_cb = ttk.Combobox(controls_frame, values=chart_type_options, state="readonly")
        chart_type_cb.set("Barras")
        chart_type_cb.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(controls_frame, text="Eje X:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        x_axis_cb = ttk.Combobox(controls_frame, values=all_axis_options, state="readonly")
        x_axis_cb.set("Fecha (Diario)")
        x_axis_cb.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(controls_frame, text="Eje Y:", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        y_axis_cb = ttk.Combobox(controls_frame, values=all_axis_options, state="readonly")
        y_axis_cb.set("Total Pagado")
        y_axis_cb.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        graph_canvas_frame = tk.Frame(stats_frame, bg="white", relief="groove", bd=1)
        graph_canvas_frame.pack(pady=10, padx=20, fill="both", expand=True)

        canvas = None

        def generar_y_mostrar_grafica():
            nonlocal canvas

            if canvas:
                canvas.get_tk_widget().destroy()
                plt.close('all')

            tipo_grafica = chart_type_cb.get()
            eje_x_key = x_axis_cb.get()
            eje_y_key = y_axis_cb.get()

            if not eje_x_key or not eje_y_key:
                messagebox.showerror("¡Faltan selecciones!", "Por favor, elige tanto la categoría del eje X como el valor del eje Y.")
                return

            x_info = available_variables[eje_x_key]
            y_info = available_variables[eje_y_key]

            if tipo_grafica == "Pastel":
                if x_info["type"] not in ["categorical", "temporal"]:
                    messagebox.showerror("Gráfica de Pastel", "Las gráficas de Pastel requieren una variable categórica o temporal en el Eje X para mostrar proporciones.")
                    return
                if y_info["type"] not in ["numerical", "numerical_count"]:
                    messagebox.showerror("Gráfica de Pastel", "Las gráficas de Pastel requieren una variable numérica (como 'Total Pagado', 'Cantidad Vendida' o 'Número de Transacciones') en el Eje Y.")
                    return

            if eje_x_key == eje_y_key and not (y_info["type"] == "numerical_count" and x_info["type"] in ["categorical", "temporal"]):
                messagebox.showerror("¡Selección Inválida!", "¡No puedes seleccionar la misma variable para ambos ejes (X e Y) de esta manera! Por favor, elige variables diferentes o un tipo de gráfica compatible.")
                return

            try:
                fig, ax = plt.subplots(figsize=(7, 5))
                plt.style.use('ggplot')

                x_labels = []
                y_data = []

                if x_info["type"] == "temporal":
                    if "Diario" in eje_x_key:
                        grouped_df_compras = df_compras.groupby(df_compras['fecha'].dt.date)
                        grouped_df_productos = df_productos_detallado.groupby(df_productos_detallado['fecha'].dt.date)
                        x_labels_raw = sorted(grouped_df_compras.groups.keys())
                    else: # Mensual
                        grouped_df_compras = df_compras.groupby(df_compras['fecha'].dt.to_period('M'))
                        grouped_df_productos = df_productos_detallado.groupby(df_productos_detallado['fecha'].dt.to_period('M'))
                        x_labels_raw = sorted(grouped_df_compras.groups.keys())

                    x_labels = [str(item) for item in x_labels_raw]

                    if y_info["display_name"] == "Total Pagado":
                        y_series = grouped_df_compras['total_pagado'].sum()
                    elif y_info["display_name"] == "Número de Transacciones":
                        y_series = grouped_df_compras.size()
                    elif y_info["display_name"] == "Cantidad Vendida":
                        y_series = grouped_df_productos['cantidad'].sum()
                    else:
                        raise ValueError(f"Combinación de ejes X='{eje_x_key}' e Y='{eje_y_key}' no es compatible para agrupamiento temporal.")

                    y_data = y_series.reindex(x_labels_raw, fill_value=0).values

                elif x_info["type"] == "categorical":
                    if x_info["display_name"] == "Producto":
                        if y_info["display_name"] == "Cantidad Vendida":
                            grouped_data = df_productos_detallado.groupby('nombre_producto')['cantidad'].sum()
                        elif y_info["display_name"] == "Total Pagado":
                            grouped_data = df_productos_detallado.groupby('nombre_producto')['subtotal'].sum()
                        elif y_info["display_name"] == "Número de Transacciones":
                            grouped_data = df_productos_detallado.groupby('nombre_producto')['id_transaccion'].nunique()
                        else:
                            raise ValueError(f"Combinación de ejes X='{eje_x_key}' e Y='{eje_y_key}' no es compatible para 'Producto'.")
                        x_labels = grouped_data.index
                        y_data = grouped_data.values

                    elif x_info["display_name"] == "Usuario":
                        if y_info["display_name"] == "Total Pagado":
                            grouped_data = df_compras.groupby('usuario')['total_pagado'].sum()
                        elif y_info["display_name"] == "Número de Transacciones":
                            grouped_data = df_compras.groupby('usuario').size()
                        elif y_info["display_name"] == "Cantidad Vendida":
                            merged_df = pd.merge(df_compras, df_productos_detallado, on=['id_transaccion', 'fecha', 'usuario', 'metodo_pago'], how='inner')
                            grouped_data = merged_df.groupby('usuario')['cantidad'].sum()
                        else:
                            raise ValueError(f"Combinación de ejes X='{eje_x_key}' e Y='{eje_y_key}' no es compatible para 'Usuario'.")
                        x_labels = grouped_data.index
                        y_data = grouped_data.values

                    elif x_info["display_name"] == "Método de Pago":
                        if y_info["display_name"] == "Total Pagado":
                            grouped_data = df_compras.groupby('metodo_pago')['total_pagado'].sum()
                        elif y_info["display_name"] == "Número de Transacciones":
                            grouped_data = df_compras.groupby('metodo_pago').size()
                        elif y_info["display_name"] == "Cantidad Vendida":
                            merged_df = pd.merge(df_compras, df_productos_detallado, on=['id_transaccion', 'fecha', 'usuario', 'metodo_pago'], how='inner')
                            grouped_data = merged_df.groupby('metodo_pago')['cantidad'].sum()
                        else:
                            raise ValueError(f"Combinación de ejes X='{eje_x_key}' e Y='{eje_y_key}' no es compatible para 'Método de Pago'.")
                        x_labels = grouped_data.index
                        y_data = grouped_data.values
                else:
                    raise ValueError("Tipo de eje X no soportado.")

                if tipo_grafica == "Barras":
                    ax.bar(x_labels, y_data, color=sns.color_palette("viridis", len(x_labels)))
                    ax.set_ylabel(y_info["display_name"])
                    if x_info["type"] == "temporal" or len(x_labels) > 5:
                        ax.tick_params(axis='x', rotation=45, ha='right')
                    else:
                        plt.xticks(rotation=0)
                elif tipo_grafica == "Líneas":
                    ax.plot(x_labels, y_data, marker='o', color='purple')
                    ax.set_ylabel(y_info["display_name"])
                    if x_info["type"] == "temporal" or len(x_labels) > 5:
                        ax.tick_params(axis='x', rotation=45, ha='right')
                    else:
                        plt.xticks(rotation=0)
                    ax.grid(True)
                elif tipo_grafica == "Pastel":
                    if len(y_data) == 0 or sum(y_data) == 0:
                        messagebox.showwarning("Sin datos para Pastel", "No hay datos para la combinación seleccionada o los valores son cero para generar un gráfico de pastel.")
                        plt.close(fig)
                        return

                    non_zero_indices = [i for i, val in enumerate(y_data) if val > 0]
                    filtered_y_data = [y_data[i] for i in non_zero_indices]
                    filtered_x_labels = [x_labels[i] for i in non_zero_indices]

                    if not filtered_y_data:
                        messagebox.showwarning("Sin datos para Pastel", "Todos los valores son cero después del filtrado.")
                        plt.close(fig)
                        return

                    ax.pie(filtered_y_data, labels=filtered_x_labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel", len(filtered_x_labels)))
                    ax.axis('equal')
                    ax.set_title(f'Distribución de {y_info["display_name"]} por {x_info["display_name"]}')
                    plt.tight_layout()
                    canvas = FigureCanvasTkAgg(fig, master=graph_canvas_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                    return

                ax.set_title(f'{tipo_grafica} de {y_info["display_name"]} por {x_info["display_name"]}')
                ax.set_xlabel(x_info["display_name"])
                plt.tight_layout()

                canvas = FigureCanvasTkAgg(fig, master=graph_canvas_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            except Exception as e:
                messagebox.showerror("Error al generar gráfica", f"Ocurrió un error: {e}. Asegúrate de que las variables seleccionadas sean compatibles con el tipo de gráfica y que haya datos para ellas.")
                if canvas:
                    canvas.get_tk_widget().destroy()
                plt.close('all')

        tk.Button(controls_frame, text="Generar Gráfica", command=generar_y_mostrar_grafica, bg="#AED581").grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(stats_frame, text="Volver al Panel de Administración", command=stats_window.destroy, bg="lightgray").pack(pady=10)

        generar_y_mostrar_grafica()
        stats_window.wait_window()

# --- Clase de Diálogo para Añadir/Editar Producto ---
class ProductDialog(tk.Toplevel):
    def __init__(self, parent, title, product_data=None):
        super().__init__(parent)
        self.title(title)
        self.parent = parent
        self.grab_set() # Modal
        self.transient(parent) # Mantener sobre la ventana padre

        self.result = None # Almacenará los datos del producto si se guardan

        self.nombre_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.precio_var = tk.DoubleVar()
        self.stock_var = tk.IntVar()

        if product_data:
            self.nombre_var.set(product_data.get('nombre', ''))
            self.descripcion_var.set(product_data.get('descripcion', ''))
            self.precio_var.set(product_data.get('precio', 0.0))
            self.stock_var.set(product_data.get('stock', 0))

        self._create_widgets()

        self.wait_window() # Espera a que la ventana se cierre

    def _create_widgets(self):
        main_frame = tk.Frame(self, padx=20, pady=20, bg="white")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Nombre:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.nombre_var).grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Descripción:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.descripcion_var).grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Precio:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.precio_var).grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Stock:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.stock_var).grid(row=3, column=1, sticky="ew", pady=5)

        main_frame.grid_columnconfigure(1, weight=1)

        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="Guardar", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=5)

    def _on_save(self):
        try:
            nombre = self.nombre_var.get().strip()
            descripcion = self.descripcion_var.get().strip()
            precio = self.precio_var.get()
            stock = self.stock_var.get()

            if not nombre or not descripcion:
                messagebox.showwarning("Entrada Inválida", "Nombre y descripción no pueden estar vacíos.", parent=self)
                return
            if precio <= 0:
                messagebox.showwarning("Entrada Inválida", "El precio debe ser mayor que cero.", parent=self)
                return
            if stock < 0:
                messagebox.showwarning("Entrada Inválida", "El stock no puede ser negativo.", parent=self)
                return

            self.result = {
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'stock': stock
            }
            self.destroy() # Cierra la ventana de diálogo

        except tk.TclError:
            messagebox.showerror("Error de Formato", "Por favor, ingresa un número válido para Precio y Stock.", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}", parent=self)


# --- Inicio de la Aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaApp(root)
    root.mainloop()