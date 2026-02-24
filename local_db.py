import sqlite3
# cursor.execute("CREATE TABLE Users(NAME TEXT, POINTS INTEGER)")  

class LocalDB:
    def __init__(self):
        conn = sqlite3.connect('local_users.db') 
        conn.cursor()
            
    def create_user(self, name):
        
        conn = sqlite3.connect('local_users.db') 
        cursor = conn.cursor()
        res = self.get_user(name)
        
        if res is not None:
            return 409
        
        try:
            cursor.execute('''INSERT INTO Users VALUES(?, ?)''', (name, 0,))
            print("User added to db:", name)
            conn.commit()
            
            return name
            
        finally:
            cursor.close()
            conn.close()

    
    def get_user(self, name):
        conn = sqlite3.connect('local_users.db') 
        cursor = conn.cursor()
        
        try:
            cursor.execute('''SELECT NAME FROM Users WHERE NAME = ?''', (name,))
            res = cursor.fetchone()
            
            if res is not None:
                return res[0]
            return None
        
        finally:
            cursor.close()
            conn.close()

            
    def get_points(self, name):
        conn = sqlite3.connect('local_users.db') 
        cursor = conn.cursor()
        
        try:
            cursor.execute('''SELECT POINTS FROM Users WHERE NAME = ?''', (name,))
            res = cursor.fetchone()
            
            if res is not None:
                return res[0]
            return None
            
        finally:
            cursor.close()
            conn.close()


    def update_points(self, name, points):
        conn = sqlite3.connect('local_users.db') 
        cursor = conn.cursor()
        res = self.get_points(name)
        
        if res is None:
            return 404
        
        try:
            cursor.execute('''UPDATE Users SET POINTS = ?''', (points + res,))
            conn.commit()
            
            return self.get_points(name)
        finally:
            cursor.close()
            conn.close()

    
    def delete_user(self, name):
        conn = sqlite3.connect('local_users.db') 
        cursor = conn.cursor()
        res = self.get_user(name)
        
        if res is None:
            return 404
        
        try:
            cursor.execute('''DELETE FROM Users WHERE NAME = ?''', (name,))
            print("User deleted from db: ", name)
            conn.commit()
            
        finally:
            cursor.close()
            conn.close()
