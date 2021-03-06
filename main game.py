import pygame



def drawGrid():
    global screen
    blockSize = 300  # Set the size of the grid block
    for x in range(0, width, blockSize):
        for y in range(0, height, blockSize):
            rect = pygame.Rect(x, y,
                               blockSize, blockSize)
            pygame.draw.rect(screen, BLACK, rect, 1)


def get_diag_winner(placed):
    diag1 = []
    diag2 = []
    for block, player in zip(placed.keys(), placed.values()):
        x, y = block
        if x + y != 1 or x + y != 3:
            if x == y:
                diag1.append(player)
            if x + y == 2:
                diag2.append(player)
    if (len(diag1) == 3 and len(set(diag1)) == 1):
        return True, diag1[0]
    elif (len(diag2) == 3 and len(set(diag2)) == 1):
        return True, diag2[0]
    return False, 'None'


def get_winner(placed):
    print(get_diag_winner(placed)[0])
    if not get_diag_winner(placed)[0]:
        X_count = [[0, 0], [0, 0], [0, 0]]
        O_count = [[0, 0], [0, 0], [0, 0]]
        for block, player in zip(placed.keys(), placed.values()):
            if player == 'X':
                x, y = block
                X_count[x][0] += 1
                X_count[y][1] += 1
            if player == 'O':
                x, y = block
                O_count[x][0] += 1
                O_count[y][1] += 1
        if max(sum(X_count, [])) >= 3:
            return True, 'X'
        elif max(sum(O_count, [])) >= 3:
            return True, 'O'
    else:
        return get_diag_winner(placed)
    return False, 'None'


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
height = 900
width = 900
size = (height, width)
screen = pygame.display.set_mode(size)

font = pygame.font.Font('freesansbold.ttf', 64)

# create a rectangular object for the
# text surface object


pygame.display.set_caption("Tic Tac Toe")

screen.fill(WHITE)
drawGrid()
# Loop until the user clicks the close button.
run = True
X = pygame.image.load('X.png')
O = pygame.image.load('O.png')
X = pygame.transform.smoothscale(X, (300, 300))
O = pygame.transform.smoothscale(O, (300, 300))
placed = {}
turn = 0
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
done = False
won = False
# -------- Main Program Loop -----------
while run:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            x, y = x // 300, y // 300
            if turn % 2 == 0:
                if (x, y) not in placed:
                    placed[(x, y)] = 'X'
                    screen.blit(X, (x * 300, y * 300))
                    turn += 1
                    print(placed)
            else:
                if (x, y) not in placed:
                    placed[(x, y)] = 'O'
                    screen.blit(O, (x * 300, y * 300))
                    turn += 1
                    print(placed)
            if won:
                won = False
                screen.fill(WHITE)
                drawGrid()
                placed = {}
                turn = 0
            if done:
                done = False
                screen.fill(WHITE)
                drawGrid()
                placed = {}
                turn = 0
    if len(placed.keys()) > 3:
        won, winner = get_winner(placed)
    if won:
        vict = font.render(f'Game Over: {winner} won!', True, WHITE, BLUE)
        textRect = vict.get_rect()
        textRect.center = (width // 2, height // 2)
        screen.fill(WHITE)
        screen.blit(vict, textRect)

    if len(placed.keys()) == 9 and not won:
        done = True
        draw = font.render('Game Over: Draw', True, RED, BLUE)
        textRect = draw.get_rect()
        textRect.center = (width // 2, height // 2)
        screen.fill(WHITE)
        screen.blit(draw, textRect)
        # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.

    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(10)

# Close the window and quit.
pygame.quit()
