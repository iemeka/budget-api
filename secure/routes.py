from flask import Flask, request, jsonify

def secure_routes(app):

    @app.route('/signup')
    def signup():
        pass

    @app.route('/login')
    def login():
        pass

    @app.route('/welcome')
    def welcome():
        pass