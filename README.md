#Console game.

Modeling the game as a console application. Participants are: Computer and Player.
The sequence of moves is determined
randomly. Each of the players has the same number of
health (default, 100). When the health of the Computer reaches 35%, 
increase its chance of healing.
The game ends if one of the participants has reached 0 health.

### Prerequisites:

```commandline
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the game:

```commandline
python play.py
```

### Run the game with not default HP:
#### Where int is max HP.
```commandline
python play.py --max-hp=int
```