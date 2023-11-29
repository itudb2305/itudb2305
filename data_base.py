import mysql.connector as dbapi # mysql
from dotenv import load_dotenv
load_dotenv()
import os
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

def game_get_comp():
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement = """select competition_id, competitions_name
                    from competitions"""

    cursor.execute(statement)
    game_competitions = cursor.fetchall()
    result = [list(comp) for comp in game_competitions]

    for i in range(len(result)):
        result[i][1] = result[i][1].replace('-', ' ')
        result[i][1] = result[i][1].title()

    cursor.close()
    connection.close()

    return result

def game_get_season():
    connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="12345", database="futbalmania")

    cursor = connection.cursor()

    statement = """select distinct(season) from games order by season"""

    cursor.execute(statement)
    result_l = cursor.fetchall()

    cursor.close()
    connection.close()

    return result_l