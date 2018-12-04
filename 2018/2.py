from collections import Counter

data = open('input_2.txt').readlines()
data = [d.strip() for d in data]

number_of_twos = 0
number_of_threes = 0

for d in data:
    counter = Counter(d)
    if any(counter[letter] == 2 for letter in counter):
        number_of_twos += 1
    if any(counter[letter] == 3 for letter in counter):
        number_of_threes += 1

print(f'Twos: {number_of_twos}; Threes: {number_of_threes}; product: {number_of_twos * number_of_threes}')

#######

l = len(data[0])
for d1 in data:
    for d2 in data:
        ndiff = sum(1 if d1[n]!=d2[n] else 0 for n in range(l))
        if ndiff == 1:
            common = "".join([d1[n] for n in range(l) if d1[n]==d2[n]])
            found_d1 = d1
            found_d2 = d2

print(f'd1:     {found_d1}')
print(f'd2:     {found_d2}')
print(f'Common: {common}')
