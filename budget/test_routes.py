from app import *
import json
import unittest
import unittest.runner
import itertools
from scripts.db_setup import make_tables, drop_tables


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

#----------------------main test!-------------------------------------------

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
            

    
def get_tests():
    test_funcs = ['test_for_a_singel_budget','test_get_all_budget','test_delete_from_budget', 'test_post_to_budget', 'test_put_to_budget']
    return [my_budget_route_test(func) for func in test_funcs]


if __name__ == '__main__':
    test_suite = unittest.TestSuite()

    repetitions = 1
    tests = get_tests()
    for __ in xrange(0, repetitions):
        test_suite.addTests(tests)

    CustomTextTestRunner(verbosity=2).run(test_suite)