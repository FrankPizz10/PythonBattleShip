class APiece:

    def __init__(self, name, size, abbr):
        self.name = name
        self.size = size
        self.placed = False
        self.hit_arr = []
        self.locations = []
        self.abbr = abbr
        self.sunk = False

    def checkPlacement(self, locs):
        from BoardModel import LETTERS, NUMBERS
        valid = False
        alphabetical = self.checkOrder(locs, LETTERS, True)
        numerical = self.checkOrder(locs, NUMBERS, False)
        only_one_identical = self.checkOneIdentical(locs)
        if alphabetical ^ numerical:
            if only_one_identical:
                valid = True
        return valid

    def checkOneIdentical(self, locs):
        same_letter, same_number = True, True
        ele = locs[0][0]
        for loc in locs:
            if ele != loc[0]:
                same_letter = False
        ele = locs[0][1]
        for loc in locs:
            if ele != loc[1]:
                same_number = False
        return same_letter ^ same_number

    def checkOrder(self, locs, correct_values, isAlpa):
        parser = 0 if isAlpa else 1
        ordered = False
        for index in range(len(locs) - 1):
            letter_index = correct_values.index(locs[index][parser])
            if locs[index + 1][parser] == correct_values[letter_index + 1]:
                ordered = True
            elif locs[index + 1][parser:] == correct_values[letter_index + 1]:
                ordered = True
            else:
                return False
        return ordered

    def place(self, *locations):
        from BoardModel import specialSort
        locs = locations[0][0]
        locs = specialSort(locs)
        if not len(locs) == self.size:
            raise ValueError(f'The {self.name} is {self.size} squares long.')
        if not self.checkPlacement(locs):
            raise ValueError(f'The {self.name} must be in a straight line with no spaces.')
        for loc in locs:
            self.locations.append(loc)
        self.locations = specialSort(self.locations)
        self.hit_arr = [False for x in range(len(self.locations))]
        self.placed = True
        print(f'{self.name} was placed at {specialSort(self.locations)}!')

    def hit(self, square):
        for x in range(len(self.locations)):
            if square == self.locations[x]:
                self.hit_arr[x] = True
        if self.checkSunk():
            self.sunk = True

    def checkSunk(self):
        return all(self.hit_arr)


class BattleShip(APiece):

    def __init__(self):
        super().__init__('BattleShip', 4, 'BT')


class Submarine(APiece):

    def __init__(self):
        super().__init__('Submarine', 2, 'SB')


class Cruiser(APiece):

    def __init__(self):
        super().__init__('Cruiser', 4, 'CR')


class AircraftCarrier(APiece):

    def __init__(self):
        super().__init__('AircraftCarrier', 5, 'AC')


class Destroyer(APiece):

    def __init__(self):
        super().__init__('Destroyer', 3, 'DT')
