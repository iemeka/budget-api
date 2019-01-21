from flask import Flask, request
from budget.routes import budget_routes
from expense.routes import expense_routes

app = Flask(__name__)

budget_routes(app)
expense_routes(app)

if __name__ == '__main__':
    app.run(debug=True)