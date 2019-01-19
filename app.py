from flask import Flask, request
from budget.routes import budget_routes

app = Flask(__name__)

budget_routes(app)

if __name__ == '__main__':
    app.run(debug=True)