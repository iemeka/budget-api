from app import *
import json
import unittest
import unittest.runner
import itertools
from scripts.db_setup import create_tables, drop_tables, add_fixtures


#-------------------result manager~~~~~~~~~~~~~~~~~~~~~~~~~
class CustomTextTestResult(unittest.runner.TextTestResult):
    """Extension of TextTestResult to support numbering test cases"""

    def __init__(self, stream, descriptions, verbosity):
        """Initializes the test number generator, then calls super impl"""

        self.test_numbers = itertools.count(1)

        return super(CustomTextTestResult, self).__init__(stream, descriptions, verbosity)

    def startTest(self, test):
        """Writes the test number to the stream if showAll is set, then calls super impl"""

        if self.showAll:
            progress = '[{0}/{1}] '.format(next(self.test_numbers), self.test_case_count)
            self.stream.write(progress)

            # Also store the progress in the test itself, so that if it errors,
            # it can be written to the exception information by our overridden
            # _exec_info_to_string method:
            test.progress_index = progress

        return super(CustomTextTestResult, self).startTest(test)

    def _exc_info_to_string(self, err, test):
        """Gets an exception info string from super, and prepends 'Test Number' line"""

        info = super(CustomTextTestResult, self)._exc_info_to_string(err, test)

        if self.showAll:
            info = 'Test number: {index}\n{info}'.format(
                index=test.progress_index,
                info=info
            )

        return info


class CustomTextTestRunner(unittest.runner.TextTestRunner):
    """Extension of TextTestRunner to support numbering test cases"""

    resultclass = CustomTextTestResult

    def run(self, test):
        """Stores the total count of test cases, then calls super impl"""

        self.test_case_count = test.countTestCases()
        return super(CustomTextTestRunner, self).run(test)

    def _makeResult(self):
        """Creates and returns a result instance that knows the count of test cases"""

        result = super(CustomTextTestRunner, self)._makeResult()
        result.test_case_count = self.test_case_count
        return result


#____________________main test____________________

class my_expense_routes_test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        create_tables()
        self.signup_setup()
        self.login_setup()
        add_fixtures()
    
    def tearDown(self):
        drop_tables()

    def signup_setup(self):
        fixture = ['baba','mama','papa']
        for item in fixture:
            cred = {'username':item,'password':item}
            name = cred["username"]
            password = cred["password"]
            route_login = self.app.get('/userobj/%s/%s' % (name,password))
            data = json.loads(route_login.get_data(as_text=True))

    def login_setup(self):
        cred = {'username':'baba','password':'baba'}
        route_login = self.app.post('/login', data=json.dumps(cred), content_type ='application/json')
        data = json.loads(route_login.get_data(as_text=True))

    def test_for_all_expense_in_a_budget(self):
        route = self.app.get('/expenses/1')
        data = json.loads(route.get_data(as_text=True))
        self.assertEqual(data['data']['january'][0]['budget_id'], 1)

    def test_delete_an_expense(self):
        # """ delete expenses with id 2 get the remaining expenses under the 
        # budget and check if expenses still exist by checking for its id
        # fixtures - expenses - id 2 (should be under be under budget with id 2)
        #            budget - id 2
        # """

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
        # """ add new expenses with id 3 under budget id 3

        #     fixture - expenses - id 3 (should be under budget id 3)
        #               budget - id 3
        # """
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
        # """
        # edit expense title and cost of expense in 3 under budget id 3
        # fixture - expense and budget with same id
        # """
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

        

def get_tests():
    test_funcs = ['test_for_all_expense_in_a_budget','test_delete_an_expense', 'test_post_to_expense', 'test_put_to_expense']
    return [my_expense_routes_test(func) for func in test_funcs]


if __name__ == '__main__':
    test_suite = unittest.TestSuite()

    repetitions = 1
    tests = get_tests()
    for __ in xrange(0, repetitions):
        test_suite.addTests(tests)

    CustomTextTestRunner(verbosity=2).run(test_suite)