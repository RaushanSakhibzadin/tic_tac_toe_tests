from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'some_secret_key'

# The board is a list of 9 elements representing the 9 squares.
# 'X' for X, 'O' for O, and '' for empty squares.
board = [''] * 9


@app.route('/')
def index():
    return render_template('index.html', board=board)


@app.route('/play/<int:position>', methods=['POST'])
def play(position):
    global board
    if board[position] == '':
        board[position] = 'X'  # Let's assume the player is always 'X' for simplicity
        if check_win(board, 'X'):
            flash('Player X wins!')
            board = [''] * 9
            return redirect(url_for('index'))
        # Now let the 'O' (computer) play
        computer_play()
        if check_win(board, 'O'):
            flash('Player O wins!')
            board = [''] * 9
    return redirect(url_for('index'))


@app.route('/stop', methods=['POST'])
def stop_game():
    # Logic to stop the game
    flash('Game stopped.')
    return redirect(url_for('index'))


def computer_play():
    global board
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            break


def check_win(b, player):
    win_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for pos in win_positions:
        if b[pos[0]] == b[pos[1]] == b[pos[2]] == player:
            return True
    return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
