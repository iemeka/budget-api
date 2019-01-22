from flask import Flask, request, jsonify
from db_helper.query_runner import * 

def budget_routes(app):
    #create a budget
    @app.route('/budget', methods=['POST'])
    def add_budget():
        title = request.json['budget_title']

        @collecting_titles
        def get_all_titles():
            query = """
            SELECT budget_title FROM budget;
            """
            return query
        all_titles = get_all_titles()

         #check if title exists
        response = None
        if title in all_titles:
            failure ={
                "data": None,
                "error":"title name, '%s' already exists" % title
            }
            response = jsonify(failure)
        else:
            @insert_budget_query(title)
            def add_budget_to_db():
                query = "INSERT INTO budget (budget_title) VALUES(%s) RETURNING budget_id"
                return query

            get_Id = add_budget_to_db()
            def success():
                result ={
                    "data":{
                    "title":title,
                    "budget_id":get_Id
                    },
                    "error":None
                }
                return result
            response = jsonify(success())
        return response

    #get all budgets
    @app.route('/budget', methods=['GET'])
    def get_budgets():
        
        @query_data_without_arg
        def allBudgets():
            query = """
            SELECT * FROM budget;
            """
            return query
        return jsonify(allBudgets())

    #get single budget
    @app.route('/budget/<id>', methods=['GET'])
    def get_budget(id):
        
        @query_single_data_without_arg
        def oneBudget():
            query = """
            SELECT * FROM budget WHERE budget_id = %s;
            """ % id
            return query
        return jsonify(oneBudget())

    #update a budget
    @app.route('/budget/<id>', methods=['PUT'])
    def update_budget(id):
        title = request.json['budget_title']

        @collecting_titles
        def get_all_titles():
            query = """
            SELECT budget_title FROM budget;
            """
            return query
        all_titles = get_all_titles()

         #check if title exists
        response = None
        if title in all_titles:
            failure ={
                "data": None,
                "error":"title name, '%s' already exists" % title
            }
            response = jsonify(failure)
        else:
            @update_query(title,id)
            def write_update():
                query = """
                UPDATE budget SET budget_title = %s
                WHERE budget_id = %s
                """
                return query
            write_update()

            @query_single_data_without_arg
            def oneBudget():
                query = """
                SELECT * FROM budget WHERE budget_id = %s;
                """ % id
                return query
            response = jsonify(oneBudget())
        return response

    #DELETE single budget
    @app.route('/budget/<id>', methods=['DELETE'])
    def delete_budget(id):
        
        @query_single_data_without_arg
        def check_deleted():
            query = """
            SELECT * FROM budget WHERE budget_id = %s;
            """ % id
            return query
        
        deleted_row = check_deleted()

        @query_delete_with_arg(id)
        def deleteBudget():
            query = """
            DELETE FROM budget WHERE budget_id = %s;
            """
            return query
        deleteBudget()
        return jsonify(deleted_row)

    # get all budget and total cost
    @app.route('/budgets/costs', methods=['GET'])
    def get_budget_cost():

        @get_budget_cost_query_decorator
        def get_budget_cost_query():
            query = """
            SELECT bud.budget_title, sum(exp.expense_cost), bud.budget_id
            FROM budget AS bud INNER JOIN expenses AS exp 
            ON bud.budget_id = exp.budget_id 
            GROUP BY bud.budget_title,bud.budget_id 
            ORDER BY sum(exp.expense_cost);
            """
            return query

        return jsonify(get_budget_cost_query())




