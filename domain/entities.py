from abc import ABC
from .value_objects import (
    SerialNumber, 
    WeightLimit, 
    BatteryCapacity, 
    MedicationName, 
    MedicationCode, 
    Image, 
    FloatValue,
    Model,
    State
)
from uuid import UUID, uuid4
from dataclasses import dataclass


@dataclass
class Entity(ABC):
    @staticmethod
    def next_id():
        return uuid4()


@dataclass
class Item(Entity):
    def __init__(self, weight):
        self.__id: UUID = Entity.next_id()      
        self.__weight = FloatValue(weight)

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        if not isinstance(value, UUID):
            raise TypeError(f'Id attribute must be of type {UUID} (current type: {type(value)})')
        self.__id = value

    @property
    def weight(self):
        return self.__weight.value


@dataclass
class Medication(Item):
    def __init__(self, name: str, weight: float, code: str, image: bytes = None):
        super().__init__(weight)
        self.__name = MedicationName(name)
        self.__code = MedicationCode(code)
        self.__image = Image(image)

    @property
    def name(self):
        return self.__name.value
    
    @property
    def code(self):
        return self.__code.value
    
    @property
    def image(self):
        return self.__image.value


@dataclass
class Drone(Entity):
    def __init__(self, serialNumber: str, model: Model, weightLimit: float, batteryCapacity: float, state: State):
        if not isinstance(model, Model):
            raise TypeError(f'Model attribute must be of type {Model} (current type: {type(model)})')
        if not isinstance(state, State):
            raise TypeError(f'State attribute must be of type {State} (current type: {type(state)})')
        self.__id: UUID = Entity.next_id()
        self.__model = model
        self.__state = state
        self.__serial_number = SerialNumber(serialNumber)
        self.__weight_limit = WeightLimit(weightLimit)
        self.__battery_capacity = BatteryCapacity(batteryCapacity)

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        if not isinstance(value, UUID):
            raise TypeError(f'Id attribute must be of type {UUID} (current type: {type(value)})')
        self.__id = value
    
    @property
    def model(self):
        return self.__model
    
    @property
    def serial_number(self):
        return self.__serial_number.value
    
    @property
    def weight_limit(self):
        return self.__weight_limit.value
    
    @property
    def battery_level(self):
        return self.__battery_capacity.value

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if not isinstance(value, State):
            raise TypeError(f'State attribute must be of type {State} (current type: {type(value)})')
        BATTERY_LEVEL_LIMIT = 0.25
        if self.__battery_capacity.value < BATTERY_LEVEL_LIMIT and value is State.LOADING:  
            raise ValueError(f'Cannot set state to {value} because battery level is below 25% (current baterry: {self.__battery_capacity.value * 100}%)') 
        self.__state = value
