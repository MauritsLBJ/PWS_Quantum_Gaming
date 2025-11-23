# src/buildings.py
# placement rules helpers (vertex adjacency, etc.)

from .board import HEX_COORDS
from .constants import HEX_RADIUS

def compute_vertex_adjacency(hex_vertex_indices):
    """
    hex_vertex_indices is a list where each hex maps to 6 vertex indices.
    Build a mapping vertex -> set(neighbor vertices)
    """
    neighbor_map = {}
    for idxs in hex_vertex_indices:
        for i, v in enumerate(idxs):
            if v not in neighbor_map:
                neighbor_map[v] = set()
            neighbor_map[v].add(idxs[(i-1) % 6])
            neighbor_map[v].add(idxs[(i+1) % 6])
    return neighbor_map

def valid_settlement_position(v_idx, settlements_owner, neighbor_map):
    # no settlement at v_idx and no adjacent settlement
    if v_idx in settlements_owner:
        return False
    for n in neighbor_map.get(v_idx, []):
        if n in settlements_owner:
            return False
    return True
