from typing import Dict, List, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class TGLItem(Item):
    game = "TGL"


class TGLItemData(NamedTuple):
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1


def get_items_by_category(category: str) -> Dict[str, TGLItemData]:
    item_dict: Dict[str, TGLItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict


def get_itemname_by_id(itemid: int) -> str:
    for name, data in item_table.items():
        if data.code == itemid:
            return name
    

# ID code base 8471760000 = 'TGL' in ASCII decimal + 0000
TGL_ITEMID_BASE = 8471760000

# These values are the hard-coded chip count upgrade levels
# NOTE: If we decide to randomize/alter those thresholds this will have to be changed
red_lander_thresholds = [50,100,150,200,400,800,1200,1600,2400,4000,6000]

balanced_rapid_fire = [10,8,6,4,2,1]

item_table: Dict[str, TGLItemData] = {
    "Crescent Key":   TGLItemData("Keys", TGL_ITEMID_BASE+2000, ItemClassification.progression),
    "Hook Key":       TGLItemData("Keys", TGL_ITEMID_BASE+2001, ItemClassification.progression),
    "Wave Key":       TGLItemData("Keys", TGL_ITEMID_BASE+2002, ItemClassification.progression),
    "Square Key":     TGLItemData("Keys", TGL_ITEMID_BASE+2003, ItemClassification.progression),
    "Cross Key":      TGLItemData("Keys", TGL_ITEMID_BASE+2004, ItemClassification.progression),
    "Triangle Key":   TGLItemData("Keys", TGL_ITEMID_BASE+2005, ItemClassification.progression),
    "Rectangle Key":  TGLItemData("Keys", TGL_ITEMID_BASE+2006, ItemClassification.progression),

    # Subweapons - In-game itemID order, with offsets
    "Multibullets":   TGLItemData("Subweapons",  TGL_ITEMID_BASE+1000, ItemClassification.useful,  5),
    "Back Fire":      TGLItemData("Subweapons",  TGL_ITEMID_BASE+1001, ItemClassification.useful,  3),
    "Wave Attack":    TGLItemData("Subweapons",  TGL_ITEMID_BASE+1002, ItemClassification.useful,  4),
    "Bullet Shield":  TGLItemData("Subweapons",  TGL_ITEMID_BASE+1003, ItemClassification.useful,  4),
    "Grenade":        TGLItemData("Subweapons",  TGL_ITEMID_BASE+1004, ItemClassification.useful,  4),
    "Fireball":       TGLItemData("Subweapons",  TGL_ITEMID_BASE+1005, ItemClassification.useful,  4),
    "Area Blaster":   TGLItemData("Subweapons",  TGL_ITEMID_BASE+1006, ItemClassification.useful,  4),
    "Repeller":       TGLItemData("Subweapons",  TGL_ITEMID_BASE+1007, ItemClassification.useful,  3),
    "Hyper Laser":    TGLItemData("Subweapons",  TGL_ITEMID_BASE+1008, ItemClassification.useful,  3),
    "Saber Laser":    TGLItemData("Subweapons",  TGL_ITEMID_BASE+1009, ItemClassification.useful,  3),
    "Cutter Laser":   TGLItemData("Subweapons",  TGL_ITEMID_BASE+1010, ItemClassification.useful,  3),

    # Filler / Non-unique
    "Enemy Eraser":  TGLItemData("Filler",  TGL_ITEMID_BASE+1011, ItemClassification.filler,  9),
    "Energy Pack":   TGLItemData("Filler",  TGL_ITEMID_BASE+1012, ItemClassification.filler,  14),

    # Stats
    "Blue Lander":     TGLItemData("Stats",  TGL_ITEMID_BASE+1013, ItemClassification.progression, 9),
    "Attack Up":       TGLItemData("Stats",  TGL_ITEMID_BASE+1014, ItemClassification.progression, 3),
    "Defense Up":      TGLItemData("Stats",  TGL_ITEMID_BASE+1015, ItemClassification.progression, 9),
    "Rapid Fire Up":   TGLItemData("Stats",  TGL_ITEMID_BASE+1016, ItemClassification.progression, 6),
    "Red Lander":      TGLItemData("Stats",  TGL_ITEMID_BASE+1017, ItemClassification.progression, 9),

    # Drops - Not shuffled, here for reference
    #"Life Heart": TGLItemData("Filler",  TGL_ITEMID_BASE+1020, ItemClassification.filler),
    #"Red Chip":   TGLItemData("Filler",  TGL_ITEMID_BASE+1021, ItemClassification.filler),
    #"Blue Chip":  TGLItemData("Filler",  TGL_ITEMID_BASE+1022, ItemClassification.filler),

}

event_item_table: Dict[str, TGLItemData] = {
    "Corridor 1 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 2 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 3 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 4 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 5 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 6 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 7 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 8 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 9 Cleared":   TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 10 Cleared":  TGLItemData("Event", classification=ItemClassification.progression),
    "Corridor 21 Cleared":  TGLItemData("Event", classification=ItemClassification.progression),

}


def get_item_count(name: str, distlevel: int) -> int:
    # Return item count based on item_distribution setting
    # option_vanilla = 0 - not called here, baked into item_table
    # option_exact = 1
    # option_reduced = 2
    # option_extra = 3

    # NOTE: There are 106 locations to place items, so each "column" here should add to 106
    #       Other than the first column which is just a reference... 

    item_counts: Dict[str, List[int]] = {
        "Subweapons":    [3 ,3 ,2 ,4 ],

        "Enemy Eraser":  [9 ,12,10,13],
        "Energy Pack":   [14,20,41,2 ],

        "Blue Lander":   [9 ,10,7 ,12],
        "Attack Up":     [3 ,3, 2 ,4 ],
        "Defense Up":    [9 ,6, 5 ,8 ],
        "Rapid Fire Up": [6 ,5, 4 ,6 ],
        "Red Lander":    [9 ,10,8 ,10]
    }

    if item_table[name].category == "Keys":
        return 1
    
    elif item_table[name].category == "Subweapons":
        return item_counts["Subweapons"][distlevel]
    
    else:
        return item_counts[name][distlevel]
    