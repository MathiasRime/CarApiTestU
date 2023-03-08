import unittest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from main import app

port = 27017


class TestCarApi(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient('localhost', port)
        self.db = self.client['car']
        self.collection = self.db['car']
        self.test_client = TestClient(app)

    def test_get(self):
        response = self.test_client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), ['welcome to cars api'])

    def test_post_cars(self):
        response = self.test_client.post('/add_car', params={'brand': 'renault', 'price': '5000', 'model': 'clio'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), ['your car has been added'])
        result = self.collection.find_one({'brand': 'renault'})
        self.assertIsNotNone(result)
        self.assertEqual('renault', result['brand'])
        self.assertEqual('5000', result['price'])
        self.assertEqual('clio', result['model'])

    def test_put_cars(self):
        # Requête
        response = self.test_client.put('/update_model',
                                        params={'modelFilter': 'clio', 'brand': 'renault', 'price': '5000',
                                                'model': "laguna"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), ['the car clio has been renamed laguna'])
        result = self.collection.find_one({'model': 'laguna'})
        self.assertIsNotNone(result)
        self.assertEqual('renault', result['brand'])
        self.assertEqual('5000', result['price'])
        self.assertEqual('laguna', result['model'])
        self.test_client.put('/update_model',
                             params={'modelFilter': 'laguna', 'brand': 'renault', 'price': '5000',
                                     'model': "clio"})

    def test_delete_cars(self):
        response = self.test_client.delete('/delete_car',
                                           params={'brand': 'renault', 'price': '5000', 'model': 'clio'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), ['the car laguna has been deleted'])
        self.assertEqual(self.collection.count_documents({'brand': 'renault', 'price': '5000', 'model': 'clio'}), 0)


if __name__ == "__main__":
    unittest.main()
