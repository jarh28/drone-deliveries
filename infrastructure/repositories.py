from domain.entities import Drone, Medication
from uuid import UUID
from infrastructure.decorators import sqlite_connection_handler
from config import DATABASE_CONNECTION_STRING
from infrastructure.data_mapper import SQLiteDroneDataMapper, SQLiteMedicationDataMapper
from sqlite3 import Connection
from domain.repositories import DroneRepository, ItemRepository


class SQLiteMedicationRepository(ItemRepository):
    def connection_handler():
        return sqlite_connection_handler(DATABASE_CONNECTION_STRING)

    def get_all(self, conn: Connection):
        data = conn.execute("SELECT * FROM medications").fetchall()
        medication = [SQLiteMedicationDataMapper.data_to_entity(medication) for medication in data]
        return medication

    def get_by_id(self, entity_id: UUID, conn: Connection):
        if not isinstance(entity_id, UUID):
            raise TypeError
        drone = conn.execute("SELECT * FROM medications WHERE medication_id = ?", (str(entity_id), )).fetchone()
        if drone:
            return SQLiteDroneDataMapper.data_to_entity(drone)
        raise Exception('Medication not found')

    @connection_handler()
    def get_by_drone_id(self, drone_id: UUID, conn: Connection):
        if not isinstance(drone_id, UUID):
            raise TypeError
        medications = conn.execute("SELECT * FROM medications WHERE drone_id = ?", (str(drone_id), )).fetchall()
        medications = [SQLiteMedicationDataMapper.data_to_entity(medication)[0] for medication in medications]
        return medications
     
    @connection_handler()
    def save(self, medication: Medication, drone_id: UUID,conn: Connection):
        if not isinstance(medication, Medication):
            raise TypeError
        cursor = conn.cursor() 
        data = SQLiteMedicationDataMapper.entity_to_data(medication, drone_id) 
        cursor.execute("""
        INSERT INTO medications (
            medication_id, drone_id, name, weight, code, image
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

    def update(self, medication: Medication, conn: Connection):
        if not isinstance(medication, Medication):
            raise TypeError
        cursor = conn.cursor()
        data = SQLiteMedicationDataMapper.entity_to_data(medication)
        cursor.execute("""
        UPDATE medications SET  
        name = ?, 
        weight = ?, 
        code = ?, 
        image = ?
        WHERE medication_id = ?
        """, (*data[2:], data[0], ))
        conn.commit()

    def remove(self, medication: Medication, conn: Connection):
        if not isinstance(medication, Medication):
            raise TypeError
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM medications WHERE medication_id = ?
        """, (str(medication.id), ))
        conn.commit()


class SQLiteDroneRepository(DroneRepository):
    def connection_handler():
        return sqlite_connection_handler(DATABASE_CONNECTION_STRING)
    
    @connection_handler()
    def get_all(self, conn: Connection):
        data = conn.execute("SELECT * FROM drones").fetchall()
        drones = [SQLiteDroneDataMapper.data_to_entity(drone) for drone in data]
        return drones

    @connection_handler()
    def get_by_id(self, entity_id: UUID, conn: Connection):
        if not isinstance(entity_id, UUID):
            raise TypeError
        drone = conn.execute("SELECT * FROM drones WHERE drone_id = ?", (str(entity_id), )).fetchone()
        if drone:
            return SQLiteDroneDataMapper.data_to_entity(drone)
        raise Exception('Drone not found')
    
    @connection_handler()
    def save(self, drone: Drone, conn: Connection):
        if not isinstance(drone, Drone):
            raise TypeError
        cursor = conn.cursor() 
        data = SQLiteDroneDataMapper.entity_to_data(drone) 
        cursor.execute("""
        INSERT INTO drones (
            drone_id, serial_number, model_id, weight_limit, battery_capacity, state_id
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

    @connection_handler()
    def update(self, drone: Drone, conn: Connection):
        if not isinstance(drone, Drone):
            raise TypeError
        cursor = conn.cursor()
        data = SQLiteDroneDataMapper.entity_to_data(drone)
        cursor.execute("""
        UPDATE drones SET  
        serial_number = ?, 
        model_id = ?, 
        weight_limit = ?, 
        battery_capacity = ?, 
        state_id = ?
        WHERE drone_id = ?
        """, (*data[1:], data[0], ))
        conn.commit()

    def remove(self, drone: Drone, conn: Connection):
        if not isinstance(drone, Drone):
            raise TypeError
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM drones WHERE drone_id = ?
        """, (str(drone.id), ))
        conn.commit()