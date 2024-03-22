from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = 'key'

boggle_game = Boggle()

@app.route('/')
def index():
    if 'board' not in session:
        board = boggle_game.make_board()
        session['board'] = board
        session['highscore'] = 0
        session['nplays'] = 0
    else:
        board = session['board']
    highscore = session['highscore']
    nplays = session['nplays']
    return render_template("index.html", board=board, 
                           highscore=highscore, 
                           nplays=nplays)

@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)

if __name__ == '__main__':
    app.run(debug=True)
