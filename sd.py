from flask import Flask, render_template, url_for, request , session, redirect
import random
from data_base import *
import random


app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/player")
def player():
    search_query = request.args.get('search', '')
    country_filter = request.args.get('country')
    position_filter = request.args.get('position')
    club_filter = request.args.get('club')
    page = request.args.get('page', 1, type=int)
    per_page = 30

    available_countries = get_available_countries()
    available_positions = get_available_positions()
    available_clubs = get_available_clubs()

    player_values = player_t()  

    if search_query:
        player_values = [player for player in player_values if search_query.lower() in player[0].lower()]

    if country_filter:
        player_values = [player for player in player_values if player[1] == country_filter]

    if position_filter:
        player_values = [player for player in player_values if player[2] == position_filter]

    if club_filter:
        player_values = [player for player in player_values if player[3] == club_filter]

    total = len(player_values)
    start = (page - 1) * per_page
    end = start + per_page
    players_on_page = player_values[start:end]

    total_pages = total // per_page + (1 if total % per_page > 0 else 0)
    return render_template('player.html', title='Player', result=players_on_page,  countries=available_countries, positions=available_positions, clubs=available_clubs ,page=page, total_pages=total_pages)




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



@app.route("/quiz_game", methods=['GET', 'POST'])
def quiz_game():
    if 'score' not in session:
        session['score'] = 0

    if request.method == 'POST':
        user_answer = request.form.get('answer')  
        if not user_answer:
            q = session.get('last_question', '')
            values = session.get('last_values', [])
            return render_template('quiz_game.html', title='Quiz Game', q=q, values=values, submitted=False, error_message="Please select an answer.")

        correct_answer = session.get('correct_answer', '')
        is_correct = user_answer == correct_answer

        if is_correct:
            session['score'] += 1
            return render_template('quiz_game.html', is_correct=True, score=session['score'], submitted=True)
        else:
            final_score = session['score']
            session['score'] = 0
            return render_template('quiz_game.html', is_correct=False, correct_answer=correct_answer, score=final_score, submitted=True, game_over=True)
    else:
        q = question_game()
        session['correct_answer'] = q[0]['country_of_citizenship']
        n = q[-1]['players_name']

        values = [session['correct_answer']]
        while len(values) < 3:
            random_country = random_value()[0]['country_of_citizenship']
            if random_country not in values:
                values.append(random_country)

        random.shuffle(values)
        session['last_question'] = n
        session['last_values'] = values

        return render_template('quiz_game.html', title='Quiz Game', q=n, values=values, submitted=False)



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

@app.route("/games_delete")
def games_delete():
    game_id = request.args.get("game_id")
    
    games_delete_game( int(game_id) )

    return redirect( request.headers.get("Referer") ) 

@app.route("/transfer", methods=['POST', 'GET'])
def transfer():
    if request.method == 'POST':
        players = get_transfer_list(request)
        return render_template('transfer.html', title='Transfer', players=players)
    else:
        return render_template('transfer.html', title='Transfer', players=None)

@app.route("/player_valuation")
def player_valuation():
    return render_template('player_valuation.html', title='Player Valuation')

@app.route("/sell_player")
def sell_player():
    return render_template('sell_player.html', title='Sell Player')

@app.route("/update_market_value", methods=['POST', 'GET'])
def update_market_value():
    if request.method == 'POST':
        update_value(request)
        return render_template('update_market_value.html', title='UpdateValue')
    else:
        return render_template('update_market_value.html', title='Update Market Value')

@app.route("/correct_valuation")
def correct_valuation():
    return render_template('correct_valuation.html', title='Correct Valuation')

if __name__ == '__main__':
    app.run(debug=True, port=8000)