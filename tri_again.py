import copy
import itertools

board = ((71, 1, 1, 71, 711, 711, 17, 711, 71, 1, 71, 17, 71, 711, 711, 1),
         (71, 711, 17, 71, 711, 17, 1, 71, 17, 17, 711, 711, 17, 711, 1, 71),
         (17, 711, 1, 711, 71, 1, 711, 17, 711, 1, 711, 17, 71, 1, 17, 711),
         (1, 71, 1, 71, 17, 711, 71, 71, 17, 711, 1, 17, 71, 711, 71),
         (1, 71, 711, 71, 17, 1, 711, 17, 71, 1, 71, 17, 71, 711, 71, 17),
         (71, 711, 1, 71, 17, 1, 711, 1, 711, 71, 1, 71, 17, 711, 71),
         (71, 1, 711, 17, 17, 1, 711, 17, 71, 1, 711, 17, 1, 711, 711, 17),
         (1, 711, 1, 17, 711, 71, 711, 1, 71, 17, 711, 71, 711, 17, 17, 1))


def move(cur_pose, direction, cur_index):
    """
    given current position and pose, and the direction of the next move, return the next pose and next position
    :param cur_pose: in the form [mode, a, b, c, d]
    :param direction: 1, 2, 3, indicates three directions, corresponds to a, b, c
    :param cur_index: current position
    :return: next_pose, next_position
    """
    if cur_pose[0]:  # bottom triangle pointing up, i.e. mode 1
        if direction == 1:
            return [0, cur_pose[2], cur_pose[4], cur_pose[3], cur_pose[1]], [cur_index[0], cur_index[1]-1]
        elif direction == 2:
            return [0, cur_pose[1], cur_pose[3], cur_pose[4], cur_pose[2]], [cur_index[0], cur_index[1]+1]
        else:
            return [0, cur_pose[4], cur_pose[2], cur_pose[1], cur_pose[3]], [cur_index[0]+1, cur_index[1]+1]
    else:  # pointing down, i.e. mode 0
        if direction == 1:
            return [1, cur_pose[3], cur_pose[2], cur_pose[4], cur_pose[1]], [cur_index[0]-1, cur_index[1]-1]
        elif direction == 2:
            return [1, cur_pose[4], cur_pose[1], cur_pose[3], cur_pose[2]], [cur_index[0], cur_index[1]+1]
        else:
            return [1, cur_pose[1], cur_pose[4], cur_pose[2], cur_pose[3]], [cur_index[0], cur_index[1]-1]


def get_item(i, j):  # to deal with negative indexing in python
    if i < 0 or j < 0:
        return None
    else:
        return board[i][j]


def find_possible_direction(cur_pose, cur_index):
    """
    give the pose and position, find all possible directions for the next move
    using exception to handle the condition that index crosses the border
    :param cur_pose:
    :param cur_index:
    :return: a list containing all directions
    """
    possible_directions = []
    if cur_pose[0]:  # pointing up
        try:  # try direction 1
            if get_item(cur_index[0], cur_index[1]-1) == cur_pose[1]:
                possible_directions.append(1)
        except IndexError:
            pass

        try:  # try direction 2
            if get_item(cur_index[0], cur_index[1]+1) == cur_pose[2]:
                possible_directions.append(2)
        except IndexError:
            pass

        try:  # try direction 3
            if get_item(cur_index[0]+1, cur_index[1]+1) == cur_pose[3]:
                possible_directions.append(3)
        except IndexError:
            pass
    else:  # pointing down
        try:  # try direction 1
            if get_item(cur_index[0]-1, cur_index[1]-1) == cur_pose[1]:
                possible_directions.append(1)
        except IndexError:
            pass

        try:  # try direction 2
            if get_item(cur_index[0], cur_index[1]+1) == cur_pose[2]:
                possible_directions.append(2)
        except IndexError:
            pass

        try:  # try direction 3
            if get_item(cur_index[0], cur_index[1]-1) == cur_pose[3]:
                possible_directions.append(3)
        except IndexError:
            pass

    return possible_directions


def direction_indicator(ds):
    """
    check whether there are positions still possible to move
    -1 means the position is never visited
    [] means the position has moved to all possible directions
    :param ds:
    :return:
    """
    for i in ds:
        for j in i:
            if j != -1 and j != []:
                return True
    return False


def update_indicator(cur_index, dest_index, path_store):
    """
    check whether it is suitable to update information in destination
    :param cur_index: current position
    :param dest_index: next position
    :param path_store: a matrix stores all information of past moves
    :return:
    """
    if path_store[dest_index[0]][dest_index[1]] == -1:  # -1 means the position was not visited before
        return True
    elif path_store[dest_index[0]][dest_index[1]][0] > path_store[cur_index[0]][cur_index[1]][0] \
            + board[dest_index[0]][dest_index[1]]:
        # sum from current position to the destination is smaller, i.e. update
        return True
    else:
        return False


def evolve(ini_pose, ini_index):
    """
    given the initial position and pose, roll the tetrahedron
    :param ini_pose: initial pose
    :param ini_index: starting position
    :return: a matrix store all information of past moves
    """
    path_store = [[-1 for i in range(16)] for j in range(8)]
    # in each position, the path is in the format: [sum_value, pose, path]

    direction_store = [[-1 for i in range(16)] for j in range(8)]
    # it stores current unchecked possible directions for each position

    path_store[ini_index[0]][ini_index[1]] = [board[ini_index[0]][ini_index[1]], ini_pose, [ini_index]]
    direction_store[ini_index[0]][ini_index[1]] = find_possible_direction(ini_pose, ini_index)
    # initialize the starting information

    while direction_indicator(direction_store):  # while there are something to check
        for i in range(8):
            for j in range(16):
                if direction_store[i][j] not in [-1, []]:
                    while direction_store[i][j]:  # deal with the position [i,j], check all unchecked directions
                        d = direction_store[i][j].pop()
                        dest_pose, dest = move(path_store[i][j][1], d, [i, j])
                        if update_indicator([i, j], dest, path_store):
                            tmp = copy.deepcopy(path_store[i][j][2])
                            tmp.append(dest)
                            path_store[dest[0]][dest[1]] = [path_store[i][j][0] + board[dest[0]][dest[1]],
                                                            dest_pose, tmp]
                            direction_store[dest[0]][dest[1]] = find_possible_direction(dest_pose, dest)

                            if dest_pose != path_store[dest[0]][dest[1]][1]:
                                # it is possible that at one position,
                                # there are two paths from two different tetrahedron
                                # in this case, we have to compare all conditions together, which is more complicated
                                # fortunately, this does not happen in the given board
                                print('two poses found, need more considerations')
    return path_store


def show(b):
    """
    show the board with only sums
    :param b:
    :return:
    """
    for i in b:
        tmp = []
        for j in i:
            if j == -1:
                tmp.append('-')
            else:
                tmp.append(j[0])
        print(tmp)

results = []
initial_pose = [[0] + list(i) for i in itertools.permutations([1, 17, 71, 711])]
# top 8 triangles point downwards, i.e. mode 0


# the main solution
# simply observe the console, you can have the answer
for i in range(1, 16, 2):
    print('processing position {}'.format(i))
    for p in initial_pose:
        if p[4] == board[0][i] and find_possible_direction(p, [0, i]):
            print('current initial pose is ' + str(p))
            r = evolve(p, [0, i])
            show(r)


