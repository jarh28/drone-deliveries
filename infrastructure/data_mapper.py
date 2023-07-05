from abc import ABC
from domain.entities import Drone, Medication, Item
from domain.value_objects import Model, State
from uuid import UUID


class DataMapper(ABC):
    def data_to_entity(data):
        raise NotImplementedError
    
    def entity_to_data(entity):
        raise NotImplementedError
    

class SQLiteDroneDataMapper(DataMapper):
    def data_to_entity(data):
        id, serial_number, model, weight_limit, battery_capacity, state = data
        model = Model[[m.name for m in Model if m.value == model][0]]
        state = State[[s.name for s in State if s.value == state][0]]
        drone = Drone(
            serial_number, model, weight_limit, battery_capacity, state
        )
        if id:
            drone.id = UUID(id)
        return drone

    
    def entity_to_data(entity: Drone):
        return (
            str(entity.id), 
            entity.serial_number, 
            entity.model.value, 
            entity.weight_limit,
            entity.battery_level,
            entity.state.value
        )
    

class SQLiteMedicationDataMapper(DataMapper):
    def data_to_entity(data):
        id, drone_id, name, weight, code, image = data
        medication = Medication(
            name, weight, code, image
        )
        if id:
            medication.id = UUID(id)
        return medication, UUID(drone_id)

    
    def entity_to_data(entity: Medication, drone_id: UUID):
        return (
            str(entity.id), 
            str(drone_id), 
            entity.name, 
            entity.weight, 
            entity.code,
            entity.image,
        )