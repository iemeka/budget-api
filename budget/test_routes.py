from app import *
import json
import unittest


class my_budget_route_test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_for_a_singel_budget(self):
        route = self.app.get('/budget/5')
        actual_data = json.loads(route.get_data(as_text=True))
        expected_data = {
            "data": {   
                "budget_id": 5, 
                "budget_title": "january"
                }, 
                "error": "null"
            }

        self.assertEqual(actual_data['data'], expected_data['data'])

    def test_for_all_budget(self):
        route = self.app.get('/budget')
        data = json.loads(route.get_data(as_text=True))
        self.assertTrue(data['data'])

    def test_delete_from_budget(self):
        self.app.delete('/budget/5')

        route = self.app.get('/budget')
        data = json.loads(route.get_data(as_text=True))
        list_of_dict = data['data']
        for dict in list_of_dict:
            self.assertNotEqual(dict.get("budget_id"), 5)

    

    
            



if __name__ =='__main__':
    unittest.main()
