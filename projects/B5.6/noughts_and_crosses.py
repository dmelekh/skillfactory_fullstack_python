
import re

DIMENSION = 3

pts_noughts = set()
pts_crosses = set()
coords = []
representation = []


def get_vector(pt1, pt2):
    return pt2[0]-pt1[0], pt2[1]-pt1[1]


def get_all_vectors(pt_set):
    min_vectors_num = DIMENSION - 1
    pts = list(pt_set)
    vectors_all = []
    for pt1_i in range(0, len(pts)-min_vectors_num):
        vectors_of_fixed_base_pt = []
        for pt2_i in range(pt1_i+1, len(pts)):
            vectors_of_fixed_base_pt.append(
                get_vector(pts[pt1_i], pts[pt2_i]))
        vectors_all.append(vectors_of_fixed_base_pt)
    return vectors_all


def vectors_are_collinear(vec1, vec2):
    return abs(vec1[0]*vec2[1]-vec1[1]*vec2[0]) < 0.0001


def contains_enough_collinear_vectors(vectors_all, enough_num_of_collinears):
    collinear_vectors_num = 0
    for vectors_of_fixed_base_pt in vectors_all:
        vfs = vectors_of_fixed_base_pt
        for base_vec_i in range(0, len(vfs)-(enough_num_of_collinears-1)):
            for target_vec_i in range(base_vec_i+1, len(vfs)):
                if vectors_are_collinear(vfs[base_vec_i], vfs[target_vec_i]):
                    collinear_vectors_num += 1
            if collinear_vectors_num >= enough_num_of_collinears-1:
                return True
            collinear_vectors_num = 0
    return False


def has_three_points_on_same_line(pt_set):
    min_pts_num = DIMENSION
    if len(pt_set) < min_pts_num:
        return False
    vectors_all = get_all_vectors(pt_set)
    return contains_enough_collinear_vectors(vectors_all, DIMENSION - 1)


def report_test(name, expected, got):
    state = 'passed' if got == expected else '!!! failed'
    print(f'{state} {name}')


def test_horizontal_solution():
    pt_set = {(0, 1), (0, 0), (0, 2)}
    res = has_three_points_on_same_line(pt_set)
    report_test('test_horizontal_solution', True, res)


def test_vertical_solution():
    pt_set = {(1, 2), (1, 0), (1, 1)}
    res = has_three_points_on_same_line(pt_set)
    report_test('test_vertical_solution', True, res)


def test_diagonal_solution():
    pt_set = {(2, 2), (0, 0), (1, 1)}
    res = has_three_points_on_same_line(pt_set)
    report_test('test_vertical_solution', True, res)


def test_horizontal_mismatch():
    pt_set = {(0, 1), (1, 0), (0, 2)}
    res = has_three_points_on_same_line(pt_set)
    report_test('test_horizontal_mismatch', False, res)


def test_vertical_mismatch():
    pt_set = {(2, 2), (1, 0), (1, 1)}
    res = has_three_points_on_same_line(pt_set)
    report_test('test_vertical_mismatch', False, res)


def test_diagonal_mismatch():
    pt_set = {(2, 2), (0, 1), (1, 1)}
    res = has_three_points_on_same_line(pt_set)
    report_test('test_diagonal_mismatch', False, res)


def test_lack_of_points():
    pt_set = {(2, 2), (0, 1)}
    res = has_three_points_on_same_line(pt_set)
    report_test('test_lack_of_points', False, res)


def test_empty():
    pt_set = {}
    res = has_three_points_on_same_line(pt_set)
    report_test('test_empty', False, res)


def startegy_add_coord(target, i, j):
    target.append((i, j))


def startegy_add_default_repr(target, i, j):
    target.append('-')


def init_matrix(matrix, append_strategy):
    for i in range(DIMENSION):
        curr_line = []
        for j in range(DIMENSION):
            append_strategy(curr_line, i, j)
        matrix.append(curr_line)


def init_coords():
    init_matrix(coords, startegy_add_coord)


def init_representation():
    init_matrix(representation, startegy_add_default_repr)


def init_globals():
    init_coords()
    init_representation()


def print_curr_matrix():
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            pt = coords[i][j]
            view = '-'
            if pt in pts_noughts:
                view = 'O'
            if pt in pts_crosses:
                view = 'X'
            representation[i][j] = view
    header_columns_coords = f'  {" ".join([str(i) for i in range(DIMENSION)])}'
    print('-'*len(header_columns_coords))
    print(header_columns_coords)
    for i in range(DIMENSION):
        print(f'{i} {" ".join(representation[i])}')


def coordinates_input(symbol):
    rexpr = r'^\d \d$'
    ui = input(
        f'{symbol} player, enter coordinates in the next format, please:\n`line num` `column num`\n')
    while True:
        if (not re.match(rexpr, ui)):
            ui = input('error: format is incorrect, try again\n')
            continue
        try:
            coords = tuple(map(int, ui.split()))
            if not (0 <= coords[0] < DIMENSION and 0 <= coords[1] < DIMENSION):
                ui = input(
                    f'error: coordinates must be in range [0...{DIMENSION})\n')
                continue
            if coords in pts_crosses or coords in pts_noughts:
                ui = input(
                    f'error: this coordinates are already busy, try again\n')
                continue
            return coords
        except:
            ui = input('error: coordinates must be type Integer\n')


def victory_message(winner_symbol):
    return f'{winner_symbol}-player won the game! Game Over!'


def print_finish_message(message):
    print('*'*len(message))
    print(message)
    print('*'*len(message))


def play():
    symbols = ['X', 'O']
    pts = [pts_crosses, pts_noughts]
    curr_step = 0
    while not (
        has_three_points_on_same_line(pts_noughts) or
        has_three_points_on_same_line(pts_crosses) or
        len(pts_crosses) + len(pts_noughts) == DIMENSION**2
    ):
        new_pt = coordinates_input(symbols[curr_step % 2])
        pts[curr_step % 2].add(new_pt)
        print_curr_matrix()
        curr_step += 1
    if (len(pts_crosses) + len(pts_noughts) == DIMENSION**2):
        print_finish_message('Draw Game! No Winner')
        return
    if (has_three_points_on_same_line(pts_noughts)):
        print_finish_message(victory_message('O'))
        return
    print_finish_message(victory_message('X'))


def run_tests():
    global DIMENSION
    DIMENSION = 3
    test_horizontal_solution()
    test_vertical_solution()
    test_diagonal_solution()
    test_horizontal_mismatch()
    test_vertical_mismatch()
    test_diagonal_mismatch()
    test_lack_of_points()
    test_empty()


def run_game():
    init_globals()
    print_curr_matrix()
    play()


if __name__ == '__main__':
    # run_tests()
    run_game()
