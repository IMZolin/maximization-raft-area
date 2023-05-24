from main_algorithm import start_raft
from raft import raft, river_turn, nabla_phi, raft_makes_right_turn_stage
from vizualization_lib.raft_visualisation.main import vizualization
from constraints import *
from zoitendeik_lib.Zoitendeik import *
from raft_parametrs import get_data_for_visualization


def super_fun(stage, phi, my_raft_params_array, my_river):
    """
    На вход получаем массив значений конфигурации, а также этап.
    Строим плот и считаем значение минимального расстояния на данном этапе.
    Его и возвращаем.
    """
    my_raft = raft({'w': my_raft_params_array[0],
                    'h': my_raft_params_array[1],
                    'a': my_raft_params_array[2],
                    'q': my_raft_params_array[3]})
    t0, t1 = my_raft.find_t0_t1(f'{stage}')
    stage_1 = raft_makes_right_turn_stage(my_raft, my_river, t0, t1, phi)
    t_star_1 = stage_1.constraint(my_raft)
    d1 = stage_1.phi_1(my_raft, my_river, t_star_1)

    return d1


def arr_stage_sequence(arr):
    """
    Создаем плот по массиву
    """
    my_raft = raft({'w': arr[0],
                    'h': arr[1],
                    'a': arr[2],
                    'q': arr[3]})
    return my_raft.stages_sequence()


if __name__ == '__main__':
    raft11 = raft({'w': 60, 'h': 80, 'a': 40, 'q': 40})
    river11 = river_turn(140, 160)
    eps11 = 0.1

    phi0 = Target_function(lambda x: -1 * (x[0] * x[1] + x[2] * x[3]),
                           lambda x: [-x[1], -x[0], -x[3], -x[2]])

    phi1 = Constraint('ineq',
                      lambda x: -1 * super_fun('1', phi1_stage_1, x, river11) + eps11,
                      lambda x: nabla_phi('1', phi1_stage_1, x, river11))

    phi2 = Constraint('ineq',
                      lambda x: -x[0] + x[2] + eps11,
                      lambda x: [-1, 0, 1, 0])

    phi3 = Constraint('ineq',
                      lambda x: -1 * super_fun('2_a', phi1_stage_2_a, x, river11) + eps11 if arr_stage_sequence(x) else -1 * super_fun('2_b', phi1_stage_2_b, x, river11) + eps11,
                      lambda x: nabla_phi('2_a', phi1_stage_2_a, x, river11) if arr_stage_sequence(x) else nabla_phi('2_b', phi1_stage_2_b, x, river11))

    phi4 = Constraint('ineq',
                      lambda x: -1 * super_fun('3_a', phi1_stage_3, x, river11) + eps11 if arr_stage_sequence(
                          x) else -1 * super_fun('3_b', phi1_stage_3, x, river11) + eps11,
                      lambda x: nabla_phi('3_a', phi1_stage_3, x, river11) if arr_stage_sequence(x) else nabla_phi(
                          '3_b', phi1_stage_3, x, river11))

    z = Zoitendeik_step(phi0, [phi1, phi2, phi3, phi4], [120.0, 150.0, 40.0, 20.0], 0.25, 6.0)

    x_ = z.minimize()

    rr = raft({'w': x_[0],
               'h': x_[1],
               'a': x_[2],
               'q': x_[3]})
    move_params = get_data_for_visualization(rr, river11)
    vizualization(move_params[0], move_params[1], move_params[2],
                  rr.params_values, river11.corner_coords)
