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
4. Budget routes
5. Expense routes


##  Authentication
___ 
User authentication is done using Json Web Token. Each route is decorated with a function which checks the validity of the generated token (this happens before any response from the route is returned) then returns the user object (i.e information of the current logged in or signed up user) on successful validation. Hence each route protected with the token takes a first parameter - `current_user`, this is passed to the route on successful token validation.
Headers    | Details 
------------------- | -------------
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
Success Response | ```{```<br/>```data:{```<br/>```'username':'user_name'```,<br/>```'user_id':'user_id',```<br/>```'token':[alphanumeric]```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'invalid username or password'}```

The url to get the details of the current logged in or signed up user - `/user`

##  Budget Routes
---
These routes includes routes to create, edit, deletes, veiw (both single and all) budgets.
### Add New Budget

Headers    | Details 
------------------- | :-------------
Title       | Create a new budget
URL         | `/budget`
Method | POST
URL Params | None
Data Params | ```{'budget_title':[string]}```
Success Response | ```{```<br/>```data:{```<br/>```'budget_title':[string]```,<br/>```'budget_id':[integer],```<br/>```'user_id':[integer]```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'title name, "budget_title" already exists'}```
Notes       | Two or more users can have budget of same title but a user can't have two                 or more budget of same title

### Update Budget

Headers    | Details 
------------------- | :-------------
Title       | Edit budget title
URL         | `/budget/budget_id`
Method | PUT
URL Params | `budget_id=[integer]`
Data Params | ```{'budget_title':[string]}```
Success Response | ```{```<br/>```data:{```<br/>```'budget_title':[string]```,<br/>```'budget_id':[integer],```<br/>```'user_id':[integer]```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'title name, "budget_title" already exists'}```

### Read All Budget
Headers    | Details 
------------------- | :-------------
Title       | View all budget
URL         | `/budget`
Method | GET
URL Params | `None`
Data Params | `None`
Success Response | ```{```<br/>```data:[{```<br/>```'budget_title':[string]```,<br/>```'budget_id':[integer],```<br/>```'user_id':[integer]```<br/>```},{```<br/>```'budget_title':[string]```,<br/>```'budget_id':[integer],```<br/>```'user_id':[integer]```<br/>```} ...],```<br/>```'error':None```<br/>```}```
Error Response |  `{'data':None,'error':'no budget exist'}`

### Read A Single Budget
Headers    | Details 
------------------- | :-------------
Title       | View all budget
URL         | `/budget/budget_id`
Method | GET
URL Params | `budget_id=[integer]`
Data Params | `None`
Success Response | ```{```<br/>```data:{```<br/>```'budget_title':[string]```,<br/>```'budget_id':[integer],```<br/>```'user_id':[integer]```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  `{'data':None,'error':'budget do not exist'}`


### Delete A Budget
Headers    | Details 
------------------- | :-------------
Title       | View all budget
URL         | `/budget/budget_id`
Method | DELETE
URL Params | `budget_id=[integer]`
Data Params | `None`
Success Response | ```{```<br/>```data:{```<br/>```'budget_title':[string]```,<br/>```'budget_id':[integer],```<br/>```'user_id':[integer]```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  `{'data':None,'error':'budget do not exist'}`

Token validation is done on each route to confirm the user and before the route returns any response.

## Expense routes
---
These routes includes routes to create, edit, deletes, veiw (both single and all) expenses contained in a budget.

### Add Expenses To Budget

Headers    | Details 
------------------- | :-------------
Title       | Create expenses
URL         | `/expenses/budget_id`
Method | POST
URL Params | `budget_id=[integer]`
Data Params | `{'exp_title':[string],'exp_cost':[integer]}`
Success Response | ```{```<br/>```data:{```<br/>```'budget_title':[string]```,<br/>```'budget_id':[integer],```<br/>```'expense_id':[integer],```<br/>```'expense_title':[string],```<br/>```'expense_cost':[integer]```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'title name, "expense_title" already exists'}```
Notes       | Two or more users can have expenses of same title but a user can't have two  or more expenses of same title

### Update Expenses In A Budget

Headers    | Details 
------------------- | :-------------
Title       | Edit expense title
URL         | `/expenses/budget_id/expense_id`
Method | PUT
URL Params | `budget_id=[integer]`<br/> `expense_id=[integer]`
Data Params | ```{'expense_title':[string],'expense_cost':[integer]}```
Success Response | ```{```<br/>```data:{```<br/>```'budget_id':[integer],```<br/>```'expense_id':[integer],```<br/>```'expense_title':[string],```<br/>```'expense_cost':[integer]```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'title name, "expense_title" already exists'}```

### Read Expenses In A Budget

Headers    | Details 
------------------- | :-------------
Title       | View all expenses in a budget
URL         | `/expenses/budget_id`
Method | GET
URL Params | `budget_id=[integer]`
Data Params | `None`
Success Response | ```{```<br/> ```"data": { ```<br/>```"budget_title'": [```<br/>```{```<br/>```'budget_id':[integer],```<br/>```'expense_id':[integer],```<br/>```'expense_title':[string],```<br/>```'expense_cost':[integer]```<br/>```},``` ```{```<br/>```'budget_id':[integer],```<br/>```'expense_id':[integer],```<br/>```'expense_title':[string],```<br/>```'expense_cost':[integer]```<br/>```}, ...```<br/> <br/>```],``` <br/>```"error": null }```
Error Response |  ```{'data':None,'error':'no expenses exist against this budget'}```


### Delete Expense In A Budget

Headers    | Details 
------------------- | :-------------
Title       | Delete an expense in a budget
URL         | `/expenses/expense_id`
Method | DELETE
URL Params | `expense_id=[integer]`
Data Params | `None`
Success Response |```{```<br/>```data:{```<br/>```'budget_id':[integer],```<br/>```'expense_id':[integer],```<br/>```'expense_title':[string],```<br/>```'expense_cost':[integer]```<br/>```},```<br/>```'error':None```<br/>```}```
Error Response |  ```{'data':None,'error':'expenses does not exist'}```



additional info
authors ---
