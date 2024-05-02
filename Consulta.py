import pyodbc 

conexion = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER='#nombre del servidor
    'DATABASE='#nombre de la base de datos
    'Trusted_Connection=yes;'



) 
cursor =conexion.cursor()

cursor.execute("select * from estudiantes")

for fila in cursor:
    print(fila)

cursor.close()
conexion.close()