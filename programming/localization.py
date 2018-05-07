import numpy as np


def localize(colors, measurements, motions, sensor_right, p_move):
    """
    The function localize takes the following arguments.
    It compute the probabilities by assuming the robot initially has a uniform probability of being in any cell.
    Also assume that at each step, the robot:
    1) first makes a movement,
    2) then takes a measurement.
    :param colors: 2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
    :param measurements: list of measurements taken by the robot, each entry either 'R' or 'G'
    :param motions: list of actions taken by the robot, each entry of the form [dy,dx],
                    where dx refers to the change in the x-direction (positive meaning
                    movement to the right) and dy refers to the change in the y-direction
                    (positive meaning movement downward)
                    NOTE: the *first* coordinate is change in y; the *second* coordinate is change in x
    :param sensor_right: float between 0 and 1, giving the probability that any given
                         measurement is correct; the probability that the measurement is incorrect is 1-sensor_right
    :param p_move: float between 0 and 1, giving the probability that any given movement
                   command takes place; the probability that the movement command fails
                   (and the robot remains still) is 1-p_move; the robot will NOT overshoot
                   its destination in this exercise
    :return: a 2D list (of the same dimensions as colors) that gives the probabilities that the robot occupies
             each cell in the world.
    """
    world = np.matrix(colors)

    # Initializes p to a uniform distribution over a grid of the same dimensions as colors
    p = np.ndarray(shape=world.shape).astype(np.float)
    p[:] = 1.0 / (world.shape[0] * world.shape[1])

    # Multiplication factor when measurement matches or not. They don't have to add up to 1.
    p_match = 1
    p_mismatch = 0

    for measure, motion in zip(measurements, motions):
        print("measure: ", measure)
        print("motion: ",  motion)

        # Move
        q = np.copy(p)
        for y in range(p.shape[0]):
            for x in range(p.shape[1]):
                prev_y = (y - motion[0]) % p.shape[0]
                prev_x = (x - motion[1]) % p.shape[1]
                p[y, x] = q[prev_y, prev_x] * p_move + q[y, x] * (1 - p_move)
        del q

        # Sense
        p[world == measure] *= p_match * sensor_right + p_mismatch * (1 - sensor_right)
        p[world != measure] *= p_mismatch * sensor_right + p_match * (1 - sensor_right)
        p /= np.sum(p)

        show(p.tolist())
    return p.tolist()


def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')


#############################################################
# For the following test case, your output should be
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R', 'G', 'G', 'R', 'R'],
          ['R', 'R', 'G', 'R', 'R'],
          ['R', 'R', 'G', 'G', 'R'],
          ['R', 'R', 'R', 'R', 'R']]
measurements = ['G', 'G', 'G', 'G', 'G']
motions = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]
p = localize(colors, measurements, motions, sensor_right=0.7, p_move=0.8)
show(p)  # displays your answer