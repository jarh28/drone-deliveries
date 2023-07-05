from abc import ABC, abstractmethod
from uuid import UUID
from domain.entities import Entity, Drone, Item

class Repository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, entity_id: UUID):
        raise NotImplementedError

    def __getitem__(self, entity_id: UUID):
        return self.get_by_id(entity_id)

    @abstractmethod
    def save(self, entity: Entity):
        raise NotImplementedError
    
    @abstractmethod
    def update(self, entity: Entity):
        raise NotImplementedError
    
    @abstractmethod
    def remove(self, entity: Entity):
        raise NotImplementedError


class DroneRepository(Repository):    
    @abstractmethod
    def save(self, drone: Drone):
        raise NotImplementedError
    
    @abstractmethod
    def update(self, drone: Drone):
        raise NotImplementedError
    
    @abstractmethod
    def remove(self, drone: Drone):
        raise NotImplementedError


class ItemRepository(Repository):
    @abstractmethod
    def get_by_drone_id(self, drone_id: UUID):
        raise NotImplementedError

    @abstractmethod
    def save(self, item: Item, drone_id: UUID):
        raise NotImplementedError
    
    @abstractmethod
    def update(self, item: Item):
        raise NotImplementedError
    
    @abstractmethod
    def remove(self, item: Item):
        raise NotImplementedError