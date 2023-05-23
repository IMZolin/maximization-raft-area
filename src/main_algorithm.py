from raft import *
from raft_parametrs import *


def start_raft(my_raft, my_river, my_eps, my_param):
    raft1 = my_raft
    river1 = my_river
    eps = my_eps
    param = my_param  # 'h' for example
    lmd = 2

    raft_tmp = raft1
    distance = 10  # init by  > eps
    while distance > eps and river1.corner_coords[1] - raft_tmp.params_values['w'] > eps:

        raft_tmp.params_values[f'{param}'] += lmd

        t0, t1 = raft_tmp.find_t0_t1('1')
        stage_1 = raft_makes_right_turn_stage(raft_tmp, river1, t0, t1, phi1_stage_1)
        t_star_1 = stage_1.constraint(raft_tmp)
        d1 = stage_1.phi_1(raft_tmp, river1, t_star_1)

        if not raft_tmp.stages_sequence():
            t00, t11 = raft_tmp.find_t0_t1('2_b')
            stage_2 = raft_makes_right_turn_stage(raft_tmp, river1, t00, t11, phi1_stage_2_b)
            t_star_2 = stage_2.constraint(raft_tmp)
            d2 = stage_2.phi_1(raft_tmp, river1, t_star_2)

            t000, t111 = raft_tmp.find_t0_t1('3_b', river1.corner_coords[1])

        else:
            t00, t11 = raft_tmp.find_t0_t1('2_a')
            stage_2 = raft_makes_right_turn_stage(raft_tmp, river1, t00, t11, phi1_stage_2_a)
            t_star_2 = stage_2.constraint(raft_tmp)
            d2 = stage_2.phi_1(raft_tmp, river1, t_star_2)

            t000, t111 = raft_tmp.find_t0_t1('3_a', river1.corner_coords[1])

        if t000 < t111:  # если y2 уже выше z2
            stage_3 = raft_makes_right_turn_stage(raft_tmp, river1, t000, t111, phi1_stage_3)
            t_star_3 = stage_3.constraint(raft_tmp)
            d3 = stage_3.phi_1(raft_tmp, river1, t_star_1)

        else:
            d3 = d2
            t_star_3 = None

        distance = min(d1, d2, d3)
        print()
        print('t: ', t_star_1, t_star_2, t_star_3)
        print('d: ', d1, d2, d3)

        if (distance < 0) or (raft_tmp.params_values['w'] >= river1.corner_coords[1]):
            raft_tmp.params_values[f'{param}'] -= lmd  # возвращаем как было
            lmd = lmd / 2
            distance = eps + 1  # на этом этапе нельзя заканчивать цикл
        else:
            raft1 = raft_tmp

    print('\nFINAL DISTANCE:', distance)
    print('\nFINAL PARAMS:', raft1.params_values)
    print()

    return get_data_for_visualization(raft1, river1)