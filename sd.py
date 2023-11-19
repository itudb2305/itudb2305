from flask import Flask, render_template, url_for
import random
import mysql.connector as dbapi
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
    return render_template('games.html', title='Games')


if __name__ == '__main__':
    app.run(debug=True)