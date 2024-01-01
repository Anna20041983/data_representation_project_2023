import mysql.connector
import dbconfig as cfg
class DisabilityDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
         
    def create(self, values):
        cursor = self.getcursor()
        sql="insert into disability (year, age_group, county, sex, sev_of_disability, no_of_children) values (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid
    
    def getAll(self):
        cursor = self.getcursor()
        sql="select * from disability"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByYear(self, year):
        cursor = self.getcursor()
        sql="select * from disability where year = %s"
        values = (year,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        sql="update disability set age_group= %s, county=%s, sex=%s, sev_of_disability=%s, no_of_children=%s  where year = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def delete(self, year):
        cursor = self.getcursor()
        sql="delete from disability where year = %s"
        values = (year,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        print("delete done")
    
    def convertToDictionary(self, result):
        colnames=['year', 'age_group', 'county', 'sex', 'sev_of_disability', 'no_of_children']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
disabilityDAO = DisabilityDAO()