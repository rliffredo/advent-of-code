def read_data(day, by_lines=False):
    file_name = f'data/{day}.txt'
    f = open(file_name)
    data = f.read()
    return data.split('\n') if by_lines else data
