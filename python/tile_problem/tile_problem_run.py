from tile_problem import Tile_problem
from searchGeneric import AStarSearcher

def main():
    prob = Tile_problem(4, [1,1,0,1, 1,0,0,0, 1,0,1,0, 1,1,0,0])
    #prob = Tile_problem(3, [1,1,0, 1,0,0, 1,0,1])
    s = AStarSearcher(prob)
    path = s.search()
    if path:
        print(f"Path found (cost = {path.cost})\n{path}")
        return path
if __name__ == '__main__':
    main()
