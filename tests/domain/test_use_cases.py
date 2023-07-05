import unittest
from tests.domain.dummy import InMemoryDroneRepository, InMemoryMedicationRepository, DRONES, MEDICATIONS
from domain.use_cases import register_drone, load_drone, check_loaded_items, check_availables_drones, check_drone_battery_level
from domain.value_objects import State


class RegisterDroneTestCase(unittest.TestCase):
    def setUp(self):
        self.drone_repository = InMemoryDroneRepository()
        self.drone = DRONES[0]

    def test_register_drone(self):
        register_drone(self.drone, self.drone_repository)
        self.assertTupleEqual(self.drone_repository.get_all(), (self.drone, ))

    def test_register_drone_invalid_input(self):
        with self.assertRaises(TypeError):
            register_drone('drone', self.drone_repository)
        
        with self.assertRaises(TypeError):
            register_drone(self.drone, 'repository')


class LoadDroneTestCase(unittest.TestCase):
    def setUp(self):
        self.drone_repository = InMemoryDroneRepository()
        self.item_repository = InMemoryMedicationRepository()
        self.drones = DRONES
        self.items = MEDICATIONS

    def test_load_drone(self):
        drone, item = self.drones[0], self.items[2]
        self.drone_repository.save(drone)
        load_drone(drone.id, item, self.drone_repository, self.item_repository)
        self.assertTupleEqual((item, drone.id), self.item_repository.get_all()[0])
        self.assertEqual(drone.state, State.LOADED)

    def test_overload_drone(self):
        drone, item1, item2, item3 = self.drones[0], *self.items
        self.drone_repository.save(drone)
        with self.assertRaises(ValueError):
            load_drone(drone.id, item1, self.drone_repository, self.item_repository)
        load_drone(drone.id, item3, self.drone_repository, self.item_repository)
        with self.assertRaises(ValueError):
            load_drone(drone.id, item2, self.drone_repository, self.item_repository)

    def test_load_low_battery_drone(self):
        drone, item = self.drones[2], self.items[2]
        self.drone_repository.save(drone)
        with self.assertRaises(Exception):
            load_drone(drone.id, item, self.drone_repository, self.item_repository)


class CheckLoadedItemsTestCase(unittest.TestCase):
    def setUp(self):
        self.drone = DRONES[1]
        self.drone_repository = InMemoryDroneRepository()
        self.items = MEDICATIONS
        self.item_repository = InMemoryMedicationRepository()

    def test_check_loaded_items(self):
        self.drone_repository.save(self.drone)
        for item in self.items:
            load_drone(self.drone.id, item, self.drone_repository, self.item_repository)
        loaded_items = check_loaded_items(self.drone.id, self.item_repository)
        self.assertListEqual(loaded_items, self.items)

class CheckAvailablesDronesTestCase(unittest.TestCase):
    def setUp(self):
        self.drones = DRONES
        self.drone_repository = InMemoryDroneRepository()
        self.item_repository = InMemoryMedicationRepository()
        self.item = MEDICATIONS[2]

    def test_check_availables_drones(self):
        for drone in self.drones:
            self.drone_repository.save(drone)
        load_drone(self.drones[0].id, self.item, self.drone_repository, self.item_repository)
        available_drones = check_availables_drones(self.drone_repository)
        self.assertListEqual([self.drones[0], self.drones[1]], available_drones)


class CheckDroneBatteryLevelTestCase(unittest.TestCase):
    def setUp(self):
        self.drones = DRONES
        self.batteries = (0.5, 0.75, 0.20)
        self.drone_repository = InMemoryDroneRepository()

    def test_check_drone_battery_level(self):
        for drone in self.drones:
            self.drone_repository.save(drone)
        for i, drone in enumerate(self.drones):
            battery = check_drone_battery_level(drone.id, self.drone_repository)
            self.assertEqual(self.batteries[i], battery)


if __name__ == '__main__':
    unittest.main()