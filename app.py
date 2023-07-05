from fastapi import FastAPI, Response, status
from domain.use_cases import register_drone, load_drone, check_loaded_items, check_availables_drones, check_drone_battery_level
from infrastructure.repositories import SQLiteDroneRepository, SQLiteMedicationRepository
from infrastructure.data_mapper import SQLiteDroneDataMapper, SQLiteMedicationDataMapper
from uuid import UUID
from application.data_mappers import DroneModelDataMapper, MedicationModelDataMapper
from application.models import DroneModel, MedicationModel


app = FastAPI()


@app.get('/drones/')
async def get_drones():
    drones = SQLiteDroneRepository().get_all()    
    drones = [SQLiteDroneDataMapper.entity_to_data(drone) for drone in drones]
    drones = [DroneModelDataMapper.data_to_model(drone) for drone in drones]   
    return drones


@app.post('/drones/register/')
async def post_drone(drone: DroneModel, response: Response):
    try:
        drone = DroneModelDataMapper.model_to_data(drone)
        drone = SQLiteDroneDataMapper.data_to_entity(drone)
        register_drone(drone, SQLiteDroneRepository())
        response.status_code = status.HTTP_201_CREATED
        return {'message': 'drone registered'}
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'error': str(exception)}


@app.post('/drones/load/')
async def post_medication(medication: MedicationModel, response: Response):
    try:
        medication = MedicationModelDataMapper.model_to_data(medication)
        medication, drone_id = SQLiteMedicationDataMapper.data_to_entity(medication)
        load_drone(drone_id,medication, SQLiteDroneRepository(), SQLiteMedicationRepository())
        response.status_code = status.HTTP_201_CREATED
        return {'message': 'drone loaded'}
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'error': str(exception)}


@app.get('/drones/medications/')
async def get_medications_by_drone(drone_id: str, response: Response):
    try:
        medications = check_loaded_items(UUID(drone_id), SQLiteMedicationRepository())
        medications = [SQLiteMedicationDataMapper.entity_to_data(medication, drone_id) for medication in medications]
        medications = [MedicationModelDataMapper.data_to_model(medication) for medication in medications]  
        return medications
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'error': str(exception)}


@app.get('/drones/available/')
async def get_available_drones(response: Response):
    drones = check_availables_drones(SQLiteDroneRepository())
    drones = [SQLiteDroneDataMapper.entity_to_data(drone) for drone in drones]
    drones = [DroneModelDataMapper.data_to_model(drone) for drone in drones]   
    return drones


@app.get('/drones/battery/')
async def get_drone_battery_level(drone_id: str, response: Response):
    try:
        return check_drone_battery_level(UUID(drone_id), SQLiteDroneRepository())
    except Exception as exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'error': str(exception)}