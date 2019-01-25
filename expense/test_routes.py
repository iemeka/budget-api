
from app import *
import json
import unittest


class my_expense_routes_test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_for_all_expense_in_a_budget(self):
        route = self.app.get('/expenses/1')
        data = json.loads(route.get_data(as_text=True))
        self.assertEqual(data['data']['january'][0]['budget_id'], 1)

    def test_delete_an_expense(self):
        #delete expense
        self.app.delete('/expenses/12')
      
        # get the remaining list expenses under same budget
        route = self.app.get('/expenses/2')
        data = json.loads(route.get_data(as_text=True))
        list_of_dict = data['data']['febuary']
        
        # loop through the expesen_id values in the list of dictionaries
        # check if the deleted expense still exist by comparing its id with the list
        # of expenses_id still remaining in the database since the id is a primary key
        # the should be no equals it there are then nothing was deleted
        for dict in list_of_dict:
            self.assertNotEqual(dict.get("expense_id"), 12)

    def test_post_to_expense(self):
        expense = {'exp_title':'dirt','exp_cost':'4000'}
        post_route = self.app.post('/expenses/11', data=json.dumps(expense), content_type='application/json')
        post_returns = json.loads(post_route.get_data(as_text=True))
        expected_fail = {'data': None, 'error': "title name, 'dirt' already exists"}
        expected_pass = {'data': {'budget_title': 'september', 'expense_cost': '4000', 'expense_title': 'dirt', 'budget_id': '10', 'expense_id': 50}, 'error': None}
        
        if post_returns == expected_pass:
            print "new"
            self.assertEqual(post_returns, expected_pass)
        elif post_returns == expected_fail:
            print "same"
            self.assertEqual(post_returns, expected_fail)
        else:
            self.assertEqual(post_returns, expected_pass)
            self.assertEqual(post_returns, expected_fail)

    def test_put_to_expense(self):
        expense = {'expense_title':'new','expense_cost':'4000'}
        route = self.app.put('/expenses/5/23', data=json.dumps(expense), content_type='application/json')
        post_returns = json.loads(route.get_data(as_text=True))
        expected_fail = {'data': None, 'error': "title name, 'new' already exists"}
        expected_pass = {'data': {'expense_cost': 4000, 'expense_title': 'new', 'budget_id': 5, 'expense_id': 23}}
        if post_returns == expected_pass:
            print "new"
            self.assertEqual(post_returns, expected_pass)
        elif post_returns == expected_fail:
            print "same"
            self.assertEqual(post_returns, expected_fail)
        else:
            self.assertEqual(post_returns, expected_pass)
            self.assertEqual(post_returns, expected_fail)

        


if __name__ =='__main__':
    unittest.main()
