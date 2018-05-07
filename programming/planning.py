# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0] # given in the form [row,col,direction]
                 # direction = 0: up
                 #             1: left
                 #             2: down
                 #             3: right
                
goal = [2, 0] # given in the form [row,col]

cost = [2, 1, 20] # cost has 3 values, corresponding to making 
                  # a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------

# ----------------------------------------
# modify code below
# ----------------------------------------
def optimum_policy2D(grid, init, goal, cost):
    # Grid coordinate is associated with its heading:
    # head * grid_rows * grid_cols
    lookup = [[[None for col in range(len(grid[0]))]
               for row in range(len(grid))]
              for _ in range(len(forward))]
    # (y, x, heading, action_name, cost)
    
    queue = [] # (g-val, y, x, heading)
    queue.append((0, init[0], init[1], init[2]))

    while queue:
        queue.sort()
        current = queue.pop(0)
        #print '---'
        #print current
        #print queue
        g_val, cu_y, cu_x, cu_head = current

        if [cu_y, cu_x] == goal:
            # backtrace the path
            path = [[' ' for col in range(len(grid[0]))]
                     for row in range(len(grid))]
            path[cu_y][cu_x] = '*'
            previous = lookup[cu_head][cu_y][cu_x]
            while previous:
                path[previous[0]][previous[1]] = previous[3]
                previous = lookup[previous[2]][previous[0]][previous[1]]
            return path
            
        for a, c, n in zip(action, cost, action_name):
            next_head = (cu_head + a + len(forward)) % len(forward) # cyclic
            delta = forward[next_head]
            next_y = cu_y + delta[0]
            next_x = cu_x + delta[1]
            if cu_y ==0 and cu_x==5 or cu_y==2 and cu_x==3:
                print n, next_y, next_x, forward_name[next_head]

            if not (next_y >= 0 and next_y < len(grid) and
                    next_x >= 0 and next_x < len(grid[0])):
                # out of bound
                continue
            if grid[next_y][next_x] == 1:
                # grid is blocked
                continue
            next_cost = g_val + c
            if lookup[next_head][next_y][next_x] is not None and \
                lookup[next_head][next_y][next_x][4] < next_cost:
                # there existed a lower-cost path already
                continue

            # print "occupy", next_y, next_x, forward_name[next_head], next_cost
            queue.append((next_cost, next_y, next_x, next_head))
            lookup[next_head][next_y][next_x] = (cu_y, cu_x, cu_head, n, next_cost)
    else:
        return "fail"
        
output = optimum_policy2D(grid, init, goal, cost)
for row in output:
    print(row)
