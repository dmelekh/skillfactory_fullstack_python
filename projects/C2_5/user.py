from board import Board
from ships_generator import ShipsGenerator


class User:
    def __init__(self, name='USER'):
        self._name = name
        self._board = Board()
        self._ships_generator = ShipsGenerator(self._board)
        self.__init_placing_rule()
        self.__init_ships()
        self.print_board_repr_with_ships()

    def __init_placing_rule(self):
        ships_nums = self._board.MAX_SHIPS_NUM
        elements = []
        for i in range(1, len(ships_nums)):
            elements.append(f'{ships_nums[i]} {i}-ship{"s" if ships_nums[i] > 1 else ""}')
        self._placing_rule = 'place on board ' + ', '.join(elements)

    def __init_ships(self):
        self._board.clear()
        while not self._board.ships_number_is_ok():
            self.__add_new_ship()

    def __add_new_ship(self):
        try:
            self.__print_head_of_user_input()
            user_input = input()
            if user_input == '':
                self._ships_generator.generate_ships()
                return
            user_input = user_input.split()
            x = int(user_input[1])
            y = int(user_input[0])
            direction = user_input[2]
            ship_size = int(user_input[3])
            self._board.add_ship(direction, ship_size, x, y)

        except Exception as e:
            print(f'!!! input fails: {str(e)}')
            input('press enter to try again\n')

    def __print_head_of_user_input(self):
        self.print_board_repr_with_ships()
        print(self._placing_rule)
        print('enter empty line if you want to generate ships')
        print(
            'enter ship parameters in the next order:\n"left-upper Y" "left-upper X" "direction (x, or y)" "ship size"')

    def get_name(self):
        return self._name

    def get_next_own_shot(self):
        while True:
            try:
                user_input = input('enter shot point as "y x":\n').split()
                if len(user_input) != 2:
                    self.__print_input_invalid()
                    continue
                x = int(user_input[1])
                y = int(user_input[0])
                return x, y
            except:
               self.__print_input_invalid()

    def __print_input_invalid(self):
        print("input of shot coordinates is invalid - try again\n")

    def set_own_shot_miss(self):
        pass

    def set_own_shot_hit(self):
        pass

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
