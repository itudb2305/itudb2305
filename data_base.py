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

    statement = """
    SELECT p.players_name, c.clubs_name ,p.position ,p.country_of_citizenship,p.player_id
    FROM players p
    INNER JOIN clubs c ON p.current_club_id = c.club_id
    ORDER BY p.players_name;
     """

    cursor.execute(statement)
    result_2 = cursor.fetchall()

    cursor.close()
    connection.close()

    return result_2

def club_list():
    #xto get the clublist
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement =  '''
                    SELECT clubs_name, country_name, club_id
                    FROM clubs
                    JOIN competitions
                    ON clubs.domestic_competition_id = competitions.domestic_league_code; 
                '''

    cursor.execute(statement)
    clubslist = cursor.fetchall()

    cursor.close()
    connection.close()

    return clubslist

def clubgame_list(club_id):
    #xto get the clublist
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement =  '''
                    SELECT 
                        c1.clubs_name as club_name,
                        c2.clubs_name AS opponent_name,
                        cg.own_goals as goal_for,
                        cg.opponent_goals AS goal_against,
                        cg.own_manager_name,
                        cg.opponent_manager_name,
                        CASE 
                            WHEN cg.hosting = 'Home' THEN c1.stadium_name
                            ELSE c2.stadium_name
                        END AS stadium_name
                    FROM 
                        futbalmania.club_games AS cg
                        JOIN clubs c1 ON cg.club_id = c1.club_id  
                        JOIN clubs c2 ON cg.opponent_id = c2.club_id
                    WHERE c1.club_id = %s; 
                '''
    cursor.execute(statement, (club_id, ))
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

def game_get_games(game_competitions_list, game_season_list, game_rounds_list, game_clubs_list, page_num):
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

    cursor = connection.cursor()

    statement = """SELECT A.game_id, B.competitions_name, A.games_round, A.home_club_name, A.home_club_goals, A.away_club_goals, A.away_club_name, A.games_date
                    FROM futbalmania.games A
                    JOIN futbalmania.competitions B on A.competition_id = B.competition_id
                    %s
                    order by games_date DESC
                    LIMIT 20 OFFSET %s;"""

    where_statement = "WHERE TRUE" #By default is true, so we can concatenate "AND (<condition>)" for all category without check
    comp_sel = ""
    game_season_sel = ""
    game_rounds_sel = ""
    game_clubs_sel = ""

    if len(game_competitions_list) == 0: #DONE
        comp_sel = "TRUE"
    else:
        comp_sel = "FALSE" # 0 OR <variable> = <variable>; we can use this
        for x in game_competitions_list:
            comp_sel = comp_sel + " OR A.competition_id = '%s' " %str(x)
    where_statement = where_statement + " AND ( " + comp_sel + ")"

    if len(game_season_list) == 0: #DONE
        game_season_sel = "TRUE"
    else:
        game_season_sel = "FALSE" # 0 OR <variable> = <variable>; we can use this
        for x in game_season_list:
            game_season_sel = game_season_sel + " OR A.season = %s " %str(x)
    where_statement = where_statement + " AND ( " + game_season_sel + ")"

    if len(game_rounds_list) == 0: #DONE
        game_rounds_sel = "TRUE"
    else:
        game_rounds_sel = "FALSE" # 0 OR <variable> = <variable>; we can use this
        for x in game_rounds_list:
            game_rounds_sel = game_rounds_sel + " OR A.games_round = '%s' " %str(x)
    where_statement = where_statement + " AND ( " + game_rounds_sel + ")"

    if len(game_clubs_list) == 0: #DONE
        game_clubs_sel = "TRUE"
    else:
        game_clubs_sel = "FALSE" # 0 OR <variable> = <variable>; we can use this
        for x in game_clubs_list:
            game_clubs_sel = game_clubs_sel + " OR A.home_club_id = %s OR A.away_club_id = %s " %(str(x), str(x))
    where_statement = where_statement + " AND ( " + game_clubs_sel + ")"

    print(where_statement)

    cursor.execute(statement %(where_statement, str( (page_num - 1)*20 ) ) )
    games = cursor.fetchall()
    result = [list(comp) for comp in games]

    for i in range(len(result)):
        result[i][1] = result[i][1].replace('-', ' ')
        result[i][1] = result[i][1].title()
    
    return result

def games_delete_game(game_id):

    try:
        connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")
        cursor = connection.cursor()

        statement = """DELETE FROM games WHERE game_id = %s;"""

        cursor.execute(statement %str(game_id))
        connection.commit()
    except dbapi.DatabaseError:
        connection.rollback()
        print("Database error")
    finally:
        cursor.close()
        connection.close()

    return True

