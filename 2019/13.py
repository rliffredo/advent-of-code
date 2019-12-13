import intcode
from common import read_data


class ArcadeCabinet:

    TILE_TYPES = {
        0: ' ',  # Empty
        1: '%',  # Wall
        2: '#',  # Block
        3: '-',  # Paddle
        4: '*',  # Ball
    }

    MAX_X = 40
    MAX_Y = 24

    def __init__(self, player=None):
        self.screen = {}
        self.score = 0
        self.screen_command = list()
        self.computer = intcode.IntCode(input_provider=self.joystick, output_provider=self.graphic_adapter)
        self.computer.load(read_data("13"))
        self.player = player

    def insert_coin(self):
        self.computer.memory[0] = 2

    def play(self):
        self.computer.execute()

    def graphic_adapter(self, value):
        self.screen_command.append(value)
        if len(self.screen_command) == 3:
            if self.screen_command[0] == -1:
                self.score = value
                self.screen_command = []
            else:
                position = tuple(self.screen_command[:2])
                self.screen[position] = self.screen_command[2]
                if self.player:
                    self.player.updated_screen(position)
                self.screen_command = []

    def joystick(self):
        value = self.player.decide_move() if self.player else 0
        return value

    def print_screen(self):
        print(f'Score: {self.score}       Credits: {self.computer.memory[0]}')
        for y in range(ArcadeCabinet.MAX_Y+1):
            line = [ArcadeCabinet.TILE_TYPES[self.screen[(x, y)]] for x in range(ArcadeCabinet.MAX_X+1)]
            print(''.join(line))


################
# ## PART 1 ## #
################

cabinet = ArcadeCabinet()
cabinet.play()
print(f'Number of block tiles on the screen: {sum(1 for p in cabinet.screen.values() if p == 2)}')  # 230
cabinet.print_screen()


################
# ## PART 2 ## #
################

class Player:
    def __init__(self, cabinet):
        self.cabinet = cabinet
        self.cabinet.player = self
        self.paddle_x = (0, 0)
        self.ball_x = (0, 0)

    def updated_screen(self, position):
        if self.cabinet.screen[position] == 3:
            self.paddle_x = position[0]
        elif self.cabinet.screen[position] == 4:
            self.ball_x = position[0]

    def decide_move(self):
        if self.paddle_x > self.ball_x:
            return -1
        elif self.paddle_x < self.ball_x:
            return 1
        else:
            return 0


cabinet = ArcadeCabinet()
Player = Player(cabinet)
cabinet.insert_coin()
cabinet.play()
cabinet.print_screen()
print(f'Score at the end: {cabinet.score}')  # 11140
