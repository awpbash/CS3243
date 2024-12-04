class CSP:
    def __init__(self, rows, cols, squares, obstacles):
        """
        Initialize the CSP solver with the grid size, available squares, and obstacles.
        """
        self.rows = rows
        self.cols = cols
        self.squares = squares.copy()  #Copy to avoid modifying the input data directly
        self.obstacles = set(obstacles)
        self.grid = [[0] * cols for i in range(rows)]  #create empty grid
        self.solution = [] #list to store the solution

    def is_placeable(self, size, row, col):
        """
        This one checks if a square of a given size can be placed at a given position.
        If can place, return True, else return False
        """
        if row + size > self.rows or col + size > self.cols:
            return False  #OOB check

        #check that the grid we are checking can fit the square, if got 1 obstacle or square, return False
        for r in range(row, row + size):
            for c in range(col, col + size):
                if self.grid[r][c] != 0 or (r, c) in self.obstacles:
                    return False
        return True

    def mark_square(self, size, row, col, place):
        """
        Mark the grid if a square is placed.
        """
        if place:
            value = size
        else:
            value = 0
        for r in range(row, row + size):
            for c in range(col, col + size):
                self.grid[r][c] = value

    def find_next_empty(self, row, col):
        """
        Find the next empty cell that is not filled by a square or obstacle
        """
        while row < self.rows:
            while col < self.cols:
                if self.grid[row][col] == 0 and (row, col) not in self.obstacles:
                    return row, col #empty spot found hehe
                col += 1
            row += 1
            col = 0 #count from next row
        return None, None  #no empty spots left

    def backtrack(self):

        if not any(self.squares.values()):
            return True #no more squares to place means SOLVED

        #Find the next empty position to start placing
        row, col = self.find_next_empty(0, 0)
        if row is None:
            return True  #no more empty spots left

        #Place the largest available square first
        for size in sorted(self.squares.keys(), reverse=True):
            if self.squares[size] == 0:
                continue

            if self.is_placeable(size, row, col):
                #if can place, we mark then reduce count then add to solution
                self.mark_square(size, row, col, True)
                self.solution.append((size, row, col))
                self.squares[size] -= 1
                #Recursively try to place the next square
                if self.backtrack():
                    return True

                #if cannot then we just backtrack
                self.mark_square(size, row, col, False)
                self.solution.pop()
                self.squares[size] += 1  #add back the square we tried to place

        return False  #no valid placement found for this square

    def solve(self):
        """
        Start the CSP solver and return the solution (if found).
        Returns a list of tuples representing placed squares (size, row, col).
        """
        if self.backtrack():
            return self.solution
        return []

def solve_CSP(dct):
    rows = dct['rows']
    cols = dct['cols']
    input_squares = dct['input_squares']
    obstacles = dct['obstacles']

    solver = CSP(rows, cols, input_squares, obstacles)
    return solver.solve()

"""
Aight big guy here's the big deal
Greedy method is to fit big squares first
We create a grid of 0s. If we can fit a square, we mark the grid with the size of the square
now instead of naively checking if 

Since it is constraint that all grid will be filled by either square or obstacle,
if the square no longer contains 0 then we have solved it

So right, we fit biggest square first, then we backtrack if we cannot fit the square
Once we fit a square, instead of trying brute forcing the next square, we first find the next empty spot
Then we fit the next biggest square there, and so on

This way we prune the search space
"""