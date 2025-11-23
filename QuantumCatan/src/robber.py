# src/robber.py
# robber logic: placement + decoherence

import random

def initial_robber_tile(tiles):
    # choose a non-desert tile at random
    idxs = [i for i,t in enumerate(tiles) if t.get("resource") != "desert"]
    return random.choice(idxs) if idxs else 0

def move_robber_to(tile_idx, tiles, settlements_owner):
    """
    Move robber to a tile: if tile is classical -> make it quantum (decohere)
    If tile is entangled -> break entanglement into superpositions
    If tile is already quantum -> optionally break entanglement or leave.
    Returns list of affected tile indices so UI can animate.
    """
    affected = []
    t = tiles[tile_idx]
    if not t.get("quantum", False):
        # make it a simple superposition with two possibilities
        t["quantum"] = True
        t["superposed"] = [t["resource"], random.choice(["wood","brick","sheep","wheat","ore"])]
        t["resource"] = None
        t["ent_group"] = None
        affected.append(tile_idx)
    else:
        # if entangled, separate group into independent superpositions
        if t.get("ent_group"):
            group = t["ent_group"]
            # break all tiles with same group
            for i, tt in enumerate(tiles):
                if tt.get("ent_group") == group:
                    tt["ent_group"] = None
                    tt["quantum"] = True
                    tt["superposed"] = tt.get("superposed", random.sample(["wood","brick","sheep","wheat","ore"], 2))
                    tt["resource"] = None
                    affected.append(i)
        else:
            # already superposed - maybe shuffle possibilities
            t["superposed"] = random.sample(["wood","brick","sheep","wheat","ore"], 2)
            affected.append(tile_idx)
    # steal one resource from one owner adjacent? (omitted for simplicity)
    return affected
