from abc import ABC
from application.models import DroneModel, MedicationModel


class DataMapper(ABC):
    def data_to_model(data):
        raise NotImplementedError
    
    def model_to_data(model):
        raise NotImplementedError
    

class DroneModelDataMapper(DataMapper):
    def data_to_model(data):
        params = DroneModel.__fields__.keys()
        drone_model = DroneModel(**dict(zip(params, data))) 
        return drone_model

    def model_to_data(model: DroneModel):
        id = model.drone_id and str(model.drone_id) or None
        data = (
            id, 
            model.serial_number, 
            model.model_id, 
            model.weight_limit, 
            model.battery_capacity, 
            model.state_id
        )
        return data
    

class MedicationModelDataMapper(DataMapper):
    def data_to_model(data):
        params = MedicationModel.__fields__.keys()
        medication_model = MedicationModel(**dict(zip(params, data))) 
        return medication_model

    def model_to_data(model: MedicationModel):
        id = model.medication_id and str(model.medication_id) or None
        data = (
            id, 
            str(model.drone_id), 
            model.name, 
            model.weight, 
            model.code, 
            model.image
        )
        return data