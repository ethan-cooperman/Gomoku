import pygame
from enum import Enum
from Button import Button
pygame.init()


## COLORS ##
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,255,0)

## GAME CONSTANTS ##
WIDTH = 720
GRID_WIDTH = WIDTH // 144
WIN = pygame.display.set_mode((WIDTH, WIDTH))
FPS = 60

## FILE IMPORTS ##
WOOD_PICTURE = pygame.image.load('Assets/wooden_background.jpeg')
BACKGROUND = pygame.transform.scale(WOOD_PICTURE, (WIDTH, WIDTH))
HIGHLIGHT_PICTURE = pygame.image.load('Assets/light-alpha-gradient-transparency-and-translucency-web-browser-luz-9c61015f077b3ac9d8000909ca2f0115.png')
HIGHLIGHT = pygame.transform.scale(HIGHLIGHT_PICTURE, (WIDTH // 30,WIDTH // 30))
ENDSCREEN_FONT = pygame.font.SysFont('timesnewroman', WIDTH // 15, True)
STARTUP_FONT = pygame.font.SysFont('helveticaneue', WIDTH // 15, True, True)


## EVENTS ##
WHITE_WINS = pygame.USEREVENT + 1
BLACK_WINS = pygame.USEREVENT + 2
DRAW = pygame.USEREVENT + 3
## LOGIC METHODS ##

class Player(Enum):
    WHITE_PLAYER = 2
    BLACK_PLAYER = 3

def generate_new_board():
    game_board = []
    for i in range(1, 16):
        game_board.append([])
        for j in range(1, 16):
            game_board[i - 1].append(Intersection((i * (WIDTH // 16)), j * (WIDTH // 16), i, j))
    return game_board

class Intersection:
    '''
    constructor
    '''
    def __init__(self, x, y, row, column):
        self.x = x
        self.y = y
        self.row = row
        self.column = column
        self.state = None

    '''
    returns True if the mouse is hovering within 10 pixel radius of the intersection
    '''
    def is_mouse_hov(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return not self.state and abs(mouse_x - self.x) < WIDTH // 36 and abs(mouse_y - self.y) < WIDTH // 36
    
    '''
    returns True if the mouse is clicked when hovering on the intersection (if it's clicked on)
    '''
    def is_clicked_on(self):
        return self.is_mouse_hov() and pygame.mouse.get_pressed()[0]
    
    '''
    draws the intersection with piece / highlights as necessary
    '''
    def draw(self):
        if self.state == None and self.is_mouse_hov():
            WIN.blit(HIGHLIGHT, (self.x - HIGHLIGHT.get_width() // 2, self.y - HIGHLIGHT.get_height() // 2))
        elif self.state == Player.WHITE_PLAYER:
            pygame.draw.circle(WIN, WHITE, (self.x, self.y), WIDTH // 48)
        elif self.state == Player.BLACK_PLAYER:
            pygame.draw.circle(WIN, BLACK, (self.x, self.y), WIDTH // 48)

def calculate_move(game_state):
    turn, game_board = game_state
    for row in game_board:
        for intersection in row:
            if intersection.is_mouse_hov() and intersection.is_clicked_on() and turn:
                intersection.state = Player.WHITE_PLAYER
                turn = not turn
            elif intersection.is_mouse_hov() and intersection.is_clicked_on():
                intersection.state = Player.BLACK_PLAYER
                turn = not turn
    return (turn, game_board)

def check_win(game_state):
    game_board = game_state[1]
    # check row wins
    for row in game_board:
        for col in range(len(game_board) - 4):
            if row[col].state == row[col + 1].state and row[col].state == row[col + 2].state and row[col].state == row[col + 3].state and row[col].state == row[col + 4].state and row[col].state != None:
                return row[col].state
    # check column wins
    for row in range(len(game_board) - 4):
        for col in range(len(game_board)):
            if game_board[row][col].state == game_board[row + 1][col].state and game_board[row][col].state == game_board[row + 2][col].state and game_board[row][col].state == game_board[row + 3][col].state and game_board[row][col].state == game_board[row + 4][col].state and game_board[row][col].state != None:
                return game_board[row][col].state
    # check northeast wins
    for row in range(len(game_board) - 4):
        for col in range(len(game_board) - 4):
            if game_board[row][col].state == game_board[row + 1][col + 1].state and game_board[row][col].state == game_board[row + 2][col + 2].state and game_board[row][col].state == game_board[row + 3][col + 3].state and game_board[row][col].state == game_board[row + 4][col + 4].state and game_board[row][col].state != None:
                return game_board[row][col].state
    # check southeast wins
    for row in range(len(game_board) - 4):
        for col in range(4, len(game_board)):
            if game_board[row][col].state == game_board[row + 1][col - 1].state and game_board[row][col].state == game_board[row + 2][col - 2].state and game_board[row][col].state == game_board[row + 3][col - 3].state and game_board[row][col].state == game_board[row + 4][col - 4].state and game_board[row][col].state != None:
                return game_board[row][col].state
    return None

def check_draw(game_state):
    game_board = game_state[1]
    for row in game_board:
        for intersection in row:
            if intersection.state == None:
                return False
    return True

def game_loop(clock, game_state):
    run = True
    while run:
        clock.tick(FPS)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == WHITE_WINS:
                WIN.fill(WHITE)
                END_TEXT = ENDSCREEN_FONT.render("White Wins!", 1, BLACK)
                WIN.blit(END_TEXT, (WIDTH // 2 - END_TEXT.get_width() // 2, WIDTH // 2 - END_TEXT.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(3000)
                main()
            if event.type == BLACK_WINS:
                WIN.fill(BLACK)
                END_TEXT = ENDSCREEN_FONT.render("Black Wins!", 1, WHITE)
                WIN.blit(END_TEXT, (WIDTH // 2 - END_TEXT.get_width() // 2, WIDTH // 2 - END_TEXT.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(3000)
                main()
            if event.type == DRAW:
                WIN.fill(YELLOW)
                END_TEXT = ENDSCREEN_FONT.render("Draw", 1, BLACK)
                WIN.blit(END_TEXT, (WIDTH // 2 - END_TEXT.get_width() // 2, WIDTH // 2 - END_TEXT.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(3000)
                main()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause(clock, game_state)
        game_state = calculate_move(game_state)
        if check_win(game_state) == Player.WHITE_PLAYER:
            pygame.event.post(pygame.event.Event(WHITE_WINS))
        elif check_win(game_state) == Player.BLACK_PLAYER:
            pygame.event.post(pygame.event.Event(BLACK_WINS))
        elif check_draw(game_state):
            pygame.event.post(pygame.event.Event(DRAW))
        draw(game_state)

    pygame.quit()

def pause(clock, game_state):
    pause = True
    while pause:
        clock.tick(FPS)
        pygame.mouse.set_visible(False)
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
        WIN.blit(BACKGROUND, (0, 0))
        pygame.display.update()
    game_loop(clock, game_state)
                
## DRAW METHODS ##
def draw_board():
    WIN.blit(BACKGROUND, (0, 0))

    #render columns
    for i in range(1, 16):
        pygame.draw.rect(WIN, BLACK, pygame.Rect((WIDTH // 16) * i - (GRID_WIDTH // 2), WIDTH // 16, GRID_WIDTH, (WIDTH * 14) // 16))
    
    # TODO: render rows
    for i in range(1, 16):
        pygame.draw.rect(WIN, BLACK, pygame.Rect(WIDTH // 16, (WIDTH // 16) * i - (GRID_WIDTH // 2), (WIDTH * 14) // 16, GRID_WIDTH))
    
    
def draw_pieces(game_state):
    game_board = game_state[1]
    for row in game_board:
        for piece in row:
            piece.draw()

def draw_mouse(game_state):
    turn = game_state[0]
    if turn:
        pygame.draw.circle(WIN, WHITE,  pygame.mouse.get_pos(), WIDTH // 72)
    else:
        pygame.draw.circle(WIN, BLACK,  pygame.mouse.get_pos(), WIDTH // 72)

def draw(game_state):
    draw_board()
    draw_pieces(game_state)
    draw_mouse(game_state)
    pygame.display.update()

def start_up():
    WIN.blit(BACKGROUND, (0, 0))
    START_TEXT = STARTUP_FONT.render("Gomoku", 1, WHITE)
    WIN.blit(START_TEXT, (WIDTH // 2 - START_TEXT.get_width() // 2, WIDTH // 4))
    start_button = Button(WIN, 'Assets/start_button_image.png', WIDTH // 2 - WIDTH // 3, WIDTH // 2 - WIDTH // 8, 2 * WIDTH // 3, WIDTH // 4, 'Assets/start_button_on_hover.png')
    start_button.draw()
    pygame.display.update()
    return start_button.is_clicked_on()

def loading_screen():
    WIN.blit(BACKGROUND, (0, 0))
    LOADING_TEXT = STARTUP_FONT.render("Loading...", 1, WHITE)
    WIN.blit(LOADING_TEXT, (WIDTH // 2 - LOADING_TEXT.get_width() // 2, WIDTH // 2 - LOADING_TEXT.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1000)

## MAIN METHOD ##
def main():
    clock = pygame.time.Clock()
    game_state = (True, generate_new_board())
    start = False
    pygame.mouse.set_visible(True)
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        start = start_up()
    loading_screen()
    game_loop(clock, game_state)

if __name__ == '__main__':
    main()