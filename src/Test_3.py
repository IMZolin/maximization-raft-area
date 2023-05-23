from raft import *
from raft_parametrs import *

if __name__ == '__main__':
    raft1 = raft({'w': 6, 'h': 5, 'a': 2, 'q': 2})
    river1 = river_turn(8, 6)

    print(get_data_for_visualization(raft1, river1))
