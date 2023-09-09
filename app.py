from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'some_secret_key'

board = [''] * 9
game_on = True


@app.route('/')
def index():
    return render_template('index.html', board=board)


@app.route('/new_game', methods=['POST'])
def new_game():
    global board, game_on
    board = [''] * 9
    game_on = True
    return redirect(url_for('index'))


@app.route('/play/<int:position>', methods=['POST'])
def play(position):
    global board, game_on
    if not game_on:
        flash('Game is not ongoing. Start a new game!')
        return redirect(url_for('index'))

    if board[position] == '':
        board[position] = 'X'
        if check_win(board, 'X'):
            flash('Player X wins!')
            game_on = False
            return redirect(url_for('index'))
        computer_play()
        if check_win(board, 'O'):
            flash('Player O wins!')
            game_on = False
    if '' not in board:
        flash('It\'s a draw!')
        game_on = False
    return redirect(url_for('index'))


@app.route('/restart', methods=['POST'])
def restart_game():
    global board, game_on
    board = [''] * 9
    game_on = True
    flash('Game restarted.')
    return redirect(url_for('index'))


def computer_play():
    global board
    # Check for computer's winning move
    # for i in range(9):
    #     if board[i] == '':
    #         board[i] = 'O'
    #         if check_win(board, 'O'):
    #             return
    #         board[i] = ''
    #
    # # Check to block player's winning move
    # for i in range(9):
    #     if board[i] == '':
    #         board[i] = 'X'
    #         if check_win(board, 'X'):
    #             board[i] = 'O'
    #             return
    #         board[i] = ''

    # Play first available move
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
    app.run(host='0.0.0.0', port=5001, debug=True)
