# wordle-benchmark
A performant Wordle simulator for benchmarking and evaluating agents.

Do you like Wordle? I like Wordle. 
I wanted to see if I could teach my computer to play a decent game, but I couldn't find a good way to grade my solutions.
I put together a Python package to play Wordle games and keep track of game statistics for Wordle "agents": Python software written to play Wordle.

![](https://media.githubusercontent.com/media/peterbbryan/wordle-benchmark/main/resources/docs/script-manual-game.gif)


## Getting started

If you want to run scripts, tests, or contribute to the package, pip install from requirements.
```
pip install -r requirements.txt
```

If you just want to get started fast, pip install locally after cloning!
```
git clone https://github.com/peterbbryan/wordle-benchmark.git
cd wordle-benchmark
pip install . 
```

## Sample use

`python scripts/play_manual_game.py --word robin`

This will prompt for user input and let you play through a game.
Note, to run the scripts, you will need additional dependencies included in the requirements.py but not in the setup.py.

The package includes an abstract base class for Wordle agents.
I've included a script showing how to evaluate your own software using wordle_benchmark!

`python scripts/sample_agent_definition.py --target_words "[plate, train]"`              

```
INFO:wordle_benchmark.benchmark.wordle_benchmark:Playing game with target word "plate"
INFO:wordle_benchmark.game.wordle_game:Starting game...
INFO:wordle_benchmark.game.wordle_game:Waiting for guess...
This agent predicts crane
INFO:wordle_benchmark.game.wordle_game:Received guess crane
INFO:wordle_benchmark.game.wordle_game:Waiting for guess...
This agent predicts state
INFO:wordle_benchmark.game.wordle_game:Received guess state
INFO:wordle_benchmark.game.wordle_game:Waiting for guess...
This agent predicts plate
INFO:wordle_benchmark.game.wordle_game:Received guess plate
INFO:wordle_benchmark.game.wordle_game:Ending game
INFO:wordle_benchmark.game.wordle_game:Correct! The word was plate
INFO:wordle_benchmark.benchmark.wordle_benchmark:Playing game with target word "train"
INFO:wordle_benchmark.game.wordle_game:Starting game...
INFO:wordle_benchmark.game.wordle_game:Waiting for guess...
This agent predicts crane
INFO:wordle_benchmark.game.wordle_game:Received guess crane
INFO:wordle_benchmark.game.wordle_game:Waiting for guess...
This agent predicts train
INFO:wordle_benchmark.game.wordle_game:Received guess train
INFO:wordle_benchmark.game.wordle_game:Ending game
INFO:wordle_benchmark.game.wordle_game:Correct! The word was train
BenchmarkResults(average_n_turns=2.5, average_turn_time=0.03678504625956217, percent_successes=1.0, std_turn_time=0.04001420116714126)
```

## Project structure
```
├── scripts
│   └── play_manual_game.py        |> Basic implementation to exercise the package and demo interfaces.
└── wordle_benchmark
    ├── agents
    │   └── wordle_agent.py        |> ABC of Wordle playing agent and sample concrete implementations.
    ├── dictionary
    │   └── wordle_dictionary.py   |> Dictionary of possible valid Wordle words.
    └── game
        ├── wordle_game.py         |> Logic to handle game play for a specific target word.
        └── wordle_words.py        |> Logic to compare guesses with target words, returning blacks, yellows, and greens.
```
