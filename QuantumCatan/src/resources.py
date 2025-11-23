# src/resources.py
# trading, ports and helper functions

def best_trade_ratio_for(player_idx, give_resource, sea_tiles, port_vertex_map, settlements_owner):
    # check specific port
    need_port = "port_" + give_resource
    for si, st in enumerate(sea_tiles):
        if st.get("port") == need_port:
            verts = port_vertex_map.get(si, [])
            for v in verts:
                owner = settlements_owner.get(v)
                if owner and owner[0] == player_idx:
                    return 2
    # check any port
    for si, st in enumerate(sea_tiles):
        if st.get("port") == "port_any":
            verts = port_vertex_map.get(si, [])
            for v in verts:
                owner = settlements_owner.get(v)
                if owner and owner[0] == player_idx:
                    return 3
    return 4

def perform_trade(players_resources, player_idx, give_resource, receive_resource, ratio):
    if players_resources[player_idx].get(give_resource,0) < ratio:
        return False
    players_resources[player_idx][give_resource] -= ratio
    players_resources[player_idx][receive_resource] += 1
    return True
