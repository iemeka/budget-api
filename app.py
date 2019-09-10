from flask import Flask, request
from budget.routes import budget_routes
from expense.routes import expense_routes
from secure.routes import secure_routes
from flask_cors import CORS


app = Flask(__name__)

budget_routes(app)
expense_routes(app)
secure_routes(app)
CORS(app)


if __name__ == '__main__':
    app.run(debug=True)