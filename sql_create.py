import sqlite3 

def create_sql(): # création de la database avec les tables requises
    con = sqlite3.connect("db_sncf_v5.db")

    cur = con.cursor()

    cur.executescript("""

        CREATE TABLE disruption(
            id_disruption TEXT,
            name VARCHAR(50),
            status VARCHAR(50),
            message VARCHAR(50),
            amended_departure_time VARCHAR(50),
            amended_arrival_time VARCHAR(50),
            PRIMARY KEY(id_disruption)
        );

        CREATE TABLE line (
            id_line INT,
            departure_train_station VARCHAR(50),
            arrival_train_station VARCHAR(50),
            PRIMARY KEY(id_line)
        );


        CREATE TABLE train (
            id_train INTEGER PRIMARY KEY AUTOINCREMENT,
            base_departure_time INT,
            base_arrival_time INT,
            train_number INT,
            departure_date INT,
            id_disruption TEXT,
            id_line INT,
            FOREIGN KEY(id_disruption) REFERENCES disruption(id_disruption),
            FOREIGN KEY(id_line) REFERENCES line(id_line)
        );

        CREATE TABLE favorite (
            id_favorite INTEGER PRIMARY KEY AUTOINCREMENT,
            id_line INTEGER NOT NULL,
            FOREIGN KEY (id_line) REFERENCES line(id_line)
        );

        CREATE TABLE account (
            id_account INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname VARCHAR(50),
            lastname VARCHAR(50),
            email VARCHAR(50) UNIQUE,
            password VARCHAR(50),
            username VARCHAR(50) UNIQUE,
            id_favorite INTEGER,
            FOREIGN KEY (id_favorite) REFERENCES favorite(id_favorite)
        );

        CREATE TABLE station (
            id_station INTEGER PRIMARY KEY AUTOINCREMENT,
            name_station TEXT,
            longitude REAL,
            latitude REAL,
            id_line INT,
            position INT,
            FOREIGN KEY (id_line) REFERENCES line(id_line)
        );

    """)

    con.close()