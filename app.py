from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle


# from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.route('/')
def boggle_home():
    """Returns the boggle board"""

    boggle_board = boggle_game.make_board()
    session["boggle_board"] = boggle_board

    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("base.html", boggle_board=boggle_board, highscore=highscore, nplays=nplays)


@app.route('/check-word')
def check_word():
    """Checks the word the user input against the words.txt file to see if it's valid"""

    word = request.args['word']
    boggle_board = session['boggle_board']
    res = boggle_game.check_valid_word(boggle_board, word)

    return jsonify({"result": res})


@app.route('/user-score', methods=["POST"])
def user_score():
    """Grabs the score and updates the number of plays and highscore."""

    score = request.json["$score"]
    nplays = session.get("nplays", 0)8
    highscore = session.get("highscore", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify({'highscore': session['highscore']})