def get_available_countries():
        connection = dbapi.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database="futbalmania")
        cursor = connection.cursor()
        statement = """SELECT DISTINCT country_of_citizenship FROM players ORDER BY country_of_citizenship;"""
        cursor.execute(statement)
        countries = [country[0] for country in cursor.fetchall()]
        cursor.close()
        connection.close()
        return countries

def get_available_positions():
        connection = dbapi.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database="futbalmania")
        cursor = connection.cursor()
        statement = "SELECT DISTINCT position FROM players ORDER BY position;"
        cursor.execute(statement)
        positions = [position[0] for position in cursor.fetchall()]
        cursor.close()
        connection.close()
        return positions

def get_available_clubs():
        connection = dbapi.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database="futbalmania")
        cursor = connection.cursor()
        statement = "SELECT DISTINCT c.clubs_name FROM players p JOIN clubs c ON p.current_club_id = c.club_id ORDER BY c.clubs_name;"
        cursor.execute(statement)
        clubs = [club[0] for club in cursor.fetchall()]
        cursor.close()
        connection.close()
        return clubs

def question_game():
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")
    
    cursor = connection.cursor(dictionary=True)

    statement = """SELECT players_name,country_of_citizenship 
    FROM players 
    WHERE highest_market_value_in_eur >= 50000000 
    AND last_season > 2017 
    AND players_name IS NOT NULL 
    AND country_of_citizenship IS NOT NULL 
    ORDER BY RAND() 
    LIMIT 1;"""
   
    cursor.execute(statement)
    result_3 = cursor.fetchall()
    cursor.close()
    connection.close()

    return result_3

def random_value():
    connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")
    
    cursor = connection.cursor(dictionary=True)

    statement = """ SELECT country_of_citizenship 
    FROM players 
    WHERE highest_market_value_in_eur >= 50000000 
    AND last_season > 2015 
    AND country_of_citizenship IS NOT NULL
    ORDER BY RAND() 
    LIMIT 1;"""
   
    cursor.execute(statement)
    random_value = cursor.fetchall()

    cursor.close()
    connection.close()

    return random_value

def get_player_details(player_id):
    connection = dbapi.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database="futbalmania")
    cursor = connection.cursor()

    statement = """
        SELECT first_name, last_name, players_name, last_season, country_of_birth, city_of_birth, 
               country_of_citizenship, date_of_birth, sub_position, position, foot, height_in_cm, 
               market_value_in_eur, highest_market_value_in_eur, contract_expiration_date, 
               agent_name, image_url, competitions_name , current_club_name,player_id ,current_club_id, 
               player_code,current_club_domestic_competition_id
        FROM players
        INNER JOIN competitions ON players.current_club_domestic_competition_id = competitions.competition_id
        WHERE player_id = %s;
    """

    cursor.execute(statement, (player_id,))
    player_data = cursor.fetchone()


    if player_data:
        player_data = list(player_data)

        if isinstance(player_data[17], str):
            player_data[17] = player_data[17].replace('-', ' ')

        player_info = {
            "first_name": player_data[0],
            "last_name": player_data[1],
            "players_name": player_data[2],
            "last_season": player_data[3],
            "country_of_birth": player_data[4],
            "city_of_birth": player_data[5],
            "country_of_citizenship": player_data[6],
            "date_of_birth": player_data[7],
            "sub_position": player_data[8],
            "position": player_data[9],
            "foot": player_data[10],
            "height_in_cm": player_data[11],
            "market_value_in_eur": player_data[12],
            "highest_market_value_in_eur": player_data[13],
            "contract_expiration_date": player_data[14],
            "agent_name": player_data[15],
            "image_url": player_data[16],
            "competitions_name": player_data[17],
            "current_club_name": player_data[18],
            "player_id": player_data[19],
            "current_club_id": player_data[20],
            "player_code": player_data[21],
            "current_club_domestic_competition_id": player_data[22]
        }
    else:
        player_info = None

    cursor.close()
    connection.close()
    return player_info

def update_player_details(player_id, **updated_data):
    connection = dbapi.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database="futbalmania")
    cursor = connection.cursor()

    update_parts = [f"{key} = %s" for key in updated_data]
    update_statement = f"UPDATE players SET {', '.join(update_parts)} WHERE player_id = %s;"

    update_values = tuple(updated_data.values()) + (player_id,)

    cursor.execute(update_statement, update_values)
    connection.commit()
    cursor.close()
    connection.close()



def get_transfer_list(request):
        if request.method == 'POST':
            #connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="Emre1234", database="futbalmania")
            connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")

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
            #connection = dbapi.connect(host = "localhost", port = 3306, user = "root", password="Emre1234", database="futbalmania")
            connection = dbapi.connect(host = HOST, port = PORT, user = USER, password=PASSWORD, database="futbalmania")
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
    