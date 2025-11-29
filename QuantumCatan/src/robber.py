# src/robber.py
# robber logic: placement + decoherence

import random

def initial_robber_tile(tiles):
    # choose a non-desert tile at random
    idxs = [i for i,t in enumerate(tiles) if t.get("resource") != "desert"]
    return random.choice(idxs) if idxs else 0
