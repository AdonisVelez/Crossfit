import tkinter as tk
from tkinter import ttk, messagebox
import easygui
import psycopg2


class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            dbname="crossfit",
            user="openpg",
            password="openpgpwd"
        )
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def execute_query(self, query, *params):
        self.cursor.execute(query, params)
        self.conn.commit()
        if self.cursor.description is not None:
            return self.cursor.fetchall()
        else:
            return []


class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def check_user_exists(self, username, user_type):
        query = f"SELECT * FROM registro_{user_type} WHERE usuario = %s"
        result = self.db_manager.execute_query(query, username)
        return bool(result)

    def save_user(self, username, password, user_type, nombre=None, apellido=None, correo=None, edad=None, genero=None, telefono=None):
        if user_type == "cliente":
            cliente_query = "INSERT INTO cliente (nombre, apellido, correo, edad, genero, telefono) VALUES (%s, %s, %s, %s, %s, %s) RETURNING cliente_id"
            cliente_id = self.db_manager.execute_query(cliente_query, nombre, apellido, correo, edad, genero, telefono)[0][0]

            registro_query = "INSERT INTO registro_cliente (usuario, contrasena, cliente_id) VALUES (%s, %s, %s)"
            self.db_manager.execute_query(registro_query, username, password, cliente_id)
        elif user_type == "instructor":
            instructor_query = "INSERT INTO instructor (nombre, apellido, correo, edad, genero, telefono) VALUES (%s, %s, %s, %s, %s, %s) RETURNING instructor_id"
            instructor_id = self.db_manager.execute_query(instructor_query, nombre, apellido, correo, edad, genero, telefono)[0][0]

            registro_query = "INSERT INTO registro_instructor (usuario, contrasena, instructor_id) VALUES (%s, %s, %s)"
            self.db_manager.execute_query(registro_query, username, password, instructor_id)

    def update_user(self, username, user_type, nombre=None, apellido=None, correo=None, edad=None, genero=None, telefono=None):
        if user_type == "cliente":
            query = "UPDATE cliente SET nombre = %s, apellido = %s, correo = %s, edad = %s, genero = %s, telefono = %s WHERE cliente_id = (SELECT cliente_id FROM registro_cliente WHERE usuario = %s)"
            self.db_manager.execute_query(query, nombre, apellido, correo, edad, genero, telefono, username)
        elif user_type == "instructor":
            query = "UPDATE instructor SET nombre = %s, apellido = %s, correo = %s, edad = %s, genero = %s, telefono = %s WHERE instructor_id = (SELECT instructor_id FROM registro_instructor WHERE usuario = %s)"
            self.db_manager.execute_query(query, nombre, apellido, correo, edad, genero, telefono, username)
 
    def get_user_type(self, username):
        query_cliente = "SELECT * FROM registro_cliente WHERE usuario = %s"
        result_cliente = self.db_manager.execute_query(query_cliente, username)
        if result_cliente:
            return "cliente"

        query_instructor = "SELECT * FROM registro_instructor WHERE usuario = %s"
        result_instructor = self.db_manager.execute_query(query_instructor, username)
        if result_instructor:
            return "instructor"

        return None

class InstructorManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_instructors(self):
        query = "SELECT instructor_id, nombre, apellido, correo, edad, telefono FROM instructor"
        return self.db_manager.execute_query(query)

    def get_instructor_details(self, instructor_id):
        query = "SELECT nombre, apellido, correo, edad, genero, telefono FROM instructor WHERE instructor_id = %s"
        result = self.db_manager.execute_query(query, instructor_id)
        if result:
            nombre, apellido, correo, edad, genero, telefono = result[0]
            return f"Instructor seleccionado: {nombre} {apellido}\nEdad: {edad}\nCorreo: {correo} \nGénero: {genero}\nTeléfono: {telefono}"
        else:
            return ""

class DietManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_diets(self):
        query = "SELECT dieta_id, nombre FROM dieta"
        return self.db_manager.execute_query(query)

    def get_diet_details(self, dieta_id):
        query = "SELECT nombre, descripcion, forma_dieta, calorias_total FROM dieta WHERE dieta_id = %s"
        result = self.db_manager.execute_query(query, dieta_id)
        if result:
            nombre, descripcion, forma_dieta, calorias_total = result[0]
            return f"Nombre: {nombre}\nDescripción: {descripcion}\nForma de la dieta: {forma_dieta}\nCalorías Totales: {calorias_total}"
        else:
            return None
    
    def save_diet(self, nombre, descripcion, forma_dieta, calorias_total):
        query = "INSERT INTO dieta (nombre, descripcion, forma_dieta, calorias_total) VALUES (%s, %s, %s, %s)"
        self.db_manager.execute_query(query, nombre, descripcion, forma_dieta, calorias_total)

    def update_routine(self, dieta_id, nombre, descripcion, forma_dieta, calorias_total):
        query = "UPDATE rutina SET nombre = %s, descripcion = %s, forma_dieta = %s, calorias_total = %s WHERE dieta_id = %s"
        self.db_manager.execute_query(query, nombre, descripcion, forma_dieta, calorias_total, dieta_id)
        
    def delete_diet(self, dieta_id):
        query = "DELETE FROM dieta WHERE dieta_id = %s"
        self.db_manager.execute_query(query, dieta_id)
        return True

class RoutineManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_all_routines(self):
        query = "SELECT rutina_id, nombre FROM rutina"
        return self.db_manager.execute_query(query)
    
    def save_routine(self, nombre, descripcion, series, repeticion, tiempo_descanso):
        query = "INSERT INTO rutina (nombre, descripcion, series, repeticion, tiempo_descanso) VALUES (%s, %s, %s, %s, %s)"
        self.db_manager.execute_query(query, nombre, descripcion, series, repeticion, tiempo_descanso)

    def update_routine(self, rutina_id, nombre, descripcion, series, repeticion, tiempo_descanso):
        query = "UPDATE rutina SET nombre = %s, descripcion = %s, series = %s, repeticion = %s, tiempo_descanso = %s WHERE rutina_id = %s"
        self.db_manager.execute_query(query, nombre, descripcion, series, repeticion, tiempo_descanso, rutina_id)

    def get_routine_details(self, rutina_id):
        query = "SELECT rutina_id, nombre, descripcion, series, repeticion, tiempo_descanso FROM rutina WHERE rutina_id = %s"
        result = self.db_manager.execute_query(query, rutina_id)
        if result:
            rutina_id, nombre, descripcion, series, repeticion, tiempo_descanso = result[0]
            return f"Rutina ID: {rutina_id}\nNombre: {nombre}\nDescripción: {descripcion}\nSeries: {series}\nRepeticiones: {repeticion}\nTiempo de Descanso: {tiempo_descanso} segundos"
        else:
            return ""

    def delete_routine(self, rutina_id):
        query = "DELETE FROM rutina WHERE rutina_id = %s"
        self.db_manager.execute_query(query, rutina_id)
        return True
    
