import mysql.connector
import dbconfig as cfg

class DataDAO:
    def __init__(self):
        self.host = cfg.mysql['host']
        self.user = cfg.mysql['user']
        self.password = cfg.mysql['password']
        self.database = cfg.mysql['database']
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor(prepared=True)

    def getcursor(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.cursor
    
    def close(self):
        if self.connection:
            self.connection.close()

    def closeAll(self):
        self.close()
        if self.cursor:
            self.cursor.close()

    def create(self, values):
        self.connect()
        sql = "INSERT INTO data (year, sex, age_group, average_height, average_weight) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, values)
        self.connection.commit()
        newid = self.cursor.lastrowid
        self.close()
        return newid

    def getAll(self):
        connection, cursor = self.getcursor()
        sql = "SELECT year, sex, age_group, average_height FROM data"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = [self.convertToDictionary(result) for result in results]
        cursor.close()
        connection.close()
        print("getAll - Return Array:", returnArray)  # Add this line
        return returnArray

    def getAllWeight(self):
        connection, cursor = self.getcursor()
        sql = "SELECT year, sex, age_group, average_weight FROM data"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = [self.convertToDictionary(result, include_weight=True) for result in results]
        cursor.close()
        connection.close()
        print("getAllWeight - Return Array:", returnArray)  # Add this line
        return returnArray

    def findByYear(self, year):
        cursor = self.getcursor()
        sql="SELECT * FROM data WHERE year = %s"
        values = (year,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        sql="UPDATE data set sex=%s, age_group= %s, average_height=%s, average_weight=%s WHERE year = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        print("update done")

    def delete(self, year):
        try:
            connection, cursor = self.getcursor()
            sql = "DELETE FROM data WHERE year = %s"
            values = (year,)
            cursor.execute(sql, values)
            connection.commit()
            print("Delete done")
            self.closeAll()
        except mysql.connector.Error as e:
            print("Error deleting data:", e)
        finally:
            self.closeAll()

    def convertToDictionary(self, result, include_weight=False):
        colnames = ['year', 'sex', 'age_group', 'average_height']
        item = {}

        if result:
            for i, colName in enumerate(colnames):
                try:
                    value = result[i]
                    item[colName] = value
                except IndexError:
                    item[colName] = None

        if include_weight and len(result) > 4:
            item['average_weight'] = result[4]
        elif include_weight:
            item['average_weight'] = None

        return item

# Create an instance of the DataDAO class
dataDAO_instance = DataDAO()
