import pygame
import sys
import random

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
            
        hoshi_points = self._hoshi_points()

        for x, y in hoshi_points:
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

    def draw_stones(self):
        """Draws all placed stones on the board."""
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.board[y][x] == 1:
                    self.draw_stone(x, y, BLACK)
                elif self.board[y][x] == 2:
                    self.draw_stone(x, y, WHITE)
        
    def hover_indicator(self):
        """Draws a hover indicator where the mouse is hovering."""
        mouse_pos = pygame.mouse.get_pos()
        x, y = self.get_board_position(mouse_pos)
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[y][x] == 0:
            hover_x = CELL_SIZE * x + CELL_SIZE // 2
            hover_y = CELL_SIZE * y + CELL_SIZE // 2
            pygame.draw.circle(self.screen, (150,150,150), (hover_x, hover_y), STONE_RADIUS, 2)
    
    def handle_mouse_click(self, pos):
        """Handles a mouse click event."""
        x, y = self.get_board_position(pos)
        if self.is_valid_move(x, y):
            self.board[y][x] = self.turn
            self.turn = 3 - self.turn
    
    def menu(self):
        play_button = pygame.Rect(SCREEN_SIZE//2-100,SCREEN_SIZE//2+150,200,50)
        exit_button = pygame.Rect(SCREEN_SIZE//2-100,SCREEN_SIZE//2+220,200,50)

        menu_running = True

        self._menu_background()

        default_font = pygame.font.get_default_font()

        font = pygame.font.Font(default_font,36)

        caption_font = pygame.font.Font(default_font,12)
        caption_font.set_italic(True)

        welcome = font.render("WELCOME TO GRANT'S GO!",True,BLACK)

        welcome_caption = caption_font.render("A classic 19x19 go game",True,BLACK)

        self.screen.blit(welcome,(SCREEN_SIZE // 2 - welcome.get_width() // 2, 20))
        self.screen.blit(welcome_caption, (SCREEN_SIZE // 2 - welcome_caption.get_width() // 2, 60))

        while menu_running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            pygame.draw.rect(self.screen,(200,200,200),play_button)
            pygame.draw.rect(self.screen,(200,200,200),exit_button)

            if play_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen,(170,170,170),play_button)
                if mouse_click[0]:
                    menu_running = False
            
            if exit_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen,(170,170,170),exit_button)
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            play_text = font.render("Play", True, BLACK)
            exit_text = font.render("Exit", True, BLACK)

            self.screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2,
                                         play_button.centery - play_text.get_height() // 2))
            self.screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2,
                                         exit_button.centery - exit_text.get_height() // 2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()


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
            self.hover_indicator()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
    
    def _hoshi_points(self):
        """Calculates star points based on the board size."""
        positions = [
            BOARD_SIZE // 4,
            BOARD_SIZE // 2,
            3 * BOARD_SIZE // 4
        ]
        hoshi = []
        for x in positions:
            for y in positions:
                hoshi.append((x, y))
        return hoshi
    
    def _menu_background(self):
        self.screen.fill((240, 180, 120))

        for x in range(0, SCREEN_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, SCREEN_SIZE), 1)

        for y in range(0, SCREEN_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (SCREEN_SIZE, y), 1)
        
        for _ in range(random.randint(40,80)):
            x = random.randint(BOARD_SIZE//4,3*BOARD_SIZE//4)
            y = random.randint(BOARD_SIZE//4,2*BOARD_SIZE//3)

            color = BLACK if random.choice([True, False]) else WHITE

            pygame.draw.circle(self.screen, color,
                               (CELL_SIZE * x + CELL_SIZE // 2, CELL_SIZE * y + CELL_SIZE // 2),
                               CELL_SIZE // 2 - 5)



def main():
    game = GoGame()
    game.menu()
    game.run()

if __name__ == "__main__":
    main()
