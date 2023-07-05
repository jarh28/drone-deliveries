import sqlite3
from uuid import UUID
from config import DATABASE_CONNECTION_STRING

conn = sqlite3.connect(DATABASE_CONNECTION_STRING)
conn.execute("PRAGMA foreign_keys=on;")

cursor = conn.cursor()

with conn:
    # Creating tables
    conn.execute("""
    CREATE TABLE IF NOT EXISTS drones (
        drone_id VARCHAR(36) PRIMARY KEY,
        serial_number VARCHAR(100) NOT NULL UNIQUE,
        model_id INT NOT NULL,
        weight_limit REAL NOT NULL,
        battery_capacity REAL NOT NULL,
        state_id INT NOT NULL,
        CONSTRAINT fk_models
            FOREIGN KEY (model_id) 
            REFERENCES models(model_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        CONSTRAINT fk_states
            FOREIGN KEY (state_id) 
            REFERENCES states(state_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """)
             
    conn.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        medication_id VARCHAR(36) PRIMARY KEY,
        drone_id VARCHAR(36),
        name VARCHAR NOT NULL,
        weight REAL NOT NULL,
        code VARCHAR NOT NULL UNIQUE,
        image BLOB,
        CONSTRAINT fk_drones
            FOREIGN KEY (drone_id) 
            REFERENCES drones(drone_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS models (
        model_id INT PRIMARY KEY,
        model_name VARCHAR
    );
    """)
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS states (
        state_id INT PRIMARY KEY,
        state_name VARCHAR
    );
    """)

    # Populating tables
    MODELS = [('LIGHTWEIGHT', 1), ('MIDDLEWEIGHT', 2), ('CRUISERWEIGHT', 3), ('HEAVYWEIGHT', 4)]
    for (name, id) in MODELS:
        cursor.execute("""
        INSERT INTO models (model_id, model_name) VALUES (?, ?);
        """, (id, name))

    STATES = [('IDLE', 1), ('LOADING', 2), ('LOADED', 3), ('DELIVERING', 4), ('DELIVERED', 5), ('RETURNING', 6)]
    for (name, id) in STATES:
        cursor.execute("""
        INSERT INTO states (state_id, state_name) VALUES (?, ?);
        """, (id, name))
    
    drone_id = str(UUID('30df78ec-0532-4067-855e-79644bfcc48f'))
    cursor.execute("""
    INSERT INTO drones (
        drone_id, serial_number, model_id, weight_limit, battery_capacity, state_id
    ) VALUES (?, ?, ?, ?, ?, ?);
    """, (drone_id, "dr001", 3, 300.0, 0.75, 1))
             
    medication_id = str(UUID('6bf4e4b9-6406-4594-8030-87d7ec3c37e3'))
    cursor.execute("""
    INSERT INTO medications (
        medication_id, drone_id, name, weight, code
    ) VALUES (?, ?, ?, ?, ?);
    """, (medication_id, drone_id, 'Paracetamol', 200.0, 'XYZ_10450'))