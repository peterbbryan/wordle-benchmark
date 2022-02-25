# wordle-benchmark
A performant Wordle simulator for benchmarking and evaluating agents.

Do you like Wordle? I like Wordle. 
I wanted to see if I could my computer to play a decent game, but I couldn't find a good way to grade my agents.
I put together a Python package to play Wordle games and keep track of game statistics.

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
