import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import os
import json
import datetime # Para registrar la fecha y hora de la compra
from collections import defaultdict # Para agrupar productos en el carrito

ARCHIVO_DATOS = "data.json" #Para usuarios
HISTORIAL_COMPRAS_FILE = "historial_compras.json" #historial de compras

usuario_actual = None

# Rutas de imagenes absolutas
# IMPORTANTE: Asegúrate de que esta ruta sea ABSOLUTA y correcta en tu sistema.
# Si no estás seguro, puedes usar:
# IMG_BASE = os.path.dirname(os.path.abspath(__file__))
# Y colocar las imágenes en la misma carpeta que este script.
IMG_BASE = "C:\\Users\\kevin\\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras"

# --- Funciones de Utilidad para Archivos JSON ---

def cargar_json(filepath):
    """Carga datos desde un archivo JSON. Retorna una lista vacía si hay error o no existe."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if data is not None else []
    except json.JSONDecodeError:
        messagebox.showerror("Error de Archivo", f"El archivo '{filepath}' está corrupto o vacío. Se inicializará vacío.")
        return []
    except Exception as e:
        messagebox.showerror("Error de Carga", f"No se pudo cargar '{filepath}': {e}")
        return []

def guardar_json(datos, filepath):
    """Guarda datos en un archivo JSON."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
    except IOError as e:
        messagebox.showerror("Error de Escritura", f"No se pudo guardar en '{filepath}': {e}")


