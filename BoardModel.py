import random
import numpy as np
from Pieces import *

SYMBOLS2D = [
            ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'],
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10'],
            ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'],
            ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
            ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10'],
            ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10'],
            ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10'],
            ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10'],
            ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10'],
            ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10']
        ]

LABELS = [
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
            'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1',
        ]

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

NUMBERS = [str(num) for num in range(1, 11)]


class GameBoardModel:

    def __init__(self):
        self.game_width = 10  # number of rows
        self.game_height = 10 # number of columns
        self.box_size = 50  # size of box height & width in pixels
        self.gapsize = 5  # size of gap between boxes in pixels
        self.xmargin = 50  # space on left of board for labels
        self.ymargin = 50  # space on top of board for labels
        self.board_height = self.getBoardHeight()  # height of board in pixels
        self.board_width = self.getBoardWidth()  # width of board in pixels
        self.symbols = [item for row in SYMBOLS2D for item in row]  # all square names
        self.user_locations, self.cpu_locations = self.getSquareLocations()  # two dicts of str -> Square (Square locations)
        self.labels = LABELS  # column and row labels
        self.user_pieces = {
            'BattleShip': BattleShip(),
            'Submarine': Submarine(),
            'Cruiser': Cruiser(),
            'AircraftCarrier': AircraftCarrier(),
            'Destroyer': Destroyer()
            }  # dict of str -> Piece
        self.cpu_pieces = {
            'BattleShip': BattleShip(),
            'Submarine': Submarine(),
            'Cruiser': Cruiser(),
            'AircraftCarrier': AircraftCarrier(),
            'Destroyer': Destroyer()
        }  # dict of str -> Piece
        self.placementStrategy = 0
        self.piece_placement_order = sorted(self.user_pieces.keys())
        self.loc_inputs = self.create_blank_inputs()
        self.user_ship_locations = []
        self.cpu_ship_locations = []
        self.targeted_squares = [[], []]  # user squares, cpu squares already selected respectively
        self.cpu_available_targets = [item for row in SYMBOLS2D for item in row]
        self.report = IntelligenceReport()

    def getBoardHeight(self):
        return ((self.box_size + self.gapsize) * self.game_height) + self.ymargin  # size of windows' height in pixels

    def getBoardWidth(self):
        return ((self.box_size + self.gapsize) * self.game_width) + self.xmargin  # size of window's width in pixels

    def getSquareLocations(self):
        user_board = self.getSquareLocationsPerBoard(0)
        cpu_board = self.getSquareLocationsPerBoard(self.board_width)
        return user_board, cpu_board

    def getSquareLocationsPerBoard(self, spacer):
        locations = {}
        symbol_index = 0
        left, top, right, bottom = self.xmargin, self.ymargin, self.box_size + self.xmargin, self.box_size + self.ymargin
        left += spacer
        right += spacer
        for box_row in range(self.game_width):
            for box_col in range(self.game_height):
                square_arr = [left, top, left + self.box_size,
                              top + self.box_size]  # topleft, topright, bottomleft, bottomright locations
                left += self.box_size + self.gapsize
                right += self.box_size + self.gapsize
                locations[self.symbols[symbol_index]] = Square(self.symbols[symbol_index], square_arr)
                symbol_index += 1
            bottom, top = bottom + self.box_size + self.gapsize, top + self.box_size + self.gapsize
            left, right = self.xmargin, self.box_size
            left += spacer
            right += spacer
        return locations

    def checkWithinSquare(self, xpos, ypos):
        boards = [self.user_locations, self.cpu_locations]
        for board in boards:
            for key in board.keys():
                square = board[key]
                pos_array = square.locations
                if pos_array[0] < xpos < pos_array[2] and pos_array[1] < ypos < pos_array[3]:
                    return square.name
        return None

    def placePiece(self, board, piece, *locations):
        if not self.checkOccupied(board, locations):
            if board == 'user':
                target_board = self.user_pieces
            else:
                target_board = self.cpu_pieces
            target_board[piece].place(locations)
        else:
            raise ValueError('One of these squares is already occupied.')

    def checkOccupied(self, board, *locations):
        attempted_inputs = locations[0][0]
        occupied_locs = []
        if board == 'user':
            target_board = self.user_pieces
        else:
            target_board = self.cpu_pieces
        for piece in target_board:
            for loc in target_board[piece].locations:
                occupied_locs.append(loc)
            for loc in attempted_inputs:
                if loc in occupied_locs:
                    return True
        return False

    def create_blank_inputs(self):
        loc_dict = {}
        for piece in self.piece_placement_order:
            loc_dict[piece] = []
        return loc_dict

    def generateCPUPiecePlacement(self):
        rand_2Dnum = [random.randint(0, len(SYMBOLS2D[0]) - 1), random.randint(0, len(SYMBOLS2D[0]) - 1)]
        for piece in self.cpu_pieces:
            validPlacement = False
            while not validPlacement:
                squares = self.executePlacementStrategy(rand_2Dnum, self.cpu_pieces[piece].size, self.placementStrategy)
                try:
                    self.placePiece('cpu', piece, squares)
                    rand_2Dnum = [random.randint(0, len(SYMBOLS2D[0]) - 1), random.randint(0, len(SYMBOLS2D[0]) - 1)]
                    validPlacement = True
                except ValueError or IndexError as ie:
                    if ie == IndexError:
                        print(self.cpu_pieces[piece].locations)
                    if self.placementStrategy == 3:
                        self.placementStrategy = 0
                        rand_2Dnum = [random.randint(0, len(SYMBOLS2D[0]) - 1), random.randint(0, len(SYMBOLS2D[0]) - 1)]
                    else:
                        self.placementStrategy += 1
        for piece in self.cpu_pieces:
            for loc in self.cpu_pieces[piece].locations:
                self.cpu_ship_locations.append(loc)
        for piece in self.user_pieces:
            for loc in self.user_pieces[piece].locations:
                self.user_ship_locations.append(loc)

    def executePlacementStrategy(self, start_square, size, strategy):
        row = start_square[0]
        col = start_square[1]
        squares = [SYMBOLS2D[row][col]]
        switcher = {
            0: lambda x, y: [x+1, y],  # place to the right
            1: lambda x, y: [x, y+1],  # place to the left
            2: lambda x, y: [x-1, y],  # place up
            3: lambda x, y: [x, y-1],  # place down
        }
        for x in range(size-1):
            next_square = switcher[strategy](row, col)
            row = next_square[0]
            col = next_square[1]
            try:
                squares.append(SYMBOLS2D[row][col])
            except IndexError:
                continue
        return squares

    # Random square fire
    def cpurFireStandard(self, square):
        prox_fire = False
        if len(self.report.recent_shot_stack) > 0:
            prox_fire = True
            self.cpuProximityFire()
        if not prox_fire:
            square = self.cpu_available_targets[square]
            ship = ''
            if square not in self.targeted_squares[1]:
                self.targeted_squares[1].append(square)
            else:
                while square in self.targeted_squares[1]:
                    row = random.randint(0, len(SYMBOLS2D[0]) - 1)
                    col = random.randint(0, len(SYMBOLS2D[0]) - 1)
                    square = SYMBOLS2D[row][col]
                    if square not in self.targeted_squares[1]:
                        self.targeted_squares[1].append(square)
                        break
            print(f'The CPU selected {square}.')
            remove_sqr = self.cpu_available_targets.index(square)
            self.cpu_available_targets.pop(remove_sqr)
            if square in self.user_ship_locations:
                self.user_locations[square].hit = True
                print(f'{square} is a hit!')
                self.report.hit_squares.append(square)
                self.report.recent_shot_stack.append(square)
                for piece in self.user_pieces:
                    if square in self.user_pieces[piece].locations:
                        ship = self.user_pieces[piece]
                        self.report.ship_progress[ship.name] -= 1
                self.report.recent_shot_neighbor_map['Origin_Target'] = ship.name
                self.report.recent_shot_neighbor_map[square] = []
                ship.hit(square)
                if ship.sunk:
                    print(f"THE CPU HAS SUNK YOUR {ship.name}!")
                if self.checkCPUWin():
                    print("SORRY YOU LOSE!")
                    exit(0)
            else:
                self.user_locations[square].missed = True
                print(f'{square} is a miss!')

    def cpuProximityFire(self):
        valid_target = False
        next_target = ''
        ship = ''
        sqr = ''
        while not valid_target:
            start_sqr = self.report.recent_shot_stack[-1]
            fire_dir = ''
            if len(self.report.recent_shot_neighbor_map[start_sqr]) < 4:
                for dir in self.report.fire_directions:
                    if not dir in self.report.recent_shot_neighbor_map[start_sqr]:
                        fire_dir = dir
                        self.report.recent_shot_neighbor_map[start_sqr].append(fire_dir)
                        break
            array = np.array(SYMBOLS2D)
            coords = np.argwhere(array == start_sqr)
            row = coords[0][0]
            col = coords[0][1]
            squares = [SYMBOLS2D[row][col]]
            shooter = {
                'right': lambda x, y: [x, y + 1],  # place to the right
                'left': lambda x, y: [x, y - 1],  # place to the left
                'up': lambda x, y: [x - 1, y],  # place up
                'down': lambda x, y: [x + 1, y],  # place down
            }
            if not fire_dir == '':
                next_target = shooter[fire_dir](row, col)
                row = next_target[0]
                col = next_target[1]
                inbounds = self.checkInbounds(next_target)
                if inbounds:
                    sqr = SYMBOLS2D[row][col]
                    if sqr in self.cpu_available_targets:
                        self.report.recent_shot_stack.append(sqr)
                        self.report.recent_shot_neighbor_map[sqr] = [invert_dir(fire_dir)]
                        valid_target = True
            else:
                self.report.recent_shot_stack.pop()
        self.targeted_squares[1].append(sqr)
        remove_sqr = self.cpu_available_targets.index(sqr)
        self.cpu_available_targets.pop(remove_sqr)
        print(f'The CPU selected {sqr}.')
        if sqr in self.user_ship_locations:
            self.user_locations[sqr].hit = True
            print(f'{sqr} is a hit!')
            self.report.hit_squares.append(sqr)
            for piece in self.user_pieces:
                if sqr in self.user_pieces[piece].locations:
                    ship = self.user_pieces[piece]
                    self.report.ship_progress[ship.name] -= 1
            ship.hit(sqr)
            if ship.sunk:
                print(f"THE CPU HAS SUNK YOUR {ship.name}!")
                if self.report.recent_shot_neighbor_map['Origin_Target'] == ship.name:
                    self.report.recent_shot_stack = []
                    self.report.recent_shot_neighbor_map = {}
                if self.checkCPUWin():
                    print("SORRY YOU LOSE!")
                    exit(0)
        else:
            self.user_locations[sqr].missed = True
            print(f'{sqr} is a miss!')
            remove_sqr = self.report.recent_shot_stack.index(sqr)
            self.report.recent_shot_stack.pop(remove_sqr)

    def checkInbounds(self, target):
        return 0 <= target[0] < len(SYMBOLS2D) and 0 <= target[1] < len(SYMBOLS2D[1])

    def checkUserWin(self):
        ships_sunk = 0
        for piece in self.cpu_pieces:
            if self.cpu_pieces[piece].sunk:
                ships_sunk += 1
        return ships_sunk == 5

    def checkCPUWin(self):
        ships_sunk = 0
        for piece in self.user_pieces:
            if self.user_pieces[piece].sunk:
                ships_sunk += 1
        return ships_sunk == 5

    def playCPUMove(self):
        rand_num = random.randint(0, len(self.cpu_available_targets) - 1)
        self.cpurFireStandard(rand_num)


