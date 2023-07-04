from domain.value_objects import (
    SerialNumber, 
    WeightLimit, 
    BatteryCapacity, 
    MedicationName, 
    MedicationCode,
)
import unittest


class SerialNumberTestCase(unittest.TestCase):
    def test_cannot_create_invalid_length_serial_number(self):
        with self.assertRaises(ValueError):
            SerialNumber('1' * 101)

        with self.assertRaises(ValueError):
            SerialNumber('')


class WeightLimitTestCase(unittest.TestCase):
    def test_cannot_create_invalid_range_weight_limit(self):
        with self.assertRaises(ValueError):
            WeightLimit(501.0)

        with self.assertRaises(ValueError):
            WeightLimit(-1e-5)


class BatteryCapacityTestCase(unittest.TestCase):
    def test_cannot_create_invalid_range_battery_capacity(self):
        with self.assertRaises(ValueError):
            BatteryCapacity(1.0001)
        
        with self.assertRaises(ValueError):
            BatteryCapacity(-0.0001)


class MedicationNameTestCase(unittest.TestCase):
    def test_create_invalid_character_medication_name(self):
        with self.assertRaises(ValueError):
            MedicationName('!@#$%^&*()+=`~:;\'"[{}]/?\\|.>,<')

        with self.assertRaises(ValueError):
            MedicationName('')


class MedicationCodeTestCase(unittest.TestCase):
    def test_create_invalid_character_medication_code(self):
        with self.assertRaises(ValueError):
            MedicationCode('!@#$%^&*()+=`~:;\'"[{}]/?\\|.>,<')

        with self.assertRaises(ValueError):
            MedicationCode('qwertyuiopasdfghjklzxcvbnm-')

        with self.assertRaises(ValueError):
            MedicationCode('')


if __name__ == '__main__':
    unittest.main()