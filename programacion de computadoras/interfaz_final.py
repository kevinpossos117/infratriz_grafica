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
import shutil
import hashlib
import seaborn as sns # Importar seaborn para estilos de gráficos más bonitos

# --- Rutas de Archivos y Directorios ---
ARCHIVO_DATOS = "data.json"
HISTORIAL_COMPRAS_FILE = "historial_compras.json"

usuario_actual = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMG_PRODUCTOS_DIR = os.path.join(BASE_DIR, "imagenes_productos")
IMG_INTERFAZ_DIR = os.path.join(BASE_DIR, "imagenes_interfaz")
REPORTES_DIR = os.path.join(BASE_DIR, "reportes_exportados") # Aunque no exportaremos individualmente, lo mantenemos por si acaso.


if not os.path.exists(IMG_PRODUCTOS_DIR):
    os.makedirs(IMG_PRODUCTOS_DIR)
if not os.path.exists(IMG_INTERFAZ_DIR):
    os.makedirs(IMG_INTERFAZ_DIR)
if not os.path.exists(REPORTES_DIR):
    os.makedirs(REPORTES_DIR)

# --- Funciones JSON ---
def cargar_json(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
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

# --- Funciones de Hashing de Contraseñas ---
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# --- Funciones de Carga de Imágenes ---
def load_icon(filename):
    path = os.path.join(IMG_INTERFAZ_DIR, filename)
    try:
        image = Image.open(path)
        image = image.resize((30, 30), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"No pude cargar el icono en '{path}'. ¿Está ahí?: {e}")
        return None

def load_image(filename_or_path, size=(80, 80)):
    if not os.path.isabs(filename_or_path):
        filepath = os.path.join(IMG_PRODUCTOS_DIR, filename_or_path)
    else:
        filepath = filename_or_path

    try:
        image = Image.open(filepath)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"No pude cargar la imagen en '{filepath}'. ¿Está ahí?: {e}")
        return None

# --- Datos de Productos ---
productos_disponibles = [
    {"nombre": "comida para gatos", "precio": 15000, "imagen": "ringogato.png", "stock": 10},
    {"nombre": "comida para perro", "precio": 25000, "imagen": "perro.png", "stock": 15},
    {"nombre": "comida para gatos pequenos", "precio": 10000, "imagen": "gato_pequeño.png", "stock": 20},
    {"nombre": "comida para cachorros", "precio": 20000, "imagen": "perros_pequeños.png", "stock": 12},
]

# --- Autenticación ---
def iniciar_autenticacion():
    def login():
        nonlocal root
        global usuario_actual
        user = entry_user.get()
        password = entry_pass.get()
        for u in cargar_json(ARCHIVO_DATOS):
            if u["user"] == user and u["pass"] == hash_password(password):
                usuario_actual = u
                messagebox.showinfo("¡Bienvenido de nuevo!", f"¡Hola {user}, qué bueno verte por aquí!")
                root.destroy()
                abrir_tienda()
                return
        messagebox.showerror("Acceso denegado", "¡Uy! Parece que tu usuario o contraseña no son correctos. Intenta de nuevo.")

    def registrar():
        user = entry_new_user.get().strip()
        password = entry_new_pass.get().strip()
        if not user or not password:
            messagebox.showerror("¡Faltan datos!", "Por favor, llena todos los campos para registrarte.")
            return
        if len(password) < 6:
            messagebox.showerror("Contraseña débil", "Tu contraseña debe tener al menos 6 caracteres.")
            return

        datos = cargar_json(ARCHIVO_DATOS)
        for u in datos:
            if u["user"] == user:
                messagebox.showerror("Usuario ya existe", "¡Vaya! Parece que ese nombre de usuario ya está en uso. Elige otro, por favor.")
                return
        datos.append({"user": user, "pass": hash_password(password), "foto": ""})
        guardar_json(datos, ARCHIVO_DATOS)
        messagebox.showinfo("¡Registro exitoso!", "¡Felicidades! Ya estás registrado. Ahora puedes iniciar sesión.")
        frame_reg.pack_forget()
        frame_login.pack(fill="both", expand=True)

    root = tk.Tk()
    root.title("¡Bienvenido a AGRO.MAX!")
    root.geometry("300x400")
    root.configure(bg="#195E5E")
    root.resizable(True, True)

    try:
        img_path = os.path.join(IMG_INTERFAZ_DIR, "unnamed.png")
        img = Image.open(img_path).resize((100, 100))
        logo = ImageTk.PhotoImage(img)
        tk.Label(root, image=logo, bg="#195E5E").pack(pady=10)
    except Exception as e:
        print(f"No pude cargar el logo: {e}.")
        tk.Label(root, text="AGRO.MAX", font=("Arial", 20, "bold"), bg="#195E5E", fg="white").pack(pady=10)

    frame_login = tk.Frame(root, bg="#195E5E")
    tk.Label(frame_login, text="Tu Usuario", bg="#195E5E", fg="white").pack()
    entry_user = tk.Entry(frame_login)
    entry_user.pack()
    tk.Label(frame_login, text="Tu Contraseña", bg="#195E5E", fg="white").pack()
    entry_pass = tk.Entry(frame_login, show="*")
    entry_pass.pack()
    tk.Button(frame_login, text="Entrar", command=login, bg="#B7CE63").pack(pady=10)
    tk.Button(frame_login, text="¿Eres nuevo? Regístrate aquí", command=lambda: switch(True)).pack()
    frame_login.pack(fill="both", expand=True)

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
            frame_reg.pack(fill="both", expand=True)
        else:
            frame_reg.pack_forget()
            frame_login.pack(fill="both", expand=True)

    root.mainloop()

