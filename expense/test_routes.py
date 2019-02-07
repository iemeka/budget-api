
from app import *
import json
import unittest
from scripts.db_setup import make_tables, drop_tables


class my_expense_routes_test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        make_tables()
    
    def tearDown(self):
        drop_tables()

    def test_for_all_expense_in_a_budget(self):
        """ get all expenses under budget ( id 1)
        make sure that the budget id of each expense has a relationship with
        (or is same with) budget id of budget

        fixture - expenses - of id 1 under
                  budget id of one with title january
        """

        route = self.app.get('/expenses/1')
        data = json.loads(route.get_data(as_text=True))
        self.assertEqual(data['data']['january'][0]['budget_id'], 1)

    def test_delete_an_expense(self):
        """ delete expenses with id 2 get the remaining expenses under the 
        budget and check if expenses still exist by checking for its id
        fixtures - expenses - id 2 (should be under be under budget with id 2)
                   budget - id 2
        """

        self.app.delete('/expenses/2')
      
        # get the remaining list expenses under same budget
        route = self.app.get('/expenses/2')
        data = json.loads(route.get_data(as_text=True))
        list_of_dict = data['data']['febuary']
        
        # loop through the expesen_id values in the list of dictionaries
        # check if the deleted expense still exist by comparing its id with the list
        # of expenses_id still remaining in the database since the id is a primary key
        # the should be no equals it there are then nothing was deleted
        for dict in list_of_dict:
            self.assertNotEqual(dict.get("expense_id"), 2)

    def test_post_to_expense(self):
        """ add new expenses with id 3 under budget id 3

            fixture - expenses - id 3 (should be under budget id 3)
                      budget - id 3
        """
        expense = {'exp_title':'third','exp_cost':'30000'}
        post_route = self.app.post('/expenses/3', data=json.dumps(expense), content_type='application/json')
        post_returns = json.loads(post_route.get_data(as_text=True))
        expected_fail = {'data': None, 'error': "title name, 'third' already exists"}
        expected_pass = {'data': {'budget_title': 'march', 'expense_cost': '30000', 'expense_title': 'third', 'budget_id': '3', 'expense_id': 3}, 'error': None}
        
        if post_returns == expected_pass:
            self.assertEqual(post_returns, expected_pass)
        elif post_returns == expected_fail:
            self.assertEqual(post_returns, expected_fail)
        else:
            self.assertEqual(post_returns, expected_pass)
            self.assertEqual(post_returns, expected_fail)

    def test_put_to_expense(self):
        """
        edit expense title and cost of expense in 3 under budget id 3
        fixture - expense and budget with same id
        """
        expense = {'expense_title':'new','expense_cost':'45000'}
        route = self.app.put('/expenses/1/1', data=json.dumps(expense), content_type='application/json')
        post_returns = json.loads(route.get_data(as_text=True))
        expected_fail = {'data': None, 'error': "title name, 'new' already exists"}
        expected_pass = {'data': {'expense_cost': 45000, 'expense_title': 'new', 'budget_id': 1, 'expense_id': 1}}
        if post_returns == expected_pass:
            self.assertEqual(post_returns, expected_pass)
        elif post_returns == expected_fail:
            self.assertEqual(post_returns, expected_fail)
        else:
            self.assertEqual(post_returns, expected_pass)
            self.assertEqual(post_returns, expected_fail)

        

if __name__ =='__main__':
    unittest.main()
