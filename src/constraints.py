from math import sqrt


def phi1_stage_1(my_raft, my_river, t):  # n-s
    nx = sqrt(my_raft.params_values['w'] ** 2 + my_raft.params_values['h'] ** 2)
    ny = my_raft.params_values['w']
    ns = sqrt(my_raft.params_values['w'] ** 2 / 4 + (my_raft.params_values['h'] + my_raft.params_values['q']) ** 2)
    cos_a, sin_a = my_raft.corner_alpha()
    cos_g, sin_g = my_raft.corner_gamma()
    z_1 = my_river.corner_coords[0]
    z_2 = my_river.corner_coords[1]
    x_1 = (nx / ns) * (t * cos_g + sqrt(ns ** 2 - t ** 2) * sin_g)
    x_2 = (nx / ns) * (t * sin_g - sqrt(ns ** 2 - t ** 2) * cos_g) + sqrt(ns ** 2 - t ** 2)
    y_1 = (ny / ns) * (t * cos_a + sqrt(ns ** 2 - t ** 2) * sin_a)
    y_2 = (ny / ns) * (t * sin_a - sqrt(ns ** 2 - t ** 2) * cos_a) + sqrt(ns ** 2 - t ** 2)

    return z_1 - 1 / (x_2 - y_2) * ((z_2 - y_2) * x_1 + (x_2 - z_2) * y_1)


def phi1_stage_2_a(my_raft, my_river, t):  # n-m
    nx = sqrt(my_raft.params_values['w'] ** 2 + my_raft.params_values['h'] ** 2)
    ny = my_raft.params_values['w']
    nm = my_raft.params_values['h']
    cos_a, sin_a = my_raft.corner_alpha()
    cos_g, sin_g = my_raft.corner_gamma()
    cos_mnx, sin_mnx = sin_a * cos_g - sin_g * cos_a, cos_a * cos_g + sin_a * sin_g
    z_1 = my_river.corner_coords[0]
    z_2 = my_river.corner_coords[1]
    x_1 = (nx / nm) * (t * cos_mnx + sqrt(nm ** 2 - t ** 2) * sin_mnx)
    x_2 = (nx / nm) * (t * sin_mnx - sqrt(nm ** 2 - t ** 2) * cos_mnx) + sqrt(nm ** 2 - t ** 2)
    y_1 = (ny / nm) * (0 + sqrt(nm ** 2 - t ** 2) * 1)
    y_2 = (ny / nm) * (1 * t + 0) + sqrt(nm ** 2 - t ** 2)

    return z_1 - 1 / (x_2 - y_2) * ((z_2 - y_2) * x_1 + (x_2 - z_2) * y_1)


def phi1_stage_2_b(my_raft, my_river, t):  # w-m
    wx = sqrt(my_raft.params_values['w'] ** 2 / 4 + (my_raft.params_values['h'] + my_raft.params_values['q']) ** 2)
    wy = sqrt(my_raft.params_values['q'] ** 2 + my_raft.params_values['w'] ** 2 / 4)
    ws = my_raft.params_values['h'] + 2 * my_raft.params_values['q']
    cos_a, sin_a = my_raft.corner_alpha()
    cos_g, sin_g = my_raft.corner_gamma()
    cos_xwy = (-my_raft.params_values['h'] ** 2 + wy ** 2 + wx ** 2) / (2 * wx * wy)  # minus!!!!!!!!
    sin_xwy = sqrt(1 - cos_xwy ** 2)
    cos_swy = cos_xwy * sin_a - cos_a * sin_xwy  # тут все верно, т.к. 90 - alfa
    sin_swy = sqrt(1 - cos_swy ** 2)

    z_1 = my_river.corner_coords[0]
    z_2 = my_river.corner_coords[1]
    x_1 = (wx / ws) * (t * sin_a + sqrt(ws ** 2 - t ** 2) * cos_a)
    x_2 = (wx / ws) * (t * cos_a - sqrt(ws ** 2 - t ** 2) * sin_a) + sqrt(ws ** 2 - t ** 2)
    y_1 = (wy / ws) * (t * cos_swy + sqrt(ws ** 2 - t ** 2) * sin_swy)
    y_2 = (wy / ws) * (t * sin_swy - sqrt(ws ** 2 - t ** 2) * cos_swy) + sqrt(ws ** 2 - t ** 2)  # minus

    return z_1 - 1 / (x_2 - y_2) * ((z_2 - y_2) * x_1 + (x_2 - z_2) * y_1)


def phi1_stage_3(my_raft, my_river, t):  # w-s
    wx = sqrt(my_raft.params_values['w'] ** 2 / 4 + (my_raft.params_values['h'] + my_raft.params_values['q']) ** 2)
    wy = sqrt(my_raft.params_values['q'] ** 2 + my_raft.params_values['w'] ** 2 / 4)
    wm = wx
    cos_xwy = (-my_raft.params_values['h'] ** 2 + wy ** 2 + wx ** 2) / (2 * wx * wy)  # minus!!!!!!!!
    sin_xwy = sqrt(1 - cos_xwy ** 2)
    cos_mwx = 1 - 2 * (my_raft.params_values['w'] / (2 * wx)) ** 2  # 1 - 2sin^2(a/2)
    sin_mwx = sqrt(1 - cos_mwx ** 2)
    cos_mwy, sin_mwy = cos_mwx * cos_xwy - sin_mwx * sin_xwy, sin_mwx * cos_xwy + cos_mwx * sin_xwy
    z_1 = my_river.corner_coords[0]
    z_2 = my_river.corner_coords[1]
    x_1 = (wx / wm) * (t * cos_mwx + sqrt(wm ** 2 - t ** 2) * sin_mwx)
    x_2 = (wx / wm) * (t * sin_mwx - sqrt(wm ** 2 - t ** 2) * cos_mwx) + sqrt(wm ** 2 - t ** 2)
    y_1 = (wy / wm) * (t * cos_mwy + sqrt(wm ** 2 - t ** 2) * sin_mwy)
    y_2 = (wy / wm) * (t * sin_mwy - sqrt(wm ** 2 - t ** 2) * cos_mwy) + sqrt(wm ** 2 - t ** 2)

    return z_1 - 1 / (x_2 - y_2) * ((z_2 - y_2) * x_1 + (x_2 - z_2) * y_1)