# --- Aplicación Principal (Tienda) ---
def abrir_tienda():
    global root_tienda_app
    root_tienda_app = tk.Tk()
    root_tienda_app.geometry("700x800")
    root_tienda_app.title("AGRO.MAX - Tu tienda de confianza")

    frame = tk.Frame(root_tienda_app, bg="white")
    frame.pack(fill="both", expand=True)

    nav = tk.Frame(root_tienda_app, height=60, bg="white")
    nav.pack(side="bottom", fill="x")

    icon_inicio = load_icon("inicio.png")
    icon_buscar = load_icon("lupa.png")
    icon_usuario = load_icon("usuario.png")
    icon_carrito = load_icon("carrito.png")
    icon_admin = load_icon("admin.png")

    carrito = []

    def limpiar():
        for widget in frame.winfo_children():
            widget.destroy()

    def go_inicio():
        limpiar()
        tk.Label(frame, text="Nuestros Productos", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        if not productos_disponibles:
            tk.Label(frame, text="¡Vaya! Parece que no hay productos disponibles en este momento.", bg="white", fg="gray").pack(pady=20)
            return

        product_canvas = tk.Canvas(frame, bg="white")
        product_canvas.pack(side="left", fill="both", expand=True)

        product_scrollbar = tk.Scrollbar(frame, orient="vertical", command=product_canvas.yview)
        product_scrollbar.pack(side="right", fill="y")

        product_canvas.configure(yscrollcommand=product_scrollbar.set)
        scrollable_product_frame = tk.Frame(product_canvas, bg="white")
        product_canvas.create_window((0, 0), window=scrollable_product_frame, anchor="nw")

        def on_frame_configure(event):
            product_canvas.configure(scrollregion=product_canvas.bbox("all"))
            product_canvas.itemconfig(product_canvas.create_window((0, 0), window=scrollable_product_frame, anchor="nw"), width=product_canvas.winfo_width())

        scrollable_product_frame.bind("<Configure>", on_frame_configure)
        product_canvas.bind("<Configure>", on_frame_configure)


        for prod in productos_disponibles:
            f = tk.Frame(scrollable_product_frame, bg="white", relief="solid", bd=1, padx=5, pady=5)
            f.pack(padx=5, pady=5, fill="x")

            img = load_image(prod["imagen"])
            if img:
                lbl_img = tk.Label(f, image=img, bg="white")
                lbl_img.pack(side="left")
                f.image = img
            else:
                tk.Label(f, text="[IMAGEN NO DISPONIBLE]", bg="white", width=10, height=5, relief="groove").pack(side="left")

            info = tk.Frame(f, bg="white")
            info.pack(side="left", padx=10, expand=True, fill="x")

            tk.Label(info, text=prod["nombre"], bg="white", font=("Arial", 12)).pack(anchor="w")
            tk.Label(info, text=f"Precio: ${prod['precio']:,}", bg="white", fg="green").pack(anchor="w")
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

        results_canvas = tk.Canvas(frame, bg="white")
        results_canvas.pack(pady=10, fill="both", expand=True, side="left")

        results_scrollbar = tk.Scrollbar(frame, orient="vertical", command=results_canvas.yview)
        results_scrollbar.pack(side="right", fill="y")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)

        results_frame = tk.Frame(results_canvas, bg="white")
        results_canvas.create_window((0, 0), window=results_frame, anchor="nw")

        def on_results_frame_configure(event):
            results_canvas.configure(scrollregion = results_canvas.bbox("all"))
            results_canvas.itemconfig(results_canvas.create_window((0, 0), window=results_frame, anchor="nw"), width=results_canvas.winfo_width())

        results_frame.bind("<Configure>", on_results_frame_configure)
        results_canvas.bind("<Configure>", on_results_frame_configure)


        def buscar():
            for widget in results_frame.winfo_children():
                widget.destroy()

            search_term = query.get().lower()
            resultados = [p for p in productos_disponibles if search_term in p["nombre"].lower()]

            if not resultados:
                tk.Label(results_frame, text="¡Uy! No encontramos productos con ese nombre. Intenta de nuevo.", bg="white", fg="gray").pack(pady=10)
                return

            for p in resultados:
                f_res = tk.Frame(results_frame, bg="white", relief="solid", bd=1, padx=5, pady=5)
                f_res.pack(padx=5, pady=2, fill="x")

                tk.Label(f_res, text=f"{p['nombre']} - ${p['precio']:,} - En stock: {p['stock']}", bg="white").pack(side="left")

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
        path = filedialog.askopenfilename(title="Elige tu nueva foto de perfil", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")])
        if path:
            usuario_actual["foto"] = path
            datos = cargar_json(ARCHIVO_DATOS)
            for u in datos:
                if u["user"] == usuario_actual["user"]:
                    u["foto"] = path
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("¡Foto actualizada!", "¡Tu foto de perfil ha sido cambiada exitosamente!")
            go_usuario()

    def editar_perfil():
        nuevo_user = simpledialog.askstring("Cambiar Usuario", "Escribe tu nuevo nombre de usuario:", initialvalue=usuario_actual["user"])
        nueva_pass = simpledialog.askstring("Cambiar Contraseña", "Escribe tu nueva contraseña (déjalo en blanco si no quieres cambiarla):", show="*")

        cambios_realizados = False
        if nuevo_user and nuevo_user != usuario_actual["user"]:
            datos = cargar_json(ARCHIVO_DATOS)
            if any(u["user"].lower() == nuevo_user.lower() for u in datos if u["user"].lower() != usuario_actual["user"].lower()):
                messagebox.showerror("¡Usuario no disponible!", "¡Lo sentimos! Ese nombre de usuario ya lo tiene otra persona.")
                return
            usuario_actual["user"] = nuevo_user
            cambios_realizados = True

        if nueva_pass:
            if len(nueva_pass) < 6:
                messagebox.showerror("Contraseña débil", "Tu nueva contraseña debe tener al menos 6 caracteres.")
                return
            usuario_actual["pass"] = hash_password(nueva_pass)
            cambios_realizados = True

        if cambios_realizados:
            datos = cargar_json(ARCHIVO_DATOS)
            for i, u in enumerate(datos):
                if u["user"] == (usuario_actual["user"] if not nuevo_user else nuevo_user):
                    datos[i] = usuario_actual
                    break
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("¡Perfil actualizado!", "¡Tu información ha sido guardada con éxito!")
            go_usuario()
        else:
            messagebox.showinfo("¡Todo igual!", "No hiciste ningún cambio en tu perfil.")

    def eliminar_cuenta():
        if messagebox.askyesno("¡Atención! Eliminar Cuenta", "¿Estás ABSOLUTAMENTE seguro de que quieres eliminar tu cuenta?\n¡Esta acción no se puede deshacer!"):
            global usuario_actual
            datos = cargar_json(ARCHIVO_DATOS)
            datos = [u for u in datos if u["user"] != usuario_actual["user"]]
            guardar_json(datos, ARCHIVO_DATOS)
            messagebox.showinfo("¡Cuenta eliminada!", "¡Tu cuenta ha sido eliminada con éxito! Te extrañaremos.")
            cerrar_sesion(root_tienda_app)

    def cerrar_sesion(root_tienda_app_param):
        global usuario_actual
        usuario_actual = None
        root_tienda_app_param.destroy()
        iniciar_autenticacion()

    def go_carrito():
        limpiar()
        tk.Label(frame, text="Tu Carrito de Compras", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        if not carrito:
            tk.Label(frame, text="¡Tu carrito está vacío! ¿Qué esperas? ¡Agrega productos!", bg="white", fg="gray").pack(pady=20)
            return

        total = 0
        productos_agrupados = defaultdict(int)
        for item in carrito:
            productos_agrupados[item["nombre"]] += 1
            total += int(item["precio"])

        for nombre_prod, cantidad in productos_agrupados.items():
            precio_unitario = 0
            for p in productos_disponibles:
                if p["nombre"] == nombre_prod:
                    precio_unitario = int(p["precio"])
                    break

            item_frame = tk.Frame(frame, bg="white", relief="groove", bd=1)
            item_frame.pack(anchor="w", padx=20, pady=2, fill="x")
            tk.Label(item_frame, text=f"{nombre_prod} (x{cantidad}) - ${precio_unitario * cantidad:,}", bg="white").pack(side="left", fill="x", expand=True)
            tk.Button(item_frame, text="Quitar uno", command=lambda name=nombre_prod: quitar_del_carrito(name), bg="lightcoral").pack(side="right", padx=5)

        tk.Frame(frame, height=2, bg="lightgray").pack(fill="x", padx=15, pady=10)
        tk.Label(frame, text=f"Total a pagar: ${total:,}", bg="white", font=("Arial", 14, "bold"), fg="green").pack(pady=10)

        if carrito:
            tk.Button(frame, text="Proceder al Pago", command=lambda: pagar_con_opciones(total), bg="#B7CE63").pack(pady=10)

    def quitar_del_carrito(product_name):
        found = False
        for i, item in enumerate(carrito):
            if item["nombre"] == product_name:
                for p in productos_disponibles:
                    if p["nombre"] == product_name:
                        p["stock"] += 1
                        break
                carrito.pop(i)
                found = True
                messagebox.showinfo("Carrito actualizado", f"Quitamos una unidad de '{product_name}' de tu carrito.")
                break
        if not found:
            messagebox.showerror("¡Vaya!", f"'{product_name}' no se encontró en tu carrito.")
        go_carrito()

    def pagar_con_opciones(total_a_pagar):
        if not carrito:
            messagebox.showerror("¡Carrito vacío!", "Por favor, agrega algunos productos antes de intentar pagar.")
            return

        pago_window = tk.Toplevel(root_tienda_app)
        pago_window.title("Confirmar tu Pago")
        pago_window.geometry("350x400")
        pago_window.transient(root_tienda_app)
        pago_window.grab_set()

        pago_frame = tk.Frame(pago_window, bg="white", padx=20, pady=20)
        pago_frame.pack(fill="both", expand=True)

        tk.Label(pago_frame, text="¿Cómo quieres pagar?", font=("Arial", 14, "bold"), bg="white", fg="#195E5E").pack(pady=10)
        tk.Label(pago_frame, text=f"Total a Pagar: ${total_a_pagar:,}", font=("Arial", 12, "bold"), bg="white", fg="green").pack(pady=5)

        metodo_pago_var = tk.StringVar(value="Efectivo")

        card_details_frame = tk.Frame(pago_frame, bg="white")

        def mostrar_campos_tarjeta():
            for widget in card_details_frame.winfo_children():
                widget.destroy()
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
            card_details_frame.pack(fill="x", pady=5)

        tk.Radiobutton(pago_frame, text="Efectivo", variable=metodo_pago_var, value="Efectivo", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)
        tk.Radiobutton(pago_frame, text="Tarjeta Visa", variable=metodo_pago_var, value="Tarjeta Visa", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)
        tk.Radiobutton(pago_frame, text="Mastercard", variable=metodo_pago_var, value="Mastercard", bg="white", command=mostrar_campos_tarjeta).pack(anchor="w", pady=5)

        mostrar_campos_tarjeta()

        def finalizar_pago():
            metodo_seleccionado = metodo_pago_var.get()

            if metodo_seleccionado in ["Tarjeta Visa", "Mastercard"]:
                entries = [w for w in card_details_frame.winfo_children() if isinstance(w, tk.Entry)]
                if len(entries) < 3:
                    messagebox.showerror("Error de Pago", "¡Ups! Algo salió mal con los campos de la tarjeta. Intenta de nuevo.")
                    return

                card_num = entries[0].get().strip()
                expiry = entries[1].get().strip()
                cvv = entries[2].get().strip()

                if not card_num or not expiry or not cvv:
                    messagebox.showerror("¡Faltan datos de la tarjeta!", "Por favor, completa todos los campos de tu tarjeta para continuar.")
                    return
                if not card_num.isdigit() or not (13 <= len(card_num) <= 19):
                    messagebox.showerror("Número de tarjeta inválido", "El número de tarjeta debe contener solo dígitos y tener entre 13 y 19 números.")
                    return
                if not expiry.count('/') == 1 or not all(part.isdigit() for part in expiry.split('/')) or len(expiry) != 5:
                    messagebox.showerror("Fecha de vencimiento inválida", "El formato de la fecha de vencimiento debe ser MM/AA.")
                    return
                if not cvv.isdigit() or not (3 <= len(cvv) <= 4):
                    messagebox.showerror("CVV inválido", "El CVV debe ser de 3 o 4 dígitos numéricos.")
                    return

            historial = cargar_json(HISTORIAL_COMPRAS_FILE)

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
                "id_transaccion": datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "usuario": usuario_actual["user"],
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "metodo_pago": metodo_seleccionado,
                "total_pagado": total_a_pagar,
                "productos": lista_items_historial
            }
            historial.append(registro_compra)
            guardar_json(historial, HISTORIAL_COMPRAS_FILE)

            carrito.clear()
            messagebox.showinfo("¡Compra Exitosa!", f"¡Tu compra de ${total_a_pagar:,} ha sido procesada con éxito usando {metodo_seleccionado}! ¡Muchas gracias por tu compra!")
            pago_window.destroy()
            go_carrito()

        tk.Button(pago_frame, text="Confirmar Pago", command=finalizar_pago, bg="#B7CE63").pack(pady=20, fill="x")
        pago_window.mainloop()

    def agregar_carrito(prod_to_add):
        found_product = None
        for p in productos_disponibles:
            if p["nombre"] == prod_to_add["nombre"]:
                found_product = p
                break

        if found_product and found_product["stock"] > 0:
            found_product["stock"] -= 1
            carrito.append(found_product)
            messagebox.showinfo("¡Al carrito!", f"¡'{prod_to_add['nombre']}' se ha añadido a tu carrito!")
            go_inicio()
        elif found_product and found_product["stock"] <= 0:
            messagebox.showerror("¡Sin stock!", f"¡Lo sentimos mucho! '{prod_to_add['nombre']}' se ha agotado.")
        else:
            messagebox.showerror("¡Producto no encontrado!", "Parece que hubo un problema y no pudimos encontrar este producto.")

    def go_admin():
        limpiar()
        tk.Label(frame, text="Panel de Administración", font=("Arial", 16, "bold"), bg="white", fg="#195E5E").pack(pady=10)

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
        stock_entry.insert(0, "1")
        stock_entry.pack(fill="x")

        selected_image_path = {"path": ""}

        def seleccionar_imagen_admin():
            filepath = filedialog.askopenfilename(title="Elige una imagen para tu producto", filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.gif")])
            if filepath:
                selected_image_path["path"] = filepath
                messagebox.showinfo("¡Imagen lista!", f"Seleccionaste: {os.path.basename(filepath)}")

        tk.Button(add_frame, text="Elegir Imagen", command=seleccionar_imagen_admin, bg="#B7CE63").pack(pady=5)

        def agregar():
            nombre = nombre_entry.get().strip()
            precio_str = precio_entry.get().strip()
            stock_str = stock_entry.get().strip()
            imagen_original_path = selected_image_path["path"]

            if not nombre or not precio_str or not stock_str or not imagen_original_path:
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

            try:
                filename = os.path.basename(imagen_original_path)
                name, ext = os.path.splitext(filename)
                new_filename = f"{nombre.replace(' ', '_').lower()}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}{ext}"
                dest_path = os.path.join(IMG_PRODUCTOS_DIR, new_filename)

                shutil.copy(imagen_original_path, dest_path)
                imagen_guardada_nombre = new_filename
            except Exception as e:
                messagebox.showerror("Error al guardar imagen", f"No se pudo copiar la imagen: {e}. Intenta con otra imagen.")
                return

            productos_disponibles.append({"nombre": nombre, "precio": precio, "imagen": imagen_guardada_nombre, "stock": stock})
            messagebox.showinfo("¡Producto añadido!", "¡Tu nuevo producto ha sido agregado con éxito!")
            nombre_entry.delete(0, tk.END)
            precio_entry.delete(0, tk.END)
            stock_entry.delete(0, tk.END)
            stock_entry.insert(0, "1")
            selected_image_path["path"] = ""
            go_admin()

        tk.Button(add_frame, text="Añadir Producto", command=agregar, bg="#AED581").pack(pady=10)

        manage_frame = tk.LabelFrame(frame, text="Administra tus Productos Existentes", bg="white", padx=10, pady=10)
        manage_frame.pack(padx=10, pady=10, fill="x")

        if not productos_disponibles:
            tk.Label(manage_frame, text="¡Aún no tienes productos para gestionar!", bg="white", fg="gray").pack(pady=10)
        else:
            for i, p in enumerate(productos_disponibles):
                f_prod_item = tk.Frame(manage_frame, bg="white", relief="solid", bd=1)
                f_prod_item.pack(fill="x", padx=5, pady=2)
                tk.Label(f_prod_item, text=f"{p['nombre']} - ${p['precio']:,} - Stock: {p['stock']}", bg="white").pack(side="left", padx=5, expand=True, fill="x")
                tk.Button(f_prod_item, text="Eliminar", command=lambda idx=i: eliminar(idx), bg="salmon").pack(side="right", padx=5)

        def eliminar(index):
            if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar '{productos_disponibles[index]['nombre']}'?\n¡Esta acción no se puede deshacer!"):
                try:
                    img_filename = productos_disponibles[index]["imagen"]
                    img_filepath_to_delete = os.path.join(IMG_PRODUCTOS_DIR, img_filename)
                    if os.path.exists(img_filepath_to_delete):
                        os.remove(img_filepath_to_delete)
                        print(f"Imagen '{img_filename}' eliminada del directorio de productos.")
                except Exception as e:
                    print(f"Error al eliminar la imagen del producto: {e}")

                del productos_disponibles[index]
                messagebox.showinfo("¡Producto eliminado!", "¡El producto ha sido eliminado con éxito!")
                go_admin()

        tk.Button(frame, text="Ver Estadísticas y Reportes de Ventas", command=mostrar_estadisticas_admin, bg="#B7CE63").pack(pady=15)

    def mostrar_estadisticas_admin():
        stats_window = tk.Toplevel(root_tienda_app)
        stats_window.title("Estadísticas Clave de tu Tienda")
        stats_window.geometry("800x700") # Ajustamos el tamaño inicial
        stats_window.transient(root_tienda_app)
        stats_window.grab_set()

        stats_frame = tk.Frame(stats_window, bg="white")
        stats_frame.pack(fill="both", expand=True)

        tk.Label(stats_frame, text="Un Vistazo a tus Ventas", font=("Arial", 18, "bold"), bg="white", fg="#195E5E").pack(pady=10)

        historial_raw = cargar_json(HISTORIAL_COMPRAS_FILE)

        if not historial_raw:
            tk.Label(stats_frame, text="¡Parece que aún no hay datos de compras para mostrarte estadísticas!", bg="white", fg="gray").pack(pady=20)
            tk.Button(stats_frame, text="Volver al Panel de Administración", command=stats_window.destroy, bg="lightgray").pack(pady=10)
            stats_window.mainloop()
            return

        df_compras = pd.DataFrame(historial_raw)

        df_compras['total_pagado'] = pd.to_numeric(df_compras['total_pagado'], errors='coerce')
        df_compras['fecha'] = pd.to_datetime(df_compras['fecha'], errors='coerce')
        df_compras.dropna(subset=['total_pagado', 'fecha'], inplace=True)

        if df_compras.empty:
            tk.Label(stats_frame, text="¡Uy! No hay datos válidos de compras para generar las estadísticas.", bg="white", fg="gray").pack(pady=20)
            tk.Button(stats_frame, text="Volver al Panel de Administración", command=stats_window.destroy, bg="lightgray").pack(pady=10)
            stats_window.mainloop()
            return

        # --- Sección de Resumen General ---
        summary_frame = tk.Frame(stats_frame, bg="#E8F5E9", padx=10, pady=10, relief="groove", bd=1)
        summary_frame.pack(pady=10, padx=20, fill="x")

        ganancias_totales = df_compras['total_pagado'].sum()
        num_compras_totales = df_compras.shape[0]
        metodo_pago_mas_usado = df_compras['metodo_pago'].mode()[0] if not df_compras['metodo_pago'].empty else "Ninguno"

        tk.Label(summary_frame, text="Resumen General:", font=("Arial", 14, "bold"), bg="#E8F5E9", fg="#195E5E").pack(anchor="w")
        tk.Label(summary_frame, text=f"Ganancias Totales: ${ganancias_totales:,.2f}", font=("Arial", 12), bg="#E8F5E9", fg="darkgreen").pack(anchor="w")
        tk.Label(summary_frame, text=f"Número de Ventas: {num_compras_totales}", font=("Arial", 12), bg="#E8F5E9").pack(anchor="w")
        tk.Label(summary_frame, text=f"Método de Pago Preferido: {metodo_pago_mas_usado}", font=("Arial", 12), bg="#E8F5E9").pack(anchor="w")


        # --- Contenedor para los gráficos con Scrollbar ---
        graph_canvas = tk.Canvas(stats_frame, bg="white")
        graph_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        graph_scrollbar = tk.Scrollbar(stats_frame, orient="vertical", command=graph_canvas.yview)
        graph_scrollbar.pack(side="right", fill="y")
        graph_canvas.configure(yscrollcommand=graph_scrollbar.set)

        # Frame interno donde se dibujarán los gráficos
        scrollable_graph_frame = tk.Frame(graph_canvas, bg="white")
        graph_canvas.create_window((0, 0), window=scrollable_graph_frame, anchor="nw")

        def on_graph_frame_configure(event):
            graph_canvas.configure(scrollregion=graph_canvas.bbox("all"))
            # Asegura que el frame interno siempre ocupe el ancho del canvas
            graph_canvas.itemconfig(graph_canvas.create_window((0, 0), window=scrollable_graph_frame, anchor="nw"), width=graph_canvas.winfo_width())

        scrollable_graph_frame.bind("<Configure>", on_graph_frame_configure)
        graph_canvas.bind("<Configure>", on_graph_frame_configure)


        # --- Función para limpiar el área de gráficos ---
        def clear_graphs():
            for widget in scrollable_graph_frame.winfo_children():
                widget.destroy()

        # --- Funciones para generar y mostrar cada gráfico ---
        def show_payment_methods_chart():
            clear_graphs()
            if not df_compras.empty:
                metodos_pago_counts = df_compras['metodo_pago'].value_counts()
                if not metodos_pago_counts.empty:
                    fig1, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=100) # Dos subplots en una figura

                    # Gráfico de Barras
                    sns.barplot(x=metodos_pago_counts.index, y=metodos_pago_counts.values, ax=axes[0], palette="viridis")
                    axes[0].set_title('Métodos de Pago Más Usados')
                    axes[0].set_ylabel('Número de Transacciones')
                    axes[0].set_xlabel('Método de Pago')
                    axes[0].tick_params(axis='x', rotation=45)

                    # Gráfico de Torta
                    axes[1].pie(metodos_pago_counts, labels=metodos_pago_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("viridis", len(metodos_pago_counts)))
                    axes[1].axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
                    axes[1].set_title('Distribución de Métodos de Pago')

                    fig1.tight_layout() # Ajusta el layout para evitar superposiciones

                    canvas = FigureCanvasTkAgg(fig1, master=scrollable_graph_frame)
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.pack(pady=10, fill="both", expand=True)
                    canvas.draw()
                else:
                    tk.Label(scrollable_graph_frame, text="No hay datos de métodos de pago para graficar.", bg="white", fg="gray").pack(pady=10)


        def show_top_products_chart():
            clear_graphs()
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
                    top_productos = df_productos_vendidos.groupby('nombre')['cantidad'].sum().sort_values(ascending=False).head(5)

                    if not top_productos.empty:
                        fig2 = plt.Figure(figsize=(8, 6), dpi=100)
                        ax2 = fig2.add_subplot(111)
                        sns.barplot(x=top_productos.values, y=top_productos.index, ax=ax2, palette="magma")
                        ax2.set_title('Top 5 Productos Más Vendidos')
                        ax2.set_xlabel('Cantidad Total Vendida')
                        ax2.set_ylabel('Producto')
                        fig2.tight_layout()

                        canvas = FigureCanvasTkAgg(fig2, master=scrollable_graph_frame)
                        canvas_widget = canvas.get_tk_widget()
                        canvas_widget.pack(pady=10, fill="both", expand=True)
                        canvas.draw()
                    else:
                        tk.Label(scrollable_graph_frame, text="No hay datos de productos vendidos para graficar.", bg="white", fg="gray").pack(pady=10)
                else:
                    tk.Label(scrollable_graph_frame, text="No hay datos de productos vendidos para graficar.", bg="white", fg="gray").pack(pady=10)
            else:
                tk.Label(scrollable_graph_frame, text="No hay datos de productos vendidos para graficar.", bg="white", fg="gray").pack(pady=10)


        def show_daily_sales_chart():
            clear_graphs()
            if not df_compras.empty:
                df_compras['dia'] = df_compras['fecha'].dt.to_period('D')
                ventas_diarias = df_compras.groupby('dia')['total_pagado'].sum()
                ventas_diarias.index = ventas_diarias.index.to_timestamp()

                if not ventas_diarias.empty:
                    fig3 = plt.Figure(figsize=(10, 6), dpi=100)
                    ax3 = fig3.add_subplot(111)
                    sns.lineplot(x=ventas_diarias.index, y=ventas_diarias.values, ax=ax3, marker='o', color='purple')
                    ax3.set_title('Ventas Totales por Día')
                    ax3.set_ylabel('Ganancias ($)')
                    ax3.set_xlabel('Fecha de Venta')
                    ax3.tick_params(axis='x', rotation=45)
                    ax3.grid(True) # Añadir una cuadrícula para mejor lectura
                    fig3.tight_layout()

                    canvas = FigureCanvasTkAgg(fig3, master=scrollable_graph_frame)
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.pack(pady=10, fill="both", expand=True)
                    canvas.draw()
                else:
                    tk.Label(scrollable_graph_frame, text="No hay datos de ventas diarias para graficar.", bg="white", fg="gray").pack(pady=10)
            else:
                tk.Label(scrollable_graph_frame, text="No hay datos de ventas diarias para graficar.", bg="white", fg="gray").pack(pady=10)

        # --- Menú de Opciones de Gráficos ---
        menu_options_frame = tk.Frame(stats_frame, bg="#F0F8FF", padx=10, pady=10, relief="ridge", bd=1)
        menu_options_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(menu_options_frame, text="Selecciona un tipo de gráfico:", font=("Arial", 12, "bold"), bg="#F0F8FF").pack(anchor="w", pady=5)

        tk.Button(menu_options_frame, text="Métodos de Pago", command=show_payment_methods_chart, bg="#D4EEFF").pack(side="left", padx=5, pady=5, expand=True)
        tk.Button(menu_options_frame, text="Productos Más Vendidos", command=show_top_products_chart, bg="#D4EEFF").pack(side="left", padx=5, pady=5, expand=True)
        tk.Button(menu_options_frame, text="Ventas Diarias", command=show_daily_sales_chart, bg="#D4EEFF").pack(side="left", padx=5, pady=5, expand=True)

        tk.Button(stats_frame, text="Volver al Panel de Administración", command=stats_window.destroy, bg="lightgray").pack(pady=10)

        stats_window.mainloop()

    # barra de navegación
    tk.Button(nav, image=icon_inicio, text="Inicio", compound="top", command=go_inicio, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_buscar, text="Buscar", compound="top", command=go_buscar, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_usuario, text="Mi Perfil", compound="top", command=go_usuario, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_carrito, text="Carrito", compound="top", command=go_carrito, bg="white", fg="black").pack(side="left", expand=True)
    tk.Button(nav, image=icon_admin, text="Admin", compound="top", command=go_admin, bg="white", fg="black").pack(side="left", expand=True)

    go_inicio()
    root_tienda_app.mainloop()

# --- Inicio del Programa ---
if __name__ == "__main__":
    if not os.path.exists(ARCHIVO_DATOS):
        guardar_json([], ARCHIVO_DATOS)
    if not os.path.exists(HISTORIAL_COMPRAS_FILE):
        guardar_json([], HISTORIAL_COMPRAS_FILE)

    iniciar_autenticacion()


