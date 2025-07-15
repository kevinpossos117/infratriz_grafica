import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import os
import json
import datetime
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ARCHIVO_DATOS = "data.json" # Aquí guardamos la información de tus usuarios.
HISTORIAL_COMPRAS_FILE = "historial_compras.json" # Este es el registro de todas las ventas.

usuario_actual = None # Variable para saber quién está usando la app en este momento.

IMG_BASE = "C:\\Users\\kevin\\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras"

# funciones json
def cargar_json(filepath):
    """
    Trae los datos desde un archivo JSON. Si no lo encuentra o hay un problema,
    te da una lista vacía para empezar de nuevo.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Nos aseguramos de que no esté vacío o sea nulo
            return data if data is not None else []
    except json.JSONDecodeError:
        messagebox.showerror("¡Ups, un archivo dañado!", f"Parece que el archivo '{filepath}' está un poco revuelto o vacío. ¡No te preocupes, lo reiniciaremos para ti!")
        return []
    except Exception as e:
        messagebox.showerror("Error al cargar", f"No pudimos leer '{filepath}'. Algo inesperado pasó: {e}")
        return []

def guardar_json(datos, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
    except IOError as e:
        messagebox.showerror("Problemas al guardar", f"No pudimos guardar tus cambios en '{filepath}'. Revisa si hay algún problema de permisos: {e}")

# cargar imágenes
def load_icon(path):
    """Carga y ajusta el tamaño de una imagen para que se vea bien como un icono."""
    try:
        image = Image.open(path)
        image = image.resize((30, 30), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"No pude cargar el icono en '{path}'. ¿Está ahí?: {e}")
        return None

def load_image(path, size=(80, 80)):
    try:
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"No pude cargar la imagen en '{path}'. ¿Está ahí?: {e}")
        return None

# datos de productos
productos_disponibles = [
    {"nombre": "comida para gatos", "precio": "15000", "imagen": os.path.join(IMG_BASE, "ringogato.png"), "stock": 10},
    {"nombre": "comida para perro", "precio": "25000", "imagen": os.path.join(IMG_BASE, "perro.png"), "stock": 15},
    {"nombre": "comida para gatos pequenos", "precio": "10000", "imagen": os.path.join(IMG_BASE, "gato_pequeño.png"), "stock": 20},
    {"nombre": "comida para cachorros", "precio": "20000", "imagen": os.path.join(IMG_BASE, "perros_pequeños.png"), "stock": 12},
]

# autenticación
def iniciar_autenticacion():
    def login():
        nonlocal root
        global usuario_actual
        user = entry_user.get()
        password = entry_pass.get()
        for u in cargar_json(ARCHIVO_DATOS):
            if u["user"] == user and u["pass"] == password:
                usuario_actual = u
                messagebox.showinfo("¡Bienvenido de nuevo!", f"¡Hola {user}, qué bueno verte por aquí!")
                root.destroy() 
                abrir_tienda() 
                return
        messagebox.showerror("Acceso denegado", "¡Uy! Parece que tu usuario o contraseña no son correctos. Intenta de nuevo.")

    def registrar():
        user = entry_new_user.get()
        password = entry_new_pass.get()
        if not user or not password:
            messagebox.showerror("¡Faltan datos!", "Por favor, llena todos los campos para registrarte.")
            return
        datos = cargar_json(ARCHIVO_DATOS)
        for u in datos:
            if u["user"] == user:
                messagebox.showerror("Usuario ya existe", "¡Vaya! Parece que ese nombre de usuario ya está en uso. Elige otro, por favor.")
                return
        datos.append({"user": user, "pass": password, "foto": ""})
        guardar_json(datos, ARCHIVO_DATOS)
        messagebox.showinfo("¡Registro exitoso!", "¡Felicidades! Ya estás registrado. Ahora puedes iniciar sesión.")
        frame_reg.pack_forget()
        frame_login.pack() 
    root = tk.Tk()
    root.title("¡Bienvenido a AGRO.MAX!")
    root.geometry("300x400")
    root.configure(bg="#195E5E") 
    try:
        img_path = os.path.join(IMG_BASE, "unnamed.png")
        img = Image.open(img_path).resize((100, 100))
        logo = ImageTk.PhotoImage(img)
        tk.Label(root, image=logo, bg="#195E5E").pack(pady=10)
    except Exception as e:
        print(f"No pude cargar el logo: {e}. Quizás la imagen no está en la ruta correcta.")
        tk.Label(root, text="AGRO.MAX", font=("Arial", 20, "bold"), bg="#195E5E", fg="white").pack(pady=10)

    # Marco para iniciar sesión
    frame_login = tk.Frame(root, bg="#195E5E")
    tk.Label(frame_login, text="Tu Usuario", bg="#195E5E", fg="white").pack()
    entry_user = tk.Entry(frame_login)
    entry_user.pack()
    tk.Label(frame_login, text="Tu Contraseña", bg="#195E5E", fg="white").pack()
    entry_pass = tk.Entry(frame_login, show="*")
    entry_pass.pack()
    tk.Button(frame_login, text="Entrar", command=login, bg="#B7CE63").pack(pady=10)
    tk.Button(frame_login, text="¿Eres nuevo? Regístrate aquí", command=lambda: switch(True)).pack()
    frame_login.pack()

    # Marco para registrarse
    frame_reg = tk.Frame(root, bg="#195E5E")
    tk.Label(frame_reg, text="Elige un nuevo usuario", bg="#195E5E", fg="white").pack()
    entry_new_user = tk.Entry(frame_reg)
    entry_new_user.pack()
    tk.Label(frame_reg, text="Crea tu contraseña", bg="#195E5E", fg="white").pack()
    entry_new_pass = tk.Entry(frame_reg, show="*")
    entry_new_pass.pack()
    tk.Button(frame_reg, text="Crear cuenta", command=registrar, bg="#B7CE63").pack(pady=10)
    tk.Button(frame_reg, text="¡Ya tengo cuenta! Iniciar sesión", command=lambda: switch(False)).pack()

    def switch(to_reg):
        if to_reg:
            frame_login.pack_forget() 
            frame_reg.pack() # Muestra el registro.
        else:
            frame_reg.pack_forget() # Oculta el registro.
            frame_login.pack() # Muestra el login.

    root.mainloop() 

# aplicación principal
def abrir_tienda():
    global root_tienda_app 
    root_tienda_app = tk.Tk()
    root_tienda_app.geometry("700x800") # El tamaño de tu tienda.
    root_tienda_app.title("AGRO.MAX - Tu tienda de confianza")

    # El área principal donde se mostrará todo el contenido (productos, carrito, etc.)
    frame = tk.Frame(root_tienda_app, bg="white")
    frame.pack(fill="both", expand=True)

    # La barra de navegación en la parte de abajo.
    nav = tk.Frame(root_tienda_app, height=60, bg="white")
    nav.pack(side="bottom", fill="x")

    # Cargamos los pequeños iconos para la navegación.
    icon_inicio = load_icon(os.path.join(IMG_BASE, "inicio.png"))
    icon_buscar = load_icon(os.path.join(IMG_BASE, "lupa.png"))
    icon_usuario = load_icon(os.path.join(IMG_BASE, "usuario.png"))
    icon_carrito = load_icon(os.path.join(IMG_BASE, "carrito.png"))
    icon_admin = load_icon(os.path.join(IMG_BASE, "admin.png"))

    carrito = [] #guardae lo que el cliente ponga en su carrito.

    def limpiar():
        for widget in frame.winfo_children():
            widget.destroy()

    def go_inicio():
        limpiar()
        tk.Label(frame, text="Nuestros Productos", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        if not productos_disponibles:
            tk.Label(frame, text="¡Vaya! Parece que no hay productos disponibles en este momento.", bg="white", fg="gray").pack(pady=20)
            return

        # Mostramos cada producto.
        for prod in productos_disponibles:
            f = tk.Frame(frame, bg="white", relief="solid", bd=1, padx=5, pady=5)
            f.pack(padx=5, pady=5, fill="x")

            img = load_image(prod["imagen"])
            if img:
                lbl_img = tk.Label(f, image=img, bg="white")
                lbl_img.pack(side="left")
                f.image = img # ¡Importante! Mantenemos la referencia para que no se borre.
            else:
                tk.Label(f, text="[IMAGEN NO DISPONIBLE]", bg="white", width=10, height=5, relief="groove").pack(side="left")

            info = tk.Frame(f, bg="white")
            info.pack(side="left", padx=10, expand=True, fill="x")

            tk.Label(info, text=prod["nombre"], bg="white", font=("Arial", 12)).pack(anchor="w")
            tk.Label(info, text=f"Precio: ${prod['precio']}", bg="white", fg="green").pack(anchor="w")
            tk.Label(info, text=f"En stock: {prod['stock']}", bg="white", fg="blue").pack(anchor="w")

            if prod["stock"] > 0:
                tk.Button(info, text="comprar", command=lambda p=prod: agregar_carrito(p), bg="#C8E6C9").pack(anchor="e", pady=5)
            else:
                tk.Label(info, text="¡AGOTADO!", bg="white", fg="red", font=("Arial", 10, "bold")).pack(anchor="e", pady=5)

    def go_buscar():
        limpiar()
        tk.Label(frame, text="Busca tus productos favoritos", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        search_frame = tk.Frame(frame, bg="white")
        search_frame.pack(pady=10)

        query = tk.Entry(search_frame, width=30)
        query.pack(side="left", padx=5)

        results_frame = tk.Frame(frame, bg="white")
        results_frame.pack(pady=10, fill="both", expand=True)

        def buscar():
            for widget in results_frame.winfo_children():
                widget.destroy() # Borra los resultados anteriores.

            search_term = query.get().lower()
            resultados = [p for p in productos_disponibles if search_term in p["nombre"].lower()]

            if not resultados:
                tk.Label(results_frame, text="¡Uy! No encontramos productos con ese nombre. Intenta de nuevo.", bg="white", fg="gray").pack(pady=10)
                return

            for p in resultados:
                f_res = tk.Frame(results_frame, bg="white", relief="solid", bd=1, padx=5, pady=5)
                f_res.pack(padx=5, pady=2, fill="x")

                tk.Label(f_res, text=f"{p['nombre']} - ${p['precio']} - En stock: {p['stock']}", bg="white").pack(side="left")

                if p["stock"] > 0:
                    tk.Button(f_res, text="comprar", command=lambda prod_item=p: agregar_carrito(prod_item), bg="#C8E6C9").pack(side="right", padx=5)
                else:
                    tk.Label(f_res, text="¡AGOTADO!", bg="white", fg="red", font=("Arial", 9, "bold")).pack(side="right", padx=5)

        tk.Button(search_frame, text="Buscar", command=buscar, bg="#AED581").pack(side="left", padx=5)

    def go_usuario():
        limpiar()
        tk.Label(frame, text="Tu Perfil", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        path = usuario_actual.get("foto", "")
        img = load_image(path, size=(120, 120))
        if img:
            lbl = tk.Label(frame, image=img, bg="white")
            lbl.image = img
            lbl.pack(pady=10)
        else:
            tk.Label(frame, text="¡Aún no tienes una foto de perfil!", bg="white", fg="gray").pack(pady=10)

        tk.Button(frame, text="Cambiar mi foto", command=cambiar_foto, bg="lightblue").pack(pady=5)
        tk.Label(frame, text=f"Tu usuario: {usuario_actual['user']}", bg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(frame, text="Editar mi información y contraseña", command=editar_perfil, bg="lightsteelblue").pack(pady=5)
        tk.Button(frame, text="Eliminar mi cuenta (¡Cuidado!)", command=eliminar_cuenta, bg="salmon").pack(pady=5)
        tk.Button(frame, text="Cerrar Sesión", command=lambda: cerrar_sesion(root_tienda_app), bg="khaki").pack(pady=5)

    def cambiar_foto():
        """Permite al usuario seleccionar una nueva foto de perfil."""
        path = filedialog.askopenfilename(title="Elige tu nueva foto de perfil", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")])
        if path:
            usuario_actual["foto"] = path
            datos = cargar_json(ARCHIVO_DATOS)
            for u in datos:
                if u["user"] == usuario_actual["user"]:
                    u["foto"] = path
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("¡Foto actualizada!", "¡Tu foto de perfil ha sido cambiada exitosamente!")
            go_usuario() # Volvemos a cargar el perfil para que veas tu nueva foto.

    def editar_perfil():
        """Permite al usuario cambiar su nombre de usuario o contraseña."""
        nuevo_user = simpledialog.askstring("Cambiar Usuario", "Escribe tu nuevo nombre de usuario:", initialvalue=usuario_actual["user"])
        nueva_pass = simpledialog.askstring("Cambiar Contraseña", "Escribe tu nueva contraseña (déjalo en blanco si no quieres cambiarla):", show="*")

        cambios_realizados = False
        if nuevo_user and nuevo_user != usuario_actual["user"]:
            datos = cargar_json(ARCHIVO_DATOS)
            if any(u["user"] == nuevo_user for u in datos if u["user"] != usuario_actual["user"]):
                messagebox.showerror("¡Usuario no disponible!", "¡Lo sentimos! Ese nombre de usuario ya lo tiene otra persona.")
                return
            usuario_actual["user"] = nuevo_user
            cambios_realizados = True

        if nueva_pass:
            usuario_actual["pass"] = nueva_pass
            cambios_realizados = True

        if cambios_realizados:
            datos = cargar_json(ARCHIVO_DATOS)
            # Buscamos al usuario por su nombre original para actualizarlo.
            for i, u in enumerate(datos):
                # Usamos el nuevo_user si se cambió, de lo contrario, el actual.
                if u["user"] == (nuevo_user if ('nuevo_user' in locals() and nuevo_user) else usuario_actual["user"]):
                    datos[i] = usuario_actual
                    break
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("¡Perfil actualizado!", "¡Tu información ha sido guardada con éxito!")
            go_usuario() # Recargamos la vista del perfil para que veas los cambios.
        else:
            messagebox.showinfo("¡Todo igual!", "No hiciste ningún cambio en tu perfil.")

    def eliminar_cuenta():
        """Permite al usuario eliminar su cuenta."""
        if messagebox.askyesno("¡Atención! Eliminar Cuenta", "¿Estás ABSOLUTAMENTE seguro de que quieres eliminar tu cuenta?\n¡Esta acción no se puede deshacer!"):
            global usuario_actual
            datos = cargar_json(ARCHIVO_DATOS)
            # Filtramos para quedarnos solo con las cuentas que no son la del usuario actual.
            datos = [u for u in datos if u["user"] != usuario_actual["user"]]
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("¡Cuenta eliminada!", "¡Tu cuenta ha sido eliminada con éxito! Te extrañaremos.")
            cerrar_sesion(root_tienda_app) # Cerramos la tienda y volvemos a la pantalla de inicio.

    def cerrar_sesion(root_tienda_app_param): # Recibimos la ventana como parámetro para cerrarla.
        global usuario_actual
        usuario_actual = None # Desvinculamos el usuario actual.
        root_tienda_app_param.destroy() # Cerramos la ventana de la tienda.
        iniciar_autenticacion() # Volvemos a la pantalla de inicio de sesión.

    def go_carrito():
        limpiar()
        tk.Label(frame, text="Tu Carrito de Compras", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        if not carrito:
            tk.Label(frame, text="¡Tu carrito está vacío! ¿Qué esperas? ¡Agrega productos!", bg="white", fg="gray").pack(pady=20)
            return

        total = 0
        # Agrupamos los productos para mostrarlos de forma ordenada y calcular el total.
        productos_agrupados = defaultdict(int)
        for item in carrito:
            productos_agrupados[item["nombre"]] += 1
            total += int(item["precio"])

        for nombre_prod, cantidad in productos_agrupados.items():
            # Buscamos el precio original del producto para mostrarlo.
            precio_unitario = 0
            for p in productos_disponibles:
                if p["nombre"] == nombre_prod:
                    precio_unitario = int(p["precio"])
                    break

            item_frame = tk.Frame(frame, bg="white", relief="groove", bd=1)
            item_frame.pack(anchor="w", padx=20, pady=2, fill="x")
            tk.Label(item_frame, text=f"{nombre_prod} (x{cantidad}) - ${precio_unitario * cantidad:,}", bg="white").pack(side="left", fill="x", expand=True)
            tk.Button(item_frame, text="Quitar uno", command=lambda name=nombre_prod: quitar_del_carrito(name), bg="lightcoral").pack(side="right", padx=5)

        tk.Frame(frame, height=2, bg="lightgray").pack(fill="x", padx=15, pady=10) # Una línea bonita para separar.
        tk.Label(frame, text=f"Total a pagar: ${total:,}", bg="white", font=("Arial", 14, "bold"), fg="green").pack(pady=10)

        if carrito: # Solo mostramos el botón de pagar si hay algo en el carrito.
            tk.Button(frame, text="Proceder al Pago", command=lambda: pagar_con_opciones(total), bg="#B7CE63").pack(pady=10)

    def quitar_del_carrito(product_name):
        """Quita una unidad de un producto del carrito y vuelve a añadirlo al stock."""
        found = False
        for i, item in enumerate(carrito):
            if item["nombre"] == product_name:
                # Devolvemos el producto al stock general.
                for p in productos_disponibles:
                    if p["nombre"] == product_name:
                        p["stock"] += 1
                        break
                carrito.pop(i) # Lo sacamos del carrito.
                found = True
                messagebox.showinfo("Carrito actualizado", f"Quitamos una unidad de '{product_name}' de tu carrito.")
                break
        if not found:
            messagebox.showerror("¡Vaya!", f"'{product_name}' no se encontró en tu carrito.")
        go_carrito() # Refrescamos la vista de tu carrito.

    def pagar_con_opciones(total_a_pagar):
        if not carrito:
            messagebox.showerror("¡Carrito vacío!", "Por favor, agrega algunos productos antes de intentar pagar.")
            return

        pago_window = tk.Toplevel(root_tienda_app) # Abrimos una nueva ventana para el pago.
        pago_window.title("Confirmar tu Pago")
        pago_window.geometry("350x400")
        pago_window.transient(root_tienda_app) # Esta ventana "pertenece" a la principal.
        pago_window.grab_set() # Bloquea la interacción con la ventana principal hasta que esta se cierre.

        pago_frame = tk.Frame(pago_window, bg="white", padx=20, pady=20)
        pago_frame.pack(fill="both", expand=True)

        tk.Label(pago_frame, text="¿Cómo quieres pagar?", font=("Arial", 14, "bold"), bg="white", fg="#195E5E").pack(pady=10)
        tk.Label(pago_frame, text=f"Total a Pagar: ${total_a_pagar:,}", font=("Arial", 12, "bold"), bg="white", fg="green").pack(pady=5)

        metodo_pago_var = tk.StringVar(value="Efectivo") # Por defecto, pago en efectivo.

        card_details_frame = tk.Frame(pago_frame, bg="white") # Aquí irán los campos de la tarjeta.

        def mostrar_campos_tarjeta():
            """Muestra u oculta los campos para la tarjeta según el método de pago seleccionado."""
            for widget in card_details_frame.winfo_children():
                widget.destroy() # Borramos los campos anteriores.
            if metodo_pago_var.get() in ["Tarjeta Visa", "Mastercard"]:
                tk.Label(card_details_frame, text="Número de Tarjeta:", bg="white").pack(anchor="w", pady=(10,0))
                entry_card_number = tk.Entry(card_details_frame, width=30)
                entry_card_number.pack(fill="x", pady=2)

                tk.Label(card_details_frame, text="Fecha de Vencimiento (MM/AA):", bg="white").pack(anchor="w", pady=(10,0))
                entry_expiry = tk.Entry(card_details_frame, width=10)
                entry_expiry.pack(fill="x", pady=2)

                tk.Label(card_details_frame, text="Código de Seguridad (CVV):", bg="white").pack(anchor="w", pady=(10,0))
                entry_cvv = tk.Entry(card_details_frame, width=5, show="*")
                entry_cvv.pack(fill="x", pady=2)
            card_details_frame.pack(fill="x", pady=5) # Mostramos el marco de los detalles de la tarjeta.

        tk.Radiobutton(pago_frame, text="Efectivo", variable=metodo_pago_var, value="Efectivo", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)
        tk.Radiobutton(pago_frame, text="Tarjeta Visa", variable=metodo_pago_var, value="Tarjeta Visa", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)
        tk.Radiobutton(pago_frame, text="Mastercard", variable=metodo_pago_var, value="Mastercard", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)

        # Para que se muestren los campos de la tarjeta al inicio si ya está seleccionada esa opción.
        mostrar_campos_tarjeta()

        def finalizar_pago():
            metodo_seleccionado = metodo_pago_var.get()

            if metodo_seleccionado in ["Tarjeta Visa", "Mastercard"]:
                # Tomamos los valores de los campos de la tarjeta.
                entries = [w for w in card_details_frame.winfo_children() if isinstance(w, tk.Entry)]
                if len(entries) < 3:
                    messagebox.showerror("Error de Pago", "¡Ups! Algo salió mal con los campos de la tarjeta. Intenta de nuevo.")
                    return

                card_num = entries[0].get()
                expiry = entries[1].get()
                cvv = entries[2].get()

                if not card_num or not expiry or not cvv:
                    messagebox.showerror("¡Faltan datos de la tarjeta!", "Por favor, completa todos los campos de tu tarjeta para continuar.")
                    return
                # Hacemos algunas validaciones básicas.
                if not card_num.isdigit() or not (13 <= len(card_num) <= 19):
                    messagebox.showerror("Número de tarjeta inválido", "El número de tarjeta debe contener solo dígitos y tener entre 13 y 19 números.")
                    return
                if not expiry.count('/') == 1 or not all(part.isdigit() for part in expiry.split('/')) or len(expiry) != 5:
                    messagebox.showerror("Fecha de vencimiento inválida", "El formato de la fecha de vencimiento debe ser MM/AA.")
                    return
                if not cvv.isdigit() or not (3 <= len(cvv) <= 4):
                    messagebox.showerror("CVV inválido", "El CVV debe ser de 3 o 4 dígitos numéricos.")
                    return

            # registrar la compra en el historial
            historial = cargar_json(HISTORIAL_COMPRAS_FILE)

            # Organizamos los productos del carrito para el registro.
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
                "id_transaccion": datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"), # Un número único para cada compra.
                "usuario": usuario_actual["user"],
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "metodo_pago": metodo_seleccionado,
                "total_pagado": total_a_pagar,
                "productos": lista_items_historial # Tus productos con cantidades y precios.
            }
            historial.append(registro_compra)
            guardar_json(historial, HISTORIAL_COMPRAS_FILE)

            carrito.clear() # ¡Listo! Vaciamos el carrito después de la compra.
            messagebox.showinfo("¡Compra Exitosa!", f"¡Tu compra de ${total_a_pagar:,} ha sido procesada con éxito usando {metodo_seleccionado}! ¡Muchas gracias por tu compra!")
            pago_window.destroy() # Cerramos la ventana de pago.
            go_carrito() # Actualizamos la vista del carrito (ahora estará vacío).

        tk.Button(pago_frame, text="Confirmar Pago", command=finalizar_pago, bg="#B7CE63").pack(pady=20, fill="x")
        pago_window.mainloop() # Mantenemos esta ventana activa hasta que se cierre.

    def agregar_carrito(prod_to_add):
        """Agrega un producto al carrito y actualiza su stock."""
        # Buscamos el producto real en nuestra lista para modificar su stock.
        found_product = None
        for p in productos_disponibles:
            if p["nombre"] == prod_to_add["nombre"]:
                found_product = p
                break

        if found_product and found_product["stock"] > 0:
            found_product["stock"] -= 1 # Le restamos uno al stock.
            carrito.append(found_product) # Añadimos el producto al carrito.
            messagebox.showinfo("¡Al carrito!", f"¡'{prod_to_add['nombre']}' se ha añadido a tu carrito!")
            go_inicio() # Refrescamos la página de inicio para que veas el stock actualizado.
        elif found_product and found_product["stock"] <= 0:
            messagebox.showerror("¡Sin stock!", f"¡Lo sentimos mucho! '{prod_to_add['nombre']}' se ha agotado.")
        else:
            messagebox.showerror("¡Producto no encontrado!", "Parece que hubo un problema y no pudimos encontrar este producto.")

    def go_admin():
        limpiar()
        tk.Label(frame, text="Panel de Administración", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        # añadir producto
        add_frame = tk.LabelFrame(frame, text="Agregar un Producto Nuevo", bg="white", padx=10, pady=10)
        add_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(add_frame, text="Nombre del Producto:", bg="white").pack(anchor="w")
        nombre_entry = tk.Entry(add_frame)
        nombre_entry.pack(fill="x")

        tk.Label(add_frame, text="Precio ($):", bg="white").pack(anchor="w")
        precio_entry = tk.Entry(add_frame)
        precio_entry.pack(fill="x")

        tk.Label(add_frame, text="Cantidad en Stock:", bg="white").pack(anchor="w")
        stock_entry = tk.Entry(add_frame)
        stock_entry.insert(0, "1") # Valor inicial sugerido.
        stock_entry.pack(fill="x")

        selected_image_path = {"path": ""} # Usamos un diccionario para guardar la ruta de la imagen.

        def seleccionar_imagen_admin():
            """Abre un diálogo para que el administrador elija una imagen para el producto."""
            filepath = filedialog.askopenfilename(title="Elige una imagen para tu producto", filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.gif")])
            if filepath:
                selected_image_path["path"] = filepath
                messagebox.showinfo("¡Imagen lista!", f"Seleccionaste: {os.path.basename(filepath)}")

        tk.Button(add_frame, text="Elegir Imagen", command=seleccionar_imagen_admin, bg="#B7CE63").pack(pady=5)

        def agregar():
            """Añade el nuevo producto a la lista de productos disponibles."""
            nombre = nombre_entry.get().strip()
            precio_str = precio_entry.get().strip()
            stock_str = stock_entry.get().strip()
            imagen_path = selected_image_path["path"]

            if not nombre or not precio_str or not stock_str or not imagen_path:
                messagebox.showerror("¡Faltan campos!", "Por favor, llena todos los campos y selecciona una imagen para el producto.")
                return

            try:
                precio = int(precio_str)
                stock = int(stock_str)
                if precio <= 0 or stock < 0:
                    messagebox.showerror("¡Valores incorrectos!", "El precio debe ser un número positivo y el stock no puede ser negativo.")
                    return
            except ValueError:
                messagebox.showerror("¡Error de números!", "El precio y el stock deben ser números válidos. ¡Revísalos!")
                return

            if any(p["nombre"].lower() == nombre.lower() for p in productos_disponibles):
                messagebox.showerror("¡Nombre duplicado!", f"¡Oops! Ya tienes un producto llamado '{nombre}'. Por favor, elige otro nombre.")
                return

            productos_disponibles.append({"nombre": nombre, "precio": str(precio), "imagen": imagen_path, "stock": stock})
            messagebox.showinfo("¡Producto añadido!", "¡Tu nuevo producto ha sido agregado con éxito!")
            # Limpiamos los campos para que puedas añadir otro.
            nombre_entry.delete(0, tk.END)
            precio_entry.delete(0, tk.END)
            stock_entry.delete(0, tk.END)
            stock_entry.insert(0, "1")
            selected_image_path["path"] = ""
            go_admin() # Recargamos la vista de administración para ver el nuevo producto.

        tk.Button(add_frame, text="Añadir Producto", command=agregar, bg="#AED581").pack(pady=10)

        # gestionar productos existentes
        manage_frame = tk.LabelFrame(frame, text="Administra tus Productos Existentes", bg="white", padx=10, pady=10)
        manage_frame.pack(padx=10, pady=10, fill="x")

        if not productos_disponibles:
            tk.Label(manage_frame, text="¡Aún no tienes productos para gestionar!", bg="white", fg="gray").pack(pady=10)
        else:
            for i, p in enumerate(productos_disponibles):
                f_prod_item = tk.Frame(manage_frame, bg="white", relief="solid", bd=1)
                f_prod_item.pack(fill="x", padx=5, pady=2)
                tk.Label(f_prod_item, text=f"{p['nombre']} - ${p['precio']} - Stock: {p['stock']}", bg="white").pack(side="left", padx=5, expand=True, fill="x")
                tk.Button(f_prod_item, text="Eliminar", command=lambda idx=i: eliminar(idx), bg="salmon").pack(side="right", padx=5)

        def eliminar(index):
            """Elimina un producto de la lista."""
            if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar '{productos_disponibles[index]['nombre']}'?\n¡Esta acción no se puede deshacer!"):
                del productos_disponibles[index]
                messagebox.showinfo("¡Producto eliminado!", "¡El producto ha sido eliminado con éxito!")
                go_admin() # Recargamos la vista de administración.

        # botón ver estadísticas
        tk.Button(frame, text="Ver Estadísticas y Reportes de Ventas", command=mostrar_estadisticas_admin, bg="#B7CE63").pack(pady=15)


    # estadísticas (ventana separada)
    def mostrar_estadisticas_admin():
        stats_window = tk.Toplevel(root_tienda_app) # Creamos la nueva ventana para las estadísticas.
        stats_window.title("Estadísticas Clave de tu Tienda")
        stats_window.geometry("800x950") # Un buen tamaño para ver las gráficas.
        stats_window.transient(root_tienda_app) # Esta ventana es parte de la tienda principal.
        stats_window.grab_set() # Te obliga a interactuar con esta ventana antes de volver a la principal.

        # El marco principal dentro de esta nueva ventana.
        stats_frame = tk.Frame(stats_window, bg="white")
        stats_frame.pack(fill="both", expand=True)

        tk.Label(stats_frame, text="Un Vistazo a tus Ventas", font=("Arial", 18, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        historial_raw = cargar_json(HISTORIAL_COMPRAS_FILE)

        if not historial_raw:
            tk.Label(stats_frame, text="¡Parece que aún no hay datos de compras para mostrarte estadísticas!", bg="white", fg="gray").pack(pady=20)
            tk.Button(stats_frame, text="Volver al Panel de Administración", command=stats_window.destroy, bg="lightgray").pack(pady=10)
            stats_window.mainloop() # Iniciamos el ciclo para esta ventana.
            return

        # Convertimos los datos a un formato que Pandas entiende (¡es genial para analizar datos!).
        df_compras = pd.DataFrame(historial_raw)

        # Nos aseguramos de que los números y fechas sean correctos.
        df_compras['total_pagado'] = pd.to_numeric(df_compras['total_pagado'], errors='coerce')
        df_compras['fecha'] = pd.to_datetime(df_compras['fecha'], errors='coerce')

        # Eliminamos cualquier fila que tenga errores después de la conversión.
        df_compras.dropna(subset=['total_pagado', 'fecha'], inplace=True)

        if df_compras.empty:
            tk.Label(stats_frame, text="¡Uy! No hay datos válidos de compras para generar las estadísticas.", bg="white", fg="gray").pack(pady=20)
            tk.Button(stats_frame, text="Volver al Panel de Administración", command=stats_window.destroy, bg="lightgray").pack(pady=10)
            stats_window.mainloop()
            return

        # Calculamos algunas métricas importantes para tu negocio.
        ganancias_totales = df_compras['total_pagado'].sum()
        num_compras_totales = df_compras.shape[0]
        # mode()[0] nos da el método de pago más popular.
        metodo_pago_mas_usado = df_compras['metodo_pago'].mode()[0] if not df_compras['metodo_pago'].empty else "Ninguno"

        tk.Label(stats_frame, text=f"Ganancias Totales: ${ganancias_totales:,.2f}", font=("Arial", 14), bg="white", fg="darkgreen").pack(pady=5)
        tk.Label(stats_frame, text=f"Número de Ventas: {num_compras_totales}", font=("Arial", 14), bg="white").pack(pady=5)
        tk.Label(stats_frame, text=f"Método de Pago Preferido: {metodo_pago_mas_usado}", font=("Arial", 14), bg="white").pack(pady=5)

        # gráficas matplotlib
        plt.style.use('ggplot') # Un estilo de gráficos que se ve muy bien.

        # Este será el área donde pondremos las gráficas, y permitirá desplazamiento si hay muchas.
        canvas_container = tk.Canvas(stats_frame, bg="white")
        canvas_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(stats_frame, orient="vertical", command=canvas_container.yview)
        scrollbar.pack(side="right", fill="y")
        canvas_container.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas_container, bg="white")
        canvas_container.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Ajustamos el área de desplazamiento para que el scroll funcione correctamente.
        scrollable_frame.bind("<Configure>", lambda e: canvas_container.configure(scrollregion = canvas_container.bbox("all")))

        # gráfica métodos de pago
        if not df_compras.empty:
            metodos_pago_counts = df_compras['metodo_pago'].value_counts()

            if not metodos_pago_counts.empty:
                # Gráfico de Barras
                fig1 = plt.Figure(figsize=(6, 4), dpi=100)
                ax1 = fig1.add_subplot(111)
                metodos_pago_counts.plot(kind='bar', ax=ax1, color=['#4CAF50', '#2196F3', '#FFC107']) # Colores bonitos.
                ax1.set_title('Tus Métodos de Pago Más Usados')
                ax1.set_ylabel('Cuántas Veces se Usó')
                ax1.set_xlabel('Tipo de Pago')
                fig1.tight_layout() # Aseguramos que todo se vea bien.

                canvas1 = FigureCanvasTkAgg(fig1, master=scrollable_frame)
                canvas1_widget = canvas1.get_tk_widget()
                canvas1_widget.pack(pady=10, fill="both", expand=True)

                # Gráfico Circular (pastel)
                fig_pie = plt.Figure(figsize=(6, 4), dpi=100)
                ax_pie = fig_pie.add_subplot(111)
                ax_pie.pie(metodos_pago_counts, labels=metodos_pago_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#2196F3', '#FFC107'])
                ax_pie.axis('equal')  # Para que el círculo se vea redondo.
                ax_pie.set_title('Distribución de tus Métodos de Pago')
                fig_pie.tight_layout()

                canvas_pie = FigureCanvasTkAgg(fig_pie, master=scrollable_frame)
                canvas_pie_widget = canvas_pie.get_tk_widget()
                canvas_pie_widget.pack(pady=10, fill="both", expand=True)

        # gráfica productos más vendidos
        productos_vendidos_raw = []
        for _, row in df_compras.iterrows():
            if 'productos' in row and isinstance(row['productos'], list):
                for prod in row['productos']:
                    productos_vendidos_raw.append({'nombre': prod['nombre'], 'cantidad': prod['cantidad']})

        if productos_vendidos_raw:
            df_productos_vendidos = pd.DataFrame(productos_vendidos_raw)
            df_productos_vendidos['cantidad'] = pd.to_numeric(df_productos_vendidos['cantidad'], errors='coerce')
            df_productos_vendidos.dropna(subset=['cantidad'], inplace=True)

            if not df_productos_vendidos.empty:
                top_productos = df_productos_vendidos.groupby('nombre')['cantidad'].sum().sort_values(ascending=False).head(5) # Los 5 mejores.

                if not top_productos.empty:
                    fig2 = plt.Figure(figsize=(6, 4), dpi=100)
                    ax2 = fig2.add_subplot(111)
                    top_productos.plot(kind='barh', ax=ax2, color='skyblue')
                    ax2.set_title('Tus 5 Productos Más Vendidos')
                    ax2.set_xlabel('Cantidad Total Vendida')
                    ax2.set_ylabel('Producto')
                    fig2.tight_layout()

                    canvas2 = FigureCanvasTkAgg(fig2, master=scrollable_frame)
                    canvas2_widget = canvas2.get_tk_widget()
                    canvas2_widget.pack(pady=10, fill="both", expand=True)

        # gráfica ventas diarias
        if not df_compras.empty:
            df_compras['dia'] = df_compras['fecha'].dt.to_period('D') # Agrupamos las ventas por día.
            ventas_diarias = df_compras.groupby('dia')['total_pagado'].sum()
            ventas_diarias.index = ventas_diarias.index.to_timestamp() # Para que el eje X se vea como fechas.

            if not ventas_diarias.empty:
                fig3 = plt.Figure(figsize=(6, 4), dpi=100)
                ax3 = fig3.add_subplot(111)
                ventas_diarias.plot(kind='line', ax=ax3, marker='o', color='purple')
                ax3.set_title('Tus Ventas Totales por Día')
                ax3.set_ylabel('Ganancias ($)')
                ax3.set_xlabel('Fecha de Venta')
                ax3.tick_params(axis='x', rotation=45) # Rotamos las fechas para que no se amontonen.
                fig3.tight_layout()

                canvas3 = FigureCanvasTkAgg(fig3, master=scrollable_frame)
                canvas3_widget = canvas3.get_tk_widget()
                canvas3_widget.pack(pady=10, fill="both", expand=True)

        # Un botón para regresar al panel de administración.
        tk.Button(stats_frame, text="Volver al Panel de Administración", command=stats_window.destroy, bg="lightgray").pack(pady=10)

        stats_window.mainloop() # Mantenemos esta ventana de estadísticas abierta.

    # barra de navegación
    tk.Button(nav, image=icon_inicio, text="Inicio", compound="top", command=go_inicio, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_buscar, text="Buscar", compound="top", command=go_buscar, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_usuario, text="Mi Perfil", compound="top", command=go_usuario, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_carrito, text="Carrito", compound="top", command=go_carrito, bg="white", fg="black").pack(side="left", expand=True)
    # ¡Un botón solo para ti, Administrador!
    tk.Button(nav, text="Admin", compound="top", command=go_admin, bg="white", fg="black").pack(side="left", expand=True)

    # Cuando inicie la aplicación, te mostraremos la página de inicio.
    go_inicio()
    root_tienda_app.mainloop()

# inicio del programa
if __name__ == "__main__":
    # Nos aseguramos de que tus archivos de datos existan para empezar.
    if not os.path.exists(ARCHIVO_DATOS):
        guardar_json([], ARCHIVO_DATOS)
    if not os.path.exists(HISTORIAL_COMPRAS_FILE):
        guardar_json([], HISTORIAL_COMPRAS_FILE)

    # Empezamos con la pantalla para iniciar sesión o registrarse.
    iniciar_autenticacion()