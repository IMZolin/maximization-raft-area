from math import sqrt, degrees
import numpy as np


def get_data_for_visualization(my_raft, my_river):
    c_1 = []
    c_2 = []
    alf = []
    n = 20

    '''--st1---'''

    nx = sqrt(my_raft.params_values['w'] ** 2 + my_raft.params_values['h'] ** 2)
    ny = my_raft.params_values['w']
    ns = sqrt(my_raft.params_values['w'] ** 2 / 4 + (my_raft.params_values['h'] + my_raft.params_values['q']) ** 2)
    cos_a, sin_a = my_raft.corner_alpha()
    cos_g, sin_g = my_raft.corner_gamma()

    t0, t1 = my_raft.find_t0_t1('1')
    t01 = [t0 + (t1 - t0)/n * i for i in range(n+1)]
    x_1 = lambda t: (nx / ns) * (t * cos_g + sqrt(ns ** 2 - t ** 2) * sin_g)
    x_2 = lambda t: (nx / ns) * (t * sin_g - sqrt(ns ** 2 - t ** 2) * cos_g) + sqrt(ns ** 2 - t ** 2)
    y_1 = lambda t: (ny / ns) * (t * cos_a + sqrt(ns ** 2 - t ** 2) * sin_a)
    y_2 = lambda t: (ny / ns) * (t * sin_a - sqrt(ns ** 2 - t ** 2) * cos_a) + sqrt(ns ** 2 - t ** 2)

    c_1 += [0.5 * x_1(t_) + 0.5 * 0 for t_ in t01]
    c_2 += [0.5 * x_2(t_) + 0.5 * sqrt(ns ** 2 - t_ ** 2) for t_ in t01]

    alf += [degrees(np.arccos((y_1(t_) * 1 + y_2(t_) * 0) / ny)) for t_ in t01]

    '''--st2---'''

    if not my_raft.stages_sequence():
        t00, t11 = my_raft.find_t0_t1('2_b')
        t0011 = [t00 + (t11 - t00) / n * i for i in range(n + 1)]
        ws = my_raft.params_values['h'] + 2 * my_raft.params_values['q']

        c_1 += [0.5 * t_ for t_ in t0011]
        c_2 += [0.5 * sqrt(ws**2 - t_**2) for t_ in t0011]

        alf += [degrees(np.arccos((sqrt(ws**2 - t_**2) * 1 - t_ * 0) / ws)) for t_ in t0011]

        t000, t111 = my_raft.find_t0_t1('3_b', my_river.corner_coords[1])
        t000111 = [t000 + (t111 - t000)/n * i for i in range(n+1)]

    else:
        t00, t11 = my_raft.find_t0_t1('2_a')
        t0011 = [t00 + (t11 - t00) / n * i for i in range(n + 1)]

        nx = sqrt(my_raft.params_values['w'] ** 2 + my_raft.params_values['h'] ** 2)
        ny = my_raft.params_values['w']
        nm = my_raft.params_values['h']
        cos_a, sin_a = my_raft.corner_alpha()
        cos_g, sin_g = my_raft.corner_gamma()
        cos_mnx, sin_mnx = sin_a * cos_g - sin_g * cos_a, cos_a * cos_g + sin_a * sin_g
        z_1 = my_river.corner_coords[0]
        z_2 = my_river.corner_coords[1]
        x_1 = lambda t: (nx / nm) * (t * cos_mnx + sqrt(nm ** 2 - t ** 2) * sin_mnx)
        x_2 = lambda t: (nx / nm) * (t * sin_mnx - sqrt(nm ** 2 - t ** 2) * cos_mnx) + sqrt(nm ** 2 - t ** 2)
        y_1 = lambda t: (ny / nm) * (0 + sqrt(nm ** 2 - t ** 2) * 1)
        y_2 = lambda t: (ny / nm) * (1 * t + 0) + sqrt(nm ** 2 - t ** 2)

        c_1 += [0.5 * x_1(t_) for t_ in t0011]
        c_2 += [0.5 * sqrt(nm ** 2 - t_ ** 2) + 0.5 * x_2(t_) for t_ in t0011]

        alf += [degrees(np.arccos((y_1(t_) * 1 - t_ * 0) / ny)) for t_ in t0011]

        t000, t111 = my_raft.find_t0_t1('3_a', my_river.corner_coords[1])
        t000111 = [t000 + (t111 - t000) / n * i for i in range(n + 1)]

    '''--st3---'''

    if t111 > t000:

        wx = sqrt(my_raft.params_values['w'] ** 2 / 4 + (my_raft.params_values['h'] + my_raft.params_values['q']) ** 2)
        wy = sqrt(my_raft.params_values['q'] ** 2 + my_raft.params_values['w'] ** 2 / 4)
        wm = wx
        xy = my_raft.params_values['h']
        cos_xwy = (-my_raft.params_values['h'] ** 2 + wy ** 2 + wx ** 2) / (2 * wx * wy)  # minus!!!!!!!!
        sin_xwy = sqrt(1 - cos_xwy ** 2)
        cos_mwx = 1 - 2 * (my_raft.params_values['w'] / (2 * wx)) ** 2  # 1 - 2sin^2(a/2)
        sin_mwx = sqrt(1 - cos_mwx ** 2)
        cos_mwy, sin_mwy = cos_mwx * cos_xwy - sin_mwx * sin_xwy, sin_mwx * cos_xwy + cos_mwx * sin_xwy

        x_1 = lambda t: (wx / wm) * (t * cos_mwx + sqrt(wm ** 2 - t ** 2) * sin_mwx)
        x_2 = lambda t: (wx / wm) * (t * sin_mwx - sqrt(wm ** 2 - t ** 2) * cos_mwx) + sqrt(wm ** 2 - t ** 2)
        y_1 = lambda t: (wy / wm) * (t * cos_mwy + sqrt(wm ** 2 - t ** 2) * sin_mwy)
        y_2 = lambda t: (wy / wm) * (t * sin_mwy - sqrt(wm ** 2 - t ** 2) * cos_mwy) + sqrt(wm ** 2 - t ** 2)

        c_1 += [0.5 * y_1(t_) + 0.5 * t_ for t_ in t000111]
        c_2 += [0.5 * y_2(t_) + 0.5 * 0 for t_ in t000111]

        alf += [degrees(np.arccos((-(x_2(t_) - y_2(t_)) * 1 - (x_1(t_) - y_1(t_)) * 0) / xy)) for t_ in t000111]

    return c_1, c_2, alf