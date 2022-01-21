import sqlite3
import datetime

class Database(object):
    def __init__(self):
        self.__computer_db = "computersDB.sqlite3"
        self.assembled_computers_tb = "assembledComputersTB"
        self.products_tb = "productsTB"
        self.computer_parts_tb = "computerPartsTB"
        self.__createDB()

    def connectDB(self):
        self.conn = sqlite3.connect(self.__computer_db)
        self.cursor = self.conn.cursor()

    def closeDB(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def __createDB(self):
        self.connectDB()
        self.cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS 
            {self.assembled_computers_tb} 
            (
                ComputerID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                CurrencySymbol TEXT NOT NULL,
                PriceTotal INTEGER,
                Description TEXT,
                CreatedAt DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UpdatedAt DATE NOT NULL
            );
            ''')
        self.cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS 
            {self.products_tb} 
            (
                ProductID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                ProductType TEXT NOT NULL,
                Model TEXT NOT NULL,
                Brand TEXT NOT NULL,
                CurrencySymbol TEXT NOT NULL,
                Price INTEGER NOT NULL,
                Description TEXT,
                Link TEXT,
                CreatedAt DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UpdatedAt DATE NOT NULL
            );
            ''')
        self.cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS 
            {self.computer_parts_tb} 
            (
                ComputerID INTEGER,
                ProductID INTEGER,
                FOREIGN KEY(ComputerID) REFERENCES {self.assembled_computers_tb}(ComputerID),
                FOREIGN KEY(ProductID) REFERENCES {self.products_tb}(ProductID)  
            );
            ''')
        self.conn.commit()
        self.closeDB()

    def insert_computer(self, data: tuple):
        try:
            date_now = datetime.datetime.now().isoformat(" ")
            self.connectDB()
            self.cursor.execute(
                f'''insert into 
                {self.assembled_computers_tb} 
                (Name, CurrencySymbol, PriceTotal, Description, CreatedAt, UpdatedAt) 
                values(?,?,?,?,?,?);''',
                (data[0], data[1], data[2], data[3], date_now, date_now))
            self.conn.commit()
            print("Values added sucessfully to database.")
        except Exception as e:
            print(f"Error inserting values in database. Error: {str(e)}")
            self.conn.rollback()
        finally:
            self.closeDB()

    def insert_product(self, data: tuple):
        try:
            date_now = datetime.datetime.now().isoformat(" ")
            self.connectDB()
            self.cursor.execute(
                f'''insert into 
                {self.products_tb} 
                (ProductType, Model, Brand, CurrencySymbol, Price, Description, Link, CreatedAt, UpdatedAt) 
                values(?,?,?,?,?,?,?,?,?);''',
                (data[0], data[1], data[2], data[3], data[4], data[5], data[6], date_now, date_now))
            self.conn.commit()
            print("Values added sucessfully to database.")
        except Exception as e:
            print(f"Error inserting values in database. Error: {str(e)}")
            self.conn.rollback()
        finally:
            self.closeDB()

    def queryDB(self, table, sql):
        self.connectDB()
        # self.cursor.execute(sql)
        self.cursor.execute(
            f"""
            SELECT * FROM {table};
            """)

        for linha in cursor.fetchall():
            print(linha)
        self.closeDB()
