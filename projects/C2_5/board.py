
from ship import Ship

class Board:

    @staticmethod
    def empty_lists(size):
        return [[] for _ in range(size)]

    def __init__(self):
        self.FIELD_SIZE = 6
        self.MAX_SHIPS_NUM = [0, 4, 2, 1]
        self._ships_by_size = Board.empty_lists(len(self.MAX_SHIPS_NUM) + 1)
        # self._ships_by_size[0] must be always empty as far as ships with size 0 are not possible
        self._symbol_of_free_place = 'O'
        self._symbol_of_ship = u"\u25A0"
        self._symbol_of_hits = 'X'
        self._symbol_of_miss = 'T'
        self._repr_lines = []
        self._repr_lines_elements = Board.empty_lists(self.FIELD_SIZE + 1)
        self._repr_lines_elements_clear = Board.empty_lists(
            self.FIELD_SIZE + 1)
        self.__init_clear_repr_lines()
        self._misses = set()
        self._hits = set()

    def clear(self):
        self._hits.clear()
        self._misses.clear()
        for ships_of_given_size in self._ships_by_size:
            ships_of_given_size.clear()

    def to_str_with_no_ships(self):
        basic_symbol_of_ship = self._symbol_of_ship
        self._symbol_of_ship = self._symbol_of_free_place
        repr = str(self)
        self._symbol_of_ship = basic_symbol_of_ship
        return repr

    def __str__(self):
        self._repr_lines.clear()
        self.__clear_repr_lines_elements()
        for ships_of_given_size in self._ships_by_size:
            for ship in ships_of_given_size:
                for x, y in ship.pts:
                    self._repr_lines_elements[y][x] = self._symbol_of_ship
                for x, y in ship.hits:
                    self._repr_lines_elements[y][x] = self._symbol_of_hits
        for x, y in self._misses:
            self._repr_lines_elements[y][x] = self._symbol_of_miss
        for line in self._repr_lines_elements:
            self._repr_lines.append('|'.join(map(str, line)))
        return '\n'.join(self._repr_lines)

    def __update_hits(self):
        self._hits.clear()
        for ships_of_given_size in self._ships_by_size:
            for ship in ships_of_given_size:
                self._hits.update(ship.hits)

    def all_ships_sunken(self):
        res = True
        for ships_of_given_size in self._ships_by_size:
            for ship in ships_of_given_size:
                res &= ship.is_sunken()
        return res

    def __init_clear_repr_lines(self):
        self._repr_lines_elements_clear[0].append(' ')
        self._repr_lines_elements_clear[0].extend(
            range(1, self.FIELD_SIZE + 1))
        empty_fields_symbols = [self._symbol_of_free_place for _ in range(0, self.FIELD_SIZE)]
        for i in range(1, self.FIELD_SIZE + 1):
            self._repr_lines_elements_clear[i].append(i)
            self._repr_lines_elements_clear[i].extend(empty_fields_symbols)

    def __clear_repr_lines_elements(self):
        for i in range(len(self._repr_lines_elements)):
            self._repr_lines_elements[i].clear()
            self._repr_lines_elements[i].extend(
                self._repr_lines_elements_clear[i])

    def add_ship(self, direction, ship_size, x, y):
        self._validate_ship_size(ship_size)
        self._validate_direction(direction)
        self._validate_max_ships_limit(ship_size)
        new_ship = Ship(direction, ship_size, x, y)
        self._validate_ships_relative_position(new_ship)
        self._validate_board_interruption(new_ship)
        self._ships_by_size[ship_size].append(new_ship)

    def ships_number_is_ok(self):
        res = True
        for ship_size in range(len(self.MAX_SHIPS_NUM)):
            res &= self.MAX_SHIPS_NUM[ship_size] == len(self._ships_by_size[ship_size])
        return res

    def _validate_ship_size(self, ship_size):
        if (ship_size < 1 or ship_size >= len(self.MAX_SHIPS_NUM)):
            message = f'ship size num must be in range "1...{len(self.MAX_SHIPS_NUM)-1}", but "{ship_size}" was given'
            raise ValueError(message)

    def _validate_direction(self, direction):
        if direction.lower() != 'x' and direction.lower() != 'y':
            message = f'direction of Ship must be "x", or "y" - but "{direction}" was given'
            raise ValueError(message)

    def _validate_max_ships_limit(self, ship_size):
        if (len(self._ships_by_size[ship_size]) >= self.MAX_SHIPS_NUM[ship_size]):
            message = f'maximum number of ships with size {ship_size} is {self.MAX_SHIPS_NUM[ship_size]}, ' \
                f'but attempted to insert {self.MAX_SHIPS_NUM[ship_size]}th ship of such size'
            raise ValueError(message)

    def _validate_ships_relative_position(self, new_ship):
        for ships_of_given_size in self._ships_by_size:
            for ship in ships_of_given_size:
                if (new_ship.is_too_close_to(ship)):
                    message = f'{str(new_ship)} can not be inserted as far as it is too close to {str(ship)}'
                    raise ValueError(message)

    def _validate_board_interruption(self, new_ship):
        for pt in new_ship.pts:
            if (not (1 <= pt[0] <= self.FIELD_SIZE) or not (1 <= pt[1] <= self.FIELD_SIZE)):
                message = f'{str(new_ship)} interrupts board size x=1...{self.FIELD_SIZE}, y=1...{self.FIELD_SIZE}'
                raise ValueError(message)

    def shot_is_invalid(self, shot_pt):
        message = ''
        x = shot_pt[0]
        y = shot_pt[1]
        if not 1 <= x <= self.FIELD_SIZE or not 1 <= y <= self.FIELD_SIZE:
            message = f'point({x}, {y}) interrupts board size x=1...{self.FIELD_SIZE}, y=1...{self.FIELD_SIZE}'
        self.__update_hits()
        if shot_pt in self._misses or shot_pt in self._hits:
            message = f'shot can not be done as far as point({x}, {y}) is already busy'
        return message

    def shot(self, shot_pt):
        for ships_of_given_size in self._ships_by_size:
            for ship in ships_of_given_size:
                ship.try_hit_success(shot_pt)
        if not self.shot_is_hit(shot_pt):
            self._misses.add(shot_pt)

    def shot_is_hit(self, shot_pt):
        self.__update_hits()
        return shot_pt in self._hits

