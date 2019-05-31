#!/home/acaruso/anaconda3/bin/python
import sys
import chess
import chess.pgn
import chess.engine #StockFish engine
import pandas as pd

engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") #install with sudo apt-get install stockfish

pgn = sys.stdin

board_positions = []
scores = []
num_games = 2 # the number of games for which to get pgn data from the file - just used for testing purposes
count = 0
# while count < num_games:

#there are about 5000 games in one month of data . . . 
while chess.pgn.read_game(pgn):
    game = chess.pgn.read_game(pgn)
    board = game.board() #fresh game
    while not game.is_end(): #iterate through every board position in the game
        node = game.variations[0]
        board = game.board()
        game = node 

        info = engine.analyse(board, chess.engine.Limit(time=0.100)) #get Stockfish score for every board position

        clean_board = [] #stores a length 64 representation of the current position of the board (rows flattened into single sequence)
        for char in str(board):
            if char.strip(): #ignore empty lines
                if char == 'p':
                    char = -10
                elif char in ['n', 'b']:
                    char = -30
                elif char == 'r':
                    char = -50
                elif char == 'q':
                    char = -90
                elif char == 'k':
                    char = -10000
                elif char == 'P':
                    char = 10
                elif char in ['N', 'B']:
                    char = 30
                elif char == 'R':
                    char = 50
                elif char == 'Q':
                    char = 90
                elif char == 'K':
                    char = 10000
                elif char == '.':
                    char = 0

                clean_board.append(char)
        board_positions.append(clean_board)
        scores.append(str(info["score"]))

    count += 1
    if count%100 == 0:
        print(f"{count} games processed")

features = pd.DataFrame(board_positions)
response = pd.DataFrame(scores)
data = pd.concat([features, response], axis=1)

data.to_csv("one_month.csv", sep=',', header=False, index=False)
print('done parsing & wrote to csv')

exit()
