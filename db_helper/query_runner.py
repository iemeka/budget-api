import psycopg2
from config import config
import functools


#insert into budget database decorator functions
def insert_budget_query(title):
    def insert_query_decorator(query):
        @functools.wraps(query)
        def connect_run_close():
            conn = None
            budget_id = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(query(), [title])
                budget_id = cur.fetchone()[0]
                conn.commit()
                print "%s.. \n%s" % (cur.query, cur.statusmessage)
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print error
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection ended.')
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
                budget_list.append(db)        
            
           
            print "%s.. \n%s" % (cur.query, cur.statusmessage)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
                print('Database connection ended.')
        return budget_list
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
                print "%s.. \n%s" % (cur.query, cur.statusmessage)
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print error
            finally:
                if conn is not None:
                    conn.close()
                    return 'Database connection ended.'
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
                print "%s.. \n%s" % (cur.query, cur.statusmessage)
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print error
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection ended.')
        return connect_run_close
    return delete_query_decorator

    
    

