# @Date:   2017-02-15 00:20:56
# @Last modified time: 2017-02-15 01:27:15

import math
import random
from PIL import Image

def writeMap(arch_map):
    with open("map.txt", "w") as file:
        for row in arch_map:
            for j in range(0, len(row)):
                file.write("%d" % row[j])
                if j < len(row) - 1:
                    file.write(" ")
            file.write("\n")

def createImg(arch_map):
    img = Image.new('RGB', (len(arch_map), len(arch_map)), "black") # create a new black image
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]):    # for every pixel:
        for j in range(img.size[1]):
            color = (0, 17, 242)
            if arch_map[i][j] == 1:
                color = (8, 59, 8)
            pixels[i,j] = color #(i, j, 100) # set the colour accordingly

    img.save("output.png")

# Random true or false swtich
def pickRandBool(probability):
	return random.random() < probability

# Pick a random open spot in the square to fill
def pickRandSpot(size):
    fill_spot = random.randint(1, size * size)

    # Convert the random fill spot to row column notation for accessing 2D array
    row = int(fill_spot / size) - 1
    col = fill_spot % size

    return (row, col)

def getProbLand(origin, x, y):
    distance = math.sqrt(math.pow(origin[0] - x, 2) + math.pow(origin[1] - y, 2))
    return (1.0 / math.pow(distance, 0.2))

def recursive_grow(arch_map, origin, x, y):
    if x < 0 or x >= len(arch_map) or y < 0 or y >= len(arch_map[x]):
        return
    elif not arch_map[x][y] == 1 and not (origin[0] == x and origin[1] == y):
        # print("Grew to [%d][%d]" % (x, y))
        arch_map[x][y] = 1

    # Down grow
    if x + 1 < len(arch_map) and arch_map[x + 1][y] == 0:
        prob_land = getProbLand(origin, x + 1, y)
        if pickRandBool(prob_land):
            recursive_grow(arch_map, origin, x + 1, y)

    # Up grow
    if x - 1 > 0 and arch_map[x - 1][y] == 0:
        prob_land = getProbLand(origin, x - 1, y)
        if pickRandBool(prob_land):
            recursive_grow(arch_map, origin, x - 1, y)

    # Right grow
    if y + 1 < len(arch_map[x]) and arch_map[x][y + 1] == 0:
        prob_land = getProbLand(origin, x, y + 1)
        if pickRandBool(prob_land):
            recursive_grow(arch_map, origin, x, y + 1)

    # Left grow
    if y - 1 > 0 and arch_map[x][y - 1] == 0:
        prob_land = getProbLand(origin, x, y - 1)
        if pickRandBool(prob_land):
            recursive_grow(arch_map, origin, x, y - 1)

def main():
    num_init_pts = int(input("Number of starting points to grow: "))
    size = int(input("Map size: "))

    arch_map = [[0 for j in range(0, size)] for i in range(0, size)]

    init_coords = []
    for i in range(0, num_init_pts):
        coords = pickRandSpot(size)
        while coords in init_coords:
            coords = pickRandSpot(size)

        init_coords.append(coords)

    for point in init_coords:
        arch_map[point[0]][point[1]] = 1

    print(init_coords)
    for origin in init_coords:
        recursive_grow(arch_map, origin, origin[0], origin[1])

    # writeMap(arch_map)
    createImg(arch_map)

if __name__ == "__main__":
    main()
