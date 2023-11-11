from flask import Flask, render_template, url_for
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
    return render_template('competitions.html', title='Competitions')


if __name__ == '__main__':
    app.run(debug=True)