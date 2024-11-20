import go
import constants as cs

"""
Handles all game logic including captures, liberties, territories, and score.

Color assignment: black = 1, white = 2
"""

class GameLogic:
    def __init__(self, game:go.GoGame) -> None:
        self.go = game
        self.captured = {1:0,2:0}


    def captures(self,x,y):
        color = self.go.board[y][x]

        opponent_color = 3-color

        captures = []

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cs.BOARD_SIZE and 0 <= ny < cs.BOARD_SIZE and self.go.board[ny][nx] == opponent_color:
                if self.liberties(nx, ny) == 0:
                    captures.append((nx, ny))
        
        for cx, cy in captures:
            total_captures = self.remove_group(cx, cy)
            self.captured[color] = total_captures

    def liberties(self, x, y):
        """Finds the number of liberties for a group of pieces containing the coordinates (x,y)"""
        color = self.go.board[y][x]
        visited = set()
        return self._dfs_liberties(x,y,color,visited)

    def _dfs_liberties(self,x,y,color,visited):
        """Helper function using dfs to find the number of liberties"""
        if (x,y) in visited:
            return 0
        
        visited.add((x,y))
        liberties = 0

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cs.BOARD_SIZE and 0 <= ny < cs.BOARD_SIZE:
                if self.go.board[ny][nx] == 0:
                    liberties += 1
                elif self.go.board[ny][nx] == color:
                    liberties += self._dfs_liberties(nx, ny, color, visited)
        
        return liberties
    
    def remove_group(self, x, y):
        """Removes all stones in the group containing (x, y) and returns the number of captured pieces."""
        color = self.go.board[y][x]
        remove = set()
        self._dfs_group(x, y, color, remove)

        captured = 0
        for x, y in remove:
            self.go.board[y][x] = 0
            captured += 1
        
        return captured

    def _dfs_group(self, x, y, color, remove):
        """Helper function to find all stones in the group using DFS."""
        if (x, y) in remove:
            return
        
        remove.add((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cs.BOARD_SIZE and 0 <= ny < cs.BOARD_SIZE and self.go.board[ny][nx] == color:
                self._dfs_group(nx, ny, color, remove)
    