def load_icon(path):
    try:
        image = Image.open(path)
        image = image.resize((30, 30), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        # print(f"Error loading icon {path}: {e}") # Descomentar para depurar
        return None

def load_image(path, size=(80, 80)):
    try:
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        # print(f"Error loading image {path}: {e}") # Descomentar para depurar
        return None

# Inicialización de productos con stock
productos_disponibles = [
    {"nombre": "comida para gatos", "precio": "15000", "imagen": os.path.join(IMG_BASE, "ringogato.png"), "stock": 10},
    {"nombre": "comida para perro", "precio": "25000", "imagen": os.path.join(IMG_BASE, "perro.png"), "stock": 15},
    {"nombre": "comida para gatos pequenos", "precio": "10000", "imagen": os.path.join(IMG_BASE, "gato_pequeño.png"), "stock": 20},
    {"nombre": "comida para cachorros", "precio": "20000", "imagen": os.path.join(IMG_BASE, "perros_pequeños.png"), "stock": 12},
]

#

def iniciar_autenticacion():
    def login():
        global usuario_actual
        user = entry_user.get()
        password = entry_pass.get()
        # Usar cargar_json para usuarios
        for u in cargar_json(ARCHIVO_DATOS):
            if u["user"] == user and u["pass"] == password:
                usuario_actual = u
                messagebox.showinfo("Bienvenido", f"Hola {user}")
                root.destroy()
                abrir_tienda()
                return
        messagebox.showerror("Error", "Credenciales incorrectas")

    def registrar():
        user = entry_new_user.get()
        password = entry_new_pass.get()
        if not user or not password:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        datos = cargar_json(ARCHIVO_DATOS) # Usar cargar_json
        for u in datos:
            if u["user"] == user:
                messagebox.showerror("Error", "Usuario ya existe")
                return
        datos.append({"user": user, "pass": password, "foto": ""})
        guardar_json(datos, ARCHIVO_DATOS) # Usar guardar_json
        messagebox.showinfo("Éxito", "Usuario registrado")
        frame_reg.pack_forget()
        frame_login.pack()

    root = tk.Tk()
    root.title("Login AGRO.MAX")
    root.geometry("300x400")
    root.configure(bg="#195E5E")

    try:
        img_path = os.path.join(IMG_BASE, "unnamed.png")
        img = Image.open(img_path).resize((100, 100))
        logo = ImageTk.PhotoImage(img)
        tk.Label(root, image=logo, bg="#195E5E").pack(pady=10)
    except Exception as e:
        print(f"Error al cargar logo: {e}")
        tk.Label(root, text="AGRO.MAX", font=("Arial", 20, "bold"), bg="#195E5E", fg="white").pack(pady=10)

    frame_login = tk.Frame(root, bg="#195E5E")
    tk.Label(frame_login, text="Usuario", bg="#195E5E", fg="white").pack()
    entry_user = tk.Entry(frame_login)
    entry_user.pack()
    tk.Label(frame_login, text="Contraseña", bg="#195E5E", fg="white").pack()
    entry_pass = tk.Entry(frame_login, show="*")
    entry_pass.pack()
    tk.Button(frame_login, text="Iniciar sesión", command=login, bg="#B7CE63").pack(pady=10)
    tk.Button(frame_login, text="Registrarse", command=lambda: switch(True)).pack()
    frame_login.pack()

    frame_reg = tk.Frame(root, bg="#195E5E")
    tk.Label(frame_reg, text="Nuevo usuario", bg="#195E5E", fg="white").pack()
    entry_new_user = tk.Entry(frame_reg)
    entry_new_user.pack()
    tk.Label(frame_reg, text="Nueva contraseña", bg="#195E5E", fg="white").pack()
    entry_new_pass = tk.Entry(frame_reg, show="*")
    entry_new_pass.pack()
    tk.Button(frame_reg, text="Registrar", command=registrar, bg="#B7CE63").pack(pady=10)
    tk.Button(frame_reg, text="Ya tengo cuenta", command=lambda: switch(False)).pack()

    def switch(to_reg):
        if to_reg:
            frame_login.pack_forget()
            frame_reg.pack()
        else:
            frame_reg.pack_forget()
            frame_login.pack()

    root.mainloop()

# Aplicación Principal de la Tienda 

def abrir_tienda():
    root = tk.Tk()
    root.geometry("400x600")
    root.title("AGRO.MAX - tienda")

    frame = tk.Frame(root, bg="white")
    frame.pack(fill="both", expand=True)

    nav = tk.Frame(root, height=60, bg="white")
    nav.pack(side="bottom", fill="x")

    icon_inicio = load_icon(os.path.join(IMG_BASE, "inicio.png"))
    icon_buscar = load_icon(os.path.join(IMG_BASE, "lupa.png"))
    icon_usuario = load_icon(os.path.join(IMG_BASE, "usuario.png"))
    icon_carrito = load_icon(os.path.join(IMG_BASE, "carrito.png"))

    carrito = [] # Almacena los productos agregados al carrito

    def limpiar():
        for widget in frame.winfo_children():
            widget.destroy()

    def go_inicio():
        limpiar()
        tk.Label(frame, text="Nuestros Productos", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)
        
        if not productos_disponibles:
            tk.Label(frame, text="No hay productos disponibles en este momento.", bg="white", fg="gray").pack(pady=20)
            return

        for prod in productos_disponibles:
            f = tk.Frame(frame, bg="white", relief="solid", bd=1, padx=5, pady=5)
            f.pack(padx=5, pady=5, fill="x")
            
            img = load_image(prod["imagen"])
            if img:
                tk.Label(f, image=img, bg="white").pack(side="left")
                f.image = img # Keep a reference!
            
            info = tk.Frame(f, bg="white")
            info.pack(side="left", padx=10, expand=True, fill="x")
            
            tk.Label(info, text=prod["nombre"], bg="white", font=("Arial", 12)).pack(anchor="w")
            tk.Label(info, text=f"Precio: ${prod['precio']}", bg="white", fg="green").pack(anchor="w")
            tk.Label(info, text=f"Stock: {prod['stock']}", bg="white", fg="blue").pack(anchor="w") # Mostrar stock

            if prod["stock"] > 0:
                tk.Button(info, text="Comprar", command=lambda p=prod: agregar_carrito(p), bg="#C8E6C9").pack(anchor="e", pady=5)
            else:
                tk.Label(info, text="AGOTADO", bg="white", fg="red", font=("Arial", 10, "bold")).pack(anchor="e", pady=5)

    def go_buscar():
        limpiar()
        tk.Label(frame, text="Buscar productos", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)
        
        search_frame = tk.Frame(frame, bg="white")
        search_frame.pack(pady=10)
        
        query = tk.Entry(search_frame, width=30)
        query.pack(side="left", padx=5)
        
        results_frame = tk.Frame(frame, bg="white")
        results_frame.pack(pady=10, fill="both", expand=True)

        def buscar():
            for widget in results_frame.winfo_children():
                widget.destroy()

            search_term = query.get().lower()
            resultados = [p for p in productos_disponibles if search_term in p["nombre"].lower()]
            
            if not resultados:
                tk.Label(results_frame, text="No se encontraron productos.", bg="white", fg="gray").pack(pady=10)
                return

            for p in resultados:
                f_res = tk.Frame(results_frame, bg="white", relief="solid", bd=1, padx=5, pady=5)
                f_res.pack(padx=5, pady=2, fill="x")
                
                tk.Label(f_res, text=f"{p['nombre']} - ${p['precio']} - Stock: {p['stock']}", bg="white").pack(side="left")
                
                if p["stock"] > 0:
                    tk.Button(f_res, text="Comprar", command=lambda prod_item=p: agregar_carrito(prod_item), bg="#C8E6C9").pack(side="right", padx=5)
                else:
                    tk.Label(f_res, text="AGOTADO", bg="white", fg="red", font=("Arial", 9, "bold")).pack(side="right", padx=5)

        tk.Button(search_frame, text="Buscar", command=buscar, bg="#AED581").pack(side="left", padx=5)

    def go_usuario():
        limpiar()
        tk.Label(frame, text="Perfil de Usuario", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)
        
        path = usuario_actual.get("foto", "")
        img = load_image(path, size=(120, 120)) # Tamaño un poco más grande
        if img:
            lbl = tk.Label(frame, image=img, bg="white")
            lbl.image = img
            lbl.pack(pady=10)
        else:
            tk.Label(frame, text="No hay foto de perfil", bg="white", fg="gray").pack(pady=10)

        tk.Button(frame, text="Cambiar foto", command=cambiar_foto, bg="lightblue").pack(pady=5)
        tk.Label(frame, text=f"Usuario/Email: {usuario_actual['user']}", bg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(frame, text="Editar perfil y contraseña", command=editar_perfil, bg="lightsteelblue").pack(pady=5)
        tk.Button(frame, text="Eliminar cuenta", command=eliminar_cuenta, bg="salmon").pack(pady=5)
        tk.Button(frame, text="Cerrar sesion", command=lambda: cerrar_sesion(root), bg="khaki").pack(pady=5)

    def cambiar_foto():
        path = filedialog.askopenfilename(title="Seleccionar foto de perfil", filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.gif")])
        if path:
            usuario_actual["foto"] = path
            datos = cargar_json(ARCHIVO_DATOS)
            for u in datos:
                if u["user"] == usuario_actual["user"]:
                    u["foto"] = path
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("Éxito", "Foto de perfil actualizada")
            go_usuario()

    def editar_perfil():
        nuevo_user = simpledialog.askstring("Editar usuario", "Nuevo nombre de usuario:")
        nueva_pass = simpledialog.askstring("Editar contraseña", "Nueva contraseña:", show="*")
        
        cambios_realizados = False
        if nuevo_user and nuevo_user != usuario_actual["user"]:
            datos = cargar_json(ARCHIVO_DATOS)
            if any(u["user"] == nuevo_user for u in datos if u["user"] != usuario_actual["user"]):
                messagebox.showerror("Error", "Este nombre de usuario ya está en uso.")
                return
            usuario_actual["user"] = nuevo_user
            cambios_realizados = True
        
        if nueva_pass:
            usuario_actual["pass"] = nueva_pass
            cambios_realizados = True

        if cambios_realizados:
            datos = cargar_json(ARCHIVO_DATOS)
            for i, u in enumerate(datos):
                if u["user"] == (nuevo_user if 'user' in locals() and nuevo_user else usuario_actual["user"]):
                    datos[i] = usuario_actual
                    break
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("Éxito", "Perfil actualizado")
            go_usuario()
        else:
            messagebox.showinfo("Información", "No se realizaron cambios en el perfil.")

    def eliminar_cuenta():
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar tu cuenta?\nEsta acción es irreversible."):
            global usuario_actual
            datos = cargar_json(ARCHIVO_DATOS)
            datos = [u for u in datos if u["user"] != usuario_actual["user"]]
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("OK", "Cuenta eliminada")
            cerrar_sesion(root)

    def cerrar_sesion(root_tienda_app):
        global usuario_actual
        usuario_actual = None
        root_tienda_app.destroy()
        iniciar_autenticacion()

    def go_carrito():
        limpiar()
        tk.Label(frame, text="Tu Carrito de Compras", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)
        
        if not carrito:
            tk.Label(frame, text="El carrito está vacío. ¡Agrega productos!", bg="white", fg="gray").pack(pady=20)
            return

        total = 0
        # Agrupar productos para mostrar y calcular el total correctamente
        productos_agrupados = defaultdict(int)
        for item in carrito:
            productos_agrupados[item["nombre"]] += 1
            total += int(item["precio"])

        for nombre_prod, cantidad in productos_agrupados.items():
            # Encontrar el precio original para mostrar
            precio_unitario = 0
            for p in productos_disponibles:
                if p["nombre"] == nombre_prod:
                    precio_unitario = int(p["precio"])
                    break
            
            tk.Label(frame, text=f"{nombre_prod} (x{cantidad}) - ${precio_unitario * cantidad:,}", bg="white").pack(anchor="w", padx=20)
            
        tk.Frame(frame, height=2, bg="lightgray").pack(fill="x", padx=15, pady=10) # Separador
        tk.Label(frame, text=f"Total: ${total:,}", bg="white", font=("Arial", 14, "bold"), fg="green").pack(pady=10)
        
        if carrito:
            tk.Button(frame, text="Pagar", command=lambda: pagar_con_opciones(total), bg="#B7CE63").pack(pady=10)
    
    # MODIFICACIÓN CLAVE: Función pagar_con_opciones
    def pagar_con_opciones(total_a_pagar):
        if not carrito:
            messagebox.showerror("Error", "El carrito está vacío. Agrega productos para pagar.")
            return

        pago_window = tk.Toplevel(root)
        pago_window.title("Confirmar Pago")
        pago_window.geometry("350x400")
        pago_window.transient(root) # Hace que la ventana de pago esté encima de la principal
        pago_window.grab_set() # Bloquea la interacción con la ventana principal

        pago_frame = tk.Frame(pago_window, bg="white", padx=20, pady=20)
        pago_frame.pack(fill="both", expand=True)

        tk.Label(pago_frame, text="Selecciona Método de Pago", font=("Arial", 14, "bold"), bg="white", fg="#195E5E").pack(pady=10)
        tk.Label(pago_frame, text=f"Total a Pagar: ${total_a_pagar:,}", font=("Arial", 12, "bold"), bg="white", fg="green").pack(pady=5)

        metodo_pago_var = tk.StringVar(value="Efectivo")

        card_details_frame = tk.Frame(pago_frame, bg="white") # Frame para campos de tarjeta

        def mostrar_campos_tarjeta():
            for widget in card_details_frame.winfo_children():
                widget.destroy() # Limpiar campos anteriores
            if metodo_pago_var.get() in ["Tarjeta Visa", "Mastercard"]:
                tk.Label(card_details_frame, text="Número de Tarjeta:", bg="white").pack(anchor="w", pady=(10,0))
                entry_card_number = tk.Entry(card_details_frame, width=30)
                entry_card_number.pack(fill="x", pady=2)
                
                tk.Label(card_details_frame, text="Fecha Vencimiento (MM/AA):", bg="white").pack(anchor="w", pady=(10,0))
                entry_expiry = tk.Entry(card_details_frame, width=10)
                entry_expiry.pack(fill="x", pady=2)
                
                tk.Label(card_details_frame, text="CVV:", bg="white").pack(anchor="w", pady=(10,0))
                entry_cvv = tk.Entry(card_details_frame, width=5, show="*")
                entry_cvv.pack(fill="x", pady=2)
            card_details_frame.pack(fill="x", pady=5) # Empaquetar el frame de detalles de tarjeta

        tk.Radiobutton(pago_frame, text="Efectivo", variable=metodo_pago_var, value="Efectivo", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)
        tk.Radiobutton(pago_frame, text="Tarjeta Visa", variable=metodo_pago_var, value="Tarjeta Visa", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)
        tk.Radiobutton(pago_frame, text="Mastercard", variable=metodo_pago_var, value="Mastercard", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)
        
        # Mostrar campos de tarjeta al inicio si es necesario (cuando se selecciona una tarjeta por defecto)
        mostrar_campos_tarjeta()

        def finalizar_pago():
            metodo_seleccionado = metodo_pago_var.get()
            
            if metodo_seleccionado in ["Tarjeta Visa", "Mastercard"]:
                # Simulación de validación de campos de tarjeta
                card_num = ""
                expiry = ""
                cvv = ""
                
                # Acceder a los entries creados en mostrar_campos_tarjeta
                # Esto es un poco hacky porque las variables locales de mostrar_campos_tarjeta no son accesibles directamente
                # Una mejor práctica sería hacer los entries variables de instancia o de un ámbito superior.
                # Para mantener la simplicidad y el estilo del código original, buscaré los widgets por su tipo y contenido.
                entries = [w for w in card_details_frame.winfo_children() if isinstance(w, tk.Entry)]
                if len(entries) == 3:
                    card_num = entries[0].get()
                    expiry = entries[1].get()
                    cvv = entries[2].get()

                if not card_num or not expiry or not cvv:
                    messagebox.showerror("Error de Pago", "Por favor, completa todos los campos de la tarjeta.")
                    return
                if not card_num.isdigit() or len(card_num) not in [10, 20]: # Simulación de longitud de tarjeta
                    messagebox.showerror("Error de Pago", "Número de tarjeta inválido.")
                    return
                if not expiry.count('/') == 1 or not all(part.isdigit() for part in expiry.split('/')) or len(expiry) != 5:
                    messagebox.showerror("Error de Pago", "Formato de fecha de vencimiento inválido (MM/AA).")
                    return
                if not cvv.isdigit() or len(cvv) not in [3,4]:
                    messagebox.showerror("Error de Pago", "CVV inválido.")
                    return
            
            # --- Registrar la compra en el historial ---
            historial = cargar_json(HISTORIAL_COMPRAS_FILE)
            
            # Agrupar productos para el historial de compra
            items_comprados_historial = defaultdict(lambda: {"precio_unitario": 0, "cantidad": 0})
            for item_c in carrito:
                items_comprados_historial[item_c["nombre"]]["precio_unitario"] = int(item_c["precio"])
                items_comprados_historial[item_c["nombre"]]["cantidad"] += 1
            
            lista_items_historial = []
            for nombre, datos in items_comprados_historial.items():
                lista_items_historial.append({
                    "nombre": nombre,
                    "precio_unitario": datos["precio_unitario"],
                    "cantidad": datos["cantidad"]
                })

            registro_compra = {
                "id_transaccion": datetime.datetime.now().strftime("%Y%m%d%H%M%S"), # ID único basado en timestamp
                "usuario": usuario_actual["user"],
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "metodo_pago": metodo_seleccionado,
                "total_pagado": total_a_pagar,
                "productos": lista_items_historial
            }
            historial.append(registro_compra)
            guardar_json(historial, HISTORIAL_COMPRAS_FILE)

            carrito.clear() # Vaciar el carrito
            messagebox.showinfo("¡Compra Realizada!", f"Tu compra de ${total_a_pagar:,} ha sido procesada con éxito usando {metodo_seleccionado}. ¡Gracias!")
            pago_window.destroy()
            go_carrito() # Refrescar la vista del carrito (ahora vacía)

        tk.Button(pago_frame, text="Confirmar Pago", command=finalizar_pago, bg="#B7CE63").pack(pady=20, fill="x")
        pago_window.mainloop()

    def agregar_carrito(prod_to_add):
        # Buscar el producto real en la lista global para modificar su stock
        found_product = None
        for p in productos_disponibles:
            if p["nombre"] == prod_to_add["nombre"]:
                found_product = p
                break
        
        if found_product and found_product["stock"] > 0:
            found_product["stock"] -= 1 # Decrementar stock
            carrito.append(found_product) # Añadir referencia al carrito
            messagebox.showinfo("Carrito", f"'{prod_to_add['nombre']}' agregado al carrito.")
            go_inicio() # Refrescar la vista para mostrar el stock actualizado
        elif found_product and found_product["stock"] <= 0:
            messagebox.showerror("Sin Stock", f"Lo sentimos, '{prod_to_add['nombre']}' está agotado.")
        else:
            messagebox.showerror("Error", "Producto no encontrado en la base de datos.") # Debería ser raro

    def go_admin():
        limpiar()
        tk.Label(frame, text="Panel de Administración", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        # Sección para agregar producto
        add_frame = tk.LabelFrame(frame, text="Añadir Nuevo Producto", bg="white", padx=10, pady=10)
        add_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(add_frame, text="Nombre:", bg="white").pack(anchor="w")
        nombre_entry = tk.Entry(add_frame)
        nombre_entry.pack(fill="x")

        tk.Label(add_frame, text="Precio:", bg="white").pack(anchor="w")
        precio_entry = tk.Entry(add_frame)
        precio_entry.pack(fill="x")
        
        tk.Label(add_frame, text="Stock Inicial:", bg="white").pack(anchor="w") # Campo de stock
        stock_entry = tk.Entry(add_frame)
        stock_entry.insert(0, "1") # Valor predeterminado
        stock_entry.pack(fill="x")

        selected_image_path = {"path": ""} # Usar un diccionario para pasar por referencia

        def seleccionar_imagen_admin():
            filepath = filedialog.askopenfilename(title="Seleccionar imagen para el producto", filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.gif")])
            if filepath:
                selected_image_path["path"] = filepath
                messagebox.showinfo("Imagen", f"Imagen seleccionada: {os.path.basename(filepath)}")

        tk.Button(add_frame, text="Seleccionar Imagen", command=seleccionar_imagen_admin, bg="#B7CE63").pack(pady=5)

        def agregar():
            nombre = nombre_entry.get().strip()
            precio_str = precio_entry.get().strip()
            stock_str = stock_entry.get().strip()
            imagen_path = selected_image_path["path"]

            if not nombre or not precio_str or not stock_str or not imagen_path:
                messagebox.showerror("Error", "Todos los campos y la imagen son obligatorios.")
                return
            
            try:
                precio = int(precio_str)
                stock = int(stock_str)
                if precio <= 0 or stock < 0:
                    messagebox.showerror("Error", "El precio debe ser positivo y el stock no puede ser negativo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "El precio y el stock deben ser números válidos.")
                return

            if any(p["nombre"].lower() == nombre.lower() for p in productos_disponibles):
                messagebox.showerror("Error", f"Ya existe un producto con el nombre '{nombre}'.")
                return

            productos_disponibles.append({"nombre": nombre, "precio": str(precio), "imagen": imagen_path, "stock": stock})
            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            nombre_entry.delete(0, tk.END)
            precio_entry.delete(0, tk.END)
            stock_entry.delete(0, tk.END)
            stock_entry.insert(0, "1")
            selected_image_path["path"] = "" # Resetear path
            go_admin() # Recargar la vista de admin

        tk.Button(add_frame, text="Agregar producto", command=agregar, bg="#AED581").pack(pady=10)

        # Sección para gestionar productos existentes
        manage_frame = tk.LabelFrame(frame, text="Gestionar Productos Existentes", bg="white", padx=10, pady=10)
        manage_frame.pack(padx=10, pady=10, fill="x")

        if not productos_disponibles:
            tk.Label(manage_frame, text="No hay productos para gestionar.", bg="white", fg="gray").pack(pady=10)
        else:
            for i, p in enumerate(productos_disponibles):
                f_prod_item = tk.Frame(manage_frame, bg="white", relief="solid", bd=1)
                f_prod_item.pack(fill="x", padx=5, pady=2)
                # Mostrar nombre, precio y stock
                tk.Label(f_prod_item, text=f"{p['nombre']} - ${p['precio']} - Stock: {p['stock']}", bg="white").pack(side="left", padx=5, expand=True, fill="x")
                tk.Button(f_prod_item, text="Eliminar", command=lambda idx=i: eliminar(idx), bg="salmon").pack(side="right", padx=5)

        def eliminar(index):
            if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar '{productos_disponibles[index]['nombre']}'?"):
                del productos_disponibles[index]
                messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
                go_admin() # Recargar la vista de admin

    # Botones de navegación
    tk.Button(nav, image=icon_inicio, text="inicio", compound="top", command=go_inicio, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_buscar, text="buscar", compound="top", command=go_buscar, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_usuario, text="usuario", compound="top", command=go_usuario, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_carrito, text="carrito", compound="top", command=go_carrito, bg="white", fg="black").pack(side="left", expand=True)
    
    # El botón de admin siempre visible en este código original
    tk.Button(nav, text="admin", compound="top", command=go_admin, bg="white", fg="black").pack(side="left", expand=True)

    go_inicio()
    root.mainloop()

if __name__ == "__main__":
    # Opcional: Crear el directorio de imágenes si no existe
    # if not os.path.exists(IMG_BASE):
    #     os.makedirs(IMG_BASE)
    #     messagebox.showwarning("Advertencia", f"Se ha creado el directorio de imágenes en:\n{IMG_BASE}\nPor favor, coloca tus imágenes de producto allí.")
    
    # Asegurarse de que el archivo de historial de compras existe o crearlo vacío al inicio
    if not os.path.exists(HISTORIAL_COMPRAS_FILE):
        guardar_json([], HISTORIAL_COMPRAS_FILE)

    iniciar_autenticacion()


