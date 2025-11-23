# src/board.py
# Handles tile coordinate generation, tile randomization, sea ring & ports

import random
import math
from collections import defaultdict
from .util import hex_to_pixel, polygon_corners
from .constants import HEX_RADIUS, SEA_RING, HEX_SIZE, SQRT3

def generate_hex_coords(radius=HEX_RADIUS):
    coords = []
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            #print(f"q, r = {(q, r)}")
            s = -q - r
            #print(f"s = {s}")
            if abs(s) <= radius:
                coords.append((q, r))
    coords.sort()
    #print(coords)
    return coords

def generate_sea_coords(radius=SEA_RING):
    coords = []
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            s = -q - r
            if max(abs(q), abs(r), abs(s)) == radius:
                coords.append((q, r))
    # sort by angle around origin to preserve ring order
    def angle_key(coord):
        x, y = hex_to_pixel(coord[0], coord[1], size=HEX_SIZE, origin=(0,0))
        return math.atan2(y, x)
    coords.sort(key=angle_key)
    return coords

HEX_COORDS = generate_hex_coords()
SEA_COORDS = generate_sea_coords()

STANDARD_NUMBERS = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]

RESOURCE_POOL = ["wood"]*4 + ["brick"]*3 + ["sheep"]*4 + ["wheat"]*4 + ["ore"]*3

def randomize_tiles():
    coords = list(HEX_COORDS)
    resources = RESOURCE_POOL.copy()
    random.shuffle(resources)
    numbers = STANDARD_NUMBERS.copy()
    random.shuffle(numbers)
    desert_pos = random.randrange(len(coords))
    tiles = []
    for i, coord in enumerate(coords):
        if i == desert_pos:
            tiles.append({"coord": coord, "resource": "desert", "number": None, "quantum": False, "ent_group": None})
        else:
            res = resources.pop()
            num = numbers.pop()
            # randomly decide some tiles are quantum or entangled
            q_state = random.random()
            if q_state < 0.18:
                # entangled pair will be assigned later; mark as entangled placeholder
                tiles.append({"coord": coord, "resource": None, "number": num, "quantum": True, "ent_group": "pending"})
            elif q_state < 0.36:
                # simple superposition: choose two possible resources
                a = res
                # pick alternative different resource
                alt = random.choice([r for r in ["wood","brick","sheep","wheat","ore"] if r != a])
                tiles.append({"coord": coord, "resource": None, "number": num, "quantum": True, "superposed": [a, alt], "ent_group": None})
            else:
                tiles.append({"coord": coord, "resource": res, "number": num, "quantum": False, "ent_group": None})
    # assign entangled groups: pair up pending tiles
    pending = [i for i,t in enumerate(tiles) if t.get("ent_group") == "pending"]
    random.shuffle(pending)
    group_id = 1

    while len(pending) >= 2:
        a = pending.pop()
        b = pending.pop()

        # two distinct possible outcomes
        possibilities = random.sample(["wood","brick","sheep","wheat","ore"], 2)

        tiles[a]["ent_group"] = group_id
        tiles[b]["ent_group"] = group_id
        tiles[a]["quantum"] = True
        tiles[b]["quantum"] = True

        # both tiles share the same two possibilities
        tiles[a]["superposed"] = possibilities[:]
        tiles[b]["superposed"] = possibilities[:]

        # encode correlation sign:
        # +1 = positive entanglement (same result)
        # -1 = negative entanglement (opposite result)
        tiles[a]["correlation"] = 1 if group_id % 2 == 0 else -1
        tiles[b]["correlation"] = 1 if group_id % 2 == 0 else -1

        group_id += 1

    # leftover tile → simple superposition
    for idx in pending:
        tiles[idx]["ent_group"] = None
        tiles[idx]["quantum"] = True
        tiles[idx]["superposed"] = random.sample(["wood","brick","sheep","wheat","ore"], 2)
        tiles[idx]["correlation"] = None
    
    for t in tiles:
        print(tiles[tiles.index(t)])

    return tiles


def generate_sea_ring():
    coords = list(SEA_COORDS)
    n = len(coords)
    pattern = ["port" if i % 2 == 0 else "sea" for i in range(n)]
    rotation = random.randint(0, n - 1)
    pattern = pattern[rotation:] + pattern[:rotation]
    ports = ["port_brick","port_wood","port_sheep","port_wheat","port_ore"] + ["port_any"]*4
    random.shuffle(ports)
    sea_tiles = []
    port_i = 0
    for idx,coord in enumerate(coords):
        if pattern[idx] == "port" and port_i < len(ports):
            sea_tiles.append({"coord": coord, "port": ports[port_i]})
            port_i += 1
        else:
            sea_tiles.append({"coord": coord, "port": "sea"})
    return sea_tiles

def compute_centers_and_polys(origin, hex_size=HEX_SIZE):
    centers = []
    polys = []
    for q,r in HEX_COORDS:
        c = hex_to_pixel(q,r,size=hex_size,origin=origin)
        centers.append(c)
        polys.append(polygon_corners(c,size=hex_size))
    return centers, polys

def compute_sea_polys(origin, hex_size=HEX_SIZE):
    centers = []
    polys = []
    for q,r in SEA_COORDS:
        c = hex_to_pixel(q,r,size=hex_size,origin=origin)
        centers.append(c)
        polys.append(polygon_corners(c,size=hex_size))
    return centers, polys
