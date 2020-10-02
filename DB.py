#from urllib.parse import urlparse
import mysql.connector
import hashlib

#url = urlparse('mysql://user:pass@localhost:3306/dbname')

class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = 'yatsushironct',
            database = 'member_database',
        )

    def all_select(self,sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close
        return data

    def select(self, sql, data):
        cur = self.conn.cursor()
        cur.execute(sql,data)
        data = cur.fetchall()
        cur.close
        return data
        self.conn.commit()

    def insert(self,sql,data):
        cur = self.conn.cursor()
        cur.execute(sql,data)
        cur.close
        self.conn.commit()

    def insert_request(self,sql,data):
        cur = self.conn.cursor()
        cur.execute(sql,data)
        cur.close
        self.conn.commit()

    def insert_many(self, sql, data):
        cur = self.conn.cursor()
        cur.executemany(sql,data)
        cur.close
        self.conn.commit()

    def select_many(self, sql, data):
        cur = self.conn.cursor()
        cur.executemany(sql,data)
        cur.close
        self.conn.commit()


    def end_DB(self):
        self.conn.close
    

if __name__ == "__main__":
    import hashlib
    db=DB()


     #db.insert()
    #db.end_DB()
    #print('done')
     #member add
    #key = '3'
    #db.insert('INSERT INTO boarders_table (boardernumber,grade,class,password) VALUES (%s,%s,%s,%s)',(123459,1,'MI',hashlib.md5(key.encode('utf-8')).hexdigest()))
    #print(db.all_select('SELECT * FROM boarders_table'))


     


    #print(conn.is_connected())

     #cur = conn.cursor()
     #db.insert(12345,1,1,1,1,'2020-09-14')
     #db.insert(12346,1,1,1,2,'2020-09-14')
    
    #cur.execute('INSERT INTO dormitory_member_table (id ,name ,password ) VALUES (0,%s,111)',['a'])INSERT INTO dormitory_member_table (id ,name ,password ) VALUES (0,%s,111)',['a'])

    #conn.commit()

    #cur.execute('SELECT * FROM dormitory_member_table')

    #print(cur.fetchall())
