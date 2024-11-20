import go
import constants as cs

"""
Handles all game logic including captures, liberties, territories, and score.

Color assignment: black = 1, white = 2
"""

class GameLogic:
    def __init__(self) -> None:
        self.go = go.GoGame()
        self.captured = {1:0,2:0}


    def captures(self,x,y):
        color = self.go.board[y][x]




    def liberties(self, x, y):
        """Finds the number of liberties for a group of pieces containing the coordinates (x,y)"""
        assert color == 1 or color == 2
        color = self.go.board[y][x]
        return self._dfs_liberties(x,y,color)

    def _dfs_liberties(self,x,y,color):
        """Helper function using dfs to find the number of liberties"""
        visited = set()

        if (x,y) in visited:
            return 0
        
        visited.add((x,y))
        liberties = 0

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cs.BOARD_SIZE and 0 <= ny < cs.BOARD_SIZE:
                if self.go.board[ny][nx] == 0:
                    liberties += 1
                elif self.board[ny][nx] == color:
                    liberties += self._dfs_liberties(nx, ny, color, visited)
        
        return liberties
    
