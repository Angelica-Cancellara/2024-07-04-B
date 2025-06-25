from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select year(datetime) as year
                from sighting
                group by year(`datetime`)
                order by year(`datetime`) asc """
        cursor.execute(query)
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getState(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select st.Name as name
                from sighting si, state st
                where year(si.`datetime`) = %s 
                and st.id = si.state  
                group by st.Name 
                order by st.Name asc"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row["name"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(anno, stato):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select s.*
                from sighting s, state s2 
                where year(s.`datetime`) = %s 
                and s.state = s2.id 
                and s2.Name = %s"""
        cursor.execute(query, (anno, stato))
        for row in cursor:
            result.append(Sighting(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(anno, stato, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select s1.id as id1, s2.id as id2
                from sighting s1, sighting s2, state st1, state st2
                where s1.shape = s2.shape 
                and s1.id != s2.id 
                and year(s1.datetime) = %s
                and year(s2.datetime) = %s
                and s1.state = st1.id
                and s2.state = st2.id 
                and st1.Name = %s
                and st2.Name = %s
                and s1.datetime < s2.datetime"""
        cursor.execute(query, (anno, anno, stato, stato))
        for row in cursor:
            result.append((idMap[row["id1"]], idMap[row["id2"]]))
        cursor.close()
        conn.close()
        return result
