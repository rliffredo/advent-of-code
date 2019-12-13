data = open('input_01.txt').readlines()
data = [d.strip() for d in data]
data = [int(d) for d in data]
cnt = sum(data)
print(f'Frequency is {cnt}')

######

known_numbers = set()
current = 0
while current not in known_numbers:
    for d in data:
        known_numbers.add(current)
        current += d
        if current in known_numbers:
            print(f'First frequency reached twice is {current}')
            break
