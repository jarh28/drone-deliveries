from domain.repositories import DroneRepository, ItemRepository
from domain.entities import Drone, Medication
from domain.value_objects import Model, State
from uuid import UUID
from typing import List

DRONES = [
    Drone('dr001', Model.LIGHTWEIGHT, 100.0, 0.5, State.IDLE),
    Drone('dr002', Model.HEAVYWEIGHT, 450.0, 0.75, State.IDLE),
    Drone('dr003', Model.MIDDLEWEIGHT, 150.0, 0.20, State.IDLE)
]

MEDICATIONS = [
    Medication('Paracetamol', 200.0, 'XYZ_123'),
    Medication('Aspirin', 120.0, 'ABC_153'),
    Medication('Ibuprofen', 60.0, "JHI_876")
]

class InMemoryDroneRepository(DroneRepository):
    def __init__(self):
        self.__data: List[Drone] = []

    def get_all(self):
        return tuple(self.__data)
    
    def get_by_id(self, entity_id: UUID):
        for drone in self.__data:
            if drone.id == entity_id:
                return drone
        raise ValueError
    
    def save(self, drone: Drone):
        self.__data.append(drone)

    def update(self, drone: Drone):
        for entity in self.__data:
            if entity.id == drone.id:
                entity = drone
                return
        raise ValueError

    def remove(self, drone: Drone):
        for i, entity in enumerate(self.__data):
            if entity.id == drone.id:
                self.__data.pop(i)
                return
        raise ValueError


class InMemoryMedicationRepository(ItemRepository):
    def __init__(self):
        self.__data: List[(Medication, UUID)] = []

    def get_all(self):
        return tuple(self.__data)
    
    def get_by_id(self, entity_id: UUID):
        for medication, _ in self.__data:
            if medication.id == entity_id:
                return medication
        raise ValueError
    
    def get_by_drone_id(self, drone_id: UUID):
        medications = []
        for medication, data_drone_id in self.__data:
            if data_drone_id == drone_id:
                medications.append(medication)
        return medications
    
    def save(self, medication: Medication, drone_id: UUID):
        self.__data.append((medication, drone_id))

    def update(self, medication: Medication):
        for entity, _ in self.__data:
            if entity.id == medication.id:
                entity = medication
                return
        raise ValueError

    def remove(self, medication: Medication):
        for i, entity, _ in enumerate(self.__data):
            if entity.id == medication.id:
                self.__data.pop(i)
                return
        raise ValueError