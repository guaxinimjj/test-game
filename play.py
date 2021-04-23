import argparse
import random

from functools import partial

# Settings
ATTACK_IN_SMALL_RANGE_LOW = 18
ATTACK_IN_SMALL_RANGE_HIGH = 25
ATTACK_IN_LARGE_RANGE_LOW = 10
ATTACK_IN_LARGE_RANGE_HIGH = 35
HEAL_LOW = ATTACK_IN_SMALL_RANGE_LOW
HEAL_HIGH = ATTACK_IN_SMALL_RANGE_HIGH


class Player:
    """The Player's class stores HP and the maximum amount of HP,
    has methods for dealing moderate to high damage, as well as healing."""

    def __init__(self, name: str, max_hp: int):
        self.hp = max_hp
        self.max_hp = max_hp
        self.name = name

    @property
    def hp_percent(self) -> int:
        """ Method for checking HP in percent. """
        return int((self.hp / self.max_hp) * 100)

    def attack_in_small_range(self, opponent: "Player") -> int:
        """ Method for attack in small range. """
        return self._attack(
            opponent,
            low=ATTACK_IN_SMALL_RANGE_LOW,
            high=ATTACK_IN_SMALL_RANGE_HIGH,
        )

    def attack_in_large_range(self, opponent: "Player") -> int:
        """ Method for attack in large range."""
        return self._attack(
            opponent,
            low=ATTACK_IN_LARGE_RANGE_LOW,
            high=ATTACK_IN_LARGE_RANGE_HIGH,
        )

    def heal(self, low: int = HEAL_LOW, high: int = HEAL_HIGH) -> int:
        """ Method for healing: restores HP points according to the maximum amount of HP. """
        amount = random.randint(low, high)

        if self.hp + amount > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp += amount

        return amount

    def _attack(self, opponent: "Player", *, low: int, high: int) -> int:
        """ The method of inflicting damage on the enemy."""
        amount = random.randint(low, high)

        if opponent.hp - amount < 0:
            opponent.hp = 0
        else:
            opponent.hp -= amount

        return amount


class Computer(Player):
    """ Class for the computer inherited from the Player class."""

    def heal(self, low: int = HEAL_LOW, high: int = HEAL_HIGH) -> int:
        """ Overriding the healing method when health is below 35% increase the healing."""
        if self.hp_percent < 35:
            print("Computer HP below 35%, increased chances to heal")
            high *= 2
        return super().heal(low=low, high=high)


class Game:
    """Game class. Accepts two users. The sequence of moves is determined randomly.
    After each action, prints a message."""

    def __init__(self, player: Player, computer: Computer):
        self.player = player
        self.computer = computer

        self.players = [self.player, self.computer]

    @property
    def in_progress(self):
        """ The game ends when health drops to 0."""
        return all([player.hp > 0 for player in self.players])

    def play(self):
        while self.in_progress:
            # Random move selection.
            random.shuffle(self.players)
            player, opponent = self.players

            # Random choice of action.
            description, action = random.choice(
                [
                    (
                        "attack in small range",
                        partial(player.attack_in_small_range, opponent),
                    ),
                    (
                        "attack in large range",
                        partial(player.attack_in_large_range, opponent),
                    ),
                    ("heal", player.heal),
                ]
            )
            amount = action()

            # Displaying messages.
            print(f"{player.name} decided to {description} with {amount} points.")
            print(
                f"{self.player.name}: {self.player.hp} HP\n"
                f"{self.computer.name}: {self.computer.hp} HP",
            )

        print("Game over!")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-hp",
        type=int,
        default=100,
        help="Maximum player's health",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    max_hp = args.max_hp

    game = Game(
        player=Player("Player", max_hp),
        computer=Computer("Computer", max_hp),
    )
    game.play()


if __name__ == "__main__":
    main()
