from random import randint, choice, shuffle
from itertools import chain
from string import ascii_uppercase


class Crossword:
    def __init__(self, grid_size, words=[], allow_reverse = True):
        """

        :param grid_size:The NxN size of the grid
        :param words: The words in the word search
        :param allow_reverse: If True the words in the word search can appear in reverse/backwards
        """
        self.grid_size = grid_size
        self.words = words
        self.grid = []
        self.allow_reverse = allow_reverse
        self.word_index = 0

        self.create_grid()

        self.word = 'fast' #for testing
        self.reset_direction()
        ##TESTING METHOD
        # self._only_test()

    def create_grid(self):
        """Create a NxN grid with '0' as placeholders"""
        self.placeholder = '-'
        self.grid = [[self.placeholder for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        return self.grid

    def random_cell(self):
        """Choose a random starting cell for word"""

        # if self.direction == 'vertical':
        #     available_grid = [[0 for _ in range(self.grid_size-len(self.word)+1)] for _ in range(self.grid_size)]
        #     print(available_grid)
        #     available_grid[][] = '1'
        return (randint(0, self.grid_size-1), randint(0, self.grid_size-1))


    def reset_direction(self):
        self.directions = ['vertical', 'horizontal', 'diagonal_forward', 'diagonal_back']
        shuffle(self.directions)
        # print(self.directions)

    def build_grid(self):
        while self.word_index < len(self.words):
            self.word = self.words[self.word_index]

            if self.grid_size < len(self.word):
                raise IndexError("The word is too long to fit in the grid")

            # row, col = self.random_cell() #returns (row, column) of location
            # directions = ['vertical', 'horizontal', 'diagonal_forward', 'diagonal_back']
            self.direction = self.directions.pop()
            # print('******',len(self.directions))

            if self.direction == 'horizontal':
                horizontal_available = [[(j,i) for i in range(self.grid_size - len(self.word) + 1)] for j in range(self.grid_size)]
                horizontal_available = list(chain.from_iterable(horizontal_available))
                self.grid_temp = horizontal_available[::]
                self.find_space(self.grid_temp)


            if self.direction == 'vertical':
                vertical_available = [[(j,i) for i in range(self.grid_size )] for j in range(self.grid_size- len(self.word) + 1)]
                vertical_available = list(chain.from_iterable(vertical_available))
                self.grid_temp = vertical_available[::]
                self.find_space(self.grid_temp)

            if self.direction == 'diagonal_forward' or self.direction == 'diagonal_back':
                diagonal_available = [[(j,i) for i in range(self.grid_size)] for j in range(self.grid_size)]
                diagonal_available = list(chain.from_iterable(diagonal_available))
                self.grid_temp = diagonal_available[::]
                self.find_space(self.grid_temp)

        return self.fill_in_grid()

    def find_space(self,grid):
        """This method find avaialble space for the word by iterating through all open cells then removing them if that cells cannot hold the word.
        An index error is raised if the word cannot fit anywhere on the grid"""
        if len(grid) == 0:
            """
            If code gets here, it means that the word cannot be placed in the direction chosen.
            Remove that direction from the list of possibilities and try with a different direction.
            """
            self.build_grid()

        if len(self.directions)==4:
            """
            If code gets here, it means that the grid cannot be resolved (I think).
            I that case instead of raising an error we can just reset the everything and try again.
            """
            # self.create_grid()
            self.word_index == 0
            self.reset_direction()
            self.build_grid()
            return

        # print(len(grid), len(self.directions))
        cell = choice(grid)
        grid.pop(grid.index(cell))
        # print(len(grid))
        # print(grid)
        self.validate_location(cell[0], cell[1])


    def validate_location(self, row, col):
            if self.is_space(row,col):
                if self.is_fit(row,col):
                    self.place_word()
                    self.word_index +=1
                    self.reset_direction()
                else:
                    self.find_space(self.grid_temp)
            else:
                self.find_space(self.grid_temp)


    def is_space(self, row, col):
        """Returns if there is enough space to fit the word"""
        # directions = ['vertical', 'horizontal', 'diagonal_forward', 'diagonal_back']
        # self.direction = choice(directions)

        if self.direction == 'vertical':
            if self.grid_size - row < len(self.word):
                return False
            else:
                return True

        elif self.direction == 'horizontal':
            if self.grid_size - col < len(self.word):
                return False
            else:
                return True

        elif self.direction == 'diagonal_forward':
            if self.grid_size - row < len(self.word) or self.grid_size - col < len(self.word):
                return False
            else:
                return True

        elif self.direction == 'diagonal_back':
            if row < len(self.word) or self.grid_size - col < len(self.word):
                return False
            else:
                return True

    def is_fit(self,row,col):
        """Returns whether the word will fit in the cells"""
        self.coords = []
        if self.direction == 'vertical':
            for i in range(len(self.word)):
                # print('here')
                if self.grid[row + i][col] == self.placeholder or self.word[i] == self.grid[row + i][col]:
                    self.coords.append((row + i, col))
                else:
                    return False
            return True

        if self.direction == 'horizontal':
            for i in range(len(self.word)):
                # print('here')
                if self.grid[row][col + i] == self.placeholder or self.word[i] == self.grid[row][col + i]:
                    self.coords.append((row, col + i))
                else:
                    return False
            return True

        if self.direction == 'diagonal_forward':
            for i in range(len(self.word)):
                # print('here')
                if self.grid[row + i][col + i] == self.placeholder or self.word[i] == self.grid[row + i][col + i]:
                    self.coords.append((row + i, col + i))
                else:
                    return False
            return True

        if self.direction == 'diagonal_back':
            for i in range(len(self.word)):
                # print('here')
                if self.grid[row - i][col + i] == self.placeholder or self.word[i] == self.grid[row - i][col + i]:
                    self.coords.append((row - i, col + i))
                else:
                    return False
            return True


    def place_word(self):
        # print(coords)
        # Allow a 1 in 3 chance of a word being placed in reverse if allow_reverse is passed in as True (default)
        if self.allow_reverse == True:
            reverse_or_not = randint(1,3)
            if reverse_or_not == 1:
                self.coords = self.coords[::-1]
        # print(self.direction)
        for i, letter in enumerate(self.word):
            # print(i, letter)
            self.grid[self.coords[i][0]][self.coords[i][1]] = letter
        # print(self.grid)

    def fill_in_grid(self):
        self.grid = [[choice(ascii_uppercase) if char == self.placeholder else char for char in row] for row in self.grid]
        return self.grid

    def _only_test(self):
        """Method to test functionality"""
        self.grid[3][1] = 'e'
        self.grid[4][1] = 'a'
        self.grid[5][1] = 't'
        # print(self.grid)

    def __str__(self):
        my_str = ''
        for i in range(len(self.grid)):
            for cell in self.grid[i]:
                my_str += str(cell) + '  '
            my_str += '\n'
        return my_str

if __name__ == '__main__':
    crossword = Crossword(10, words=['PHP', 'JAVA', 'JAVASCRIPT', 'HTML', 'SWIFT', 'RUBY', 'FORTRAN', 'SQL', 'BASIC', 'RUST'], allow_reverse=True)
    # crossword.place_word('hello')
    data = crossword.build_grid()
    print(crossword)
    print(data)