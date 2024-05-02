from tkinter import ttk, messagebox
from tkinter import *
import tkinter as tk
import pyodbc

def nuevo():
    global conexion, textBoxNombres, textBoxApellidos, textBoxFecha, textBoxTel, textCorreo, textCargo, textSalario

    nombre = textBoxNombres.get()
    apellido = textBoxApellidos.get()
    fecha_nac = textBoxFecha.get()
    telefono = textBoxTel.get()
    correo = textCorreo.get()
    cargo = textCargo.get()
    salario = textSalario.get()

    if nombre and apellido and fecha_nac and telefono and correo and cargo and salario:
        try:
            with conexion.cursor() as cur:
                sql = '''INSERT INTO Empleados_ (Nombre, Apellido, FechaNac, Telefono, Correo, Cargo, Salario) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)'''
                cur.execute(sql, (nombre, apellido, fecha_nac, telefono, correo, cargo, salario))
                conexion.commit()
                messagebox.showinfo("Éxito", "Empleado agregado exitosamente")
                limpiar_campos()
                llenar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el empleado: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "Por favor complete todos los campos")

def modificar():
    seleccion = tree.selection()

    if seleccion:
        detalles_empleado = tree.item(seleccion)

        def guardar_modificaciones():
            nuevo_nombre = textBoxNombres.get()
            nuevo_apellido = textBoxApellidos.get()
            nueva_fecha = textBoxFecha.get()
            nuevo_telefono = textBoxTel.get()
            nuevo_correo = textCorreo.get()
            nuevo_cargo = textCargo.get()
            nuevo_salario = textSalario.get()

            tree.item(seleccion, values=(nuevo_nombre, nuevo_apellido, nueva_fecha, nuevo_telefono, nuevo_correo, nuevo_cargo, nuevo_salario))
            ventana_modificar.destroy()

        ventana_modificar = tk.Toplevel()
        ventana_modificar.title("Alerta")

        nuevo_nombre_label = tk.Label(ventana_modificar, text="Seguro que quiere modificar el empleado " + detalles_empleado['values'][0])
        nuevo_nombre_label.grid(row=0, column=0)

        guardar_button = tk.Button(ventana_modificar, text="Modificar", command=guardar_modificaciones)
        guardar_button.grid(row=8, columnspan=2)

    else:
        messagebox.showwarning("Advertencia", "Por favor seleccione un empleado para modificar")

def eliminar():
    seleccion = tree.selection()
    if seleccion:
        id_empleado = tree.item(seleccion)['text']
        try:
            with conexion.cursor() as cur:
                sql = "DELETE FROM Empleados WHERE Id = ?"
                cur.execute(sql, id_empleado)
                conexion.commit()
                messagebox.showinfo("Éxito", "Empleado eliminado exitosamente")
                llenar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el empleado: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "Por favor seleccione un empleado")

def llenar_datos():
    tree.delete(*tree.get_children())
    try:
        with conexion.cursor() as cur:
            cur.execute("SELECT * FROM Empleados")
            datos = cur.fetchall()
            for row in datos:
                tree.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            
            # Ajustar el tamaño de la tabla
            altura_tabla = len(datos) * 20  # 20 es la altura promedio de cada fila
            tree.configure(height=altura_tabla)
            
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener los datos de los empleados: {str(e)}")

def limpiar_campos():
    textBoxNombres.delete(0, tk.END)
    textBoxApellidos.delete(0, tk.END)
    textBoxFecha.delete(0, tk.END)
    textBoxTel.delete(0, tk.END)
    textCorreo.delete(0, tk.END)
    textCargo.delete(0, tk.END)
    textSalario.delete(0, tk.END)

# Configuración de la ventana principal
base = tk.Tk()
base.title("Gestión de Empleados")
base.geometry("1200x600")

# Definición de los frames
top_frame = tk.Frame(base)
top_frame.pack(side=TOP, fill=X)

bottom_frame = tk.Frame(base)
bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

# Definición de los widgets en top_frame
groupBox = LabelFrame(top_frame, text="Datos del Empleado", padx=5, pady=5)
groupBox.grid(row=0, column=0, padx=10, pady=10)

labelNombres = Label(groupBox, text="Nombres: ", width=12, font=("arial", 10)).grid(row=0, column=0)
textBoxNombres = Entry(groupBox)
textBoxNombres.grid(row=0, column=1)

labelApellidos = Label(groupBox, text="Apellidos: ", width=12, font=("arial", 10)).grid(row=1, column=0)
textBoxApellidos = Entry(groupBox)
textBoxApellidos.grid(row=1, column=1)

labelFecha = Label(groupBox, text="Fecha de\nNacimiento: ", width=12, font=("arial", 10)).grid(row=2, column=0)
textBoxFecha = Entry(groupBox)
textBoxFecha.grid(row=2, column=1)

labelTel = Label(groupBox, text="Teléfono: ", width=12, font=("arial", 10)).grid(row=3, column=0)
textBoxTel = Entry(groupBox)
textBoxTel.grid(row=3, column=1)

labelCorreo = Label(groupBox, text="Correo: ", width=12, font=("arial", 10)).grid(row=4, column=0)
textCorreo = Entry(groupBox)
textCorreo.grid(row=4, column=1)

labelCargo = Label(groupBox, text="Cargo: ", width=12, font=("arial", 10)).grid(row=5, column=0)
textCargo = Entry(groupBox)
textCargo.grid(row=5, column=1)

labelSalario = Label(groupBox, text="Salario: ", width=12, font=("arial", 10)).grid(row=6, column=0)
textSalario = Entry(groupBox)
textSalario.grid(row=6, column=1)

Button(groupBox, text="Guardar", width=10, command=nuevo).grid(row=7, column=0)
Button(groupBox, text="Modificar", width=10, command=modificar).grid(row=7, column=1)
Button(groupBox, text="Eliminar", width=10, command=eliminar).grid(row=7, column=2)

# Definición del TreeView en bottom_frame
tree = ttk.Treeview(bottom_frame, columns=("Nombres", "Apellidos", "F/ Nacimiento", "Teléfono", "Correo", "Cargo", "Salario"), show='headings')
tree.column("#1", anchor=CENTER)
tree.heading("#1", text="Nombres")
tree.column("#2", anchor=CENTER)
tree.heading("#2", text="Apellidos")
tree.column("#3", anchor=CENTER)
tree.heading("#3", text="F/ Nacimiento")
tree.column("#4", anchor=CENTER)
tree.heading("#4", text="Teléfono")
tree.column("#5", anchor=CENTER)
tree.heading("#5", text="Correo")
tree.column("#6", anchor=CENTER)
tree.heading("#6", text="Cargo")
tree.column("#7", anchor=CENTER)
tree.heading("#7", text="Salario")
tree.pack(fill=BOTH, expand=True)

try:
    conexion = pyodbc.connect(
        'DRIVER={SQL Server};'
        'Server=LINAA\SQLEXPRESS;'
        'DATABASE=Empleados_;'
        'Trusted_Connection=yes;'
    )
    print("Conexion Exitosa")

    llenar_datos()

except Exception as e:
    print ("Error al mostar, error:  {}".format(e))

base.mainloop()