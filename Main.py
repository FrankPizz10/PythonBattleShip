import pygame, sys
from BoardModel import GameBoardModel
from pygame.locals import *

GRAY = (192, 192, 192)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
WHITESMOKE = (245, 245, 245)
BLACK = (0, 0, 0)

BGCOLOR = WHITESMOKE


def main():
    global DISPLAYSURF
    model = GameBoardModel()
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((model.board_width * 2, model.board_height))

    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    pygame.display.set_caption('BattlesShip')

    DISPLAYSURF.fill(BGCOLOR)
    initGameBoard(model)

    print("Please select where you would like to place your pieces.")

    piecesPlaced = False
    piece_index = 0
    time_to_prompt = True
    ship = ''
    turn = 'user'
    stop_printing = False

    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)  # drawing the window
        initGameBoard(model)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        if not piecesPlaced:
            square = model.checkWithinSquare(mousex, mousey)
            piece = model.piece_placement_order[piece_index]

            if time_to_prompt:
                print(f'Please place the {piece}, it is {model.user_pieces[piece].size} spaces long.')
                time_to_prompt = False

            if mouseClicked and square is not None:
                print(square)
                model.loc_inputs[piece].append(square)

            if model.user_pieces[piece].size == len(model.loc_inputs[piece]):
                try:
                    model.placePiece('user', piece, model.loc_inputs[piece])
                    time_to_prompt = True
                    piece_index += 1
                except ValueError as err:
                    print(err)
                    model.loc_inputs[piece] = []

            if piece_index == len(model.user_pieces):
                piecesPlaced = True
                time_to_prompt = False
                model.generateCPUPiecePlacement()
                print("All Pieces were Placed!")
        # Begin Play
        else:
            if turn == 'user':
                if not stop_printing:
                    print("It is your turn to Fire! Please select a square.")
                square = model.checkWithinSquare(mousex, mousey)
                # User Move
                if mouseClicked and square is not None:
                    if not model.cpu_locations[square].hit and not model.cpu_locations[square].missed:
                        if square in model.cpu_ship_locations:
                            print(f'{square} IS A HIT!')
                            model.cpu_locations[square].hit = True
                            model.targeted_squares[0].append(square)
                            for piece in model.cpu_pieces:
                                if square in model.cpu_pieces[piece].locations:
                                    ship = model.cpu_pieces[piece]
                            ship.hit(square)
                            if ship.sunk:
                                print(f"YOU SUNK MY {ship.name}!")
                            if model.checkUserWin():
                                print("CONGRATS YOU WIN!")
                                exit(0)
                        else:
                            print(f'{square} IS A MISS!')
                            model.targeted_squares[0].append(square)
                            model.cpu_locations[square].missed = True
                        turn = 'cpu'
                    else:
                        print(f'You already selected {square}. Please select a new square.')
                stop_printing = True
            else:
                # CPU Move
                print("It is the CPU's turn.")
                model.playCPUMove()
                turn = 'user'
                stop_printing = False

        for name in model.user_pieces.keys():
            if model.user_pieces[name].placed:
                drawShip(model, 'user', model.user_pieces[name])
                drawShip(model, 'cpu', model.cpu_pieces[name])
                drawMisses(model, 'user')
                drawMisses(model, 'cpu')

        pygame.display.update()


def drawBoxes(model):
    drawBoxesPerBoard(model, 0)
    drawBoxesPerBoard(model, model.board_width)


def drawBoxesPerBoard(model, spacer):
    left, top, right, bottom = model.xmargin, model.ymargin, model.box_size, model.box_size + model.ymargin
    left += spacer
    right += spacer
    for box_row in range(model.game_width):
        for box_col in range(model.game_height):
            pygame.draw.rect(DISPLAYSURF, BLUE, (left, top, model.box_size, model.box_size))
            left += model.box_size + model.gapsize
            right += model.box_size + model.gapsize
        bottom, top = bottom + model.box_size + model.gapsize, top + model.box_size + model.gapsize
        left, right = model.xmargin, model.box_size
        left += spacer
        right += spacer


def drawLabels(model):
    drawLabelsPerBoard(model, 0)
    drawLabelsPerBoard(model, model.board_width)


def drawLabelsPerBoard(model, spacer):
    xpos = model.box_size + (model.xmargin / 3) + spacer
    ypos = model.ymargin / 3
    for label in range(len(model.labels)):
        font = pygame.font.SysFont('', 32)
        img = font.render(model.labels[label], True, BLACK)
        DISPLAYSURF.blit(img, (xpos, ypos))
        if label < model.game_width - 1:
            xpos += model.box_size + model.gapsize
        else:
            xpos = model.xmargin / 3 + spacer
            if label == model.game_width - 1:
                ypos += (model.box_size * 2) + model.gapsize
            else:
                ypos += model.box_size + model.gapsize


def initGameBoard(model):
    drawBoxes(model)
    drawLabels(model)


def drawShip(model, board, ship):
    color = YELLOW
    for sqr in ship.locations:
        if board == 'user':
            color = YELLOW
            sqr_obj = model.user_locations[sqr]
        else:
            color = BLUE
            sqr_obj = model.cpu_locations[sqr]
        if sqr_obj.hit and not ship.sunk:
            color = RED
        elif ship.sunk:
            color = BLACK
        xpos = sqr_obj.locations[0] + (model.box_size / 3)
        ypos = sqr_obj.locations[1] + (model.box_size / 3)
        font = pygame.font.SysFont('', 24)
        img = font.render(ship.abbr, True, color)
        DISPLAYSURF.blit(img, (xpos, ypos))


def drawMisses(model, board):
    if board == 'user':
        for sqr in model.user_locations:
            sqr_obj = model.user_locations[sqr]
            if sqr_obj.missed:
                xpos = sqr_obj.locations[0] + (model.box_size / 3)
                ypos = sqr_obj.locations[1] + (model.box_size / 3)
                font = pygame.font.SysFont('', 36)
                img = font.render('X', True, WHITE)
                DISPLAYSURF.blit(img, (xpos, ypos))
    else:
        for sqr in model.cpu_locations:
            sqr_obj = model.cpu_locations[sqr]
            if sqr_obj.missed:
                xpos = sqr_obj.locations[0] + (model.box_size / 3)
                ypos = sqr_obj.locations[1] + (model.box_size / 3)
                font = pygame.font.SysFont('', 36)
                img = font.render('X', True, WHITE)
                DISPLAYSURF.blit(img, (xpos, ypos))


if __name__ == '__main__':
    main()
