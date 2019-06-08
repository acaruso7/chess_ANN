# chess_ANN
Neural network to "score" board positions in chess, trained on [FICS](https://www.ficsgames.org/download.html) games database 
[PGN](https://en.wikipedia.org/wiki/Portable_Game_Notation) data, and [Stockfish](https://stockfishchess.org/) board scores.

## Project Directory Structure
```
chess_ANN
│   README.md
│   parse_pgn.py  
│   clean_data.py   
│   TPU_MLP_regression.ipynb  
│
└───data
│   │
│   └───raw
│       │   2015.pgn
│       │   2016.pgn
│       │   2017.pgn
│       │   . . . 
│   │
│   └───parsed
│       │   2015_5000games.csv
│       │   2016_5000games.csv
│       │   2017_5000games.csv
│       │   . . . 
│   │
│   └───model_ready
│       │   data.csv
```


## Download Data
Raw PGN format data can be downloaded at https://www.ficsgames.org/download.html. It is recommended to select 'Standard (average rating > 2000)',
'whole year' for Period, and to name the files '{year}.pgn'. Since the parsing script is not able to fit an entire year's worth of data into memory
(16 GB), I downloaded data from 3 different years, parsed 5000 games from each, and later recombined them into a single csv file. Save the raw
pgn files to the /data/raw folder.

## Running
#### Install Stockfish Engine
```bash
sudo apt-get install stockfish
```
This should install to /usr/games/stockfish. Make sure the path to the stockfish engine specified in parse_pgn.py is correct.

#### Parse PGN Files
```bash
< ./data/raw/2018.pgn python parse_pgn.py 5000
```
Above is an example command to parse 5000 games from 2018.pgn into a csv file. The resulting csv will be written to /data/parsed.
Note: it takes several hours to parse 5000 games. Over the course of a few days, I parsed 5000 games form each of 2016.pgn, 2017.pgn, and 2018.pgn,
respectively.

#### Concatenate CSV Files & Clean Data
```bash
python clean_data.py
```
This will concatenate all of the csv files stored in /data/parsed, and store the resulting file ('data.csv') in /data/model_ready.

#### Train Model
I used the TPU accelerator in [Google Colab notebooks](https://colab.research.google.com/notebooks/welcome.ipynb) to train this neural network
model. There is too much data to train with a CPU or GPU. Regarding model architecture, I emulated the input data structure and hyperparameters
in this [research paper](https://pdfs.semanticscholar.org/5171/32097f4de960f154185a8a8fec4178a15665.pdf).
