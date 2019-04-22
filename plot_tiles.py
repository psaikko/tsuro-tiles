import numpy as np
import matplotlib.pyplot as plt
import bezier

def make_tiles(l):
    if len(l) == 0: return [[]]

    head, rest = l[0], l[1:]    

    result_tiles = []

    for other in rest:
        edge = (head, other)
        rest_edges = make_tiles([i for i in rest if i != other])
        result_tiles += [[edge] + edges for edges in rest_edges]

    return result_tiles
    
# tiles represented as sets of 4 disjoint edges on nodes [0..7]
T = make_tiles(range(8))

# turn tile 90 degrees
def turn(tile):
    R = [2,3,4,5,6,7,0,1]
    return [(R[edge[0]], R[edge[1]]) for edge in tile]

# order each edge from smaller to larger index
def orient_edges(tile):
    return [(min(edge), max(edge)) for edge in tile]

# unique string identifiers
def tile_key(tile):
    return " ".join("%d,%d" % edge for edge in tile)

# get rotation-invariant tile identifier
def unique_id(tile):
    tmp = tile[:]
    # return lexicographically smallest (wrt tile_key)
    # of 4 possible rotations of the tile
    rotations = [tile_key(tmp)]
    for _ in range(3):
        # turn tile and convert to "canonical form"
        # with edges from smaller index to larger, sorted by smaller index
        tmp = sorted(orient_edges(turn(tmp)))
        rotations.append(tile_key(tmp))
    return sorted(rotations)[0]

# filter by unique id with dict
D = dict()
for tile in T:
    D[unique_id(tile)] = tile
T = list(D.values())

# index -> coordinate mapping for plotting
coordinates = [(0,1),(0,2),(1,3),(2,3),(3,2),(3,1),(2,0),(1,0)]

plt.figaspect(1)
plt.subplots(6,6)

for i in range(6*6):
    ax = plt.subplot(6,6,i+1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect(1)

    if i >= len(T): break

    ax.set_facecolor("xkcd:sea")
    
    tile = T[i]
    for edge in tile:        
        x1, y1 = coordinates[edge[0]]
        x2, y2 = coordinates[edge[1]]
        mx, my = (x1+x2+1.5)/3, (y1+y2+1.5)/3
        pts = np.array([
            [float(x1),mx,float(x2)],
            [float(y1),my,float(y2)]
        ])
        curve = bezier.Curve(pts, degree=3)

        curve.plot(num_pts=64, ax=ax, color="xkcd:seafoam")

plt.show()