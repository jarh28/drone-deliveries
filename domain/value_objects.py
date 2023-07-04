from dataclasses import dataclass
from enum import Enum
import re
from typing import Optional


Model = Enum('Model', ['LIGHTWEIGHT', 'MIDDLEWEIGHT', 'CRUISERWEIGHT', 'HEAVYWEIGHT'])


State = Enum('State', ['IDLE', 'LOADING', 'LOADED', 'DELIVERING', 'DELIVERED', 'RETURNING'])


@dataclass(frozen=True)
class StringValue:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError(f'{self.__class__.__name__} must be a string (current type: {type(self.value)})')


@dataclass(frozen=True)
class FloatValue:
    value: float

    def __post_init__(self):
        if not isinstance(self.value, float):
            raise TypeError(f'{self.__class__.__name__} must be a float (current type: {type(self.value)})')
        

class SerialNumber(StringValue):
    def __post_init__(self):
        super().__post_init__()
        MIN_LENGTH, MAX_LENGTH = 1, 100
        if len(self.value) < MIN_LENGTH or len(self.value) > MAX_LENGTH:
            raise ValueError(f'{self.__class__.__name__} must have at maximum 100 characters and at least 1 character (current length: {len(self.value) } characters)')


class WeightLimit(FloatValue):
    def __post_init__(self):
        super().__post_init__()
        MIN_WEIGHT, MAX_WEIGHT = 0, 500
        if self.value < MIN_WEIGHT or self.value > MAX_WEIGHT:
            raise ValueError(f'{self.__class__.__name__} must be between 0.0 and 500.0 (current value: {self.value})')


class BatteryCapacity(FloatValue):
    def __post_init__(self):
        super().__post_init__()
        if self.value < 0 or self.value > 1:
            raise ValueError(f'{self.__class__.__name__} must be between 0.0 and 1.0 (current value: {self.value})')
        

class MedicationName(StringValue):
    def __post_init__(self):
        super().__post_init__()
        VALID_PATTERN = r"^[a-zA-Z0-9-_]+$"
        if not re.match(VALID_PATTERN, self.value):
            raise ValueError(f'{self.__class__.__name__} has invalid characters or is empty (current value: {self.value})')


class MedicationCode(StringValue):
    def __post_init__(self):
        super().__post_init__()
        VALID_PATTERN = r"^[A-Z0-9_]"
        if not re.match(VALID_PATTERN, self.value):
            raise ValueError(f'{self.__class__.__name__} has invalid characters or is empty (current value: {self.value})')


@dataclass(frozen=True)
class BytesValue:
    value: Optional[bytes]

    def __post_init__(self):
        if self.value is not None and not isinstance(self.value, bytes):
            raise TypeError(f'{self.__class__.__name__} must be a byte sequence (current type: {type(self.value)})')


class Image(BytesValue):
    pass

