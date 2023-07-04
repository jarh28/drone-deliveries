import unittest
from domain.value_objects import Model, State
from domain.entities import Drone, Medication


class DroneTestCase(unittest.TestCase):
    def setUp(self):
        self.serialNumber = '123'
        self.weightLimit = 250.0
        self.batteryCapacity = 0.5
        self.model = Model.CRUISERWEIGHT
        self.state = State.IDLE
        self.drone = Drone(
            serialNumber=self.serialNumber,
            model=self.model,
            weightLimit=self.weightLimit,
            batteryCapacity=self.batteryCapacity,
            state=self.state
        )

    def test_create_invalid_model_drone(self):
        with self.assertRaises(TypeError):
            Drone(
                serialNumber=self.serialNumber,
                model='unknown',
                weightLimit=self.weightLimit,
                batteryCapacity=self.batteryCapacity,
                state=self.state
            )

    def test_create_invalid_state_drone(self):
        with self.assertRaises(TypeError):
            Drone(
                serialNumber=self.serialNumber,
                model=self.model,
                weightLimit=self.weightLimit,
                batteryCapacity=self.batteryCapacity,
                state='IDLE'
            )

    def test_set_drone_state(self):
        with self.assertRaises(TypeError):
            self.drone.state = 'LOADING'

        with self.assertRaises(ValueError):
            drone = Drone(
                serialNumber=self.serialNumber,
                model=self.model,
                weightLimit=self.weightLimit,
                batteryCapacity=0.20,
                state=self.state
            )
            drone.state = State.LOADING

        self.drone.state = State.LOADING
        self.assertEqual(self.drone.state, State.LOADING)

        self.drone.state = State.DELIVERING
        self.assertEqual(self.drone.state, State.DELIVERING)


if __name__ == '__main__':
    unittest.main()