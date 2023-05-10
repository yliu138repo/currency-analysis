#!/usr/bin/python
import psycopg2

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
                self.disconnect()
                raise Exception(f"DB connection error: {error}")
            
    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')