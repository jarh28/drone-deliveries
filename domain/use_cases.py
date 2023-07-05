from domain.entities import Drone, Item
from domain.value_objects import State
from domain.repositories import DroneRepository, ItemRepository
from uuid import UUID
from typing import List


def register_drone(drone: Drone, repository: DroneRepository):
    if not isinstance(drone, Drone):
        raise TypeError(f'Drone must be an instance of {Drone} (current type: {type(drone)})')
    if not isinstance(repository, DroneRepository):
        raise TypeError(f'Repository must be a subclass of {DroneRepository} (current class: {type(repository)})')
    
    repository.save(drone)
    

def load_drone(drone_id: UUID, item: Item, drone_repository: DroneRepository, item_repository: ItemRepository):
    if not isinstance(drone_id, UUID):
        raise TypeError(f'DroneID parameter must be of type {UUID} (current type: {type(drone_id)})')
    if not isinstance(item, Item):
        raise TypeError(f'Item parameter must be of type {Item} (current type: {type(item)})')
    if not isinstance(drone_repository, DroneRepository):
        raise TypeError(f'DroneRepository parameter must be of type {DroneRepository} (current type: {type(drone_repository)})')
    if not isinstance(item_repository, ItemRepository):
        raise TypeError(f'ItemRepository parameter must be of type {ItemRepository} (current type: {type(item_repository)})')
    
    drone: Drone = drone_repository.get_by_id(drone_id)
    if not drone.state in [State.IDLE, State.LOADED]:
        raise Exception('Drone is not currently available for loading')
    
    items = item_repository.get_by_drone_id(drone_id)
    total_weight = sum([item.weight for item in items])
    if total_weight + item.weight > drone.weight_limit:
        raise ValueError(f'Total weight of items is over the weight limit (current weight: {total_weight + item.weight}, weight limit: {drone.weight_limit})')
    
    try:
        drone.state = State.LOADING
        drone_repository.update(drone)
        item_repository.save(item, drone_id)
        drone.state = State.LOADED
        drone_repository.update(drone)
    except Exception as exception:
        drone.state = State.IDLE
        drone_repository.update(drone)
        raise exception


def check_loaded_items(drone_id: UUID, repository: ItemRepository):
    if not isinstance(drone_id, UUID):
        raise TypeError(f'DroneID parameter must be of type {UUID} (current type: {type(drone_id)})')
    if not isinstance(repository, ItemRepository):
        raise TypeError(f'Repository parameter must be of type {ItemRepository} (current type: {type(repository)})')
    
    return repository.get_by_drone_id(drone_id)


def check_availables_drones(repository: DroneRepository):
    if not isinstance(repository, DroneRepository):
        raise TypeError(f'Repository parameter must be of type {DroneRepository} (current type: {type(repository)})')
    
    drones: List[Drone] = repository.get_all()
    filter = lambda drone: drone.state in [State.IDLE, State.LOADED] and drone.battery_level >= 0.25
    drones = [drone for drone in drones if filter(drone)]
    return drones


def check_drone_battery_level(drone_id: UUID, repository: DroneRepository):
    if not isinstance(drone_id, UUID):
        raise TypeError(f'DroneID parameter must be of type {UUID} (current type: {type(drone_id)})')
    if not isinstance(repository, DroneRepository):
        raise TypeError(f'DroneRepository parameter must be of type {DroneRepository} (current type: {type(repository)})')
    
    drone: Drone = repository.get_by_id(drone_id)
    return drone.battery_level