from common import read_line_groups


def parse_data():
    def parse_board(raw_board):
        board = {}
        for x, row in enumerate(raw_board):
            for y, cell in enumerate(row.split()):
                board[(x, y)] = [int(cell), False]
        return board

    raw_data = read_line_groups("04")
    numbers = [int(n) for n in raw_data[0][0].split(",")]
    boards = [parse_board(b) for b in raw_data[1:]]
    board_size = len(raw_data[1])
    return numbers, boards, board_size


def draw_number(n, board):
    for cell in board.values():
        if cell[0] == n:
            cell[1] = True


def winning(board, board_size):
    return any(all(board[(x, y)][1] for x in range(board_size)) for y in range(board_size)) or \
           any(all(board[(x, y)][1] for y in range(board_size)) for x in range(board_size))


def play_bingo(numbers, boards, board_size, on_winner):
    for n in numbers:
        for board_id, board in enumerate(boards):
            draw_number(n, board)
            if winning(board, board_size):
                result = on_winner(board_id, board, n)
                if result is not None:
                    return result
    return -1


def board_score(board, n):
    unmarked = sum(cell[0] for cell in board.values() if not cell[1])
    return n * unmarked


def part_1(print_result: bool = True) -> int:
    numbers, boards, board_size = parse_data()
    return play_bingo(numbers, boards, board_size, lambda _board_id, board, n: board_score(board, n))


def part_2(print_result: bool = True) -> int:
    numbers, boards, board_size = parse_data()
    winning_boards = set(range(len(boards)))

    def on_winner(board_id, board, n):
        winning_boards.difference_update({board_id})
        if len(winning_boards) == 0:
            return board_score(board, n)

    return play_bingo(numbers, boards, board_size, on_winner)


SOLUTION_1 = 63424
SOLUTION_2 = 23541

if __name__ == "__main__":
    print(part_1())
    print(part_2())
