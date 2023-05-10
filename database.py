#!/usr/bin/python
import psycopg2
from typing import Callable

class Database:
    def __init__(self, db_config) -> None:
        self.db_config = db_config
        self.conn = None
    
    def connect(self):
            """ Connect to the PostgreSQL database server """
            try:
                # connect to the PostgreSQL server
                print('Connecting to the PostgreSQL database...')
                self.conn = psycopg2.connect(**self.db_config)
                
                # create a cursor
                cur = self.conn.cursor()
                
                # execute a statement
                print('PostgreSQL database version:')
                cur.execute('SELECT version()')

                # display the PostgreSQL database server version
                db_version = cur.fetchone()
                print(db_version)
            
                # close the communication with the PostgreSQL
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                self.disconnect(cur)              
                raise Exception(f"DB connection error: {error}")

            
    def disconnect(self, cursor = None):
        if self.conn is not None:
            self.conn.close()
            if cursor is not None:
                cursor.close()
            print('Database connection closed.')
            
    def exec(self, fn: Callable):
        try:
            cursor = self.conn.cursor()
            fn(cursor)
        except (Exception, psycopg2.Error) as error :
            raise Exception(f"DB connection error: ", error)
        finally:
            cursor.close()
            
    def insert(self, sql: str, params):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            raise Exception(f"DB writing error", error)
        finally:
            cursor.close()
            
    def fetch_records(self, sql: str, params):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            raise Exception(f"DB reading error", error)
        finally:
            cursor.close()