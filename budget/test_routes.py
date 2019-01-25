from app import *
import json
import unittest



class my_budget_route_test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_for_a_singel_budget(self):
        route = self.app.get('/budget/2')
        actual_data = json.loads(route.get_data(as_text=True))
        expected_data = {
            "data": {   
                "budget_id": 2, 
                "budget_title": "febuary"
                }, 
                "error": "null"
            }

        self.assertEqual(actual_data['data'], expected_data['data'])


    def test_get_all_budget(self):
        route = self.app.get('/budget')
        data = json.loads(route.get_data(as_text=True))
        self.assertTrue(data['data'])


    # def test_delete_from_budget(self):
    #     self.app.delete('/budget/3')

    #     route = self.app.get('/budget')
    #     data = json.loads(route.get_data(as_text=True))
    #     list_of_dict = data['data']
    #     for dict in list_of_dict:
    #         self.assertNotEqual(dict.get("budget_id"), 3)

    def test_post_to_budget(self):
        title= {'budget_title':'december'}
        route = self.app.post('/budget', data=json.dumps(title), content_type ='application/json')
        actual_data = json.loads(route.get_data(as_text=True))
        failure ={"data": None,"error":"title name, 'december' already exists"}
        success = {"data":{"title":'december', "budget_id":11},"error":None}

        if actual_data == failure:
            self.assertEqual(actual_data, failure)
        elif actual_data['data'] == success['data']:
            self.assertEqual(actual_data['data'],success['data'])
        else:
            self.assertEqual(actual_data['data'],success['data'])
            


    def test_put_to_budget(self):
        title= {'budget_title':'oldmonth'}
        route = self.app.put('/budget/13', data=json.dumps(title), content_type ='application/json')
        actual_data = json.loads(route.get_data(as_text=True))
        failure ={"data": None,"error":"title name, 'oldmonth' already exists"}
        success = {"data":{"budget_title":'oldmonth', "budget_id":13},"error":None}

        if actual_data == failure:
            self.assertEqual(actual_data, failure)
        elif actual_data['data'] == success['data']:
            self.assertEqual(actual_data['data'],success['data'])
            print "here"
        else:
            self.assertEqual(actual_data['data'],success['data'])
            

            


        
        

    

    
            



if __name__ =='__main__':
    unittest.main()
