from typing import Dict, List

from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import add_rule, set_rule

from .Items import red_lander_thresholds

# Currently this compares to a hardcoded list of Max chip values as in the vanilla game,
#  based on the current amount of Red Landers collected.
def get_chip_max(state: CollectionState, player: int) -> int:
    return red_lander_thresholds[state.count("Red Lander", player)]

def has_area_key(state: CollectionState, player: int, keyname: str) -> bool:
    return state.has(keyname, player)

def has_enough_defense(state: CollectionState, player: int, threshold: int) -> bool:
    return min(state.count("Defense Up", player), 6) + state.count("Blue Lander", player) >= threshold

def has_enough_offense(state: CollectionState, player: int, threshold: int) -> bool:
    # Attack Up counts for double value to increase likelihood it shows up in logic
    return (min((state.count("Attack Up", player) * 2), 6)
            + min(state.count("Rapid Fire Up", player), 5) 
            + state.count("Red Lander", player)) >= threshold


''' # # Testing offense/defense split, leaving for reference
def player_stat_total(state: CollectionState, player: int) -> int:
    return state.count("Defense Up", player) + state.count("Attack Up", player) + state.count("Rapid Fire Up", player)

def player_lander_total(state: CollectionState, player: int) -> int:
    return state.count("Blue Lander", player) + state.count("Red Lander", player)
'''


# All shops are named as 'A# <chip_cost> Chip Shop' so we can pull the second word out as an int
#  to see how much we need. 
def has_enough_chips(state: CollectionState, player: int, shopname: str) -> bool:
    shop_cost = int(shopname.split(' ')[1])
    return get_chip_max(state, player) >= shop_cost


''' # Not needed due to corridors always open, leaving for reference
def has_multibullets(state: CollectionState, player: int) -> bool:
    return state.count("Multibullets", player) >= 1
'''
    
def has_final_boss_access(state: CollectionState, player: int) -> bool:
    all_cleared = True
    for i in range(1,11):
        all_cleared &= state.has("Corridor " + str(i) + " Cleared", player)
    return all_cleared

''' # Testing offense/defense split, leaving for reference
stats_gating_table: Dict[int, List[int]] = {
    0: [1,2,3,3,4,4,5,6,6 ],
    1: [1,2,3,4,5,6,7,8,8 ],
    2: [1,2,3,4,6,7,8,9,10]
}

landers_gating_table: Dict[int, List[int]] = {
    0: [1,2,3,3,4,4,5, 6, 7 ],
    1: [1,2,3,4,6,7,8, 9, 10],
    2: [1,3,5,6,8,9,11,13,14]
}
'''

defense_gating_table: Dict[int, List[int]] = {
    0: [1,2,3,3,4,4,5,6 ,7 ],
    1: [1,2,3,4,5,6,7,8 ,9 ],
    2: [1,2,3,4,6,7,9,11,12]
}

offense_gating_table: Dict[int, List[int]] = {
    0: [1,2,3,4,5,6 ,7 ,8 ,9 ],
    1: [1,2,3,4,6,7 ,9 ,11,12],
    2: [1,3,5,7,9,11,13,15,16]
}


def set_rules(multiworld: MultiWorld, player: int, gating: int):

    # Area 1-10 require a specific key, enforced by the game
    # Additional gating set by options for Area 2 and up

    multiworld.get_entrance("Area 1", player).access_rule = \
        lambda state: has_area_key(state, player, "Crescent Key")

    for i in range(9):

        # Set the stats required for areas based on options
        # For vanilla maximums, OffenseMax = 21, DefenseMax = 16 (Attack up counts double)

        areaname = "Area " + str(i+2)

        ''' # Testing offense/defense split, leaving for reference
        set_rule(multiworld.get_entrance(areaname, player),
                 lambda state, n=i: (player_stat_total(state, player) >= stats_gating_table[gating][n])
                       and (player_lander_total(state, player) >= landers_gating_table[gating][n]))
        '''
        
        set_rule(multiworld.get_entrance(areaname, player),
                 lambda state, n=i: (has_enough_defense(state, player, defense_gating_table[gating][n]))
                       and (has_enough_offense(state, player, offense_gating_table[gating][n])))
    
    add_rule(multiworld.get_entrance("Area 2", player),
            lambda state: has_area_key(state, player, "Crescent Key"))
    
    add_rule(multiworld.get_entrance("Area 3", player),
            lambda state: has_area_key(state, player, "Hook Key"))
    
    add_rule(multiworld.get_entrance("Area 4", player),
            lambda state: has_area_key(state, player, "Wave Key"))
    
    add_rule(multiworld.get_entrance("Area 5", player),
            lambda state: has_area_key(state, player, "Square Key"))
    
    add_rule(multiworld.get_entrance("Area 6", player),
            lambda state: has_area_key(state, player, "Square Key"))
    
    add_rule(multiworld.get_entrance("Area 7", player),
            lambda state: has_area_key(state, player, "Cross Key"))
    
    add_rule(multiworld.get_entrance("Area 8", player),
            lambda state: has_area_key(state, player, "Cross Key"))
    
    add_rule(multiworld.get_entrance("Area 9", player),
            lambda state: has_area_key(state, player, "Triangle Key"))
    
    add_rule(multiworld.get_entrance("Area 10", player),
            lambda state: has_area_key(state, player, "Rectangle Key"))

    '''
    multiworld.get_entrance("Area 3", player).access_rule = \
        lambda state: has_area_key(state, player, "Hook Key") and has_enough_defense(state, player, 2)

    multiworld.get_entrance("Area 4", player).access_rule = \
        lambda state: has_area_key(state, player, "Wave Key") and has_enough_defense(state, player, 3)
    
    multiworld.get_entrance("Area 5", player).access_rule = \
        lambda state: has_area_key(state, player, "Square Key") and has_enough_defense(state, player, 3)
    
    multiworld.get_entrance("Area 6", player).access_rule = \
        lambda state: has_area_key(state, player, "Square Key") and has_enough_defense(state, player, 4)
    
    multiworld.get_entrance("Area 7", player).access_rule = \
        lambda state: has_area_key(state, player, "Cross Key") and has_enough_defense(state, player, 4)
    
    multiworld.get_entrance("Area 8", player).access_rule = \
        lambda state: has_area_key(state, player, "Cross Key") and has_enough_defense(state, player, 5)
    
    multiworld.get_entrance("Area 9", player).access_rule = \
        lambda state: has_area_key(state, player, "Triangle Key") and has_enough_defense(state, player, 6)
    
    multiworld.get_entrance("Area 10", player).access_rule = \
        lambda state: has_area_key(state, player, "Rectangle Key") and has_enough_defense(state, player, 6)
    '''
    
    # Shops require Area access + enough Red Landers to afford the shop
    for s_loc in [location for location in multiworld.get_locations(player) if "Shop" in location.name]:
        add_rule(multiworld.get_location(s_loc.name, player), 
                 lambda state, s=s_loc: has_enough_chips(state, player, s.name))

    # Corridor 6 has a chip spending requirement
    # To get around checking ALL subweapons, we just check for one Multibullet.
    # NOTE: Client changed to open all Corridors, rule is not needed
    #add_rule(multiworld.get_location("A6 Corridor 6 (X16 Y11)", player), lambda state: has_multibullets(state, player))

    # Corridor 21 requires Corridor 1-10 Cleared
    multiworld.get_entrance("Corridor 21", player).access_rule = \
        lambda state: has_final_boss_access(state, player)

    # Victory
    multiworld.completion_condition[player] = lambda state: state.has("Corridor 21 Cleared", player)
