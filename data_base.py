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
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement = 'SELECT players_name,country_of_citizenship,position FROM players;'

    cursor.execute(statement)
    result_2 = cursor.fetchall()

    cursor.close()
    connection.close()

    return result_2

def club_list():
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement =  '''SELECT clubs_name, country_name 
                 FROM clubs
                JOIN competitions
                ON clubs.domestic_competition_id = competitions.domestic_league_code; '''

    cursor.execute(statement)
    clubslist = cursor.fetchall()

    cursor.close()
    connection.close()

    return clubslist

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
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")
    
    cursor = connection.cursor(dictionary=True)

    statement = 'SELECT players_name,country_of_citizenship FROM players WHERE highest_market_value_in_eur >= 50000000 AND last_season > 2017 ORDER BY RAND() LIMIT 1;'
   
    cursor.execute(statement)
    result_3 = cursor.fetchall()
    cursor.close()
    connection.close()

    return result_3

def random_value():
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")
    
    cursor = connection.cursor(dictionary=True)

    statement = 'SELECT country_of_citizenship FROM players WHERE highest_market_value_in_eur >= 50000000 AND last_season > 2015 ORDER BY RAND() LIMIT 1;'
   
    cursor.execute(statement)
    random_value = cursor.fetchall()

    cursor.close()
    connection.close()

    return random_value

def get_transfer_list(request):
        if request.method == 'POST':
            connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="Emre1234", database="futbalmania")

            cursor = connection.cursor()
            min_value = int(request.form.get('minvalue'))
            max_value = int(request.form.get('maxvalue'))
            min_age = request.form.get('minage')
            max_age = request.form.get('maxage')
            position = request.form.get('position')
            sub_position = request.form.get('subposition')
            foot=request.form.get("foot")
            nationality = request.form.get('nationality')
            team = request.form.get('team')

            position_pattern = f"%{position}%"
            sub_position_pattern = f"%{sub_position}%"
            foot_pattern = f"%{foot}%"
            nationality_pattern = f"%{nationality}%"
            team_pattern = f"%{team}%"

            statement = """SELECT A.sub_position, A.first_name, A.last_name, TIMESTAMPDIFF(YEAR, A.date_of_birth, CURDATE()) AS age, 
                           A.current_club_name, A.foot, A.height_in_cm, A.market_value_in_eur,
                           A.contract_expiration_date, MAX(B.player_valuations_date) as latest
                           FROM futbalmania.players A
                           Join futbalmania.player_valuations B on A.player_id = B.player_id
                           Join futbalmania.clubs C ON  A.current_club_id = C.club_id
                           WHERE B.market_value_in_eur BETWEEN %s AND %s
                           AND A.position LIKE %s
                           AND A.sub_position LIKE %s
                           AND A.foot LIKE %s
                           AND A.country_of_citizenship LIKE %s
                           AND A.current_club_name LIKE %s
                           AND TIMESTAMPDIFF(YEAR, A.date_of_birth, CURDATE()) BETWEEN %s AND %s
                           AND B.last_season = 2023
                           GROUP BY A.sub_position, A.first_name, A.last_name, age, 
                           A.current_club_name, A.foot, A.height_in_cm, A.market_value_in_eur, A.contract_expiration_date 
                           ORDER BY latest DESC;
                           """
            
            cursor.execute(statement, (min_value, max_value, position_pattern, sub_position_pattern, foot_pattern, nationality_pattern, team_pattern, min_age, max_age))
            result =cursor.fetchall()
            cursor.close()
            connection.close()    
            return result

def get_competition_country(request):
        if request.method == 'POST':
            connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="Emre1234", database="futbalmania")
            cursor = connection.cursor()
            country = request.form.get('country')

            statement="""SELECT A.competitions_name, A.sub_type, A.country_name, A.competition_id
                         FROM futbalmania.competitions A
                         WHERE A.country_name = %s
                         GROUP BY A.competition_id, A.competitions_name, A.sub_type
                         ORDER BY A.competitions_name"""
            
            cursor.execute(statement, (country, ))
            result =cursor.fetchall()
            cursor.close()
            connection.close()    
            return result
        
def update_value(request):
        if request.method == 'POST':
            connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="Emre1234", database="futbalmania") 
            cursor = connection.cursor()

            name = request.form.get('name')
            surname = request.form.get('surname')
            team = request.form.get('team')
            value = int(request.form.get('value'))
            team_pattern = f"%{team}%"

            statement = """ SELECT A.player_id, A.current_club_id, A.current_club_domestic_competition_id 
                            FROM futbalmania.players A
                            WHERE A.first_name = %s
                            AND A.last_name = %s
                            AND A.current_club_name LIKE %s
                            LIMIT 1;"""
            
            cursor.execute(statement, (name, surname, team_pattern))
            result =cursor.fetchall()
            if result:
                print(result[0][0], value, result[0][1], result[0][2])
            else:
                print("No results found.")

            statement2 = """ INSERT INTO futbalmania.player_valuations 
                            VALUES (%s, YEAR(CURDATE()), NOW(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY),
                            %s, 1, %s, %s); 
                            """
            
            cursor.execute(statement2, (result[0][0], value, result[0][1], result[0][2]))
            connection.commit()
            cursor.close()
            connection.close() 
    