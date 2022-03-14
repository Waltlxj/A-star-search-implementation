'''
A* implementation
Author: Walt Li
References: https://en.wikipedia.org/wiki/A*_search_algorithm
'''

import sample_input as sample


class Astar():

    # initialize class with the grid and starting and finishing point
    def __init__(self, maze, s, t):
        self.maze = maze
        self.s = s
        self.t = t
        self.traceback = {}
    
    # using diagonal heuristic
    def h(self, n):
        dx = abs(n[0] - self.t[0])
        dy = abs(n[1] - self.t[1])
        dmin = min(dx, dy)
        dmax = max(dx, dy)
        return dmin * 1.4142 + dmax - dmin
    
    # the distance between two nodes
    def d(self, direction):
        if direction[0] * direction[1] == 0:
            return 1
        else:
            return 1.4142
        
    # running A* and populating the traceback table
    def find_path(self):
        g = {} # dictionary for g scores
        f = {} # dictionary for f scores
        g[self.s] = 0
        f[self.s] = self.h(self.s)
        frontier = [self.s]
        self.traceback[self.s] = self.s

        while len(frontier) != 0:

            # put the node with smallest h(n) to the end, this is a slower substitute for heap
            for i in range(len(frontier)):
                if f[frontier[i]] < f[frontier[-1]]: 
                    frontier[i], frontier[-1] = frontier[-1], frontier[i]

            # pop the node at the end
            current = frontier.pop()
            # print(current)

            # if t is being visited
            if current == self.t:
                print('Path Found!!!')
                return self.construct_path()
            
            # for all neighbors
            for direction in [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (1, -1), (-1, 1), (-1, -1)]:
                neigh = (current[0]+direction[0], current[1]+direction[1])

                # check if out of bound or wall
                if neigh[0] < 0 or neigh[1] < 0 or \
                    neigh[0] >= len(self.maze) or neigh[1] >= len(self.maze[0]) or \
                         self.maze[neigh[0]][neigh[1]] == 1:
                    continue
                
                # a new potential g-score for the neighbor
                g_score = g[current] + self.d(direction)
                
                # if the new g-score is better than recorded
                if neigh not in g or g_score < g[neigh]:
                    self.traceback[neigh] = current
                    g[neigh] = g_score
                    f[neigh] = g_score + self.h(neigh)
                    if neigh not in frontier:
                        frontier.append(neigh)
        
        print('No path from start to end!!!')
        return None

    # use the traceback table to construct the path
    def construct_path(self):
        path = []
        current = self.t
        # tracing back until we get back to starting point
        while current != self.s:
            path.append(current)
            current = self.traceback[current]
        path.append(self.s)
        path.reverse()
        return path



def main():

    # print given maze
    print('Given maze:')
    sample.maze[sample.start[0]][sample.start[1]] = '*'
    sample.maze[sample.end[0]][sample.end[1]] = '*'
    for maze_row in sample.maze:
        print(' '.join([str(cell) for cell in maze_row]))
    print()

    # print algorithm output
    algorithm = Astar(sample.maze, sample.start, sample.end)
    path = algorithm.find_path()
    print('PATH:', path, '\n')

    # print solution of maze
    print('Solution:')
    for cell in path:
        sample.maze[cell[0]][cell[1]] = '*'
    for maze_row in sample.maze:
        print(' '.join([str(cell) for cell in maze_row]))

main()