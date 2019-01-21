from flask import Flask, request, jsonify
from db_helper.query_runner import * 

def budget_routes(app):
    #create a budget
    @app.route('/budget', methods=['POST'])
    def add_budget():
        title = request.json['budget_title']

        @insert_budget_query(title)
        def add_budget_to_db():
            query = "INSERT INTO budget (budget_title) VALUES(%s) RETURNING budget_id"
            return query
        get_Id = add_budget_to_db()

        def serialize(title,budget_id):
            return jsonify({
                'title':title,
                'budget_id':budget_id
            })

        return serialize(title, get_Id)

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
        
        @query_data_without_arg
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

        @update_query(title,id)
        def write_update():
            query = """
            UPDATE budget SET budget_title = %s
            WHERE budget_id = %s
            """
            return query
        write_update()

        @query_data_without_arg
        def oneBudget():
            query = """
            SELECT * FROM budget WHERE budget_id = %s;
            """ % id
            return query
        return jsonify(oneBudget())

    #DELETE single budget
    @app.route('/budget/<id>', methods=['DELETE'])
    def delete_budget(id):
        
        @query_data_without_arg
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





