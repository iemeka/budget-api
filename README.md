# Budget Planning api 
Budget Planning API is an itemized summary of expenses to be incurred in a budget.

## Built With :
- Frame-work - Flask
- Database - Postgresql
- Database API and Postgresql Database Adapter - Psycopg2
- Json Web Token - PyJWT

## Table Of Content 
___
1. Authentication
2. Secure-API routes
4. Expenses routes
5. Budget routes

##  Authentication
___ 
User authentication is done using Json Web Token. Each route is decorated with a function which checks the validity of the generated token (this happens before any response from the route is returned) then returns the user object (i.e information of the current logged in or signed up user) on successful validation. Hence each route protected with the token takes a first parameter - `current_user`, this is passed to the route on successful token validation.
Headers    | Details 
------------------- | :-------------
Title | Token authentication
Decorator | ```@token_required```
Returned Parameter | ```current_user```
Success Response | ```{```<br/>```data:{```<br/>```'name':'loggedInUserName'```,<br/>```'user_id':'loggedInUserId'```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'no token found'}```
Error Response |  ```{'data':None,'error':'Token is invalid'}```

### Sample Call 
```python 
@token_required 
def route(current_user): 
    return current_user 
route()
```

## Secure-API Routes
---
The secure routes includes the signup and login routes. These routes are the only routes which does not need authentication but rather creates authentication token either on successful signup or login.

### Signup
Headers    | Details 
------------------- | :-------------
Title       | Sign up
URL         | `/signup`
Method | POST
URL Params | None
Data Params | ```new_user:{```<br/>```'username':'new_username'```,<br/>```'password':'password'```<br/>```}```
Success Response | ```{```<br/>```data:{```<br/>```'username':'user_name'```,<br/>```'user_id':'user_id',```<br/>```'token':token```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'username or password not found'}```
Error Response |  ```{'data':None,'error':'invalid username or password'}```
Error Response | `{'data':None,'error':'username "name" exits'}`
Notes | On successful validation of the data parameters, this route redirect to a new route (`/userobj/name/password`) where these data parameters are sent as url parameter. The redirected route further validates these parameters, add these parameters to the database returning an id which is used for create a token.

### Login

Headers    | Details 
------------------- | :-------------
Title       | Login
URL         | `/login`
Method | POST
URL Params | None
Data Params | ```old_user:{```<br/>```'username':'old_username'```,<br/>```'password':'password'```<br/>```}```
Success Response | ```{```<br/>```data:{```<br/>```'username':'user_name'```,<br/>```'user_id':'user_id',```<br/>```'token':token```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'invalid username or password'}```

The url to get the details of the current logged in or signed up user - `/user`

##  Expenses Routes
---


autentication - (probably no tables) just describe how it works when you get authenticated - on login and signup and what happens after geting authenticated, arguement - logged in or signed up user  it takes and what parameter  - user object (current logged in or signed up user) is returns to every route it was decorated with
decohrator that retruns the ruser object
login and signup - only route to create a token
##use table for all routes
content-title
routes-title
routes name
routes description- listle discripint of routes before table
table for more analysis

secure routes - signup and login
 - signup
    -user object
 - login
- post routes, use tables(pyload ..etc just normal)* 
- only routes that dont need authentication but where token are created
- 
... tables for budget,expenses, secure routes url
... secure-routes --- tables of all routes

additional info
authors ---
