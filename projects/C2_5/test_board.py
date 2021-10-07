
from board import Board


def my_test(test_case_name, expected_message):
    def decorator(testing):
        def wrapper(*args, **kwargs):
            try:
                testing(*args, **kwargs)
            except Exception as e:
                if (str(e) == expected_message):
                    print(f'passed {test_case_name}')
                    return
                else:
                    print(
                        f'!!! {test_case_name} fails, got exception with message:')
                    print(e)
            else:
                print(f'!!! {test_case_name} fails, no exception got')
        return wrapper
    return decorator


@my_test(
    'invalid ship size',
    'ship size num must be in range "1...3", but "4" was given'
)
def test_invalid_ship_size():
    board = Board()
    board.add_ship('x', 4, 1, 1)


@my_test(
    'ships number interruption',
    'maximum number of ships with size 3 is 1, but attempted to insert 1th ship of such size'
)
def test_ships_number_interrupt():
    board = Board()
    board.add_ship('x', 3, 1, 1)
    board.add_ship('y', 3, 1, 3)


@my_test(
    'ships intersection',
    'Ship with upper_left_point=(2, 1), direction=y and size=2 can not be inserted as far as it is too close to Ship with upper_left_point=(1, 1), direction=x and size=3'
)
def test_ships_intersection():
    board = Board()
    board.add_ship('x', 3, 1, 1)
    board.add_ship('y', 2, 2, 1)


@my_test(
    'board interruption',
    'Ship with upper_left_point=(5, 1), direction=x and size=3 interrupts board size x=1...6, y=1...6'
)
def test_board_interruption():
    board = Board()
    board.add_ship('x', 3, 5, 1)


def run_tests():
    test_invalid_ship_size()
    test_ships_number_interrupt()
    test_ships_intersection()
    test_board_interruption()


if __name__ == '__main__':
    run_tests()
