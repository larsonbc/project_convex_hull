from generate import generate_random_points
from test_utils import is_convex_hull, Timer

from byu_pytest_utils import tier, with_import

baseline = tier('basic', 1)
core = tier('core', 2)
stretch1 = tier('stretch1', 3)


def run_trapezoid(compute_hull):
    points = [(0, 0), (.25, 1), (1, 0), (.75, 1)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_half_tiny(compute_hull):
    points = [(0.6, 6.4),
              (1.4, 9.5),
              (2.1, 3.7),
              (3.2, 7.8)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_tiny(compute_hull):
    points = [(0.6, 6.4),
              (1.4, 9.5),
              (2.1, 3.7),
              (3.2, 7.8),
              (4.7, 8.1),
              (6.0, 2.3),
              (8.3, 3),
              (9.8, 5.6)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_tiny_2(compute_hull):
    points = [(2.3, 7.1), (8.6, 3.4), (4.9, 9.8), (1.2, 5.7),
              (6.5, 2.0), (7.9, 6.6), (0.8, 1.3), (9.2, 4.5)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_triangle(compute_hull):
    points = [(.1, .1), (0, 1), (.5, 0)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_funny_triangle(compute_hull):
    points = [(0, 0), (1, 1), (1.1, -1), (.5, .1)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_shared_tangent_point(compute_hull):
    points = [
        (6.6, 10.0),
        (4, 6.0),
        (10.0, 5.5),
        (0.0, 5.2),
        (4.2, 4.6),
        (7.0, 0.0),
    ]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_multiple_adjusts(compute_hull):
    # These points come from the convex hull example page
    points = [(0, 0), (1, 3), (1.9, 2.9), (2, 1), (1, -1), (3, 1.5),
              (3.1, 2.8), (4.1, 4), (5, 3), (5.1, .75), (4, .5), (3.5, .5)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_guassian(compute_hull, points, seed):
    points = generate_random_points('gaussian', points, seed)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_uniform(compute_hull, points, seed):
    points = generate_random_points('uniform', points, seed)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def run_performance(compute_hull):
    timer = Timer()
    for magnitude in [10, 100, 1000, 10000, 100000]:
        points = generate_random_points('gaussian', magnitude, 91)
        timer.start_lap()
        candidate_hull = compute_hull(points)
        assert is_convex_hull(candidate_hull, points)
        print(f'{magnitude} took {timer.lap_time()}')

        if timer.lap_time() > 15:
            assert False, "Timed out. The algorithm took too long to run"


# ------------- Baseline Tests ----------------------


@baseline
@with_import('convex_hull')
def test_trapezoid_dvcq(compute_hull_dvcq):
    run_trapezoid(compute_hull_dvcq)


@baseline
@with_import('convex_hull')
def test_half_tiny_dvcq(compute_hull_dvcq):
    run_half_tiny(compute_hull_dvcq)


@baseline
@with_import('convex_hull')
def test_tiny_dvcq(compute_hull_dvcq):
    run_tiny(compute_hull_dvcq)


@baseline
@with_import('convex_hull')
def test_tiny_2(compute_hull_dvcq):
    run_tiny_2(compute_hull_dvcq)


# ------------- Core Tests ----------------------


@core
@with_import('convex_hull')
def test_triangle_dvcq(compute_hull_dvcq):
    run_triangle(compute_hull_dvcq)


@core
@with_import('convex_hull')
def test_funny_triangle_dvcq(compute_hull_dvcq):
    run_funny_triangle(compute_hull_dvcq)


@core
@with_import('convex_hull')
def test_shared_tangent_point_dvcq(compute_hull_dvcq):
    run_shared_tangent_point(compute_hull_dvcq)


@core
@with_import('convex_hull')
def test_multiple_adjusts_dvcq(compute_hull_dvcq):
    run_multiple_adjusts(compute_hull_dvcq)


@core
@with_import('convex_hull')
def test_small_uniform_dvcq(compute_hull_dvcq):
    run_uniform(compute_hull_dvcq, 16, 26)


@core
@with_import('convex_hull')
def test_small_gaussian_dvcq(compute_hull_dvcq):
    run_guassian(compute_hull_dvcq, 16, 26)


@core
@with_import('convex_hull')
def test_uniform_mid_small_dvcq(compute_hull_dvcq):
    run_uniform(compute_hull_dvcq, 20, 312)


@core
@with_import('convex_hull')
def test_gaussian_mid_small_dvcq(compute_hull_dvcq):
    run_guassian(compute_hull_dvcq, 20, 312)


@core
@with_import('convex_hull')
def test_uniform_mid_dvcq(compute_hull_dvcq):
    run_uniform(compute_hull_dvcq, 1000, 312)


@core
@with_import('convex_hull')
def test_gaussian_mid_dvcq(compute_hull_dvcq):
    run_guassian(compute_hull_dvcq, 1000, 312)


@core
@with_import('convex_hull')
def test_uniform_large_dvcq(compute_hull_dvcq):
    run_uniform(compute_hull_dvcq, 10000, 312)


@core
@with_import('convex_hull')
def test_gaussian_large_dvcq(compute_hull_dvcq):
    run_guassian(compute_hull_dvcq, 10000, 312)


@core
@with_import('convex_hull')
def test_performance_dvcq(compute_hull_dvcq):
    run_performance(compute_hull_dvcq)


# ------------- Stretch 1 Tests ----------------------
@stretch1
@with_import('convex_hull')
def test_uniform_mid_small_other(compute_hull_other):
    run_uniform(compute_hull_other, 20, 312)


@stretch1
@with_import('convex_hull')
def test_gaussian_mid_small_other(compute_hull_other):
    run_guassian(compute_hull_other, 20, 312)


@stretch1
@with_import('convex_hull')
def test_uniform_mid_other(compute_hull_other):
    run_uniform(compute_hull_other, 1000, 312)


@stretch1
@with_import('convex_hull')
def test_gaussian_mid_other(compute_hull_other):
    run_guassian(compute_hull_other, 1000, 312)


@stretch1
@with_import('convex_hull')
def test_uniform_large_other(compute_hull_other):
    run_uniform(compute_hull_other, 10000, 312)


@stretch1
@with_import('convex_hull')
def test_gaussian_large_other(compute_hull_other):
    run_guassian(compute_hull_other, 10000, 312)


@stretch1
@with_import('convex_hull')
def test_performance_other(compute_hull_other):
    run_performance(compute_hull_other)
