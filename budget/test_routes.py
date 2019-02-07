from app import *
import json
import unittest
from scripts.db_setup import make_tables, drop_tables

class my_budget_route_test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        make_tables()

    def tearDown(self):
        drop_tables()

    def test_for_a_singel_budget(self):
        route = self.app.get('/budget/1')
        actual_data = json.loads(route.get_data(as_text=True))
        expected_data = {
            "data": {   
                "budget_id": 1, 
                "budget_title": "january"
                }, 
                "error": "null"
            }

        self.assertEqual(actual_data['data'], expected_data['data'])


    def test_get_all_budget(self):
        route = self.app.get('/budget')
        data = json.loads(route.get_data(as_text=True))
        self.assertTrue(data['data'])


    def test_delete_from_budget(self):
        self.app.delete('/budget/2')

        route = self.app.get('/budget')
        data = json.loads(route.get_data(as_text=True))
        list_of_dict = data['data']
        for dict in list_of_dict:
            self.assertNotEqual(dict.get("budget_id"), 2)

    def test_post_to_budget(self):
        title= {'budget_title':'march'}
        route = self.app.post('/budget', data=json.dumps(title), content_type ='application/json')
        actual_data = json.loads(route.get_data(as_text=True))
        failure ={"data": None,"error":"title name, 'march' already exists"}
        success = {"data":{"title":'march', "budget_id":3},"error":None}

        if actual_data == failure:
            self.assertEqual(actual_data, failure)
        elif actual_data['data'] == success['data']:
            self.assertEqual(actual_data['data'],success['data'])
        else:
            self.assertEqual(actual_data['data'],success['data'])
            


    def test_put_to_budget(self):
        title= {'budget_title':'new'}
        route = self.app.put('/budget/1', data=json.dumps(title), content_type ='application/json')
        actual_data = json.loads(route.get_data(as_text=True))
        failure ={"data": None,"error":"title name, 'new' already exists"}
        success = {"data":{"budget_title":'new', "budget_id":1},"error":None}

        if actual_data == failure:
            self.assertEqual(actual_data, failure)
        elif actual_data['data'] == success['data']:
            self.assertEqual(actual_data['data'],success['data'])
        else:
            self.assertEqual(actual_data['data'],success['data'])
            

            


        
        

    

    
            



if __name__ =='__main__':
    unittest.main()
