from random import randint

from board import Board
from ships_generator import ShipsGenerator


class PrimitiveBot:

    @staticmethod
    def pt_random_index(pts):
        return randint(0, len(pts) - 1)

    @staticmethod
    def append_if_not_in(pt, pts, pts_cntrl):
        if pt not in pts and pt not in pts_cntrl:
            pts.append(pt)

    def __init__(self, name='BOT'):
        self._name = name
        self._pt_list_repr = []
        self._board = Board()
        self._ships_generator = ShipsGenerator(self._board)
        self._ships_generator.generate_ships()
        self._own_shots_potential = []
        self.__init_potential_own_shots()
        self._own_shots_done = set()
        self._own_shots_hits = set()
        self._own_shots_priority = []
        self._curr_own_shot = None

    def __init_potential_own_shots(self):
        self._own_shots_potential.clear()
        self._own_shots_potential.extend(self._ships_generator.get_pts_all())

    def get_name(self):
        return self._name

    def get_next_own_shot(self):
        if len(self._own_shots_priority) > 0:
            pt_index = PrimitiveBot.pt_random_index(self._own_shots_priority)
            self._curr_own_shot = self._own_shots_priority[pt_index]
        else:
            pt_index = PrimitiveBot.pt_random_index(self._own_shots_potential)
            self._curr_own_shot = self._own_shots_potential[pt_index]
        return self._curr_own_shot

    def set_own_shot_miss(self):
        self.__set_own_shot_done()

    def set_own_shot_hit(self):
        self.__set_own_shot_done()
        self._own_shots_hits.add(self._curr_own_shot)
        self._own_shots_priority.clear()
        if self.__set_priority_of_vector(0):
            return
        if self.__set_priority_of_vector(1):
            return
        self.__set_priority_both_sides(0)
        self.__set_priority_both_sides(1)

    def __set_own_shot_done(self):
        self.__set_pt_done(self._curr_own_shot)

    def __set_priority_of_vector(self, dimension_index):
        curr_dimension_val, pt1, pt2 = self.__neighbouring_pts(self._curr_own_shot, dimension_index)
        if pt1 in self._own_shots_hits:
            self.__set_ortho_points_done(self._curr_own_shot, dimension_index)
            self.__set_ortho_points_done(pt1, dimension_index)
            if curr_dimension_val < self._board.FIELD_SIZE:
                PrimitiveBot.append_if_not_in(pt2, self._own_shots_priority, self._own_shots_done)
                return True
        if pt2 in self._own_shots_hits:
            self.__set_ortho_points_done(self._curr_own_shot, dimension_index)
            self.__set_ortho_points_done(pt2, dimension_index)
            if curr_dimension_val > 1:
                PrimitiveBot.append_if_not_in(pt1, self._own_shots_priority, self._own_shots_done)
                return True
        return False

    def __set_ortho_points_done(self, src_pt, src_dimension_index):
        target_dimension_index = (src_dimension_index + 1) % 2
        curr_dimension_val, pt1, pt2 = self.__neighbouring_pts(src_pt, target_dimension_index)
        self.__set_pt_done(pt1)
        self.__set_pt_done(pt2)

    def __set_pt_done(self, pt):
        if pt in self._own_shots_priority:
            self._own_shots_priority.remove(pt)
        if pt in self._own_shots_potential:
            self._own_shots_potential.remove(pt)
        if pt not in self._own_shots_done:
            self._own_shots_done.add(pt)

    def __set_priority_both_sides(self, dimension_index):
        curr_dimension_val, pt1, pt2 = self.__neighbouring_pts(self._curr_own_shot, dimension_index)
        if curr_dimension_val > 1:
            PrimitiveBot.append_if_not_in(pt1, self._own_shots_priority, self._own_shots_done)
        if curr_dimension_val < self._board.FIELD_SIZE:
            PrimitiveBot.append_if_not_in(pt2, self._own_shots_priority, self._own_shots_done)

    def __neighbouring_pts(self, target_pt, target_dimension_index):
        pt = self._pt_list_repr
        pt.clear()
        pt.extend(target_pt)
        curr_dimension_val = target_pt[target_dimension_index]
        pt[target_dimension_index] = curr_dimension_val - 1
        pt1 = tuple(pt)
        pt[target_dimension_index] = curr_dimension_val + 1
        pt2 = tuple(pt)
        return curr_dimension_val, pt1, pt2

    def foreign_shot_is_invalid(self, pt):
        return self._board.shot_is_invalid(pt)

    def set_foreign_shot(self, pt):
        self._board.shot(pt)

    def foreign_shot_is_hit(self, pt):
        return self._board.shot_is_hit(pt)

    def all_ships_sunken(self):
        return self._board.all_ships_sunken()

    def print_board_repr_with_ships(self):
        print(f'board of {self._name}')
        print(str(self._board))
        print()

    def print_board_repr_with_no_ships(self):
        print(f'board of {self._name}')
        print(self._board.to_str_with_no_ships())
        print()
