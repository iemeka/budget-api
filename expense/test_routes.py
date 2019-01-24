
from app import *
import json
import unittest


class my_expense_routes_test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_for_all_expense_in_a_budget(self):
        route = self.app.get('/expenses/5')
        data = json.loads(route.get_data(as_text=True))
        self.assertEqual(data['data']['january'][0]['budget_id'], 5)

    def test_delete_an_expense(self):
        # delete expense
        self.app.delete('/expenses/11')
      
        #get the remaining list expenses under same budget
        route_get = self.app.get('/expenses/5')
        data_get = json.loads(route_get.get_data(as_text=True))
        list_of_dict = data_get['data']['january']
        
        #loop through the expesen_id values in the list of dictionaries
        #check if the deleted expense still exist by comparing its id with the list
        #of expenses_id still remaining in the database since the id is a primary key
        #the should be no equals it there are then nothing was deleted
        for dict in list_of_dict:
            self.assertNotEqual(dict.get("expense_id"), 11)
                
        



if __name__ =='__main__':
    unittest.main()
