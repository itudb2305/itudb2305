from flask import Flask, render_template, url_for, request
from data_base import *
import random

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/player")
def player():
    player_values = player_t()
    return render_template('player.html', title='Player', result=player_values)

@app.route("/clubs")
def clubs():

    data = club_list()
    datacopied = []
    country = []
    for i in range(len(data)):
        datacopied.append(data[i])

    valxvaly = []
    for i in range(len(datacopied)):
        valxvaly.append(datacopied[i][1])
    
    unique_list = []
    # traverse for all elements
    for x in valxvaly:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    
    my_dict = {key: [] for key in unique_list}

    for i in range(0, len(datacopied)):
        if datacopied[i][1] in my_dict:
            my_dict[datacopied[i][1]].append(datacopied[i][0])
        

   
    return render_template('clubs.html', title='Player',xxx=my_dict, country=my_dict, clubn=my_dict)

@app.route("/clubs_game/<int:club_id>")
def clubs_game(club_id=3):
    club_games = clubgame_list(club_id)

    
    return render_template('clubs_game.html', title='Clubs Games', result=club_games)


@app.route("/quiz_game")
def quiz_game():
    q = question_game()
    global global_variable
    global_variable = q[0]['country_of_citizenship']
    n = q[-1]['players_name']

    v1 = random_value()
    while v1[0]['country_of_citizenship'] == global_variable:
        v1 = random_value()

    v2 = random_value()
    while v2[0]['country_of_citizenship'] == global_variable or v2[0]['country_of_citizenship'] == v1[0]['country_of_citizenship']:
        v2 = random_value()

    values = [global_variable, v1[0]['country_of_citizenship'], v2[0]['country_of_citizenship']]
    random.shuffle(values)
    
    return render_template('quiz_game.html', title='Quiz Game', q=n, v0=values[0], v1=values[1], v2=values[2])



@app.route("/quiz_game_result", methods=['POST'])
def submit():
    user_answer = request.form['answer']
    correct_answer = global_variable
    is_correct = user_answer == correct_answer
    return render_template('quiz_game2.html', is_correct=is_correct, correct_answer=correct_answer,user_answer=user_answer)



@app.route("/competitions", methods=['POST', 'GET'])
def competitions():
    if request.method == 'POST':
        competition = get_competition_country(request)
        return render_template('competitions.html', title='Competitions', competition=competition)
    else:
        return render_template('competitions.html', title='Competitions', competition=None)

@app.route("/games")
def games():
    game_competitions_list = request.args.getlist('comp')
    game_season_list = request.args.getlist('game_season')
    game_rounds_list = request.args.getlist('game_rounds')
    game_clubs_list = request.args.getlist('game_clubs')
    page_get = request.args.get('page')
    page_num = 0
    try:
        page_num = int(page_get)
        if page_num < 1:
            page_num = 1
    except:
        page_num = 1

    #for filtering menu
    game_competitions = game_get_comp()
    game_season = game_get_season()
    game_rounds = game_get_round()
    game_clubs = game_get_clubs()
    #for getting list of games
    game_games = game_get_games(game_competitions_list, game_season_list, game_rounds_list, game_clubs_list, page_num)
    #page render
    return render_template('games.html', 
                            title='Games',
                            game_competitions_list = game_competitions_list,
                            game_season_list = game_season_list,
                            game_rounds_list = game_rounds_list,
                            game_clubs_list = game_clubs_list,
                            game_competitions = game_competitions,
                            game_season = game_season,
                            game_rounds = game_rounds,
                            game_clubs = game_clubs,
                            game_games = game_games,
                            page_num = page_num)

@app.route("/transfer", methods=['POST', 'GET'])
def transfer():
    if request.method == 'POST':
        players = get_transfer_list(request)
        return render_template('transfer.html', title='Transfer', players=players)
    else:
        return render_template('transfer.html', title='Transfer', players=None)

if __name__ == '__main__':
    app.run(debug=True, port=8000)