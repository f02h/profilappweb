import sqlite3
conn = sqlite3.connect('todo.db') # Warning: This file is created in the current directory
conn.execute("CREATE TABLE zaga (id INTEGER PRIMARY KEY, name char(100) NOT NULL, qty REAL NOT NULL, dimensions REAL NOT NULL, dodano INTEGER, izbrisano INTEGER, project TEXT, status bool NOT NULL)")
conn.execute("CREATE TABLE vrtalka (id INTEGER PRIMARY KEY, name char(100) NOT NULL, qty REAL NOT NULL, dimensions REAL NOT NULL, dodano INTEGER, izbrisano INTEGER, project TEXT, status bool NOT NULL)")
conn.execute("CREATE TABLE vars (id INTEGER PRIMARY KEY, name char(100) NOT NULL, value REAL NOT NULL)")
conn.execute("INSERT INTO vars (name, value) VALUES ('dolzinaRoke', 300),('debelinaZage', 3.2)")
conn.commit()

CREATE TABLE items (id INTEGER PRIMARY KEY AUTO_INCREMENT, name char(100) NOT NULL, qty REAL NOT NULL, dimensions REAL NOT NULL, dimType char(100) NOT NULL, material char(100) NOT NULL, dodano INTEGER, izbrisano INTEGER, project TEXT, status bool NOT NULL)

