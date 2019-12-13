import sys

def calc_cell_power(x, y, serial_number):
    rack_id = x + 10
    rack_id_power = rack_id * y
    power_level = rack_id_power + serial_number
    power_level *= rack_id
    hundreds = (power_level // 100) % 10
    cell_power = hundreds - 5
    return cell_power

def calc_square_power(top_x, top_y, serial_number):
    return sum(
        calc_cell_power(x, y, serial_number)
        for x in range(top_x, top_x+3)
        for y in range(top_y, top_y+3)
    )

def get_highest_square(serial_number):
    squares = [
        (x, y, calc_square_power(x, y, serial_number))
        for x in range(1, 298)
        for y in range(1, 298)
    ]
    return max(squares, key=lambda s: s[2])


best_square = get_highest_square(5535)
print(f'The best square is at {best_square[0]},{best_square[1]}')

#################

def calc_square_power_1(top_x, top_y, size, serial_number):
    return sum(
        calc_cell_power(x, y, serial_number)
        for x in range(top_x, top_x+size)
        for y in range(top_y, top_y+size)
    )

def calc_square_power_2(previous_info, top_x, top_y, size, serial_number):
    first_column = sum(
            calc_cell_power(top_x, y, serial_number)
            for y in range(top_y, top_y+size)
        )
    middle_columns = sum(
            calc_cell_power(x, y, serial_number)
            for y in range(top_y, top_y+size)
            for x in range(top_x+1, top_x+size-1)
        ) if not previous_info else previous_info[1] - first_column + previous_info[2]
    last_column = sum(
            calc_cell_power(top_x+size-1, y, serial_number)
            for y in range(top_y, top_y+size)
        )
    return first_column, middle_columns, last_column

calculated_squares = {}
def calc_square_power_3(top_x, top_y, size, serial_number):
    internal_id = (top_x, top_y, size-1)
    try:
        internal_sum = calculated_squares[internal_id]
    except KeyError:
        if size>2:
            print('skipping cache')
        internal_sum = calc_square_power_1(top_x, top_y, size-1, serial_number)
    last_row = sum(
            calc_cell_power(x, top_y+size-1, serial_number)
            for x in range(top_x, top_x+size)
        )
    last_column = sum(
            calc_cell_power(top_x+size-1, y, serial_number)
            for y in range(top_y, top_y+size)
        )
    square_sum = internal_sum + last_row + last_column - calc_cell_power(top_x+size-1, top_y+size-1, serial_number)
    square_id = (top_x, top_y, size)
    calculated_squares[square_id] = square_sum
    return square_sum

def get_highest_square_2(size, serial_number):
    if size<3:
        squares = [
            (x, y, calc_square_power_1(x, y, size, serial_number))
            for x in range(1, 300-size+1)
            for y in range(1, 300-size+1)
        ]
    else:
        squares = []
        for y in range(1, 300-size+1):
            run_info = None
            for x in range(1, 300-size+1):
                run_info = calc_square_power_2(run_info, x, y, size, serial_number)
                squares.append((x, y, sum(run_info)))
    return max(squares, key=lambda s: s[2])

def get_highest_square_3(size, serial_number):
    sys.stdout.write('\b'*100 + f'Calculating values for square size {size}...')
    sys.stdout.flush()
    squares = [
        (x, y, calc_square_power_3(x, y, size, serial_number))
        for x in range(1, 300-size+1)
        for y in range(1, 300-size+1)
    ]
    return max(squares, key=lambda s: s[2])

def get_best_square_any_size(serial_number):
    best_for_sizes = []
    for size in range(1, 300):
        best = get_highest_square_3(size, serial_number)
        best_for_sizes.append((best, size))
    sys.stdout.write("\n")
    return max(best_for_sizes, key=lambda s: s[0][2])

best_area = get_best_square_any_size(5535)
print(f'The best area is at {best_area[0][0]},{best_area[0][1]} with size {best_area[1]}')
