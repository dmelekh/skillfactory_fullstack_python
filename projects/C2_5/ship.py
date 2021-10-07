

class Ship:

    @staticmethod
    def distance(pt1, pt2):
        return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5

    def __init__(self, direction, size, x, y):
        self._strRepr = f'Ship with upper_left_point=({x}, {y}), direction={direction} and size={size}'
        self._pts = set()
        self._hits = set()
        self._init_pts(direction, size, x, y)

    def _init_pts(self, direction, points_num, x, y):
        dx, dy = (1, 0) if direction.lower() == 'x' else (0, 1)
        for i in range(points_num):
            self._pts.add((x, y))
            x += dx
            y += dy

    def __str__(self):
        return self._strRepr

    @property
    def pts(self):
        return self._pts

    @property
    def hits(self):
        return self._hits

    def is_too_close_to(self, ship):
        distances = [Ship.distance(pt1, pt2) for pt1 in self.pts for pt2 in ship.pts]
        min_dist = min(distances)
        return min_dist < 1.99

    def try_hit_success(self, shot_pt):
        if shot_pt in self._hits:
            raise ValueError(f'!!! already been shot {shot_pt}')
        if shot_pt in self._pts:
            self._hits.add(shot_pt)
            return True
        return False

    def is_sunken(self):
        return self._pts == self._hits


