import psycopg2
from config import config
import functools


#insert into budget database decorator functions
def insert_budget_query(title,cuid):
    def insert_query_decorator(query):
        @functools.wraps(query)
        def connect_run_close():
            conn = None
            budget_id = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(query(), (title,cuid))
                budget_id = cur.fetchone()[0]
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print error
            finally:
                if conn is not None:
                    conn.close()
            return budget_id
        return connect_run_close
    return insert_query_decorator


#get all and single budget from database
def query_data_without_arg(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            
            results = cur.fetchall()
            budget_list=[]
            for rows in results:
                db={}
                db["budget_id"]= rows[0]
                db["budget_title"] = rows[1]
                db["user_id"] = rows[2]
                budget_list.append(db)        
            budget_dict={"data":budget_list,"error":None}
           
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return budget_dict
    return connect_run_close

#get single
def query_single_data_without_arg(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            
            results = cur.fetchone()
            db={}
            db["budget_id"]= results[0]
            db["budget_title"] = results[1]
            db["user_id"] = results[2]
            budget_dict={"data":db,"error":None}
           
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return budget_dict
    return connect_run_close

#update budget
def update_query(update_with,where_condition):
    def update_query_decorator(query):
        @functools.wraps(query)
        def connect_run_close():
            conn = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(query(), (update_with,where_condition))
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print error
            finally:
                if conn is not None:
                    conn.close()
                    return None
        return connect_run_close
    return update_query_decorator

#delete budget
def query_delete_with_arg(arg):
    def delete_query_decorator(query):
        @functools.wraps(query)
        def connect_run_close():
            conn = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(query(), (arg,))
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print error
            finally:
                if conn is not None:
                    conn.close()
        return connect_run_close
    return delete_query_decorator

#----------------------------expenses------------------------------------------------>

#insert into expenses database 
def insert_expense_query(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        budget_id = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
                
        return None
    return connect_run_close

# get_budget_title_or_expense_id
def get_budget_title_or_expense_id(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            budget_title = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return budget_title
    return connect_run_close
    
# get all expenses in a budget
def all_expenses_in_a_budget(title):
    def all_expenses_in_a_budget(query):
        @functools.wraps(query)
        def connect_run_close():
            conn = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(query())
                
                results = cur.fetchall()
                budget_list=[]
                for rows in results:
                    db={}
                    db["expense_title"] = rows[1]
                    db["budget_id"] = rows[0]
                    db["expense_cost"] = rows[2]
                    db["expense_id"]= rows[3]
                    budget_list.append(db)  
                budget_dict={title:budget_list}
                outer_budget_dict = {"data":budget_dict,"error":None}
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print error
            finally:
                if conn is not None:
                    conn.close()
            return outer_budget_dict
        return connect_run_close
    return all_expenses_in_a_budget

#get single expense
def query_single_data_expense(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            
            results = cur.fetchone()
            db={}
            db["budget_id"]= results[0]
            db["expense_title"] = results[1]
            db["expense_cost"] = results[2]
            db["expense_id"] = results[3]
            budget_dict={"data":db,"error":None}
           
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return budget_dict
    return connect_run_close

#get deleted expenses from database
def get_updated_and_deleted_expense(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            
            results = cur.fetchall()
            budget_dict = {}
            for rows in results:
                budget_dict["expense_title"] = rows[1]
                budget_dict["budget_id"] = rows[0]
                budget_dict["expense_cost"] = rows[2]
                budget_dict["expense_id"]= rows[3]
            budget_dict_outer = {"data":budget_dict}       
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return budget_dict_outer
    return connect_run_close

# update expense
def update_expense_decorator(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return None
    return connect_run_close


    #----------------------------------------

# get budget and cost
def get_budget_cost_query_decorator(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            results = cur.fetchall()
            budget_list = []
            totalCost = 0
            for rows in results:
                inner_dict = {}
                inner_dict["budget_id"] = rows[2]
                inner_dict["budget_cost"] = rows[1]
                totalCost +=rows[1]
                outer_dict = {rows[0]:inner_dict}
                budget_list.append(outer_dict)
            cost = {"total":totalCost}
            budget_list.append(cost)
            overall_dict = {"data":budget_list,"error":None}
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return overall_dict
    return connect_run_close





# collecting_titles
def collecting_titles(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())

            results = cur.fetchall()
            budget_titles = []
            for rows in results:
                budget_titles.append(rows[0])
            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return budget_titles
    return connect_run_close



#-----------------------security-------------------------------
#add user
def add_user_query(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        user_id = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return user_id
    return connect_run_close


def check_user_query(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())

            results = cur.fetchall()
            
            #print "%s.. \n%s" % (cur.query, cur.statusmessage)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection ended.')
        return results
    return connect_run_close


def get_current_user(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query())

            results = cur.fetchone()
            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
        return results
    return connect_run_close


