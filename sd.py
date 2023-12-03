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
    return render_template('player.html', title='Player')

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