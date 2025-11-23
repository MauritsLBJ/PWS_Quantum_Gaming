# src/quantum.py
# Handles quantum tokens, measurement, collapse, entanglement

import random
from collections import defaultdict

def create_quantum_token_from_tile(tile):
    """
    If tile is classical -> returns a classical token dict
    If tile is superposed/entangled -> returns a token describing possibilities
    token structure:
      {"type":"classical","resource":"wood","tile_idx":i}
      {"type":"superposition","possible":["wood","brick"], "tile_idx":i}
      {"type":"entangled","group":g, "possible":[...], "tile_idx":i}
    """
    if not tile.get("quantum", False):
        return {"type":"classical","resource":tile.get("resource"), "tile_coord": tile["coord"]}
    if tile.get("ent_group"):
        return {"type":"entangled","group":tile["ent_group"], "possible": tile.get("superposed"), "tile_coord": tile["coord"]}
    return {"type":"superposition","possible": tile.get("superposed"), "tile_coord": tile["coord"]}

def measure_token(token, tiles_by_group=None, tiles_list=None):
    """
    Collapse quantum or entangled resources.
    Supports:
      - classical tiles
      - superposed tiles (two options)
      - entangled groups (positive & negative entanglement)
    """

    # ----- Classical ---------------------------------------------------------
    if token["type"] == "classical":
        return token["resource"]

    # ----- Superposition -----------------------------------------------------
    if token["type"] == "superposition":
        # choose randomly between the two possibilities
        res = random.choice(token["possible"])
        # collapse tile
        if tiles_list is not None:
            for t in tiles_list:
                if t["coord"] == token["tile_coord"]:
                    t["resource"] = res
                    t["quantum"] = False
                    t.pop("superposed", None)
                    t["ent_group"] = None
                    break
        return res

    # ----- Entanglement ------------------------------------------------------
    if token["type"] == "entangled":
        g = token["group"]
        if tiles_by_group is None or tiles_list is None:
            return random.choice(token["possible"])

        group_indices = tiles_by_group.get(g, [])
        if group_indices[0]["coord"] == token["tile_coord"]:
            indexOfToken = 0
        else:
            indexOfToken = 1
        # determine possible outcomes
        outcomes = token["possible"]
        random.shuffle(outcomes)
        for i, idx in group_indices:
            t = tiles_list[idx]
            t["resource"] = outcomes[i if t["correlation"] == -1 else 0]
            t["quantum"] = False
            t.pop("superposed", None)
            t["ent_group"] = None

        return outcomes[indexOfToken]


def collect_from_tile_for_player(tile, player_tokens, tile_idx, tiles_by_group=None, tiles_list=None):
    """
    Called when a dice roll activates a tile and the settlement/city belongs to a player.
    Instead of giving a classical resource, give a quantum token if tile is quantum.
    player_tokens is a list where tokens are appended.
    """
    token = create_quantum_token_from_tile(tile)
    token["tile_idx"] = tile_idx
    player_tokens.append(token)
    print(f"Player received token: {token}")
    return token
