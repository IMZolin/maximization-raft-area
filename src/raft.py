from one_d_min_lib.One_D_Problem_file import *
import matplotlib.pyplot as plt
from constraints import *


def plot_fun(t0, t1, t2, t3, t4, t5, func2, raft1, river1):
    """
    строит график расстояния от плота до берега при значении параметра t
    """
    n = 20
    x1 = [t0 + (t1 - t0) / n * i for i in range(n + 1)]
    x2 = [t2 + (t3 - t2) / n * i for i in range(n + 1)]
    x3 = [t4 + (t5 - t4) / n * i for i in range(n + 1)]
    y1 = [phi1_stage_1(raft1, river1, x_) for x_ in x1]
    y2 = [func2(raft1, river1, x_) for x_ in x2]
    y3 = [phi1_stage_3(raft1, river1, x_) for x_ in x3]
    plt.plot(x1, y1, 'r')
    plt.plot([x2[i] + t1 - t2 for i in range(len(x2))], y2, 'g')
    plt.plot([x3[i] + t1 + (t3 - t2) - t4 for i in range(len(x2))], y3, 'b')
    plt.show()


class raft:
    def __init__(self, param_dict):
        self.params_is_fixed = param_dict
        self.params_values = {k: w or 0.1 for (k, w) in self.params_is_fixed.items()}

    def square(self):
        """
        площадь плота
        """
        return self.params_values['w'] * self.params_values['h'] + \
               self.params_values['a'] * self.params_values['q']

    def find_t0_t1(self, stage, z2=0):
        """
        Определение t0 и t1 - границ для решения задачи одномерной минимизации.
        По сути при граничных значениях мы получаем пограничное положение плота между stage-ами
        """
        ns = sqrt((self.params_values['w'] ** 2) / 4 + (self.params_values['h'] + self.params_values['q']) ** 2)
        nm = self.params_values['h']
        wm = ns
        ws = self.params_values['h'] + 2 * self.params_values['q']
        wx = ns
        wy = sqrt(self.params_values['q'] ** 2 + self.params_values['w'] ** 2 / 4)

        cos_a, sin_a = self.corner_alpha()
        cos_b, sin_b = self.corner_betta()
        cos_mnw, sin_mnw = cos_b * sin_a - sin_b * cos_a, sin_b * sin_a + cos_b * cos_a
        cos_xwy = (-self.params_values['h'] ** 2 + wy ** 2 + wx ** 2) / (2 * wx * wy)
        sin_xwy = sqrt(1 - cos_xwy ** 2)
        cos_mwx = 1 - 2 * (self.params_values['w'] / (2 * wx)) ** 2  # 1 - 2sin^2(a/2)
        sin_mwx = sqrt(1 - cos_mwx ** 2)
        cos_mwy, sin_mwy = cos_mwx * cos_xwy - sin_mwx * sin_xwy, sin_mwx * cos_xwy + cos_mwx * sin_xwy

        A = 1 - (wy / wm) * cos_mwy
        R = wy ** 2 / wm ** 2 * sin_mwy ** 2 + A ** 2
        M = 2 * z2 * (wy / wm) * sin_mwy
        W = A ** 2 * wm ** 2 - z2 ** 2
        D = M ** 2 + 4 * W * R

        try:
            t_max = (M + sqrt(D)) / (2 * R)  # y2 < z2
            # y_2 = (wy / wm) * (t_max * sin_mwy - sqrt(wm ** 2 - t_max ** 2) * cos_mwy) + sqrt(wm ** 2 - t_max ** 2)
        except:
            t_max = -1

        if stage == '1':
            t0 = self.params_values['w'] / 2
            t1 = ns * min(sin_b,
                          (ns / nm - sin_a) / sqrt((ns / nm) ** 2 - 2 * (ns / nm) * sin_a + 1))
            return t0, t1

        if stage == '2_a':
            t0 = ns * (ns / nm - sin_a) / sqrt((ns / nm) ** 2 - 2 * (ns / nm) * sin_a + 1) - sqrt(
                nm ** 2 + ns ** 2 - 2 * nm * ns * sin_a)
            t1 = nm * sin_mnw

            return t0, t1

        if stage == '3_a':
            t0 = nm * sin_mnw
            return t0, t_max

        if stage == '2_b':
            t0 = ns * sin_b
            t1 = ws * (ws / wm - sin_a) / sqrt((ws / wm) ** 2 - 2 * (ws / wm) * sin_a + 1)

            return t0, t1

        if stage == '3_b':
            wm = ns
            ws = self.params_values['h'] + 2 * self.params_values['q']
            cos_mws = (self.params_values['h'] + self.params_values['q']) / wm
            t0 = ws * (ws / wm - sin_a) / sqrt((ws / wm) ** 2 - 2 * (ws / wm) * sin_a + 1) - sqrt(
                wm ** 2 + ws ** 2 - 2 * wm * ws * cos_mws)
            t1 = t_max

            return t0, t1

    def corner_gamma(self):
        cos_gamma = (self.params_values['w'] ** 2 + 2 * self.params_values['h'] ** 2 + 2 * self.params_values['h'] *
                     self.params_values['q']) / (2 * (
                sqrt(self.params_values['w'] ** 2 + self.params_values['h'] ** 2) * sqrt(
            ((self.params_values['w'] ** 2) / 4) + (self.params_values['h'] + self.params_values['q']) ** 2)))
        sin_gamma = sqrt(1 - cos_gamma ** 2)
        return cos_gamma, sin_gamma

    def corner_alpha(self):
        cos_alpha = self.params_values['w'] / (2 * sqrt(
            (self.params_values['h'] + self.params_values['q']) ** 2 + (self.params_values['w'] ** 2) / 4))
        sin_alpha = sqrt(1 - cos_alpha ** 2)
        return cos_alpha, sin_alpha

    def corner_omega(self):
        cos_omega = self.params_values['w'] / (
                2 * sqrt((self.params_values['w'] ** 2) / 4 + self.params_values['q'] ** 2))
        sin_omega = sqrt(1 - cos_omega ** 2)
        return cos_omega, sin_omega

    def corner_betta(self):
        cos_alpha, sin_alpha = self.corner_alpha()
        cos_omega, sin_omega = self.corner_omega()
        sin_betta = sin_alpha * cos_omega + cos_alpha * sin_omega
        cos_betta = cos_alpha * cos_omega - sin_alpha * sin_omega
        return cos_betta, sin_betta

    def stages_sequence(self):
        """
        метод определяет, какая последовательность stage-й будет у данной конфигурации плота
        """
        s = sqrt((self.params_values['w'] ** 2) / 4 +
                 (self.params_values['h'] + self.params_values['q']) ** 2)
        m = self.params_values['h']
        cos_a, sin_a = self.corner_alpha()
        cos_b, sin_b = self.corner_betta()
        if sin_b > (s / m - sin_a) / sqrt((s / m) ** 2 - 2 * (s / m) * sin_a + 1):
            return 1
        else:
            return 0


