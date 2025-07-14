import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import json

# configuracion de archivo de datos para usuarios
ARCHIVO_DATOS = "data.json"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # si el archivo esta corrupto o vacio, retorna una lista vacia
            return []
    else:
        #si el archivo no existe, retorna una lista vacia
        return []

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

# variables globales para el usuario actual
# esta variable almacenara el diccionario del usuario logueado.
# necesita ser global para que las funciones de autenticacion y tienda puedan accederla.
usuario_actual = None
# referencia global a la ventana de la tienda para poder cerrarla desde otras funciones
root_tienda_global = None

# funciones de autenticacion
def mostrar_login(root_auth):
    frame_registro.pack_forget()
    frame_login.pack()

def mostrar_registro(root_auth):
    frame_login.pack_forget()
    frame_registro.pack()

def login(root_auth):
    # declaramos 'usuario_actual' como global antes de cualquier uso o asignacion en esta funcion.
    global usuario_actual
    user = entry_user.get()
    password = entry_password.get()

    usuarios = cargar_datos()

    usuario_encontrado = False
    for u in usuarios:
        if u.get("user") == user and u.get("pass") == password:
            usuario_encontrado = True
            usuario_actual = u # asignamos el usuario encontrado a la variable global
            break

    if usuario_encontrado:
        messagebox.showinfo("Bienvenido", f"Bienvenido a AGRO.MAX, {user}")
        root_auth.destroy() # cierra la ventana de autenticacion
        abrir_tienda() # abre la ventana de la tienda
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrecta")

def registrar(root_auth):
    new_user = entry_new_user.get()
    new_pass = entry_new_pass.get()

    if not new_user or not new_pass:
        messagebox.showerror("Error", "Completa todos los campos")
        return

    usuarios = cargar_datos()

    for u in usuarios:
        if u.get("user") == new_user:
            messagebox.showerror("Error", "Este usuario ya existe. Intenta con otro.")
            return

    # anadir un campo para la foto por defecto (vacio) al registrar el usuario
    nuevo_usuario = {"user": new_user, "pass": new_pass, "foto": ""}
    usuarios.append(nuevo_usuario)
    guardar_datos(usuarios)

    messagebox.showinfo("Registro exitoso", f"Usuario {new_user} registrado exitosamente")

    entry_new_user.delete(0, tk.END)
    entry_new_pass.delete(0, tk.END)
    mostrar_login(root_auth) # vuelve a la pantalla de login para que el usuario pueda iniciar sesion

# ventana de autenticacion (inicial)
def iniciar_autenticacion():
    # estas variables son de ambito global para la ventana de autenticacion.
    # no necesitan 'global' aqui si solo se les asigna una vez en el ambito global o se leen.
    global entry_user, entry_password, entry_new_user, entry_new_pass, frame_login, frame_registro

    root_auth = tk.Tk()
    root_auth.title("AGRO.MAX - autenticacion")
    root_auth.geometry("300x400")
    root_auth.configure(bg="#195E5E")

    # logo de autenticacion
    try:
        image = Image.open("C:Users\\kevin\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\unnamed.png")
        image = image.resize((100, 100), Image.LANCZOS)
        logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(root_auth, image=logo, bg="#195E5E")
        logo_label.image = logo # mantener una referencia para evitar que el recolector de basura la elimine
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"': {e}")

    # frame de login
    frame_login = tk.Frame(root_auth, bg="#195E5E")
    tk.Label(frame_login, text="AGRO.MAX", font=("Arial", 18, "bold"), fg="white", bg="#195E5E").pack(pady=10)
    tk.Label(frame_login, text="email o usuario", fg="white", bg="#195E5E").pack(pady=(20, 5))
    entry_user = tk.Entry(frame_login, width=30)
    entry_user.pack()

    tk.Label(frame_login, text="contrasena", fg="white", bg="#195E5E").pack(pady=(20, 5))
    entry_password = tk.Entry(frame_login, show="*", width=30)
    entry_password.pack()

    # usamos lambda para pasar 'root_auth' como argumento a las funciones de autenticacion
    tk.Button(frame_login, text="iniciar sesion", width=25, bg="#B7CE63", command=lambda: login(root_auth)).pack(pady=20)
    tk.Button(frame_login, text="¿no tienes cuenta? registrate", bg="#195E5E", fg="white", borderwidth=0, command=lambda: mostrar_registro(root_auth)).pack()

    # frame de registro
    frame_registro = tk.Frame(root_auth, bg="#195E5E")
    tk.Label(frame_registro, text="registro agro.max", font=("Arial", 16, "bold"), fg="white", bg="#195E5E").pack(pady=10)
    tk.Label(frame_registro, text="nuevo usuario (email)", fg="white", bg="#195E5E").pack(pady=(20, 5))
    entry_new_user = tk.Entry(frame_registro, width=30)
    entry_new_user.pack()

    tk.Label(frame_registro, text="nueva contrasena", fg="white", bg="#195E5E").pack(pady=(20, 5))
    entry_new_pass = tk.Entry(frame_registro, show="*", width=30)
    entry_new_pass.pack()

    tk.Button(frame_registro, text="registrarse", width=25, bg="#B7CE63", command=lambda: registrar(root_auth)).pack(pady=20)
    tk.Button(frame_registro, text="ya tengo cuenta. iniciar sesion", bg="#195E5E", fg="white", borderwidth=0, command=lambda: mostrar_login(root_auth)).pack()

    frame_login.pack() # muestra el frame de login por defecto al iniciar
    root_auth.mainloop() # inicia el bucle principal de la ventana de autenticacion


