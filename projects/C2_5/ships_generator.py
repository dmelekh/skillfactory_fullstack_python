
from random import randint

class ShipsGenerator:

    @staticmethod
    def pt_random_index(pts):
        return randint(0, len(pts) - 1)

    @staticmethod
    def append_if_not_in(pt, pts, pts_cntrl):
        if pt not in pts and pt not in pts_cntrl:
            pts.append(pt)

    def __init__(self, board):
        self._board = board
        self._pts_all = []
        self._pts_operating = []
        self.__init_pts_all()

    def __init_pts_all(self):
        field_size = self._board.FIELD_SIZE
        for i in range(1, field_size + 1):
            self._pts_all.extend((i, j) for j in range(1, field_size + 1))

    def get_pts_all(self):
        return self._pts_all

    def generate_ships(self):
        self.__init_ships()

    def __init_ships(self):
        attempts_num = 1
        while not self.__attempt_to_init_ships():
            attempts_num += 1

    def __attempt_to_init_ships(self):
        ships_nums = self._board.MAX_SHIPS_NUM
        directions = 'x', 'y'
        self._board.clear()
        self._pts_operating.clear()
        self._pts_operating.extend(self._pts_all)
        for ship_size in range(len(ships_nums) - 1, 0, -1):
            ships_num_of_given_size = ships_nums[ship_size]
            for _ in range(ships_num_of_given_size):
                ship_was_added = False
                while not ship_was_added and len(self._pts_operating):
                    try:
                        pt_index = ShipsGenerator.pt_random_index(self._pts_operating)
                        pt = self._pts_operating.pop(pt_index)
                        direction = directions[randint(0, 1)]
                        self._board.add_ship(direction, ship_size, pt[0], pt[1])
                    except Exception:
                        pass
                    else:
                        ship_was_added = True
        return self._board.ships_number_is_ok()
        