from dataclasses import dataclass
from typing import Optional

@dataclass
class Marble:
    value: int
    next_cw: Optional['Marble']
    next_ccw: Optional['Marble']
    
class MarbleCircle:

    def __init__(self):
        self.current = None
        self.first = None

    def next_cw(self):
        return self.current.next_cw
    
    def second_next_cw(self):
        return self.next_cw().next_cw

    def add_new_marble(self, marble):
        if self.current is None:
            self.update_circle(marble, marble, marble)
            self.first = marble
        else:
            self.update_circle(marble, self.next_cw(), self.second_next_cw())
        self.current = marble
    
    def remove_marble_seven_ccw(self):
        first_ccw = self.current.next_ccw
        second_ccw = first_ccw.next_ccw
        third_ccw = second_ccw.next_ccw
        fourth_ccw = third_ccw.next_ccw
        fifth_ccw = fourth_ccw.next_ccw
        sixth_ccw = fifth_ccw.next_ccw
        seventh_ccw = sixth_ccw.next_ccw
        eight_ccw = seventh_ccw.next_ccw
        # Update
        sixth_ccw.next_ccw = eight_ccw
        eight_ccw.next_cw = sixth_ccw
        self.current = seventh_ccw.next_cw
        return seventh_ccw.value
    
    def update_circle(self, new_marble, first_cw, second_cw):
        new_marble.next_cw = second_cw
        new_marble.next_ccw = first_cw
        first_cw.next_cw = new_marble
        second_cw.next_ccw = new_marble
    
    def __repr__(self):
        marbles = [self.first]
        while marbles[-1].next_cw.value != self.first.value:
            marbles.append(marbles[-1].next_cw)
        return marbles

    def __str__(self):
        marbles = [str(m.value) for m in self.__repr__()]
        return ",".join(marbles)


class Players:
    def __init__(self, number_of_elves):
        self.players = [0] * number_of_elves
        self.current_player = -1
    
    def get_next_player(self):
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0
        return self.current_player

    def add_score(self, player, score):
        self.players[player] += score
    
    def get_highest_score(self):
        return max(self.players)


def play_marble(value, mc, pl):
    player = pl.get_next_player()
    if value and value % 23 == 0:
        pl.add_score(player, value)
        bonus = mc.remove_marble_seven_ccw()
        pl.add_score(player, bonus)
    else:
        m = Marble(value=value, next_cw=None, next_ccw=None)
        mc.add_new_marble(m)


def play_game(max_marble, number_of_elves):
    mc = MarbleCircle()
    pl = Players(number_of_elves)
    for value in range(max_marble):
        play_marble(value, mc, pl)
    return mc, pl


mc, pl = play_game(72170, 470)
print(f'Higest score is {pl.get_highest_score()}')

#######

mc, pl = play_game(72170*100, 470)
print(f'Higest score for 100 times longer case is {pl.get_highest_score()}')