class Square:

    def __init__(self, name, locations):
        self.locations = locations
        self.name = name
        self.hit = False
        self.missed = False


class IntelligenceReport:

    def __init__(self):
        self.hit_squares = []
        self.ship_progress = {
            'BattleShip': 4,
            'Cruiser': 4,
            'AircraftCarrier': 5,
            'Destroyer': 3,
            'Submarine': 2
        }  # map of ships to remaining hits str -> int
        self.fire_directions = ['up', 'down', 'left', 'right']
        self.dir_index = 0
        self.recent_shot_stack = []  # Tracks the shots from the latest targeted search
        self.recent_shot_neighbor_map = {}  # Tracks the directions checked in each recent shot


def specialSort(list):
    try:
        vertical = False
        sorted_list = []
        if list[0][1:] == list[1][1:]:
            vertical = True
        if vertical:
            sorted_list = sorted(list)
        else:
            sorted_list = sorted(list, key=lambda x: x[1:])
            for item in range(len(sorted_list)):
                if '10' in sorted_list[item]:
                    sorted_list.append(sorted_list[item])
                    sorted_list.pop(item)
    except IndexError:
        return list
    return sorted_list


def invert_dir(direction):
    switcher = {
        'right': 'left',
        'left': 'right',
        'up': 'down',
        'down': 'up'
    }
    return switcher[direction]


