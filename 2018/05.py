data = open('input_05.txt').read()

def fetch_next(d):
    pos = iter(d)
    while True:
        val = '_'
        while val == '_':
            val = next(pos)
            yield val

def get_removed(data):
    new_data = []
    last_letter = None
    for letter in data:
        if last_letter is None:
            last_letter = letter
        elif letter == last_letter:
            new_data.append(last_letter)
            last_letter = letter
        elif letter.lower() == last_letter.lower():
            last_letter = None
        else:
            new_data.append(last_letter)
            last_letter = letter
    if last_letter:
        new_data.append(last_letter)
    return new_data, len(data) != len(new_data)

def polimerize(data):
    d, shortened = get_removed(data)
    while shortened:
        d, shortened = get_removed(d)
    return len(d)

print(f'Remaining units: {polimerize(data)}')

######################
import re

def get_min_poli(data):
    min_poli = len(data)
    for code in range(ord('a'), ord('z')+1):
        unit = chr(code) + chr(code).upper()
        #print(f'Unit is {unit}')
        d_simple = re.sub(f'[{unit}]', '', data)
        #print(f'Analyzing {d_simple}')
        new_len = polimerize(d_simple)
        #print(f'Got len {new_len}')
        if new_len < min_poli:
            min_poli = new_len
    return min_poli

print(f'Shortest polymer is {get_min_poli(data)}')