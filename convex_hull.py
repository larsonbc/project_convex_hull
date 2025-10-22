# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point


def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    # return []
    if not points:
        return []

        # Sort points by x-coordinate (and by y if x is equal)
    sorted_points = sorted(points, key=lambda p: (p[0], p[1]))

    # Call recursive function
    hull = divide_conquer_hull(sorted_points)

    return hull


def divide_conquer_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Recursively compute convex hull using divide and conquer"""
    n = len(points)

    # Base case: 1 point
    if n == 1:
        return [points[0]]

    # Base case: 2 points - return with bottom point first
    if n == 2:
        # Both points are on the hull, order them consistently
        # Since points are sorted by x, and we want counter-clockwise order,
        # we need to ensure we go from bottom to top
        if points[0][1] < points[1][1]:
            return [points[0], points[1]]
        elif points[0][1] > points[1][1]:
            return [points[1], points[0]]
        else:
            # Same y-coordinate, already sorted by x
            return [points[0], points[1]]

    # Base case: 3 points - compute hull
    if n == 3:
        return convex_hull_3(points[0], points[1], points[2])

    # Divide: split into left and right halves
    mid = n // 2
    left_points = points[:mid]
    right_points = points[mid:]

    # Conquer: recursively find hulls
    left_hull = divide_conquer_hull(left_points)
    right_hull = divide_conquer_hull(right_points)

    # Combine: merge the two hulls
    merged_hull = merge_hulls(left_hull, right_hull)

    return merged_hull


def convex_hull_3(p1: tuple[float, float], p2: tuple[float, float],
                  p3: tuple[float, float]) -> list[tuple[float, float]]:
    """Compute convex hull of 3 points, returning them in counter-clockwise order from bottom-left"""
    # Sort by x-coordinate
    points = sorted([p1, p2, p3], key=lambda p: (p[0], p[1]))
    a, b, c = points[0], points[1], points[2]

    # Calculate cross product to check if c is left or right of line a-b
    cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    if cross > 0:
        # Counter-clockwise: a, b, c
        return [a, b, c]
    elif cross < 0:
        # Clockwise: need a, c, b for counter-clockwise
        return [a, c, b]
    else:
        # Collinear: return just the two endpoints
        if b[1] < a[1] or (b[1] == a[1] and b[0] < a[0]):
            a, b = b, a
        if c[1] < a[1] or (c[1] == a[1] and c[0] < a[0]):
            a, c = c, a
        if c[1] < b[1] or (c[1] == b[1] and c[0] < b[0]):
            b, c = c, b
        # Return bottom and top points
        return [a, c]


def merge_hulls(left_hull: list[tuple[float, float]],
                right_hull: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Merge two convex hulls by finding upper and lower tangents"""
    n_left = len(left_hull)
    n_right = len(right_hull)

    # Find rightmost point of left hull
    left_right = 0
    for i in range(1, n_left):
        if left_hull[i][0] > left_hull[left_right][0]:
            left_right = i

    # Find leftmost point of right hull
    right_left = 0
    for i in range(1, n_right):
        if right_hull[i][0] < right_hull[right_left][0]:
            right_left = i

    # Find upper and lower tangents
    upp_l, upp_r = find_upper_tangent(left_hull, right_hull, left_right, right_left)
    low_l, low_r = find_lower_tangent(left_hull, right_hull, left_right, right_left)

    # Construct the merged hull
    result = []

    # Add points from left hull starting at lower tangent, going to upper tangent
    idx = low_l
    while True:
        result.append(left_hull[idx])
        if idx == upp_l:
            break
        idx = (idx + 1) % n_left

    # Add points from right hull starting at upper tangent, going to lower tangent
    idx = upp_r
    while True:
        result.append(right_hull[idx])
        if idx == low_r:
            break
        idx = (idx + 1) % n_right

    return result


def find_upper_tangent(left_hull: list[tuple[float, float]],
                       right_hull: list[tuple[float, float]],
                       l: int, r: int) -> tuple[int, int]:
    """Find the upper common tangent between two convex hulls"""
    n_left = len(left_hull)
    n_right = len(right_hull)

    done = False
    while not done:
        done = True

        # Move counter-clockwise on left hull if slope increases
        while True:
            l_next = (l - 1 + n_left) % n_left
            if slope(left_hull[l_next], right_hull[r]) > slope(left_hull[l], right_hull[r]):
                l = l_next
                done = False
            else:
                break

        # Move clockwise on right hull if slope increases
        while True:
            r_next = (r + 1) % n_right
            if slope(left_hull[l], right_hull[r_next]) < slope(left_hull[l], right_hull[r]):
                r = r_next
                done = False
            else:
                break

    return l, r


def find_lower_tangent(left_hull: list[tuple[float, float]],
                       right_hull: list[tuple[float, float]],
                       l: int, r: int) -> tuple[int, int]:
    """Find the lower common tangent between two convex hulls"""
    n_left = len(left_hull)
    n_right = len(right_hull)

    done = False
    while not done:
        done = True

        # Move clockwise on left hull if slope decreases
        while True:
            l_next = (l + 1) % n_left
            if slope(left_hull[l_next], right_hull[r]) < slope(left_hull[l], right_hull[r]):
                l = l_next
                done = False
            else:
                break

        # Move counter-clockwise on right hull if slope decreases
        while True:
            r_next = (r - 1 + n_right) % n_right
            if slope(left_hull[l], right_hull[r_next]) > slope(left_hull[l], right_hull[r]):
                r = r_next
                done = False
            else:
                break

    return l, r


def slope(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calculate the slope between two points"""
    if p2[0] == p1[0]:
        return float('inf') if p2[1] > p1[1] else float('-inf')
    return (p2[1] - p1[1]) / (p2[0] - p1[0])



def compute_hull_other(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    # return []

    if len(points) < 3:
        return points

        # Find the leftmost point (guaranteed to be on hull)
    start = min(points, key=lambda p: (p[0], p[1]))

    hull = []
    current = start

    while True:
        hull.append(current)
        next_point = points[0]

        # Find the most counter-clockwise point from current
        for candidate in points:
            if candidate == current:
                continue

            # If next_point is the same as current, or candidate is more counter-clockwise
            if next_point == current:
                next_point = candidate
            else:
                # Use cross product to determine orientation
                cross = orientation(current, next_point, candidate)

                # If candidate is more counter-clockwise (or collinear but farther)
                if cross > 0:
                    next_point = candidate
                elif cross == 0:
                    # Collinear case - pick the farther point
                    if distance_squared(current, candidate) > distance_squared(current, next_point):
                        next_point = candidate

        current = next_point

        # If we've wrapped around to the start, we're done
        if current == start:
            break

    return hull


def orientation(p: tuple[float, float], q: tuple[float, float],
                r: tuple[float, float]) -> float:
    """
    Calculate orientation of ordered triplet (p, q, r).
    Returns:
        > 0: counter-clockwise (r is left of line p->q)
        = 0: collinear
        < 0: clockwise (r is right of line p->q)
    """
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def distance_squared(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Calculate squared distance between two points (avoids sqrt for efficiency)"""
    return (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2
