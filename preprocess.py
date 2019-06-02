#!/home/acaruso/anaconda3/bin/python
import sys
import chess
import chess.pgn
import chess.engine #StockFish engine
import pandas as pd

pgn = sys.stdin
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") #install with sudo apt-get install stockfish

# num_games = 1 # the number of games for which to get pgn data from the file - just used for testing purposes
count = 0 #count the number of games that have been parsed
scores = []
board_positions = []
piece_list = ('p','n','b','r','q','k','P','N','B','R','Q','K')

# while count < num_games:
while chess.pgn.read_game(pgn):
    try:
        game = chess.pgn.read_game(pgn)
        board = game.board() #fresh game
        while not game.is_end(): #iterate through every board position in the game
            node = game.variations[0]
            board = game.board()
            game = node 

            feature_vector = [] #stores a length 768 representation of the current board position
            # 12 elements for each square, corresponding to each unique piece (black and white)
            # 1 if the square is occupied by a white piece, -1 if occupied by black piece, 0 otherwise

            for square in str(board):
                if square.strip(): #ignore empty lines
                    if square.islower():
                        for piece in piece_list:
                            if square == piece:
                                feature_vector.append(-1) #use -1 for black pieces, denoted by lowercase
                            else:
                                feature_vector.append(0)
                    elif square.isupper():
                        for piece in piece_list:
                            if square == piece:
                                feature_vector.append(1) #use 1 for white pieces, denoted by uppercase
                            else:
                                feature_vector.append(0)
                    else: # if the square is empty, append 12 0s (one for each piece)
                        for i in range(12):
                            feature_vector.append(0)

            board_positions.append(feature_vector)

            info = engine.analyse(board, chess.engine.Limit(time=0.100)) #get Stockfish score for current board position
            scores.append(str(info["score"]))

        count += 1
        if count%100 == 0:
            print(f"{count} games processed")
    
    except:
        break

features = pd.DataFrame(board_positions)
response = pd.DataFrame(scores)
data = pd.concat([features, response], axis=1)

data.to_csv("one_month768.csv", sep=',', header=False, index=False)
print('done parsing & wrote to csv')

exit()
