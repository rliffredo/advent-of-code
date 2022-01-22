import functools
import itertools

from common import read_data


def parse_data():
    lines = read_data("21", True)
    return [int(lines[0].split()[-1]), int(lines[1].split()[-1])]


def new_state(new_state_for_player, player_id, old_state):
    other_player = (player_id + 1) % 2
    new_results = [0, 0]
    new_results[player_id] = new_state_for_player
    new_results[other_player] = old_state[other_player]
    return tuple(new_results)


def move_player(player, scores, players, r1, r2, r3, print_debug):

    movement = r1 + r2 + r3
    new_position = ((players[player] - 1) + movement) % 10 + 1
    new_score = scores[player] + new_position
    if print_debug:
        print(f"Player {player + 1} rolls {r1}+{r2}+{r3} and moves to space {new_position} "
              f"for a total score of {new_score}.")

    new_scores = new_state(new_score, player, scores)
    new_positions = new_state(new_position, player, players)

    return new_scores, new_positions


def play_game_1(players, print_debug):
    scores = [0, 0]
    dice = itertools.cycle(range(1, 101))
    rolls = 0
    while True:
        rolls += 3
        scores, players = move_player(0, scores, players, next(dice), next(dice), next(dice), print_debug)
        if scores[0] >= 1000:
            break
        rolls += 3
        scores, players = move_player(1, scores, players, next(dice), next(dice), next(dice), print_debug)
        if scores[1] >= 1000:
            break
    return rolls, scores, players


def part_1(print_result: bool = True) -> int:
    players = parse_data()
    results = play_game_1(players, print_result)
    if print_result:
        print(results)
    return results[0] * min(results[1])


@functools.cache
def play_game_2(scores, players, player_to_move):
    possibilities = (move_player(player_to_move, scores, players, *roll, False) for roll in play_game_2.rolls)
    wins = [0, 0]
    for universe in possibilities:
        new_scores, new_positions = universe
        if new_scores[player_to_move] >= 21:
            wins[player_to_move] += 1
        else:
            other_player = (player_to_move + 1) % 2
            branch_wins = play_game_2(new_scores, new_positions, other_player)
            wins[0] += branch_wins[0]
            wins[1] += branch_wins[1]
    return wins


play_game_2.rolls = list(itertools.product([1, 2, 3], repeat=3))


def part_2(print_result: bool = True) -> int:
    players = parse_data()
    results = play_game_2((0, 0), tuple(players), 0)
    if print_result:
        print(results)
    return max(results)


SOLUTION_1 = 605070
SOLUTION_2 = 218433063958910

if __name__ == "__main__":
    print(part_1())
    print(part_2())
