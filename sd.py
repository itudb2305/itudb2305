from flask import Flask, render_template, url_for
#import mysql.connector

app = Flask(__name__)

#mysql_config = {
   # 'host': 'localhost',
   # 'user': 'root',
   # 'password': 'momo',
   # 'database': 'Football',
#}

#conn = mysql.connector.connect(**mysql_config)
#cursor = conn.cursor()




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/player")
def player():
    return render_template('player.html', title='Player')

@app.route("/competitions")
def competitions():
    return render_template('competitions.html', title='Competitions')

@app.route("/games")
def games():
    return render_template('games.html', title='Games')


if __name__ == '__main__':
    app.run(debug=True)