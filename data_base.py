import mysql.connector as dbapi # mysql

def game_get_comp():
    connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="12345", database="futbalmania")

    cursor = connection.cursor()

    statement = """select distinct(competition_id) from games"""

    cursor.execute(statement)
    game_competitions = cursor.fetchall()

    cursor.close()
    connection.close()

    return game_competitions

def game_get_season():
    connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="12345", database="futbalmania")

    cursor = connection.cursor()

    statement = """select distinct(season) from games order by season"""

    cursor.execute(statement)
    result_l = cursor.fetchall()

    cursor.close()
    connection.close()

    return result_l