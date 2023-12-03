import mysql.connector as dbapi # mysql
from flask import Flask, render_template, request
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
                    from competitions
                    order by competitions_name"""

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
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement = """SELECT distinct(season)
                    FROM futbalmania.games
                    order by season DESC;"""

    cursor.execute(statement)
    seasons = cursor.fetchall()

    cursor.close()
    connection.close()

    return seasons

def game_get_round():
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement = """SELECT distinct(games_round)
                    FROM futbalmania.games
                    ORDER BY games_round;"""

    cursor.execute(statement)
    rounds = cursor.fetchall()
    return rounds

def player_t():
    connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="12345", database="futbalmania")

    cursor = connection.cursor()

    statement = 'SELECT players_name,country_of_citizenship,position FROM players;'

    cursor.execute(statement)
    result_2 = cursor.fetchall()

    cursor.close()
    connection.close()

    return result_2

def game_get_clubs():
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement = """SELECT distinct(A.club_id), (A.clubs_name) FROM futbalmania.clubs A
                    WHERE A.club_id in (SELECT B.home_club_id FROM futbalmania.games B)
	                OR A.club_id in (SELECT C.away_club_id FROM futbalmania.games C)
                    order by A.clubs_name;"""

    cursor.execute(statement)
    seasons = cursor.fetchall()

    cursor.close()
    connection.close()

    return seasons

def game_get_games():
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement = """SELECT A.game_id, B.competitions_name, A.games_round, A.home_club_name, A.home_club_goals, A.away_club_goals, A.away_club_name, A.games_date
                    FROM futbalmania.games A
                    JOIN futbalmania.competitions B on A.competition_id = B.competition_id
                    order by games_date DESC
                    LIMIT 20 OFFSET 0;"""

    cursor.execute(statement)
    games = cursor.fetchall()
    result = [list(comp) for comp in games]

    for i in range(len(result)):
        result[i][1] = result[i][1].replace('-', ' ')
        result[i][1] = result[i][1].title()
    
    return result

def question_game():
    connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="12345", database="futbalmania")
    
    cursor = connection.cursor(dictionary=True)

    statement = 'SELECT players_name,country_of_citizenship FROM players WHERE highest_market_value_in_eur >= 50000000 AND last_season > 2015 ORDER BY RAND() LIMIT 1;'
   
    cursor.execute(statement)
    result_3 = cursor.fetchall()
    cursor.close()
    connection.close()

    return result_3

def random_value():
    connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="12345", database="futbalmania")
    
    cursor = connection.cursor(dictionary=True)

    statement = 'SELECT country_of_citizenship FROM players WHERE highest_market_value_in_eur >= 50000000 AND last_season > 2015 ORDER BY RAND() LIMIT 1;'
   
    cursor.execute(statement)
    random_value = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def get_transfer_list():
        if request.method == 'POST':
            connection = dbapi.connect(host = 'localhost', port = 3306, user = 'root', password='Emre1234', database="futbalmania")

            cursor = connection.cursor()
            min_value = request.form.get('minvalue')
            max_value = request.form.get('maxvalue')
            min_age = request.form.get('minage')
            max_age = request.form.get('maxage')
            position = request.form.get('position')
            sub_position = request.form.get('subposition')
            foot=request.form.get("foot")
            nationality = request.form.get('nationality')
            team = request.form.get('team')

            statement = """SELECT A.first_name, A.last_name
                            FROM futbalmania.players A
                            Join futbalmania.player_valuations B on A.player_id = B.player_id
                            Join futbalmania.clubs C ON  A.current_club_id = C.club_id
                            WHERE B.market_value_in_eur BETWEEN %s AND %s
                             AND A.position LIKE %s
                             AND A.sub_position LIKE %s
                             AND A.foot LIKE %s
                             AND A.country_of_citizenship LIKE %s
                             AND C.clubs_name LIKE %s
                             AND B.dateweek = '2023-09-18';"""
            
            cursor.execute(statement, (min_value, max_value, position, sub_position, foot, nationality, team))
            result =cursor.fetchall()
            cursor.close()
            connection.close()    
            return random_value