from typing import Tuple

from common import read_data


class Player:
    def __init__(self, raw_player: str):
        lines = raw_player.split("\n")
        self.name = lines[0].strip(":")
        self.deck = tuple(int(line) for line in lines[1:])
        self.history = set()
        self.original = self

    def copy(self, cards: int) -> 'Player':
        new_player = Player(self.name)
        new_player.deck = self.deck[:cards]
        new_player.original = self
        return new_player

    @property
    def has_cards(self):
        return bool(self.deck)

    @property
    def has_repeated_deck(self):
        return self.deck in self.history

    def play_card(self):
        self.history.add(self.deck)
        card, self.deck = self.deck[0], self.deck[1:]
        return card

    def assign_cards(self, cards: Tuple[int, int]):
        self.deck = self.deck + cards

    def score(self) -> int:
        cards_and_positions = list(enumerate(reversed(self.deck)))
        score = sum((n + 1) * c for n, c in cards_and_positions)
        return score


def init_players() -> Tuple[Player, Player]:
    raw_data = read_data("22", False)
    raw_player1, raw_player2 = raw_data.split("\n\n")
    return Player(raw_player1), Player(raw_player2)


def play_combat(player1: Player, player2: Player, recursive: bool) -> Tuple[Player, int]:
    game_round = 0
    while player1.has_cards and player2.has_cards:
        game_round += 1
        if player1.has_repeated_deck or player2.has_repeated_deck:
            return player1.original, game_round
        card1, card2 = player1.play_card(), player2.play_card()
        if recursive and len(player1.deck) >= card1 and len(player2.deck) >= card2:
            turn_winner, sub_rounds = play_combat(player1.copy(card1), player2.copy(card2), recursive)
            game_round += sub_rounds
        else:
            turn_winner = player1 if card1 > card2 else player2
        ordered_cards = (card1, card2) if turn_winner == player1 else (card2, card1)
        turn_winner.assign_cards(ordered_cards)

    game_winner = player1 if player1.has_cards else player2
    return game_winner.original, game_round


def part_1(print_result: bool = True) -> int:
    player1, player2 = init_players()
    winner, turn = play_combat(player1, player2 , False)
    result = winner.score()
    if print_result:
        print(f"{winner.name} wins 'Combat' after {turn} rounds with {result} points")
    return result


def part_2(print_result: bool = True) -> int:
    player1, player2 = init_players()
    winner, turn = play_combat(player1, player2, True)
    result = winner.score()
    if print_result:
        print(f"{winner.name} wins 'Recursive Combat' after {turn} rounds with {result} points")
    return result


SOLUTION_1 = 35818  # 527 rounds
SOLUTION_2 = 34771  # 361872 rounds (1543 the topmost)
IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    part_1()
    part_2()