class river_turn:
    def __init__(self, z1, z2):
        self.corner_coords = [z1, z2]


class raft_makes_right_turn_stage:
    def __init__(self, my_raft, my_river, t0, t1, phi_1):
        self.accuracy = 0.001  # точность, с которой мы будем решать задачу. Согласовать её с этапами
        self.my_river = my_river
        self.my_raft = my_raft  # допустимая точка
        self.t0 = t0
        self.t1 = t1
        self.phi_1 = phi_1

    def constraint(self, my_raft):
        pr = One_D_Problem(self.t0, self.t1, lambda t: self.phi_1(my_raft, self.my_river, t))
        return pr.golden_search(self.accuracy)[0]


def nabla_phi(stage, phi, my_raft_params_array, my_river):
    my_raft = raft({'w': my_raft_params_array[0],
                    'h': my_raft_params_array[1],
                    'a': my_raft_params_array[2],
                    'q': my_raft_params_array[3]})

    nbl = []
    for key in my_raft.params_values.keys():
        tmp_raft = raft(my_raft.params_values)
        tmp_raft.params_values[key] += 0.01

        t0, t1 = my_raft.find_t0_t1(f'{stage}')
        t00, t11 = tmp_raft.find_t0_t1(f'{stage}')
        stage_1 = raft_makes_right_turn_stage(my_raft, my_river, t0, t1, phi)
        stage_1_ = raft_makes_right_turn_stage(tmp_raft, my_river, t00, t11, phi)

        t_star_1 = stage_1.constraint(my_raft)
        d1 = stage_1.phi_1(my_raft, my_river, t_star_1)

        t_star_1_ = stage_1_.constraint(tmp_raft)
        d1_ = stage_1_.phi_1(tmp_raft, my_river, t_star_1_)

        nbl.append(-1 * (d1_ - d1) / 0.01)

    return nbl