# codigo de la ventana de la tienda
def abrir_tienda():
    # accedemos a la variable global para la ventana de la tienda
    global root_tienda_global
    root_tienda_global = tk.Tk()
    root_tienda_global.title("AGRO.MAX - tienda")
    root_tienda_global.geometry("400x600")
    root_tienda_global.configure(bg="white")

    main_frame = tk.Frame(root_tienda_global, bg="white")
    main_frame.pack(fill="both", expand=True)

    bottom_nav = tk.Frame(root_tienda_global, bg="white", height=60, bd=1, relief="raised")
    bottom_nav.pack(side="bottom", fill="x")

    # cargar iconos
    def load_icon(path, size=(30, 30)):
        try:
            image = Image.open(path)
            # image.lanczos es un filtro de alta calidad para redimensionar
            image = image.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"error al cargar el icono '{path}': {e}")
            return None

    def load_image_for_display(path, size=(80, 80)):
        try:
            image = Image.open(path)
            image = image.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"error al cargar imagen '{path}': {e}")
            # retorna una imagen por defecto si hay un error (asegurate de que 'placeholder.png' exista)
            try:
                default_img = Image.open("default_user.png") # o una imagen de "no_disponible.png"
                default_img = default_img.resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(default_img)
            except Exception as e_default:
                print(f"error al cargar imagen por defecto: {e_default}")
                return None # no se pudo cargar ni la imagen original ni la por defecto

    icon_inicio = load_icon("C:\\Users\\kevin\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\inicio.png.")
    icon_categorias = load_icon("C:\\Users\kevin\\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\lupa.png.")
    icon_tu = load_icon("C:\\Users\kevin\\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\usuario.png.")
    icon_carrito = load_icon("C:\\Users\\kevin\OneDrive\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\carrito.png")

    # datos de productos (se inicializan cada vez que se abre la tienda)
    productos_disponibles = [
        {"nombre": "comida para gatos", "precio": "15000", "imagen": "C:\\Users\\kevin\\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\ringogato.png"},
        {"nombre": "comida para perro", "precio": "25000", "imagen": "C:\\Users\\kevin\\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\perro.png"},
        {"nombre": "comida para gatos pequenos", "precio": "10000", "imagen": "C:\\Users\\kevin\\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\gato_pequeño.png"},
        {"nombre": "comida para cachorros", "precio": "20000", "imagen": "C:\\Users\\kevin\\OneDrive\\Documentos\\proyectos de programacion\\Nueva-carpeta\\interfaz graf 2\\infratriz_grafica\\programacion de computadoras\\perros_pequeños.png"},
    ]

    carrito = [] # el carrito se reinicia cada vez que se abre la tienda, lo cual es normal si no se persiste.

    # funciones comunes de la tienda
    button_style = {"bd": 0, "bg": "white", "activebackground": "white", "fg": "black"}

    def set_active(btn):
        for b in [btn_inicio, btn_categorias, btn_tu, btn_carrito]:
            b.config(bg="white", fg="black")
        btn.config(bg="#e0f7fa", fg="green")

    def limpiar_contenido():
        for widget in main_frame.winfo_children():
            widget.destroy()

    def add_product_to_catalog(parent_frame, image_path, name, price, product_dict=None, en_carrito=False):
        frame = tk.Frame(parent_frame, bg="white", bd=1, relief="solid", padx=10, pady=10)
        frame.pack(pady=5, padx=10, fill="x")

        img = load_image_for_display(image_path) # usar la funcion general para imagenes
        if img:
            img_label = tk.Label(frame, image=img, bg="white")
            img_label.image = img # mantener referencia
            img_label.pack(side="left", padx=5)

        info_frame = tk.Frame(frame, bg="white")
        info_frame.pack(side="left", padx=10, fill="both", expand=True)

        tk.Label(info_frame, text=name, font=("arial", 12, "bold"), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"precio: ${price}", font=("arial", 10), fg="green", bg="white").pack(anchor="w")

        if en_carrito:
            def eliminar():
                carrito.remove(product_dict)
                go_carrito() # recarga el carrito despues de eliminar
            tk.Button(info_frame, text="eliminar", command=eliminar, bg="#ffcdd2", fg="black").pack(anchor="e", pady=5)
        else:
            def comprar():
                carrito.append(product_dict or {"nombre": name, "precio": price, "imagen": image_path})
                messagebox.showinfo("producto agregado", f"'{name}' agregado al carrito.")
                # print(f"{name} agregado al carrito.") # puedes usar esto para depurar en consola
            tk.Button(info_frame, text="comprar", command=comprar, bg="#c8e6c9", fg="black").pack(anchor="e", pady=5)

    # catalogo principal
    def mostrar_catalogo(filtrados=None):
        limpiar_contenido()
        lista = filtrados if filtrados is not None else productos_disponibles

        if not lista:
            tk.Label(main_frame, text="no se encontraron productos.", bg="white", font=("arial", 12)).pack(pady=20)
        else:
            for prod in lista:
                add_product_to_catalog(main_frame, prod["imagen"], prod["nombre"], prod["precio"], product_dict=prod)

    # navegacion de la tienda
    def go_inicio():
        set_active(btn_inicio)
        mostrar_catalogo()

    def go_categorias():
        set_active(btn_categorias)
        limpiar_contenido()

        tk.Label(main_frame, text="buscar productos:", font=("arial", 12), bg="white").pack(pady=10)

        search_var = tk.StringVar() # variable para almacenar el texto de busqueda

        entry = tk.Entry(main_frame, textvariable=search_var, font=("arial", 12), width=30)
        entry.pack(pady=5)

        def realizar_busqueda():
            texto = search_var.get().strip().lower()
            resultados = [p for p in productos_disponibles if texto in p["nombre"].lower()]
            mostrar_catalogo(resultados) # muestra los resultados filtrados

        tk.Button(main_frame, text="buscar", command=realizar_busqueda, bg="#c8e6c9").pack(pady=5)

    def go_tu():
        set_active(btn_tu)
        limpiar_contenido()

        tk.Label(main_frame, text="perfil de usuario", font=("arial", 16, "bold"), bg="white").pack(pady=10)

        # seccion de foto de perfil
        current_photo_path = usuario_actual.get("foto", "")
        profile_photo_tk = None # para mantener la referencia de la imagen de perfil

        # cargar foto de perfil o una por defecto
        if current_photo_path and os.path.exists(current_photo_path):
            profile_photo_tk = load_image_for_display(current_photo_path, size=(80, 80))
        else:
            # asegurate de tener un archivo 'default_user.png' en la misma carpeta
            profile_photo_tk = load_image_for_display("default_user.png", size=(80, 80))

        profile_img_label = tk.Label(main_frame, image=profile_photo_tk, bg="white")
        profile_img_label.image = profile_photo_tk # importante para mantener la referencia
        profile_img_label.pack(pady=5)

        def subir_foto():
            file_path = filedialog.askopenfilename(
                title="seleccionar foto de perfil",
                filetypes=[("archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if file_path:
                # no necesitamos 'global usuario_actual' aqui porque solo modificamos un atributo del diccionario, no reasignandolo
                usuario_actual["foto"] = file_path # actualizar la ruta de la foto en el usuario actual

                # funcion auxiliar para actualizar el usuario especifico en la lista global de usuarios
                def actualizar_usuario_en_datos():
                    all_users = cargar_datos()
                    for i, u_in_list in enumerate(all_users):
                        if u_in_list["user"] == usuario_actual["user"]:
                            all_users[i] = usuario_actual # reemplazar el diccionario con el actualizado
                            break
                    guardar_datos(all_users)

                actualizar_usuario_en_datos() # guardar los datos actualizados en el json
                messagebox.showinfo("exito", "foto de perfil actualizada.")
                go_tu() # recargar la vista del perfil para mostrar la nueva foto

        tk.Button(main_frame, text="cambiar foto", command=subir_foto, bg="#bbdefb", fg="black").pack(pady=5)

        # seccion de datos del usuario (modo lectura)
        user_info_frame = tk.Frame(main_frame, bg="white")
        user_info_frame.pack(pady=10)

        tk.Label(user_info_frame, text=f"usuario/email: {usuario_actual['user']}", font=("arial", 12), bg="white").pack(anchor="w")

        # botones de accion
        action_buttons_frame = tk.Frame(main_frame, bg="white")
        action_buttons_frame.pack(pady=10)

        def editar_perfil_ui():
            limpiar_contenido()
            tk.Label(main_frame, text="editar perfil", font=("arial", 16, "bold"), bg="white").pack(pady=10)

            tk.Label(main_frame, text="nuevo usuario/email:", bg="white").pack(pady=(10,0))
            new_user_entry = tk.Entry(main_frame, width=30)
            new_user_entry.insert(0, usuario_actual["user"]) # precarga el usuario actual
            new_user_entry.pack()

            tk.Label(main_frame, text="contrasena actual:", bg="white").pack(pady=(10,0))
            current_pass_entry = tk.Entry(main_frame, show="*", width=30)
            current_pass_entry.pack()

            tk.Label(main_frame, text="nueva contrasena (dejar vacio para no cambiar):", bg="white").pack(pady=(10,0))
            new_pass_entry = tk.Entry(main_frame, show="*", width=30)
            new_pass_entry.pack()

            def guardar_cambios():
                # necesitamos 'global usuario_actual' aqui porque podriamos reasignar si el 'user' cambia
                global usuario_actual

                current_pass = current_pass_entry.get()
                new_user = new_user_entry.get()
                new_pass = new_pass_entry.get()

                if current_pass != usuario_actual["pass"]:
                    messagebox.showerror("error", "la contrasena actual es incorrecta.")
                    return

                if not new_user:
                    messagebox.showerror("error", "el usuario no puede estar vacio.")
                    return

                usuarios = cargar_datos()
                # verificar si el nuevo usuario ya existe (excepto si es el mismo usuario_actual)
                for u in usuarios:
                    if u["user"] == new_user and u["user"] != usuario_actual["user"]: # comparar por el valor del usuario
                        messagebox.showerror("error", "este nombre de usuario ya esta en uso.")
                        return

                # actualizar datos del usuario actual en memoria
                old_user_name = usuario_actual["user"] # guardamos el nombre antiguo para encontrarlo en la lista
                usuario_actual["user"] = new_user
                if new_pass: # solo cambiar la contrasena si se ingreso una nueva
                    usuario_actual["pass"] = new_pass

                # encontrar y actualizar el usuario en la lista global de usuarios y luego guardar
                for i, u_in_list in enumerate(usuarios):
                    if u_in_list["user"] == old_user_name: # encontrar por el nombre de usuario anterior
                        usuarios[i] = usuario_actual # reemplazar el diccionario con el actualizado
                        break
                guardar_datos(usuarios)
                messagebox.showinfo("exito", "perfil actualizado exitosamente.")
                go_tu() # recargar la vista de perfil para reflejar los cambios

            tk.Button(main_frame, text="guardar cambios", command=guardar_cambios, bg="#c8e6c9", fg="black").pack(pady=10)
            tk.Button(main_frame, text="cancelar", command=go_tu, bg="#ffcdd2", fg="black").pack(pady=5)


        def eliminar_cuenta():
            # necesitamos 'global usuario_actual' para poder reasignarlo a none
            global usuario_actual, root_tienda_global

            confirm = messagebox.askyesno("confirmar eliminacion",
                                          "¿estas seguro de que quieres eliminar tu cuenta? esta accion es irreversible.")
            if confirm:
                # pedir la contrasena para confirmar
                # tk.simpledialog.askstring requiere un parent, usamos main_frame para eso.
                password_confirm = tk.simpledialog.askstring("confirmar contrasena", "ingresa tu contrasena para confirmar la eliminacion:", show='*', parent=main_frame)
                if password_confirm == usuario_actual["pass"]:
                    usuarios = cargar_datos()
                    # filtra la lista para eliminar el usuario actual por su nombre de usuario
                    usuarios = [u for u in usuarios if u["user"] != usuario_actual["user"]]
                    guardar_datos(usuarios)

                    messagebox.showinfo("cuenta eliminada", "tu cuenta ha sido eliminada exitosamente.")
                    usuario_actual = None # limpiar el usuario actual despues de eliminarlo
                    root_tienda_global.destroy() # cierra la ventana de la tienda
                    iniciar_autenticacion() # vuelve a la pantalla de autenticacion
                else:
                    messagebox.showerror("error", "contrasena incorrecta. la cuenta no ha sido eliminada.")


        # botones de la vista principal del perfil
        tk.Button(action_buttons_frame, text="editar perfil y contrasena", command=editar_perfil_ui,
                  bg="#bbdefb", fg="black", font=("arial", 11)).pack(pady=5)

        tk.Button(action_buttons_frame, text="eliminar cuenta", command=eliminar_cuenta,
                  bg="#ef9a9a", fg="black", font=("arial", 11)).pack(pady=5)

        tk.Button(action_buttons_frame, text="cerrar sesion", command=lambda: cerrar_sesion(root_tienda_global),
                  bg="#ffe082", fg="black", font=("arial", 11)).pack(pady=5)


    def cerrar_sesion(root_tienda):
        # necesitamos 'global usuario_actual' para poder reasignarlo a none
        global usuario_actual
        usuario_actual = None # limpiar el usuario actual al cerrar sesion
        messagebox.showinfo("sesion cerrada", "has cerrado sesion.")
        root_tienda.destroy() # cierra la ventana de la tienda
        iniciar_autenticacion() # vuelve a la pantalla de login


    def go_carrito():
        set_active(btn_carrito)
        limpiar_contenido()

        if not carrito:
            tk.Label(main_frame, text="tu carrito esta vacio.", font=("arial", 12), bg="white").pack(pady=20)
        else:
            tk.Label(main_frame, text="productos en tu carrito:", font=("arial", 12, "bold"), bg="white").pack(pady=10)

            total = 0
            for producto in carrito:
                # mostrar los productos en el carrito, con boton de eliminar
                add_product_to_catalog(main_frame, producto["imagen"], producto["nombre"], producto["precio"], product_dict=producto, en_carrito=True)
                total += int(producto["precio"])

            tk.Label(main_frame, text=f"total: ${total}", font=("arial", 12, "bold"), fg="blue", bg="white").pack(pady=10)

            def pagar():
                if carrito:
                    confirm_pago = messagebox.askyesno("confirmar pago", f"el total a pagar es ${total}. ¿deseas continuar?")
                    if confirm_pago:
                        carrito.clear() # vacia el carrito
                        go_carrito() # recarga la vista del carrito
                        messagebox.showinfo("pago realizado", "gracias por tu compra.")
                else:
                    messagebox.showinfo("carrito vacio", "no hay productos en el carrito para pagar.")

            tk.Button(main_frame, text="pagar", command=pagar, bg="#a5d6a7", font=("arial", 11)).pack(pady=5)

    # botones navegacion de la tienda
    # se crean los botones de navegacion, cada uno vinculado a su funcion go_
    btn_inicio = tk.Button(bottom_nav, image=icon_inicio, text="inicio", compound="top", command=go_inicio, **button_style)
    btn_inicio.pack(side="left", expand=True)

    btn_categorias = tk.Button(bottom_nav, image=icon_categorias, text="buscar", compound="top", command=go_categorias, **button_style)
    btn_categorias.pack(side="left", expand=True)

    btn_tu = tk.Button(bottom_nav, image=icon_tu, text="usuario", compound="top", command=go_tu, **button_style)
    btn_tu.pack(side="left", expand=True)

    btn_carrito = tk.Button(bottom_nav, image=icon_carrito, text="carrito", compound="top", command=go_carrito, **button_style)
    btn_carrito.pack(side="left", expand=True)

    # inicio de la tienda
    # al abrir la tienda, se activa la pestana de "inicio" y se muestra el catalogo
    set_active(btn_inicio)
    mostrar_catalogo()

    root_tienda_global.mainloop() # inicia el bucle principal de la ventana de la tienda

# punto de entrada de la aplicacion
# esto asegura que la aplicacion se inicie llamando a la ventana de autenticacion
if __name__ == "__main__":
    iniciar_autenticacion()