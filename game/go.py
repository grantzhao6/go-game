import pygame
import sys

# Constants
BOARD_SIZE = 19
CELL_SIZE = 40
SCREEN_SIZE = BOARD_SIZE * CELL_SIZE
BOARD_COLOR = (250, 180, 100)
STONE_RADIUS = CELL_SIZE // 2 - 5
HOSHI_RADIUS = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GoGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Go Game")
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = 1
        self.running = True

        self.hoshi_points = [
            (3,3), (3,9), (3,15),
            (9,3), (9,9), (9,15),
            (15,3), (15,9), (15,15)
        ]

    def draw_board(self):
        """Draws the Go board with grid lines."""
        self.screen.fill(BOARD_COLOR)
        for x in range(BOARD_SIZE):
            pygame.draw.line(self.screen, BLACK, 
                             (CELL_SIZE * x + CELL_SIZE // 2, CELL_SIZE // 2),
                             (CELL_SIZE * x + CELL_SIZE // 2, SCREEN_SIZE - CELL_SIZE // 2))
            pygame.draw.line(self.screen, BLACK, 
                             (CELL_SIZE // 2, CELL_SIZE * x + CELL_SIZE // 2),
                             (SCREEN_SIZE - CELL_SIZE // 2, CELL_SIZE * x + CELL_SIZE // 2))
            
        for x,y in self.hoshi_points:
            pygame.draw.circle(self.screen, BLACK,
                               (CELL_SIZE * x + CELL_SIZE // 2, CELL_SIZE * y + CELL_SIZE // 2),
                               HOSHI_RADIUS)
    def draw_stone(self, x, y, color):
        """Draws a stone on the board."""
        pygame.draw.circle(self.screen, color, 
                           (CELL_SIZE * x + CELL_SIZE // 2, CELL_SIZE * y + CELL_SIZE // 2),
                           STONE_RADIUS)

    def get_board_position(self, pos):
        """Converts mouse position to board grid coordinates."""
        x, y = pos
        return (x // CELL_SIZE, y // CELL_SIZE)

    def is_valid_move(self, x, y):
        """Checks if a move is valid."""
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[y][x] == 0

    def handle_mouse_click(self, pos):
        """Handles a mouse click event."""
        x, y = self.get_board_position(pos)
        if self.is_valid_move(x, y):
            self.board[y][x] = self.turn
            self.turn = 3 - self.turn

    def draw_stones(self):
        """Draws all placed stones on the board."""
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.board[y][x] == 1:
                    self.draw_stone(x, y, BLACK)
                elif self.board[y][x] == 2:
                    self.draw_stone(x, y, WHITE)

    def run(self):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)

            self.draw_board()
            self.draw_stones()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GoGame()
    game.run()
