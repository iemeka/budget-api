from flask import Flask, request, jsonify
from db_helper.query_runner import * 
from secure.routes import token_required

def expense_routes(app):

    # add expenses
    @app.route('/expenses/<budget_id>', methods=['POST'])
    @token_required
    def add_expenses(current_user,budget_id):
        exp_title = request.json['exp_title']
        exp_cost = request.json['exp_cost']

        @collecting_titles
        def get_all_titles():
            query = """
            SELECT expense_title FROM expenses WHERE budget_id = %s
            """ % budget_id
            return query
        all_titles = get_all_titles()

        response = None
        # python 'or' not functionning accordingly
        if exp_title in all_titles:
            failure ={"data":None,
                "error":"title name, '%s' already exists" % exp_title
            }
            response = jsonify(failure)
        elif exp_title == "":
            failure ={"data":None,
                "error":"pls type in an expense title and expense cost"
            }
            response = jsonify(failure)
        elif exp_cost == "":
            failure ={"data":None,
                "error":"pls type in an expense title and expense cost"
            }
            response = jsonify(failure)
        elif exp_cost.isdigit() == False:
            failure ={"data":None,
                "error":"invalid value for cost"
            }
            response = jsonify(failure)
        else:
            #insert expense to db
            @insert_expense_query
            def add_expenses_to_db():
                query = """INSERT INTO expenses(budget_id,expense_title,expense_cost) 
                VALUES(%s,'%s',%s) RETURNING expense_id;""" % (budget_id,exp_title, exp_cost)
                return query
            add_expenses_to_db()

            @get_budget_title_or_expense_id
            def get_title():
                query = """
                SELECT budget_title FROM budget 
                WHERE budget_id = %s
                """ % budget_id
                return query
            budget_title = get_title()

            @get_budget_title_or_expense_id
            @token_required
            def get_id(current_user):
                #since max expense_id is the newest of expenses with same budget_id
                query = """
                SELECT max(expense_id) FROM expenses 
                WHERE budget_id = %s
                """ % budget_id
                return query
            expense_id = get_id()
           
            def success():
                result = {
                    "data":{
                        'budget_title':get_title(),
                        'expense_id':expense_id,
                        'expense_title':exp_title,
                        'expense_cost':exp_cost,
                        'budget_id':budget_id
                    },
                    "error":None
                }
                return result
            response = jsonify(success())
        return response

    #get all expenses in a budget 
    @app.route('/expenses/<budget_id>', methods=['GET'])
    @token_required
    def get_expenses(current_user, budget_id):
        @get_budget_title_or_expense_id
        def get_title():
            query = """
            SELECT budget_title FROM budget 
            WHERE budget_id = %s
            """ % budget_id
            return query
        title = get_title()

        @all_expenses_in_a_budget(title)
        def all_expenses():
            query = """
            SELECT * FROM expenses WHERE budget_id = %s ORDER BY expense_id ASC
            """ % budget_id
            return query
        data = all_expenses()
        if not data:
            return jsonify({'data':None,'error':'no expenses exist against this budget'})
        return jsonify(all_expenses())

    # get a single expenses
    @app.route('/expense/<expense_id>', methods=['GET'])
    @token_required
    def get_one_expense(current_user,expense_id):

        @query_single_data_expense
        def one_expense_query():
            query = """
            SELECT * FROM expenses WHERE expense_id = %s
            """ % expense_id
            return query

        one_expense = one_expense_query()
        print one_expense

        if not one_expense:
            return jsonify({'data':None,'error':'expense does not exist'})
        return jsonify(one_expense)

    
    # delete expense
    @app.route('/expenses/<expense_id>', methods=['DELETE'])
    @token_required
    def delete_expense(current_user,expense_id):

        @get_updated_and_deleted_expense
        def deleted_expense_query():
            query = """
            SELECT * FROM expenses WHERE expense_id = %s
            """ % expense_id
            return query

        deleted_row = deleted_expense_query()

        @query_delete_with_arg(expense_id)
        def delete():
            query = """
            DELETE FROM expenses WHERE expense_id = %s
            """
            return query
        delete()
        if not deleted_row:
            return jsonify({'data':None,'error':'expense does not exist'})
        return jsonify(deleted_row)

    # update expenses (title)
    @app.route('/expenses/title/<budget_id>/<expense_id>', methods=['PUT'])
    @token_required
    def update_expense_title(current_user,budget_id,expense_id):
        title = request.json['expense_title']

        @collecting_titles
        def get_all_titles():
            query = """
            SELECT expense_title FROM expenses WHERE budget_id = %s
            """ % budget_id
            return query
        all_titles = get_all_titles()

        response = None
        if title == "":
            failure ={"data":None,
                "error":"pls type in a title name"
            }
            response = jsonify(failure)
        elif title in all_titles :
            failure ={"data":None,
                "error":"title name, '%s' already exists" % title
            }
            response = jsonify(failure)
        else:
            @update_expense_decorator
            def update_expense_query():
                query = """
                UPDATE expenses SET expense_title = '%s'
                WHERE expense_id = %s
                """ % (title,expense_id)
                return query
            update_expense_query()

            @get_updated_and_deleted_expense
            def up_to_date_expense_query():
                query = """
                SELECT * FROM expenses WHERE expense_id = %s
                """ % expense_id
                return query
            response = jsonify(up_to_date_expense_query())
        return response

    # update expenses (cost)
    @app.route('/expenses/cost/<budget_id>/<expense_id>', methods=['PUT'])
    @token_required
    def update_expense_cost(current_user,budget_id,expense_id):
        cost = request.json['expense_cost']

        @collecting_titles
        def get_all_titles():
            query = """
            SELECT expense_title FROM expenses WHERE budget_id = %s
            """ % budget_id
            return query
        all_titles = get_all_titles()

        response = None
        if cost == "":
            failure ={"data":None,
                "error":"pls type in the appropriate value"
            }
            response = jsonify(failure)
        elif type(cost) != int:
            failure ={"data":None,
                "error":"pls type a number pleease! (a whole number)"
            }
            response = jsonify(failure)
        else:
            @update_expense_decorator
            def update_expense_query():
                query = """
                UPDATE expenses SET
                expense_cost = %s
                WHERE expense_id = %s
                """ % (cost,expense_id)
                return query
            update_expense_query()

            @get_updated_and_deleted_expense
            def up_to_date_expense_query():
                query = """
                SELECT * FROM expenses WHERE expense_id = %s
                """ % expense_id
                return query
            response = jsonify(up_to_date_expense_query())
        return response

    # update expenses and cost - Not used, separated above
    @app.route('/expenses/<budget_id>/<expense_id>', methods=['PUT'])
    @token_required
    def update_expense(current_user,budget_id,expense_id):
        title = request.json['expense_title']
        cost = request.json['expense_cost']

        @collecting_titles
        def get_all_titles():
            query = """
            SELECT expense_title FROM expenses WHERE budget_id = %s
            """ % budget_id
            return query
        all_titles = get_all_titles()

        response = None
        if title in all_titles:
            failure ={"data":None,
                "error":"title name, '%s' already exists" % title
            }
            response = jsonify(failure)
        else:
            @update_expense_decorator
            def update_expense_query():
                query = """
                UPDATE expenses SET expense_title = '%s',
                expense_cost = %s
                WHERE expense_id = %s
                """ % (title,cost,expense_id)
                return query
            update_expense_query()

            @get_updated_and_deleted_expense
            def up_to_date_expense_query():
                query = """
                SELECT * FROM expenses WHERE expense_id = %s
                """ % expense_id
                return query
            response = jsonify(up_to_date_expense_query())
        return response
        