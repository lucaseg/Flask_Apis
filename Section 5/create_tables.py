import sqlite3

# Conexion a base de datos
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Creacion de las tablas
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

# Agregamos un producto a la tabla
cursor.execute("INSERT INTO items VALUES ('test',10.99)")

# Cierre de conexion
connection.commit()
connection.close()