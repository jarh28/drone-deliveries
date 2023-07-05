import unittest
from domain.entities import Drone, Medication
from domain.value_objects import Model, State
from infrastructure.data_mapper import SQLiteDroneDataMapper, SQLiteMedicationDataMapper
from uuid import uuid4


class SQLiteDroneTestCase(unittest.TestCase):
    def setUp(self):
        self.drone = Drone('dr001', Model.CRUISERWEIGHT, 300.0, 0.75, State.IDLE)
        self.data = (str(self.drone.id), 'dr001', 3, 300.0, 0.75, 1)
        self.items = [Medication('Paracetamol', 200.0, 'XYZ_10450')]

    def test_entity_to_data(self):
        result = SQLiteDroneDataMapper.entity_to_data(self.drone)
        self.assertEqual(result, self.data)       
    
    def test_data_to_entity(self):
        result = SQLiteDroneDataMapper.data_to_entity(self.data)
        self.assertEqual(result.id, self.drone.id)   
        self.assertEqual(result.serial_number, self.drone.serial_number)   
        self.assertEqual(result.model, self.drone.model)   
        self.assertEqual(result.weight_limit, self.drone.weight_limit)   
        self.assertEqual(result.battery_level, self.drone.battery_level)   
        self.assertEqual(result.state, self.drone.state)   


class SQLiteMedicationTestCase(unittest.TestCase):
    def setUp(self):
        self.medication = Medication('Paracetamol', 200.0, 'XYZ_10450')
        self.drone_id = uuid4()
        self.data = (str(self.medication.id), str(self.drone_id), 'Paracetamol', 200.0, 'XYZ_10450', None)

    def test_entity_to_data(self):
        result = SQLiteMedicationDataMapper.entity_to_data(self.medication, self.drone_id)
        self.assertEqual(result, self.data)       
        self.assertEqual(1, 1)
    
    def test_data_to_entity(self):
        result, drone_id = SQLiteMedicationDataMapper.data_to_entity(self.data)
        self.assertEqual(result.id, self.medication.id)
        self.assertEqual(result.name, self.medication.name)
        self.assertEqual(result.weight, self.medication.weight)
        self.assertEqual(result.code, self.medication.code)
        self.assertEqual(result.image, self.medication.image)
        self.assertEqual(drone_id, self.drone_id)

if __name__ == '__main__':
    unittest.main()