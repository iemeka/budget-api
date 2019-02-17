from flask import Flask, request, jsonify
from db_helper.query_runner import * 
from secure.routes import token_required

def budget_routes(app):
    
    #create a budget
    @app.route('/budget', methods=['POST'])
    @token_required
    def add_budget(current_user):
        title = request.json['budget_title']
        cuid = current_user[0]
        @collecting_titles
        def get_all_titles():
            query = """
            SELECT budget_title FROM budget WHERE user_id = %s;
            """                                      % cuid
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
            @insert_budget_query(title,cuid)
            def add_budget_to_db():
                query = "INSERT INTO budget (budget_title,user_id) VALUES(%s,%s) RETURNING budget_id"
                return query

            get_Id = add_budget_to_db()
            def success():
                result ={
                    "data":{
                    "title":title,
                    "budget_id":get_Id,
                    "user_id":cuid
                    },
                    "error":None
                }
                return result
            response = jsonify(success())
        return response

    #get all budgets
    @app.route('/budget', methods=['GET'])
    @token_required
    def get_budgets(current_user):
        
        @query_data_without_arg
        def allBudgets():
            query = """
            SELECT * FROM budget;
            """
            return query
        data = allBudgets()
        if not data:
            return jsonify({'data':None,'error':'no budget exist'})
        return jsonify(data)

    #get single budget
    @app.route('/budget/<id>', methods=['GET'])
    @token_required
    def get_budget(current_user,id):
        
        @query_single_data_without_arg
        def oneBudget():
            query = """
            SELECT * FROM budget WHERE budget_id = %s;
            """ % id
            return query
        data = oneBudget()
        if not data:
            return jsonify({'data':None,'error':'no budget exist'})
        return jsonify(data)

    #update a budget
    @app.route('/budget/<id>', methods=['PUT'])
    @token_required
    def update_budget(current_user,id):
        title = request.json['budget_title']
        cuid = current_user[0]

        @collecting_titles
        def get_all_titles():
            query = """
            SELECT budget_title FROM budget WHERE user_id = %s;
            """ % cuid
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
    @token_required
    def delete_budget(current_user, id):
        
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
        if not deleted_row:
            return jsonify({'data':None,'error':'budget do not exist'})
        return jsonify(deleted_row)

    # get all budget and total cost
    @app.route('/budgets/costs', methods=['GET'])
    @token_required
    def get_budget_cost(current_user):

        @get_budget_cost_query_decorator
        def get_budget_cost_query():
           
            query = """
            SELECT bud.budget_title, sum(exp.expense_cost), bud.budget_id
            FROM budget AS bud INNER JOIN expenses AS exp 
            ON bud.budget_id = exp.budget_id AND bud.user_id=%s
            GROUP BY bud.budget_title,bud.budget_id 
            ORDER BY sum(exp.expense_cost);
            """ % current_user[0]
            return query
        data = get_budget_cost_query()
        user_info = {}
        data['user_info'] = user_info
        user_info['name'] = current_user[1]
        user_info['id'] = current_user[0]
        

        return jsonify(data)

#