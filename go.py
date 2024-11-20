import pygame
import sys
import random
import logic
import constants as cs

"""
Main environment to run the go game, handles all graphics and display

Color assignment: black = 1, white = 2
"""



class GoGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cs.SCREEN_SIZE, cs.SCREEN_SIZE))
        pygame.display.set_caption("Go Game")
        self.board = [[0 for _ in range(cs.BOARD_SIZE)] for _ in range(cs.BOARD_SIZE)]
        self.turn = 1
        self.running = True
        self.logic = logic.GameLogic(self)

    def draw_board(self):
        """Draws the Go board with grid lines."""
        self.screen.fill(cs.BOARD_COLOR)
        for x in range(cs.BOARD_SIZE):
            pygame.draw.line(self.screen, cs.BLACK, 
                             (cs.CELL_SIZE * x + cs.CELL_SIZE // 2, cs.CELL_SIZE // 2),
                             (cs.CELL_SIZE * x + cs.CELL_SIZE // 2, cs.SCREEN_SIZE - cs.CELL_SIZE // 2))
            pygame.draw.line(self.screen, cs.BLACK, 
                             (cs.CELL_SIZE // 2, cs.CELL_SIZE * x + cs.CELL_SIZE // 2),
                             (cs.SCREEN_SIZE - cs.CELL_SIZE // 2, cs.CELL_SIZE * x + cs.CELL_SIZE // 2))
            
        hoshi_points = self._hoshi_points()

        for x, y in hoshi_points:
            pygame.draw.circle(self.screen, cs.BLACK,
                               (cs.CELL_SIZE * x + cs.CELL_SIZE // 2, cs.CELL_SIZE * y + cs.CELL_SIZE // 2),
                               cs.HOSHI_RADIUS)
            
    def draw_stone(self, x, y, color):
        """Draws a stone on the board."""
        pygame.draw.circle(self.screen, color, 
                           (cs.CELL_SIZE * x + cs.CELL_SIZE // 2, cs.CELL_SIZE * y + cs.CELL_SIZE // 2),
                           cs.STONE_RADIUS)

    def get_board_position(self, pos):
        """Converts mouse position to board grid coordinates."""
        x, y = pos
        return (x // cs.CELL_SIZE, y // cs.CELL_SIZE)

    def is_valid_move(self, x, y):
        """Checks if a move is valid."""
        return 0 <= x < cs.BOARD_SIZE and 0 <= y < cs.BOARD_SIZE and self.board[y][x] == 0

    def draw_stones(self):
        """Draws all placed stones on the board."""
        for y in range(cs.BOARD_SIZE):
            for x in range(cs.BOARD_SIZE):
                if self.board[y][x] == 1:
                    self.draw_stone(x, y, cs.BLACK)
                elif self.board[y][x] == 2:
                    self.draw_stone(x, y, cs.WHITE)
        
    def hover_indicator(self):
        """Draws a hover indicator where the mouse is hovering."""
        mouse_pos = pygame.mouse.get_pos()
        x, y = self.get_board_position(mouse_pos)
        if 0 <= x < cs.BOARD_SIZE and 0 <= y < cs.BOARD_SIZE and self.board[y][x] == 0:
            hover_x = cs.CELL_SIZE * x + cs.CELL_SIZE // 2
            hover_y = cs.CELL_SIZE * y + cs.CELL_SIZE // 2
            pygame.draw.circle(self.screen, (150,150,150), (hover_x, hover_y), cs.STONE_RADIUS, 2)
    
    def handle_mouse_click(self, pos):
        """Handles a mouse click event to place stones. Returns True if valid, False otherwise"""
        x, y = self.get_board_position(pos)
        if self.logic.liberties(x,y) == 0:
            self.board[y][x] = 0
            return False
        elif self.is_valid_move(x, y):
            self.board[y][x] = self.turn
            self.turn = 3 - self.turn
            return True
    
    def menu(self):
        """Menu loop"""
        play_button = pygame.Rect(cs.SCREEN_SIZE//2-100,cs.SCREEN_SIZE//2+150,200,50)
        exit_button = pygame.Rect(cs.SCREEN_SIZE//2-100,cs.SCREEN_SIZE//2+220,200,50)

        menu_running = True

        self._menu_background()

        default_font = pygame.font.get_default_font()

        font = pygame.font.Font(default_font,36)

        caption_font = pygame.font.Font(default_font,12)
        caption_font.set_italic(True)

        welcome = font.render("WELCOME TO GRANT'S GO!",True,cs.BLACK)

        welcome_caption = caption_font.render("A classic 19x19 go game",True,cs.BLACK)

        self.screen.blit(welcome,(cs.SCREEN_SIZE // 2 - welcome.get_width() // 2, 20))
        self.screen.blit(welcome_caption, (cs.SCREEN_SIZE // 2 - welcome_caption.get_width() // 2, 60))

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

            play_text = font.render("Play", True, cs.BLACK)
            exit_text = font.render("Exit", True, cs.BLACK)

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
                    if self.handle_mouse_click(event.pos) == False:
                        print("Invalid Move: Suicide Formed")
                        
            self._handle_captures()
            self.draw_board()
            self.draw_stones()
            self._turn_background()
            self.hover_indicator()
            
            pygame.display.flip()
            

        pygame.quit()
        sys.exit()
    
    def _hoshi_points(self):
        """Calculates star/hoshi points based on the board size."""
        positions = [
            cs.BOARD_SIZE // 4,
            cs.BOARD_SIZE // 2,
            3 * cs.BOARD_SIZE // 4
        ]
        hoshi = []
        for x in positions:
            for y in positions:
                hoshi.append((x, y))
        return hoshi
    
    def _menu_background(self):
        """Helper function to draw the menu background"""
        self.screen.fill((240, 180, 120))

        for x in range(0, cs.SCREEN_SIZE, cs.CELL_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, cs.SCREEN_SIZE), 1)

        for y in range(0, cs.SCREEN_SIZE, cs.CELL_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (cs.SCREEN_SIZE, y), 1)
        
        for _ in range(random.randint(40,80)):
            x = random.randint(cs.BOARD_SIZE//4,3*cs.BOARD_SIZE//4+1)
            y = random.randint(cs.BOARD_SIZE//4,2*cs.BOARD_SIZE//3)

            color = cs.BLACK if random.choice([True, False]) else cs.WHITE

            pygame.draw.circle(self.screen, color,
                               (cs.CELL_SIZE * x , cs.CELL_SIZE * y),
                               cs.CELL_SIZE // 2 - 5)
    
    def _handle_captures(self):
        """Draws all placed stones on the board."""
        for y in range(cs.BOARD_SIZE):
            for x in range(cs.BOARD_SIZE):
                self.logic.captures(x,y)
    
    def _turn_background(self):
        default_font = pygame.font.get_default_font()
        font = pygame.font.Font(default_font,36)

        score_font = pygame.font.Font(default_font,12)
        score_font.set_italic(True)

        black_turn = font.render("Black's Turn",True,cs.BLACK)
        white_turn = font.render("White's Turn",True,cs.WHITE)

        black_captures = score_font.render("Captures: " + str(self.logic.captured[1]),True,cs.BLACK)
        white_captues = score_font.render("Captures: " + str(self.logic.captured[2]),True,cs.WHITE)
        
        if self.turn == 1:
            self.screen.blit(black_turn,(cs.SCREEN_SIZE//2 - black_turn.get_width() // 2, 20))
            self.screen.blit(black_captures, (cs.SCREEN_SIZE//2 - black_captures.get_width() // 2, 60))
        elif self.turn == 2:
            self.screen.blit(white_turn,(cs.SCREEN_SIZE//2 - white_turn.get_width() // 2, 20))
            self.screen.blit(white_captues, (cs.SCREEN_SIZE//2 - white_captues.get_width() // 2, 60))
        

        

        

        



def main():
    game = GoGame()
    game.menu()
    game.run()

if __name__ == "__main__":
    main()
