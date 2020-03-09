class MapBuilder:

    def __init__(self):
        self.size = 8
        self.map = [[' ' for _ in range((self.size * 2 + 1) * 2 + 1)] for _ in range((self.size * 2 + 1) * 2 + 1)]
        self.last_track_num = 0
        self.row = self.size * 2 + 1
        self.col = self.size * 2 + 1
        self.map[self.row][self.col] = str(self.last_track_num)
        self.directions_of_wave_run = list()

    def update(self, just_turn_type, cells_are_driven_amount, walls_availability):
        if just_turn_type == 0:
            self.map[self.row - 1][self.col] = ' '
            self.directions_of_wave_run.append([0, 0, cells_are_driven_amount, 0])
            for i in range(cells_are_driven_amount):
                self.row -= 2
                self.last_track_num += 1
                self.map[self.row][self.col] = str(self.last_track_num)
                self.map[self.row][self.col - 1] = '|'
                self.map[self.row][self.col + 1] = '|'

        elif just_turn_type == 1:
            self.map[self.row][self.col - 1] = ' '
            self.directions_of_wave_run.append([0, 0, 0, cells_are_driven_amount])
            for i in range(cells_are_driven_amount):
                self.col -= 2
                self.last_track_num += 1
                self.map[self.row][self.col] = str(self.last_track_num)
                self.map[self.row - 1][self.col] = '-'
                self.map[self.row + 1][self.col] = '-'

        elif just_turn_type == 2:
            self.map[self.row + 1][self.col] = ' '
            self.directions_of_wave_run.append([cells_are_driven_amount, 0, 0, 0])
            for i in range(cells_are_driven_amount):
                self.row += 2
                self.last_track_num += 1
                self.map[self.row][self.col] = str(self.last_track_num)
                self.map[self.row][self.col - 1] = '|'
                self.map[self.row][self.col + 1] = '|'

        elif just_turn_type == 3:
            self.map[self.row][self.col + 1] = ' '
            self.directions_of_wave_run.append([0, cells_are_driven_amount, 0, 0])
            for i in range(cells_are_driven_amount):
                self.col += 2
                self.last_track_num += 1
                self.map[self.row][self.col] = str(self.last_track_num)
                self.map[self.row - 1][self.col] = '-'
                self.map[self.row + 1][self.col] = '-'

        self.map[self.row - 1][self.col] = ' '
        self.map[self.row][self.col - 1] = ' '
        self.map[self.row + 1][self.col] = ' '
        self.map[self.row][self.col + 1] = ' '

        if walls_availability[0]:
            self.map[self.row - 1][self.col] = '-'

        elif not walls_availability[0] and just_turn_type != 2:
            self.map[self.row - 2][self.col] = '?'

        if walls_availability[1]:
            self.map[self.row][self.col - 1] = '|'

        elif not walls_availability[1] and just_turn_type != 3:
            self.map[self.row][self.col - 1] = '?'

        if walls_availability[2]:
            self.map[self.row + 1][self.col] = '-'

        elif not walls_availability[2] and just_turn_type != 0:
            self.map[self.row + 2][self.col] = '?'

        if walls_availability[3]:
            self.map[self.row][self.col + 1] = '|'

        elif not walls_availability[3] and just_turn_type != 1:
            self.map[self.row][self.col + 2] = '?'

    def get_last_around_cells_states(self):
        self.map_build()
        return [self.map[self.row - 2][self.col] == '?' and not self.map[self.row - 1][self.col] == '|',
                self.map[self.row][self.col - 2] == '?' and not self.map[self.row][self.col - 1] == '-',
                self.map[self.row + 2][self.col] == '?' and not self.map[self.row + 1][self.col] == '|',
                self.map[self.row][self.col + 2] == '?' and not self.map[self.row][self.col + 1] == '-']

    def map_build(self):
        for i in range(len(self.map)):
            print(self.map[i])
            print()

    def is_map_built(self):
        flag = True
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == '?':
                    flag = False
        return flag

    def get_direction_of_inverse_wave_trace(self):
        temp = self.directions_of_wave_run.pop()
        for i in range(4):
            if temp[i] > 0:
                for _ in range(temp[i]):
                    if i == 0:
                        self.row -= 2
                    elif i == 1:
                        self.col -= 2
                    elif i == 2:
                        self.row += 2
                    elif i == 3:
                        self.col += 2
                    self.last_track_num = int(self.map[self.row][self.col])
                return i, temp[i]
