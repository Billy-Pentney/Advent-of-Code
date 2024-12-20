
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        grid = [list(row.strip("\n")) for row in file.readlines()]

    return np.array(grid)


def show(map):
    for row in map:
        print("".join(row))


def find_trailheads(map) -> list:
    """
        Returns a list containing (x,y) coordinates of each trailhead (denoted '0') in the given grid 'map'.
    """
    trailheads = []
    for y in range(map.shape[0]):
        for x in range(map.shape[1]):
            if map[y][x] == '0':
                trailheads.append((x,y))
    return trailheads


vecs = [[-1,0],[0,1],[1,0],[0,-1]]


def score_trailhead(map, head) -> int:
    """
        Calculates the score and rating for the trailhead at the given coordinates in the given map.
        A valid path is one which starts at the given coordinates and steps on nodes of strictly increasing height, where no two consecutive nodes differ by more than 1 in height.
        The score is the number of cells in the grid with value 9 which are reachable from the given cell via a valid path.
        The rating is the number of unique paths starting at the trailhead and ending at a 9-cell node.
        
        Params
        ----
        `map`: 2D array of size m,n
            A string grid of m rows and n columns, describing the trails. Each element should be a digit from 0 to 9.
        `head`: a 2-tuple
            An (x,y) coordinate in `map`, corresponding to the trailhead. For the problem, these coordinates should correspond to a cell of height 0 but this is not a requirement.

        Returns
        ---
        A tuple `(S,R)`, where `S` is the trailhead score and `R` is the trailhead rating.

    """

    rows = map.shape[0]
    cols = map.shape[1]

    visited = np.zeros(map.shape, dtype='int')
    trail_score = 0
    total_rating = 0

    visited[head[1]][head[0]] = 1
    queue = [head]

    # DFS to find all 9-height cells reachable from this trailhead
    while len(queue) > 0:
        cx,cy = queue[0]
        queue = queue[1:]
        curr_height = int(map[cy][cx])       ## Get the 0-9 height value for this cell

        if curr_height == 9:
            ## The score is the number of reachable 9-cells
            trail_score += 1
            ## The rating is given by the sum of the numbers of paths to the 9-cells 
            total_rating += visited[cy][cx]
        else:
            for v in vecs:
                nx,ny = cx+v[0], cy+v[1]
                if nx < 0 or ny < 0 or nx >= cols or ny >= rows:
                    continue
                if int(map[ny][nx]) != curr_height+1:
                    # Only increase by a single step each time
                    continue
                if visited[ny][nx] == 0:
                    queue.append((nx,ny))

                ## Every path to (cx,cy) makes a new path to (nx,ny)
                visited[ny][nx] += visited[cy][cx]


    return trail_score, total_rating


def evaluate_trailheads(map):
    """
        Solves both parts of the problem, locating all trailheads (nodes with height 0) in the given map, then computing the scores and ratings of each trailhead and returning the sums of these two quantities as a tuple.

        Params
        ----
        `map`: a 2D array of size m,n
            Describes the trails; each cell should be a single digit character from '0' to '9' indicating that cell's height. Trailheads have height 0.
        
        Returns
        ---
        A tuple (S,R) where S is the sum of the trailhead scores and R is the sum of their ratings.
    """

    trailheads = find_trailheads(map)
    scores = []
    ratings = []

    for th in trailheads:
        score, rating = score_trailhead(map, th)
        scores.append(score)
        ratings.append(rating)
    
    return sum(scores), sum(ratings)







from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    map = load(fname)
    show(map)

    score_sum, rating_sum = evaluate_trailheads(map)
    print(f"(Part 1) Trailhead Score Sum: {score_sum}")
    print(f"(Part 2) Trailhead Rating Sum: {rating_sum}")