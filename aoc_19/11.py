from common import read_data, intcode


class PainterRobot:

    def __init__(self):
        self.ship_hull = {}
        self.current_x = 0
        self.current_y = 0
        self.current_direction = 'UP'
        self.current_mode = 'color'
        self.commands = []

    @property
    def current_position(self):
        return self.current_x, self.current_y

    def get_paint_color(self, position=None):
        position = position or self.current_position
        return self.ship_hull.get(position, 0)

    def set_paint_color(self, value):
        if self.current_mode == 'color':
            self.ship_hull[self.current_position] = value
        else:
            self._get_new_direction(value)
            self._advance()
            self._log_command(value)
        self._switch_current_mode()

    def print_hull(self):
        min_x = min(self.ship_hull.keys(), key=lambda p: p[0])[0]
        max_x = max(self.ship_hull.keys(), key=lambda p: p[0])[0]
        min_y = min(self.ship_hull.keys(), key=lambda p: p[1])[1]
        max_y = max(self.ship_hull.keys(), key=lambda p: p[1])[1]

        for y in range(max_y-min_y+1):
            line = []
            for x in range(max_x-min_x+1):
                color = '#' if self.get_paint_color((x, y)) == 1 else ' '
                line.append(color)
            print(''.join(line))

    def _log_command(self, value):
        self.commands.append((self.get_paint_color(), value))

    def _get_new_direction(self, value):
        command = 'left' if value == 0 else 'right'
        new_dirs = {
            ('UP', 'left'): 'LEFT',
            ('UP', 'right'): 'RIGHT',
            ('RIGHT', 'left'): 'UP',
            ('RIGHT', 'right'): 'DOWN',
            ('DOWN', 'left'): 'RIGHT',
            ('DOWN', 'right'): 'LEFT',
            ('LEFT', 'left'): 'DOWN',
            ('LEFT', 'right'): 'UP',
        }
        self.current_direction = new_dirs[(self.current_direction, command)]

    def _advance(self):
        if self.current_direction == 'UP':
            self.current_y -= 1
        elif self.current_direction == 'DOWN':
            self.current_y += 1
        elif self.current_direction == 'LEFT':
            self.current_x -= 1
        elif self.current_direction == 'RIGHT':
            self.current_x += 1
        else:
            assert False

    def _switch_current_mode(self):
        if self.current_mode == 'color':
            self.current_mode = 'move'
        else:
            self.current_mode = 'color'


################
# ## PART 1 ## #
################

robot = PainterRobot()
computer = intcode.IntCode(input_provider=robot.get_paint_color, output_provider=robot.set_paint_color)
computer.load(read_data("11"))
computer.execute()
print(f'Number of squares painted at least once: {len(robot.ship_hull)}')  # 1932


################
# ## PART 2 ## #
################

robot = PainterRobot()
robot.ship_hull[(0, 0)] = 1
computer = intcode.IntCode(input_provider=robot.get_paint_color, output_provider=robot.set_paint_color)
computer.load(read_data("11"))
computer.execute()
robot.print_hull()  # EGHKGJER
