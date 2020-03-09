class SelfLocation:
    map = [[' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', ' ', ' ', '-', ' '],
           ['|', '0', ' ', '0', ' ', '0', ' ', '0', ' ', '0', ' ', '0', '|', ' ', '|', '0', '|'],
           [' ', ' ', ' ', '-', ' ', ' ', ' ', '-', ' ', '-', ' ', ' ', ' ', '-', ' ', ' ', ' '],
           ['|', '0', '|', ' ', '|', '0', '|', '0', '|', ' ', '|', '0', ' ', '0', ' ', '0', '|'],
           [' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', '-', ' ', '-', ' '],
           ['|', '0', ' ', '0', ' ', '0', '|', '0', ' ', '0', ' ', '0', '|', ' ', '|', '0', '|'],
           [' ', '-', ' ', '-', ' ', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', '-', ' ', ' ', ' '],
           ['|', '0', '|', ' ', '|', '0', '|', '0', '|', ' ', '|', '0', ' ', '0', ' ', '0', '|'],
           [' ', ' ', ' ', '-', ' ', ' ', ' ', '-', ' ', '-', ' ', ' ', ' ', '-', ' ', ' ', ' '],
           ['|', '0', ' ', '0', ' ', '0', ' ', '0', ' ', '0', ' ', '0', '|', ' ', '|', '0', '|'],
           [' ', ' ', ' ', '-', ' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', '-', ' ', '-', ' '],
           ['|', '0', '|', ' ', '|', '0', '|', ' ', '|', '0', ' ', '0', ' ', '0', ' ', '0', '|'],
           [' ', '-', ' ', '-', ' ', ' ', ' ', '-', ' ', '-', ' ', ' ', ' ', '-', ' ', ' ', ' '],
           ['|', '0', ' ', '0', ' ', '0', ' ', '0', '|', ' ', '|', '0', '|', ' ', '|', '0', '|'],
           [' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', '-', ' ', '-', ' ', '-', ' ', ' ', ' '],
           ['|', '0', '|', ' ', '|', '0', ' ', '0', ' ', '0', ' ', '0', ' ', '0', ' ', '0', '|'],
           [' ', '-', ' ', ' ', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ', '-', ' ']]

    def main(self, movement_directions, i, j):
        self.trying(movement_directions, i, j)
        for i in range(len(movement_directions)):
            if movement_directions[i] == 0:
                movement_directions[i] == 3
            elif movement_directions[i] == 1:
                movement_directions[i] == 0
            elif movement_directions[i] == 2:
                movement_directions[i] == 1
            elif movement_directions[i] == 3:
                movement_directions[i] == 2
        self.trying(movement_directions, i, j)
        for i in range(len(movement_directions)):
            if movement_directions[i] == 0:
                movement_directions[i] == 3
            elif movement_directions[i] == 1:
                movement_directions[i] == 0
            elif movement_directions[i] == 2:
                movement_directions[i] == 1
            elif movement_directions[i] == 3:
                movement_directions[i] == 2
        self.trying(movement_directions, i, j)
        for i in range(len(movement_directions)):
            if movement_directions[i] == 0:
                movement_directions[i] == 3
            elif movement_directions[i] == 1:
                movement_directions[i] == 0
            elif movement_directions[i] == 2:
                movement_directions[i] == 1
            elif movement_directions[i] == 3:
                movement_directions[i] == 2
        self.trying(movement_directions, i, j)
        for i in range(len(movement_directions)):
            if movement_directions[i] == 0:
                movement_directions[i] == 3
            elif movement_directions[i] == 1:
                movement_directions[i] == 0
            elif movement_directions[i] == 2:
                movement_directions[i] == 1
            elif movement_directions[i] == 3:
                movement_directions[i] == 2
        for i in range(len(map)):
            for j in range(len(map[i])):
                if i != 0 and j != 0:
                    self.main(movement_directions, i, j)

    def trying(self, movement_directions, i, j):
        temp_i = i
        temp_j = j
        for num in range(len(movement_directions)):
            if movement_directions == 0:
                if map[temp_i - 1][temp_j] == '0' | | map[i - 1][j] == ' ':
                    temp_i -= 1
            elif movement_directions == 1:

            elif movement_directions == 1:

            elif movement_directions == 1:
