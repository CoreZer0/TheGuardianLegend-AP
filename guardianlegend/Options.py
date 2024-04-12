from dataclasses import dataclass

from Options import DefaultOnToggle, Choice, NamedRange, DeathLink, PerGameCommonOptions


class BalancedRapidFire(DefaultOnToggle):
    """Makes the upgrade power of Rapid Fire more evenly distributed, and gives a slightly faster starting speed.
    
    True: 10/8/6/4/2/1 frames per shot.
    False: 12/5/4/3/2/1 frames per shot (vanilla behavior)."""
    display_name = "Balanced Rapid Fire"


class ItemDistribution(Choice):
    """Determines how many copies of items and upgrades exist in the item pool. 
    Note that vanilla maximums still apply, the extra copies only make it more likely to max out earlier.
    Filler items (EEs and Energy Packs) are distributed based on intended relative difficulty.

    Vanilla: Uses the vanilla item distribution, where possible. Some items have extra copies, some don't.
    Exact: Only the exact number of items needed to max out stats and subweapons is provided.
    Reduced: Reduced maximum for stats and subweapons. This will make the game much harder!
    Extra: Some extra copies of all items are added to the pool. This will make the game slightly easier."""
    display_name = "Item Distribution"
    option_vanilla = 0
    option_exact = 1
    option_reduced = 2
    option_extra = 3
    default = 3


class ItemGating(Choice):
    """Determines how much offensive and defense power is needed before putting each Area in logic. 
    Higher settings will be easier but more likely to follow the vanilla game Area order.

    Low: 7 Defense, 9 Offense
    Normal: 9 Defense, 12 Offense
    High: 12 Defense, 16 Offense
    
    (Note: in the Offense totals, Attack Up counts as double)"""
    display_name = "Area Gating Strength"
    option_low = 0
    option_normal = 1
    option_high = 2
    default = 1


class CorridorHints(NamedRange):
    """The rooms that normally explain how to open Corridor 1-10 will instead have hints for
    the classification of items in Corridor 11-20. Choose how many Corridors receive hints.
    (If less than 10 is chosen, hinted corridors will be randomly selected.)"""
    display_name = "Corridor 11-20 Hints"
    range_start = 0
    range_end = 10
    special_range_names = {
        "none": 0,
        "all": 10
    }
    default: 10


'''
class LimitedSubweapons(Toggle):
    """An extra challenge! A random set of subweapons will be excluded from the pool entirely."""
    pass
'''


@dataclass
class TGLOptions(PerGameCommonOptions):
    balanced_rapid_fire: BalancedRapidFire
    item_distribution: ItemDistribution
    item_gating: ItemGating
    corridor_hints: CorridorHints
    # death_link: DeathLink
    