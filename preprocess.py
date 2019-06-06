#!/home/acaruso/anaconda3/bin/python
import sys
import chess
import chess.pgn
import chess.engine #StockFish engine
import pandas as pd
import time

# start = time.time()
# print("hello")
# end = time.time()
# print(end - start)

pgn = sys.stdin
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish") #install with sudo apt-get install stockfish

# num_games = 3 # the number of games for which to get pgn data from the file - just used for testing purposes
count = 0 #count the number of games that have been parsed
scores = []
board_positions = []
piece_list = ('p','n','b','r','q','k','P','N','B','R','Q','K')

# while count <= num_games:
while chess.pgn.read_game(pgn): #need to get 3 million unique rows
    try:
        game = chess.pgn.read_game(pgn)
        board = game.board() #fresh game
        move_num = 1
        while not game.is_end(): #iterate through every board position in the game
            node = game.variations[0]
            board = game.board()
            game = node 

            feature_vector = [] #stores a length 768 representation of the current board position
            # 12 elements for each square, corresponding to each unique piece (black and white)
            # 1 if the square is occupied the player whose turn is, -1 if occupied by opposing player, 0 otherwise

            for square in str(board)[0::2]: #remove spaces between squares with [0::2]
                if square.islower() and move_num % 2 != 0: #whites move
                    for piece in piece_list:
                        if square == piece:
                            feature_vector.append(-1) 
                        else:
                            feature_vector.append(0)
                elif square.islower() and move_num % 2 == 0: #blacks move
                    for piece in piece_list:
                        if square == piece:
                            feature_vector.append(1) 
                        else:
                            feature_vector.append(0)
                elif square.isupper() and move_num % 2 != 0: #whites move
                    for piece in piece_list:
                        if square == piece:
                            feature_vector.append(1) 
                        else:
                            feature_vector.append(0)
                elif square.isupper() and move_num % 2 == 0: #blacks move
                    for piece in piece_list:
                        if square == piece:
                            feature_vector.append(-1) 
                        else:
                            feature_vector.append(0)
                else: # if the square is empty, append 12 0s (one for each piece)
                    for i in range(12):
                        feature_vector.append(0)

            board_positions.append(feature_vector)

            info = engine.analyse(board, chess.engine.Limit(time=0.100)) #get Stockfish score for current board position
            scores.append(str(info["score"]))

            move_num += 1

        count += 1
        if count%500 == 0:
            print(f"{count} games processed")

        if count == 5000:
            features = pd.DataFrame(board_positions)
            response = pd.DataFrame(scores) #normalize stockfish scores to [0,1] !!!!!!
            data = pd.concat([features, response], axis=1)

            data.to_csv("2018_5k.csv", sep=',', header=False, index=False)
            print('done parsing & wrote to csv')
            break

    except:
        break

# features = pd.DataFrame(board_positions)
# response = pd.DataFrame(scores) #normalize stockfish scores to [0,1] !!!!!!
# data = pd.concat([features, response], axis=1)

# data.to_csv("one_month768.csv", sep=',', header=False, index=False)
# print('done parsing & wrote to csv')


exit()
