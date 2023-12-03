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



@app.route("/competitions")
def competitions():
    list0f_competitions = ["England", "Italy", "Germany", "Turkey"]
    random_competition = random.choice(list0f_competitions)
    return render_template('competitions.html', title='Competitions', random_competition=random_competition)

@app.route("/games")
def games():
    game_competitions = game_get_comp()
    game_season = game_get_season()
    game_rounds = game_get_round()
    game_clubs = game_get_clubs()
    game_games = game_get_games()
    return render_template('games.html', 
                            title='Games',
                            game_competitions = game_competitions,
                            game_season = game_season,
                            game_rounds = game_rounds,
                            game_clubs = game_clubs,
                            game_games = game_games)

@app.route("/transfer", methods=['POST', 'GET'])
def transfer():
    players=get_transfer_list()
    return render_template('transfer.html', title='transfer', players=players)

if __name__ == '__main__':
    app.run(debug=True)