class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CROSSFIT")
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.user_type = None
        self.selected_instructor = tk.StringVar(value="")
        self.selected_instructor_info = tk.StringVar()
        self.selected_routine_id = tk.StringVar(value="")
        self.selected_routine_details = tk.StringVar()
        self.selected_diet = tk.StringVar()
        self.selected_client = tk.StringVar(value="")

        self.db_manager = DatabaseManager()
        self.user_manager = UserManager(self.db_manager)
        self.instructor_manager = InstructorManager(self.db_manager)
        self.diet_manager = DietManager(self.db_manager)
        self.routine_manager = RoutineManager(self.db_manager)

        self.create_widgets()

    def create_widgets(self):
        lbl_username = ttk.Label(self.root, text="Usuario:")
        lbl_username.pack()
        entry_username = ttk.Entry(self.root, textvariable=self.username)
        entry_username.pack()

        lbl_password = ttk.Label(self.root, text="Contraseña:")
        lbl_password.pack()
        entry_password = ttk.Entry(self.root, textvariable=self.password, show="*")
        entry_password.pack()

        btn_login = ttk.Button(self.root, text="Iniciar Sesión", command=self.login)
        btn_login.pack()

        btn_register = ttk.Button(self.root, text="Registrarse", command=self.register_window)
        btn_register.pack()

        btn_close = ttk.Button(self.root, text="Cerrar Programa", command=self.close_app)
        btn_close.pack()

    def login(self):
        username = self.username.get()
        password = self.password.get()

        if self.check_credentials(username, password):
            self.user_type = self.user_manager.get_user_type(username)  # Obtener el tipo de usuario
            self.show_dashboard()
            if self.user_type == "cliente":
                query = "SELECT nombre, apellido FROM cliente WHERE cliente_id = (SELECT cliente_id FROM registro_cliente WHERE usuario = %s)"
                result = self.db_manager.execute_query(query, username)
                if result:
                    nombre, apellido = result[0]
            elif self.user_type == "instructor":
                query = "SELECT nombre, apellido FROM instructor WHERE instructor_id = (SELECT instructor_id FROM registro_instructor WHERE usuario = %s)"
                result = self.db_manager.execute_query(query, username)
                if result:
                    nombre, apellido = result[0]
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")



    def register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Registro de Usuario")

        lbl_username = ttk.Label(register_window, text="Usuario:")
        lbl_username.pack()
        entry_username = ttk.Entry(register_window, textvariable=self.username)
        entry_username.pack()

        lbl_password = ttk.Label(register_window, text="Contraseña:")
        lbl_password.pack()
        entry_password = ttk.Entry(register_window, textvariable=self.password, show="*")
        entry_password.pack()

        lbl_nombre = ttk.Label(register_window, text="Nombre:")
        lbl_nombre.pack()
        entry_nombre = ttk.Entry(register_window)
        entry_nombre.pack()

        lbl_apellido = ttk.Label(register_window, text="Apellido:")
        lbl_apellido.pack()
        entry_apellido = ttk.Entry(register_window)
        entry_apellido.pack()

        lbl_correo = ttk.Label(register_window, text="Correo:")
        lbl_correo.pack()
        entry_correo = ttk.Entry(register_window)
        entry_correo.pack()

        lbl_edad = ttk.Label(register_window, text="Edad:")
        lbl_edad.pack()
        entry_edad = ttk.Entry(register_window)
        entry_edad.pack()

        lbl_genero = ttk.Label(register_window, text="Género:")
        lbl_genero.pack()

        selected_gender = tk.StringVar()
        dropdown_gender = ttk.Combobox(register_window, textvariable=selected_gender, state="readonly")
        dropdown_gender["values"] = ["Masculino", "Femenino"]
        dropdown_gender.pack()

        lbl_telefono = ttk.Label(register_window, text="Teléfono:")
        lbl_telefono.pack()
        entry_telefono = ttk.Entry(register_window)
        entry_telefono.pack()

        lbl_user_type = ttk.Label(register_window, text="Tipo de usuario:")
        lbl_user_type.pack()

        selected_user_type = tk.StringVar(value="cliente")
        dropdown_user_type = ttk.Combobox(register_window, textvariable=selected_user_type, state="readonly")
        dropdown_user_type["values"] = ["cliente", "instructor"]
        dropdown_user_type.pack()

        btn_register = ttk.Button(register_window, text="Registrar",
                                  command=lambda: self.register(entry_username.get(), entry_password.get(),
                                                               selected_user_type.get(), entry_nombre.get(), entry_apellido.get(),
                                                               entry_correo.get(), entry_edad.get(),
                                                               selected_gender.get(), entry_telefono.get()))
        btn_register.pack()
        
        btn_back = ttk.Button(register_window, text="Atrás", command=register_window.destroy)
        btn_back.pack()


    def register(self, username, password, user_type, nombre, apellido, correo, edad, genero, telefono):
        if self.user_manager.check_user_exists(username, user_type):
            messagebox.showerror("Error", "El usuario ya existe")
        else:
            self.user_manager.save_user(username, password, user_type, nombre, apellido, correo, edad, genero, telefono)
            messagebox.showinfo("Éxito", "El usuario ha sido registrado correctamente")

    def check_credentials(self, username, password):
        if not username or not password:
            return False

        query = "SELECT * FROM registro_cliente WHERE usuario = %s AND contrasena = %s"
        result = self.db_manager.execute_query(query, username, password)
        if result:
            return True

        query = "SELECT * FROM registro_instructor WHERE usuario = %s AND contrasena = %s"
        result = self.db_manager.execute_query(query, username, password)
        if result:
            return True

        return False


    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        username = self.username.get()
        query_cliente = "SELECT c.nombre, c.apellido FROM cliente c JOIN registro_cliente r ON r.cliente_id = c.cliente_id WHERE r.usuario = %s"
        result_cliente = self.db_manager.execute_query(query_cliente, username)

        query_instructor = "SELECT i.nombre, i.apellido FROM instructor i JOIN registro_instructor r ON r.instructor_id = i.instructor_id WHERE r.usuario = %s"
        result_instructor = self.db_manager.execute_query(query_instructor, username)

        if result_cliente:
            nombre, apellido = result_cliente[0]
            messagebox.showinfo("Inicio de sesión exitoso", f"¡Bienvenido, {nombre} {apellido}!")

            lbl_welcome = ttk.Label(self.root, text=f"¡Bienvenido al GYM CrossFit!")
            lbl_welcome.pack()

            lbl_instructor = ttk.Label(self.root, textvariable=self.selected_instructor_info)
            lbl_instructor.pack()

            btn_profile = ttk.Button(self.root, text="Ver perfil", command=self.show_user_profile)
            btn_profile.pack()

            btn_edit_profile = ttk.Button(self.root, text="Editar perfil", command=self.edit_user_profile)
            btn_edit_profile.pack()

            btn_select_instructor = ttk.Button(self.root, text="Seleccionar instructor", command=self.search_instructor)
            btn_select_instructor.pack()

            btn_show_routines = ttk.Button(self.root, text="Rutinas", command=self.show_routines)
            btn_show_routines.pack()

            btn_suggest_diet = ttk.Button(self.root, text="Dieta", command=self.suggest_diet)
            btn_suggest_diet.pack()

            btn_logout = ttk.Button(self.root, text="Cerrar sesión", command=self.logout)
            btn_logout.pack()
        elif result_instructor:
            nombre, apellido = result_instructor[0]
            messagebox.showinfo("Inicio de sesión exitoso", f"¡Bienvenido, Instructor {nombre} {apellido}!")

            lbl_welcome = ttk.Label(self.root, text=f"¡Bienvenido al GYM CrossFit!")
            lbl_welcome.pack()

            lbl_instructor = ttk.Label(self.root, textvariable=self.selected_instructor_info)
            lbl_instructor.pack()

            btn_profile = ttk.Button(self.root, text="Ver perfil", command=self.show_user_profile)
            btn_profile.pack()

            btn_edit_profile = ttk.Button(self.root, text="Editar perfil", command=self.edit_user_profile)
            btn_edit_profile.pack()
            
            btn_show_routines = ttk.Button(self.root, text="Rutinas", command=self.show_routines)
            btn_show_routines.pack()

            btn_suggest_diet = ttk.Button(self.root, text="Dieta", command=self.suggest_diet)
            btn_suggest_diet.pack()


            btn_show_clients = ttk.Button(self.root, text="Ver clientes", command=self.show_clients)
            btn_show_clients.pack()

            btn_logout = ttk.Button(self.root, text="Cerrar sesión", command=self.logout)
            btn_logout.pack()

    def show_user_profile(self):
        username = self.username.get()
        query_cliente = "SELECT c.nombre, c.apellido, c.correo, c.edad, c.genero, c.telefono FROM cliente c JOIN registro_cliente r ON r.cliente_id = c.cliente_id WHERE r.usuario = %s"
        result_cliente = self.db_manager.execute_query(query_cliente, username)

        query_instructor = "SELECT i.nombre, i.apellido, i.correo, i.edad, i.genero, i.telefono FROM instructor i JOIN registro_instructor r ON r.instructor_id = i.instructor_id WHERE r.usuario = %s"
        result_instructor = self.db_manager.execute_query(query_instructor, username)

        if result_cliente:
            nombre, apellido, correo, edad, genero, telefono = result_cliente[0]
            messagebox.showinfo("Perfil", f"Nombre: {nombre}\nApellido: {apellido}\nCorreo: {correo}\nEdad: {edad}\nGénero: {genero}\nTeléfono: {telefono}")
        elif result_instructor:
            nombre, apellido, correo, edad, genero, telefono = result_instructor[0]
            messagebox.showinfo("Perfil", f"Nombre: {nombre}\nApellido: {apellido}\nCorreo: {correo}\nEdad: {edad}\nGénero: {genero}\nTeléfono: {telefono}")

    def edit_user_profile(self):
        username = self.username.get()
        query_cliente = "SELECT c.nombre, c.apellido, c.correo, c.edad, c.genero, c.telefono FROM cliente c JOIN registro_cliente r ON r.cliente_id = c.cliente_id WHERE r.usuario = %s"
        result_cliente = self.db_manager.execute_query(query_cliente, username)

        query_instructor = "SELECT i.nombre, i.apellido, i.correo, i.edad, i.genero, i.telefono FROM instructor i JOIN registro_instructor r ON r.instructor_id = i.instructor_id WHERE r.usuario = %s"
        result_instructor = self.db_manager.execute_query(query_instructor, username)

        if result_cliente:
            nombre, apellido, correo, edad, genero, telefono = result_cliente[0]
        elif result_instructor:
            nombre, apellido, correo, edad, genero, telefono = result_instructor[0]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar perfil")

        lbl_nombre = ttk.Label(edit_window, text="Nombre:")
        lbl_nombre.pack()
        entry_nombre = ttk.Entry(edit_window)
        entry_nombre.insert(0, nombre)
        entry_nombre.pack()

        lbl_apellido = ttk.Label(edit_window, text="Apellido:")
        lbl_apellido.pack()
        entry_apellido = ttk.Entry(edit_window)
        entry_apellido.insert(0, apellido)
        entry_apellido.pack()

        lbl_correo = ttk.Label(edit_window, text="Correo:")
        lbl_correo.pack()
        entry_correo = ttk.Entry(edit_window)
        entry_correo.insert(0, correo)
        entry_correo.pack()

        lbl_edad = ttk.Label(edit_window, text="Edad:")
        lbl_edad.pack()
        entry_edad = ttk.Entry(edit_window)
        entry_edad.insert(0, edad)
        entry_edad.pack()

        lbl_genero = ttk.Label(edit_window, text="Género:")
        lbl_genero.pack()

        selected_gender = tk.StringVar(value=genero)
        dropdown_gender = ttk.Combobox(edit_window, textvariable=selected_gender, state="readonly")
        dropdown_gender["values"] = ["Masculino", "Femenino"]
        dropdown_gender.pack()

        lbl_telefono = ttk.Label(edit_window, text="Teléfono:")
        lbl_telefono.pack()
        entry_telefono = ttk.Entry(edit_window)
        entry_telefono.insert(0, telefono)
        entry_telefono.pack()

        btn_save_changes = ttk.Button(edit_window, text="Guardar cambios",
                                      command=lambda: self.save_changes(entry_nombre.get(), entry_apellido.get(),
                                                                       entry_correo.get(), entry_edad.get(),
                                                                       selected_gender.get(), entry_telefono.get()))
        btn_save_changes.pack()

    def save_changes(self, nombre, apellido, correo, edad, genero, telefono):
        username = self.username.get()
        query_cliente = "SELECT c.nombre, c.apellido FROM cliente c JOIN registro_cliente r ON r.cliente_id = c.cliente_id WHERE r.usuario = %s"
        result_cliente = self.db_manager.execute_query(query_cliente, username)

        query_instructor = "SELECT i.nombre, i.apellido FROM instructor i JOIN registro_instructor r ON r.instructor_id = i.instructor_id WHERE r.usuario = %s"
        result_instructor = self.db_manager.execute_query(query_instructor, username)

        if result_cliente:
            self.user_manager.update_user(username, "cliente", nombre, apellido, correo, edad, genero, telefono)
            messagebox.showinfo("Éxito", "Los cambios han sido guardados correctamente")
        elif result_instructor:
            self.user_manager.update_user(username, "instructor", nombre, apellido, correo, edad, genero, telefono)
            messagebox.showinfo("Éxito", "Los cambios han sido guardados correctamente")

    def search_instructor(self):
        instructors = self.instructor_manager.get_all_instructors()

        if instructors:
            self.show_instructors(instructors)
        else:
            messagebox.showerror("Error", "No se encontraron instructores")

    def show_instructors(self, instructors):
        self.instructor_window = tk.Toplevel(self.root)
        self.instructor_window.title("Seleccionar Instructor")
        self.instructor_window.geometry("400x300")

        lbl_title = ttk.Label(self.instructor_window, text="Selecciona un instructor", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=10)

        for instructor in instructors:
            instructor_info = f"{instructor[1]} {instructor[2]}"
            rbtn_instructor = ttk.Radiobutton(self.instructor_window, text=instructor_info, value=instructor[0],
                                              variable=self.selected_instructor)
            rbtn_instructor.pack(anchor="w", padx=5, pady=5)

        btn_details = ttk.Button(self.instructor_window, text="Detalles",
                                 command=self.show_selected_instructor_details)
        btn_details.pack(pady=10)

        btn_accept = ttk.Button(self.instructor_window, text="Aceptar", command=self.select_instructor)
        btn_accept.pack(pady=10)

        btn_back = ttk.Button(self.instructor_window, text="Atrás", command=self.instructor_window.destroy)
        btn_back.pack(pady=10)

    def show_selected_instructor_details(self):
        instructor_id = self.selected_instructor.get()
        instructor_details = self.instructor_manager.get_instructor_details(instructor_id)
        if instructor_details:
            self.instructor_details_window = tk.Toplevel(self.instructor_window)
            self.instructor_details_window.title("Detalles del instructor")

            lbl_details = ttk.Label(self.instructor_details_window, text=instructor_details)
            lbl_details.pack()

            btn_close = ttk.Button(self.instructor_details_window, text="Cerrar",
                                   command=self.close_instructor_details)
            btn_close.pack(pady=10)

        else:
            messagebox.showerror("Error", "No se encontraron detalles del instructor")
            
            

    def select_instructor(self):
        instructor_id = self.selected_instructor.get()
        instructor_details = self.instructor_manager.get_instructor_details(instructor_id)
        if instructor_details:
            nombre_apellido = instructor_details.split("\n")[0]
            self.selected_instructor_info.set(nombre_apellido)
            self.instructor_window.destroy()

    def close_instructor_details(self):
        self.instructor_details_window.destroy()

    def show_instructor_selection_window(self):
        instructors = self.instructor_manager.get_all_instructors()

        if instructors:
            self.show_instructors(instructors)
        else:
            messagebox.showerror("Error", "No se encontraron instructores")


    def show_routines(self):
        routines = self.routine_manager.get_all_routines()

        if routines:
            self.show_routine_selection_window(routines)
        else:
            messagebox.showerror("Error", "No se encontraron rutinas")
    
    def open_routines_window(self):
        if self.routine_window is not None:
            self.routine_window.destroy()
        
        routines = self.routine_manager.get_all_routines()
        self.show_routine_selection_window(routines)
        
        
    def refresh_routines_window(self):
        routines = self.routine_manager.get_all_routines()
        self.show_routine_selection_window(routines)
    
    def update_routine_list(self):
        routines = self.routine_manager.get_all_routines()
        self.routine_window.destroy()
        self.show_routine_selection_window(routines)

    def show_routine_selection_window(self, routines):
        self.routine_window = tk.Toplevel(self.root)
        self.routine_window.title("Seleccionar Rutinas")

        lbl_title = ttk.Label(self.routine_window, text="Selecciona las rutinas:", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=10)

        for routine in routines:
            routine_id, routine_name = routine
            checkbox_routine = ttk.Checkbutton(self.routine_window, text=routine_name, variable=self.selected_routine_id,
                                            onvalue=routine_id, offvalue="")
            checkbox_routine.pack(anchor="w", padx=5, pady=5)

        btn_accept = ttk.Button(self.routine_window, text="Aceptar", command=self.show_selected_routines)
        btn_accept.pack(pady=10)

        if self.user_type == "instructor":
            btn_add_routine = ttk.Button(self.routine_window, text="Añadir Rutina", command=self.add_routine)
            btn_add_routine.pack()

            btn_modify_routine = ttk.Button(self.routine_window, text="Modificar Rutina", command=self.modify_routine)
            btn_modify_routine.pack(pady=10)
            
            btn_delete_routine = ttk.Button(self.routine_window, text="Eliminar Rutina", command=self.delete_routine)
            btn_delete_routine.pack(pady=10)

        btn_back = ttk.Button(self.routine_window, text="Atrás", command=self.routine_window.destroy)
        btn_back.pack(pady=10)

    def delete_routine(self):
        routine_id = self.selected_routine_id.get()
        if not routine_id:
            messagebox.showerror("Error", "Seleccione una rutina primero")
            return

        result = self.routine_manager.delete_routine(routine_id)
        if result:
            messagebox.showinfo("Rutina Eliminada", "La rutina ha sido eliminada exitosamente")
            self.show_routines()
        else:
            messagebox.showerror("Error", "No se pudo eliminar la rutina") 
        self.update_routine_list()
        
        
    def add_routine(self):
        routine_name = easygui.enterbox("Ingrese el nombre de la rutina:", "Nueva Rutina")
        routine_description = easygui.enterbox("Ingrese la descripción de la rutina:", "Nueva Rutina")
        routine_series = easygui.enterbox("Ingrese el número de series:", "Nueva Rutina")
        routine_repeticion = easygui.enterbox("Ingrese el número de repeticiones:", "Nueva Rutina")
        routine_tiempo_descanso = easygui.enterbox("Ingrese el tiempo de descanso en segundos:", "Nueva Rutina")

        if not routine_name:
            return

        self.routine_manager.save_routine(routine_name, routine_description, routine_series, routine_repeticion, routine_tiempo_descanso)
        messagebox.showinfo("Rutina Agregada", "La rutina ha sido agregada exitosamente")
        self.update_routine_list()

    def modify_routine(self):
        rutina_id = self.selected_routine_id.get()
        if not rutina_id:
            messagebox.showerror("Error", "Seleccione una rutina primero")
            return

        modify_window = tk.Toplevel(self.root)
        modify_window.title("Modificar Rutina")

        lbl_routine_name = ttk.Label(modify_window, text="Nuevo Nombre de Rutina:")
        lbl_routine_name.grid(row=0, column=0, padx=10, pady=10)
        entry_routine_name = ttk.Entry(modify_window)
        entry_routine_name.grid(row=0, column=1, padx=10, pady=10)

        lbl_routine_description = ttk.Label(modify_window, text="Nueva Descripción de Rutina:")
        lbl_routine_description.grid(row=1, column=0, padx=10, pady=10)
        entry_routine_description = ttk.Entry(modify_window)
        entry_routine_description.grid(row=1, column=1, padx=10, pady=10)

        lbl_routine_series = ttk.Label(modify_window, text="Nuevo Número de Series de Rutina:")
        lbl_routine_series.grid(row=2, column=0, padx=10, pady=10)
        entry_routine_series = ttk.Entry(modify_window)
        entry_routine_series.grid(row=2, column=1, padx=10, pady=10)

        lbl_routine_repeticion = ttk.Label(modify_window, text="Nuevo Número de Repeticiones de Rutina:")
        lbl_routine_repeticion.grid(row=3, column=0, padx=10, pady=10)
        entry_routine_repeticion = ttk.Entry(modify_window)
        entry_routine_repeticion.grid(row=3, column=1, padx=10, pady=10)

        lbl_routine_tiempo_descanso = ttk.Label(modify_window, text="Nuevo Tiempo de Descanso de Rutina:")
        lbl_routine_tiempo_descanso.grid(row=4, column=0, padx=10, pady=10)
        entry_routine_tiempo_descanso = ttk.Entry(modify_window)
        entry_routine_tiempo_descanso.grid(row=4, column=1, padx=10, pady=10)

        btn_modify = ttk.Button(modify_window, text="Modificar", command=lambda: self.update_routine_fields(rutina_id, entry_routine_name.get(), entry_routine_description.get(), entry_routine_series.get(), entry_routine_repeticion.get(), entry_routine_tiempo_descanso.get(), modify_window))
        btn_modify.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        

    def update_routine_fields(self, rutina_id, rutina_name, rutina_description, rutina_series, rutina_repeticion, rutina_tiempo_descanso, window):
        if not rutina_name:
            messagebox.showerror("Error", "Ingrese un nombre de rutina válido")
            return

        self.routine_manager.update_routine(rutina_id, rutina_name, rutina_description, rutina_series, rutina_repeticion, rutina_tiempo_descanso)
        messagebox.showinfo("Rutina Modificada", "La rutina ha sido modificada exitosamente")
        window.destroy()


    def show_selected_routines(self):
        routine_id = self.selected_routine_id.get()
        routine_details = self.routine_manager.get_routine_details(routine_id)
        self.selected_routine_details.set(routine_details)
        messagebox.showinfo("Detalles de la rutina", routine_details)
    
    def suggest_diet(self):
        diets = self.diet_manager.get_all_diets()

        if diets:
            self.show_diet_suggestion_window(diets)
        else:
            messagebox.showerror("Error", "No se encontraron dietas")

    def show_diet_suggestion_window(self, diets):
        self.diet_window = tk.Toplevel(self.root)
        self.diet_window.title("Sugerir Dieta")

        lbl_title = ttk.Label(self.diet_window, text="Selecciona una dieta:", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=10)

        for diet in diets:
            diet_id, diet_name = diet
            rbtn_diet = ttk.Radiobutton(self.diet_window, text=diet_name, value=diet_id, variable=self.selected_diet)
            rbtn_diet.pack(anchor="w", padx=5, pady=5)

        user_type = self.user_manager.get_user_type(self.username.get())
        
        if user_type == "cliente":
            btn_accept = ttk.Button(self.diet_window, text="Aceptar", command=self.show_selected_diet)
            btn_accept.pack(pady=10)

        elif user_type == "instructor":
            btn_accept = ttk.Button(self.diet_window, text="Aceptar", command=self.show_selected_diet)
            btn_accept.pack(pady=10)
            
            btn_add_diet = ttk.Button(self.diet_window, text="Añadir Dieta", command=self.add_diet)
            btn_add_diet.pack(pady=10)

            btn_modify_diet = ttk.Button(self.diet_window, text="Modificar Dieta", command=self.modify_diet)
            btn_modify_diet.pack(pady=10)
            
            btn_delete_diet = ttk.Button(self.diet_window, text="Eliminar dieta", command=self.delete_diet)
            btn_delete_diet.pack(pady=10)

        btn_back = ttk.Button(self.diet_window, text="Atrás", command=self.diet_window.destroy)
        btn_back.pack(pady=10)

    def add_diet(self):
        diet_name = easygui.enterbox("Ingrese el nombre de la dieta:", "Nueva Dieta")
        diet_description = easygui.enterbox("Ingrese la descripción de la dieta:", "Nueva Dieta")
        diet_forma_dieta = easygui.enterbox("Ingrese la forma de la dieta:", "Nueva Dieta")
        diet_calorias_total = easygui.enterbox("Ingrese el número total de calorías de la dieta:", "Nueva Dieta")

        if not diet_name:
            return

        self.diet_manager.save_diet(diet_name, diet_description, diet_forma_dieta, diet_calorias_total)
        messagebox.showinfo("Dieta Agregada", "La dieta ha sido agregada exitosamente")
        self.diet_window.destroy()
        self.suggest_diet()

    def modify_diet(self):
        diet_id = self.selected_diet.get()
        if not diet_id:
            messagebox.showerror("Error", "Seleccione una dieta primero")
            return

        diet_name = easygui.enterbox("Ingrese el nuevo nombre de la dieta:", "Modificar Dieta")
        diet_description = easygui.enterbox("Ingrese la nueva descripción de la dieta:", "Modificar Dieta")
        diet_forma_dieta = easygui.enterbox("Ingrese la nueva forma de la dieta:", "Modificar Dieta")
        diet_calorias_total = easygui.enterbox("Ingrese el nuevo número total de calorías de la dieta:", "Modificar Dieta")

        if not diet_name:
            return

        query = "UPDATE dieta SET nombre = %s, descripcion = %s, forma_dieta = %s, calorias_total = %s WHERE dieta_id = %s"
        self.db_manager.execute_query(query, diet_name, diet_description, diet_forma_dieta, diet_calorias_total, diet_id)

        messagebox.showinfo("Dieta Modificada", "La dieta ha sido modificada exitosamente")
        self.diet_window.destroy()
        self.suggest_diet()

    def delete_diet(self):
        dieta_id = self.selected_diet.get()
        if dieta_id:
            confirmar = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta dieta?")
            if confirmar:
                if self.diet_manager.delete_diet(dieta_id):
                    messagebox.showinfo("Eliminación exitosa", "La dieta ha sido eliminada correctamente.")
                    self.selected_diet.set("")
                    self.suggest_diet()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la dieta.")
        else:
            messagebox.showerror("Error", "Selecciona una dieta para eliminar.")
            
        self.diet_window.destroy()
        self.suggest_diet()

    def show_selected_diet(self):
        diet_id = self.selected_diet.get()
        diet_details = self.diet_manager.get_diet_details(diet_id)
        if diet_details:
            messagebox.showinfo("Detalles de la dieta", diet_details)
        else:
            messagebox.showerror("Error", "No se encontraron detalles de la dieta")
        self.diet_window.destroy()
        self.suggest_diet()

    def show_clients(self):
        clients_window = tk.Toplevel(self.root)
        clients_window.title("Clientes")

        query = "SELECT nombre, apellido FROM cliente"
        result = self.db_manager.execute_query(query)

        lbl_clients = ttk.Label(clients_window, text="Clientes:")
        lbl_clients.pack()

        for client in result:
            client_name = f"{client[0]} {client[1]}"
            rbtn_client = ttk.Radiobutton(clients_window, text=client_name, value=client_name, variable=self.selected_client)
            rbtn_client.pack(anchor="w", padx=5, pady=5)


        btn_details = ttk.Button(clients_window, text="Detalles", command=self.show_selected_client_details)
        btn_details.pack(pady=10)

        btn_back = ttk.Button(clients_window, text="Atrás", command=clients_window.destroy)
        btn_back.pack(pady=10)
        
    def show_client_details(self, client_name):
        query = "SELECT nombre, apellido, correo, edad, genero, telefono FROM cliente WHERE CONCAT(nombre, ' ', apellido) = %s"
        result = self.db_manager.execute_query(query, client_name)

        if result:
            nombre, apellido, correo, edad, genero, telefono = result[0]
            messagebox.showinfo("Detalles del Cliente", f"Nombre: {nombre}\nApellido: {apellido}\nCorreo: {correo}\nEdad: {edad}\nGénero: {genero}\nTeléfono: {telefono}")
        else:
            messagebox.showerror("Error", "No se encontraron detalles del cliente")

            
    def show_selected_client_details(self):
        client_name = self.selected_client.get()
        if client_name:
            self.show_client_details(client_name)
        else:
            messagebox.showerror("Error", "No se ha seleccionado ningún cliente")


    def logout(self):
        self.username.set("")
        self.password.set("")
        self.selected_instructor.set("")
        self.selected_instructor_info.set("")
        self.selected_routine_id.set("")
        self.selected_routine_details.set("")
        self.selected_diet.set("")

        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_widgets()

    def close_app(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GymApp(root)
    root.mainloop() 
