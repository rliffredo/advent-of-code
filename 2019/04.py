from collections import Counter

from common import pairwise


def generate_passwords(low_limit, up_limit):
    return (str(pwd) for pwd in range(low_limit, up_limit + 1))


def is_valid_password(pwd):
    if any(True for d1, d2 in pairwise(pwd) if d1 > d2):
        return False
    cnt = Counter(pwd)
    return cnt.most_common()[0][1] >= 2


def is_better_password(pwd):
    cnt = Counter(pwd)
    return 2 in cnt.values()


def filter_passwords(initial_list, criteria):
    return [pwd for pwd in initial_list if criteria(pwd)]


all_passwords = generate_passwords(134792, 675810)
valid_passwords = filter_passwords(all_passwords, is_valid_password)
print(f'There are {len(valid_passwords)} valid passwords')  # 1955
better_passwords = filter_passwords(valid_passwords, is_better_password)
print(f'There are {len(better_passwords)} better valid passwords')  # 1319
