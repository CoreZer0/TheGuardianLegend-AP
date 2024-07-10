from typing import Dict, NamedTuple, Optional, Tuple, List

from BaseClasses import Location


class TGLLocation(Location):
    game = "The Guardian Legend"


class TGLLocationData(NamedTuple):
    areanum: str  # In-game Area number
    category: str  # Corridor / Ground / Miniboss / Shop / Event
    code: Optional[int] = None  # AP Location code (ROM location offsets)
    bitflag: Optional[Tuple] = None  # RAM address for item flag + bit flag offset


def get_locations_by_category(category: str) -> Dict[str, TGLLocationData]:
    location_dict: Dict[str, TGLLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)
    return location_dict


def get_locations_by_areanum(areanum: str) -> Dict[str, TGLLocationData]:
    location_dict: Dict[str, TGLLocationData] = {}
    for name, data in location_table.items():
        if data.areanum == areanum:
            location_dict.setdefault(name, data)
    return location_dict

    
def get_event_locations_by_areanum(areanum: str) -> Dict[str, TGLLocationData]:
    location_dict: Dict[str, TGLLocationData] = {}
    for name, data in event_location_table.items():
        if data.areanum == areanum:
            location_dict.setdefault(name, data)
    return location_dict

def get_generic_locations_by_id(location_ids: List[int]) -> List[str]:
    location_names: List[str] = []
    for name, data in location_table_generic.items():
        if data.code in location_ids:
            location_names.append(name)
    return location_names

def get_locationcode_by_bitflag(bitflag: Tuple) -> int:
    for name, data in location_table.items():
        if data.bitflag == bitflag:
            return data.code


# ID code base 8471765000 = 'TGL' in ASCII decimal
TGL_LOCID_BASE = 8471760000
TGL_LOCID_GROUND   = TGL_LOCID_BASE + 1000
TGL_LOCID_SHOP     = TGL_LOCID_BASE + 2000
TGL_LOCID_CORRIDOR = TGL_LOCID_BASE + 3000
TGL_LOCID_BONUS    = TGL_LOCID_BASE + 4000
TGL_LOCID_GROUND_GENERIC   = TGL_LOCID_BASE + 5000
TGL_LOCID_SHOP_GENERIC     = TGL_LOCID_BASE + 6000
TGL_LOCID_CORRIDOR_GENERIC = TGL_LOCID_BASE + 7000
TGL_LOCID_BONUS_GENERIC    = TGL_LOCID_BASE + 8000


# Note: For LOCID, 1000s is Ground drops, 2000s is Shops, 3000s is Corridors, 4000s for bonus Corridor items 
# (see Rom.py)
# Total locations available: 106
location_table: Dict[str, TGLLocationData] = {
    # Area 0 - 12 locs
    "A0 Corridor 1 (X6 Y10)":      TGLLocationData("Area 0",  "Corridor",  TGL_LOCID_CORRIDOR+1,  (0x9, 0x1 )),
    "A0 Corridor 1 Bonus (X6 Y10)":TGLLocationData("Area 0",  "Corridor",  TGL_LOCID_BONUS+1),
    "A0 Crab Walker (X8 Y13)":     TGLLocationData("Area 0",  "Miniboss",  TGL_LOCID_GROUND+0x0b, (0x1, 0x8 )),
    "A0 Headcrawler (X14 Y9)":     TGLLocationData("Area 0",  "Miniboss",  TGL_LOCID_GROUND+0x0c, (0x1, 0x10)),
    "A0 (X12 Y12)":                TGLLocationData("Area 0",  "Ground",    TGL_LOCID_GROUND+0x35, (0x6, 0x20)),
    "A0 (X9 Y14)":                 TGLLocationData("Area 0",  "Ground",    TGL_LOCID_GROUND+0x39, (0x7, 0x2 )),
    "A0 (X8 Y11)":                 TGLLocationData("Area 0",  "Ground",    TGL_LOCID_GROUND+0x05, (0x0, 0x20)),
    "A0 (X8 Y9)":                  TGLLocationData("Area 0",  "Ground",    TGL_LOCID_GROUND+0x21, (0x4, 0x2 )),
    "A0 50 Chip Shop (X13 Y11)":   TGLLocationData("Area 0",  "Shop",      TGL_LOCID_SHOP+2,  (0x7, 0x4 )),
    "A0 100 Chip Shop (X13 Y10)":  TGLLocationData("Area 0",  "Shop",      TGL_LOCID_SHOP+5,  (0x7, 0x8 )),
    "A0 150 Chip Shop (X12 Y10)":  TGLLocationData("Area 0",  "Shop",      TGL_LOCID_SHOP+8,  (0x7, 0x10)),
    "A0 300 Chip Shop (X10 Y11)":  TGLLocationData("Area 0",  "Shop",      TGL_LOCID_SHOP+14, (0x7, 0x40)),
    "A0 500 Chip Shop (X10 Y10)":  TGLLocationData("Area 0",  "Shop",      TGL_LOCID_SHOP+11, (0x7, 0x20)),

    # Area 1 - 6 locs
    "A1 Corridor 11 (X1 Y8)":      TGLLocationData("Area 1",  "Corridor",  TGL_LOCID_CORRIDOR+11, (0xA, 0x4 )),
    "A1 Corridor 11 Bonus (X1 Y8)":TGLLocationData("Area 1",  "Corridor",  TGL_LOCID_BONUS+11),
    "A1 Claw Launcher (X4 Y11)":   TGLLocationData("Area 1",  "Miniboss",  TGL_LOCID_GROUND+0x0d, (0x1, 0x20)),
    "A1 Crab Walker (X0 Y6)":      TGLLocationData("Area 1",  "Miniboss",  TGL_LOCID_GROUND+0x0e, (0x1, 0x40)),
    "A1 (X3 Y10)":                 TGLLocationData("Area 1",  "Ground",    TGL_LOCID_GROUND+0x24, (0x4, 0x10)),
    "A1 (X4 Y12)":                 TGLLocationData("Area 1",  "Ground",    TGL_LOCID_GROUND+0x23, (0x4, 0x8 )),
    "A1 (X0 Y9)":                  TGLLocationData("Area 1",  "Ground",    TGL_LOCID_GROUND+0x26, (0x4, 0x40)),

    # Area 2 - 7 locs
    "A2 Corridor 2 (X2 Y16)":       TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_CORRIDOR+2,  (0x9, 0x2 )),
    "A2 Corridor 2 Bonus (X2 Y16)": TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_BONUS+2),
    "A2 Corridor 12 (X4 Y15)":      TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_CORRIDOR+12, (0xA, 0x8 )),
    "A2 Corridor 12 Bonus (X4 Y15)":TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_BONUS+12),
    "A2 Claw Launcher (X5 Y17)":    TGLLocationData("Area 2",  "Miniboss",  TGL_LOCID_GROUND+0x0f, (0x1, 0x80)),
    "A2 Crab Walker (X1 Y14)":      TGLLocationData("Area 2",  "Miniboss",  TGL_LOCID_GROUND+0x10, (0x2, 0x1 )),
    "A2 (X2 Y17)":                  TGLLocationData("Area 2",  "Ground",    TGL_LOCID_GROUND+0x36, (0x6, 0x40)),
    "A2 (X3 Y14)":                  TGLLocationData("Area 2",  "Ground",    TGL_LOCID_GROUND+0x25, (0x4, 0x20)),
    "A2 150 Chip Shop (X1 Y18)":    TGLLocationData("Area 2",  "Shop",      TGL_LOCID_SHOP+102,    (0x7, 0x80)),

    # Area 3 - 6 locs
    "A3 Corridor 3 (X4 Y20)":       TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_CORRIDOR+3,  (0x9, 0x4 )),
    "A3 Corridor 3 Bonus (X4 Y20)": TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_BONUS+3),
    "A3 Corridor 13 (X5 Y20)":      TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_CORRIDOR+13, (0xA, 0x10)),
    "A3 Corridor 13 Bonus (X5 Y20)":TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_BONUS+13),
    "A3 HeadCrawler (X1 Y20)":      TGLLocationData("Area 3",  "Miniboss",  TGL_LOCID_GROUND+0x11, (0x2, 0x2 )),
    "A3 Leech Flower (X6 Y23)":     TGLLocationData("Area 3",  "Miniboss",  TGL_LOCID_GROUND+0x12, (0x2, 0x4 )),
    "A3 (X0 Y22)":                  TGLLocationData("Area 3",  "Ground",    TGL_LOCID_GROUND+0x27, (0x4, 0x80)),
    "A3 (X6 Y22)":                  TGLLocationData("Area 3",  "Ground",    TGL_LOCID_GROUND+0x28, (0x5, 0x1 )),
    
    # Area 4 - 8 locs
    "A4 Corridor 4 (X20 Y0)":       TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_CORRIDOR+4,  (0x9, 0x8 )),
    "A4 Corridor 4 Bonus (X20 Y0)": TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_BONUS+4),
    "A4 Corridor 14 (X17 Y4)":      TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_CORRIDOR+14, (0xA, 0x20)),
    "A4 Corridor 14 Bonus (X17 Y4)":TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_BONUS+14),
    "A4 Crab Walker (X16 Y3)":      TGLLocationData("Area 4",  "Miniboss",  TGL_LOCID_GROUND+0x13, (0x2, 0x8 )),
    "A4 Leech Flower (X18 Y1)":     TGLLocationData("Area 4",  "Miniboss",  TGL_LOCID_GROUND+0x14, (0x2, 0x10)),
    "A4 (X19 Y6)":                  TGLLocationData("Area 4",  "Ground",    TGL_LOCID_GROUND+0x29, (0x5, 0x2 )),
    "A4 (X17 Y2)":                  TGLLocationData("Area 4",  "Ground",    TGL_LOCID_GROUND+0x2a, (0x5, 0x4 )),
    "A4 (X16 Y0)":                  TGLLocationData("Area 4",  "Ground",    TGL_LOCID_GROUND+0x37, (0x6, 0x80)),
    "A4 400 Chip Shop (X18 Y0)":    TGLLocationData("Area 4",  "Shop",      TGL_LOCID_SHOP+112,    (0x8, 0x2 )),

    # Area 5 - 7 locs
    "A5 Corridor 5 (X23 Y4)":         TGLLocationData("Area 5",  "Corridor",  TGL_LOCID_CORRIDOR+5,  (0x9, 0x10)),
    "A5 Corridor 5 Bonus (X23 Y4)":   TGLLocationData("Area 5",  "Corridor",  TGL_LOCID_BONUS+5),
    "A5 Corridor 15 (X21 Y8)":        TGLLocationData("Area 5",  "Corridor",  TGL_LOCID_CORRIDOR+15, (0xA, 0x40)),
    "A5 Corridor 15 Bonus (X21 Y8)":  TGLLocationData("Area 5",  "Corridor",  TGL_LOCID_BONUS+15),
    "A5 Crab Walker (X19 Y8)":        TGLLocationData("Area 5",  "Miniboss",  TGL_LOCID_GROUND+0x15, (0x2, 0x20)),
    "A5 Crystal Chaser (X21 Y4)":     TGLLocationData("Area 5",  "Miniboss",  TGL_LOCID_GROUND+0x16, (0x2, 0x40)),
    "A5 (X23 Y8)":                    TGLLocationData("Area 5",  "Ground",    TGL_LOCID_GROUND+0x01, (0x0, 0x2 )),
    "A5 (X23 Y6)":                    TGLLocationData("Area 5",  "Ground",    TGL_LOCID_GROUND+0x2b, (0x5, 0x8 )),
    "A5 (X23 Y3)":                    TGLLocationData("Area 5",  "Ground",    TGL_LOCID_GROUND+0x2c, (0x5, 0x10)),

    # Area 6 - 8 locs
    "A6 Corridor 6 (X16 Y11)":        TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_CORRIDOR+6,  (0x9, 0x20)),
    "A6 Corridor 6 Bonus (X16 Y11)":  TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_BONUS+6),
    "A6 Corridor 16 (X18 Y13)":       TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_CORRIDOR+16, (0xA, 0x80)),
    "A6 Corridor 16 Bonus (X18 Y13)": TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_BONUS+16),
    "A6 Headcrawler (X18 Y10)":       TGLLocationData("Area 6",  "Miniboss",  TGL_LOCID_GROUND+0x17, (0x2, 0x80)),
    "A6 Claw Launcher (X17 Y16)":     TGLLocationData("Area 6",  "Miniboss",  TGL_LOCID_GROUND+0x18, (0x3, 0x1 )),
    "A6 (X18 Y12)":                   TGLLocationData("Area 6",  "Ground",    TGL_LOCID_GROUND+0x2d, (0x5, 0x20)),
    "A6 (X20 Y10)":                   TGLLocationData("Area 6",  "Ground",    TGL_LOCID_GROUND+0x2e, (0x5, 0x40)),
    "A6 (X21 Y13)":                   TGLLocationData("Area 6",  "Ground",    TGL_LOCID_GROUND+0x02, (0x0, 0x4 )),
    "A6 (X16 Y12)":                   TGLLocationData("Area 6",  "Ground",    TGL_LOCID_GROUND+0x0a, (0x1, 0x4 )),

    # Area 7 - 9 locs
    "A7 Corridor 7 (X19 Y23)":       TGLLocationData("Area 7",  "Corridor",  TGL_LOCID_CORRIDOR+7,  (0x9, 0x40)),
    "A7 Corridor 7 Bonus (X19 Y23)": TGLLocationData("Area 7",  "Corridor",  TGL_LOCID_BONUS+7),
    "A7 Corridor 17 (X18 Y19)":      TGLLocationData("Area 7",  "Corridor",  TGL_LOCID_CORRIDOR+17, (0xB, 0x1 )),
    "A7 Corridor 17 Bonus (X18 Y19)":TGLLocationData("Area 7",  "Corridor",  TGL_LOCID_BONUS+17),
    "A7 Headcrawler (X16 Y18)":      TGLLocationData("Area 7",  "Miniboss",  TGL_LOCID_GROUND+0x19, (0x3, 0x2 )),
    "A7 Claw Launcher (X22 Y20)":    TGLLocationData("Area 7",  "Miniboss",  TGL_LOCID_GROUND+0x1a, (0x3, 0x4 )),
    "A7 (X17 Y23)":                  TGLLocationData("Area 7",  "Ground",    TGL_LOCID_GROUND+0x03, (0x0, 0x8 )),
    "A7 (X22 Y23)":                  TGLLocationData("Area 7",  "Ground",    TGL_LOCID_GROUND+0x30, (0x6, 0x1 )),
    "A7 (X19 Y19)":                  TGLLocationData("Area 7",  "Ground",    TGL_LOCID_GROUND+0x2f, (0x5, 0x80)),
    "A7 1000 Chip Shop (X23 Y21)":   TGLLocationData("Area 7",  "Shop",      TGL_LOCID_SHOP+107,    (0x8, 0x1 )),
    "A7 600 Chip Shop (X15 Y12)":    TGLLocationData("Area 7",  "Shop",      TGL_LOCID_SHOP+117,    (0x8, 0x4 )),

    # Area 8 - 8 locs
    "A8 Corridor 8 (X10 Y16)":        TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_CORRIDOR+8, (0x9, 0x80)),
    "A8 Corridor 8 Bonus (X10 Y16)":  TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_BONUS+8),
    "A8 Corridor 18 (X11 Y19)":       TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_CORRIDOR+18, (0xB, 0x2 )),
    "A8 Corridor 18 Bonus (X11 Y19)": TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_BONUS+18),
    "A8 Leech Flower (X12 Y18)":      TGLLocationData("Area 8",  "Miniboss",  TGL_LOCID_GROUND+0x1b, (0x3, 0x8 )),
    "A8 Crab Walker (X12 Y22)":       TGLLocationData("Area 8",  "Miniboss",  TGL_LOCID_GROUND+0x1c, (0x3, 0x10)),
    "A8 (X10 Y18)":                   TGLLocationData("Area 8",  "Ground",    TGL_LOCID_GROUND+0x31, (0x6, 0x2 )),
    "A8 (X14 Y20)":                   TGLLocationData("Area 8",  "Ground",    TGL_LOCID_GROUND+0x32, (0x6, 0x4 )),
    "A8 (X12 Y23)":                   TGLLocationData("Area 8",  "Ground",    TGL_LOCID_GROUND+0x04, (0x0, 0x10)),
    "A8 (X9 Y19)":                    TGLLocationData("Area 8",  "Ground",    TGL_LOCID_GROUND+0x38, (0x7, 0x1 )),

    # Area 9 - 9 locs
    "A9 Corridor 9 (X2 Y2)":          TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_CORRIDOR+9,  (0xA, 0x1 )),
    "A9 Corridor 9 Bonus (X2 Y2)":    TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_BONUS+9),
    "A9 Corridor 19 (X4 Y4)":         TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_CORRIDOR+19, (0xB, 0x4 )),
    "A9 Corridor 19 Bonus (X4 Y4)":   TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_BONUS+19),
    "A9 Crab Walker (X5 Y3)":         TGLLocationData("Area 9",  "Miniboss",  TGL_LOCID_GROUND+0x1d, (0x3, 0x20)),
    "A9 Headcrawler (X2 Y0)":         TGLLocationData("Area 9",  "Miniboss",  TGL_LOCID_GROUND+0x1e, (0x3, 0x40)),
    "A9 (X3 Y6)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND+0x33, (0x6, 0x8 )),
    "A9 (X3 Y3)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND+0x34, (0x6, 0x10)),
    "A9 (X6 Y3)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND+0x06, (0x0, 0x40)),
    "A9 (X0 Y3)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND+0x07, (0x0, 0x80)),
    "A9 (X1 Y0)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND+0x08, (0x1, 0x1 )),

    # Area 10 - 6 locs
    "A10 Corridor 10 (X11 Y0)":      TGLLocationData("Area 10", "Corridor",  TGL_LOCID_CORRIDOR+10, (0xA, 0x2 )),
    "A10 Corridor 10 Bonus (X11 Y0)":TGLLocationData("Area 10", "Corridor",  TGL_LOCID_BONUS+10),
    "A10 Corridor 20 (X11 Y5)":      TGLLocationData("Area 10", "Corridor",  TGL_LOCID_CORRIDOR+20, (0xB, 0x8 )),
    "A10 Corridor 20 Bonus (X11 Y5)":TGLLocationData("Area 10", "Corridor",  TGL_LOCID_BONUS+20),
    "A10 Dino Skull (X11 Y3)":       TGLLocationData("Area 10", "Miniboss",  TGL_LOCID_GROUND+0x1f, (0x3, 0x80)),
    "A10 Glider (X12 Y0)":           TGLLocationData("Area 10", "Miniboss",  TGL_LOCID_GROUND+0x20, (0x4, 0x1 )),
    "A10 (X12 Y4)":                  TGLLocationData("Area 10", "Ground",    TGL_LOCID_GROUND+0x09, (0x1, 0x2 )),
    "A10 2000 Chip Shop (X12 Y5)":   TGLLocationData("Area 10", "Shop",      TGL_LOCID_SHOP+122,    (0x8, 0x8 )),
    
}

'''
# Matches RAM bitflag for check. to ROM location address, used by map randomizer and client to find correct location id
#  to send for a given randomized item location.
location_address_lookup: Dict[int, Tuple] = {
    # Area 0
    (0x9, 0x1 ): TGL_LOCID_CORRIDOR+1,
    (0x1, 0x8 ): TGL_LOCID_GROUND+0x0b,
    (0x1, 0x10): TGL_LOCID_GROUND+0x0c,
    (0x6, 0x20): TGL_LOCID_GROUND+0x35,
    (0x7, 0x2 ): TGL_LOCID_GROUND+0x39,
    (0x0, 0x20): TGL_LOCID_GROUND+0x05,
    (0x4, 0x2 ): TGL_LOCID_GROUND+0x21,
    (0x7, 0x4 ): TGL_LOCID_SHOP+2,
    (0x7, 0x8 ): TGL_LOCID_SHOP+5,
    (0x7, 0x10): TGL_LOCID_SHOP+8,
    (0x7, 0x40): TGL_LOCID_SHOP+14,
    (0x7, 0x20): TGL_LOCID_SHOP+11,

    # Area 1
    (0xA, 0x4 ): TGL_LOCID_CORRIDOR+11,
    (0x1, 0x20): TGL_LOCID_GROUND+0x0d,
    (0x1, 0x40): TGL_LOCID_GROUND+0x0e,
    (0x4, 0x10): TGL_LOCID_GROUND+0x24,
    (0x4, 0x8 ): TGL_LOCID_GROUND+0x23,
    (0x4, 0x40): TGL_LOCID_GROUND+0x26,

    # Area 2
    (0x9, 0x2 ): TGL_LOCID_CORRIDOR+2,
    (0xA, 0x8 ): TGL_LOCID_CORRIDOR+12,
    (0x1, 0x80): TGL_LOCID_GROUND+0x0f,
    (0x2, 0x1 ): TGL_LOCID_GROUND+0x10,
    (0x6, 0x40): TGL_LOCID_GROUND+0x36,
    (0x4, 0x20): TGL_LOCID_GROUND+0x25,
    (0x7, 0x80): TGL_LOCID_SHOP+102,

    # Area 3
    (0x9, 0x4 ): TGL_LOCID_CORRIDOR+3,
    (0xA, 0x10): TGL_LOCID_CORRIDOR+13,
    (0x2, 0x2 ): TGL_LOCID_GROUND+0x11,
    (0x2, 0x4 ): TGL_LOCID_GROUND+0x12,
    (0x4, 0x80): TGL_LOCID_GROUND+0x27,
    (0x5, 0x1 ): TGL_LOCID_GROUND+0x28,
    
    # Area 4 
    (0x9, 0x8 ): TGL_LOCID_CORRIDOR+4,
    (0xA, 0x20): TGL_LOCID_CORRIDOR+14,
    (0x2, 0x8 ): TGL_LOCID_GROUND+0x13,
    (0x2, 0x10): TGL_LOCID_GROUND+0x14,
    (0x5, 0x2 ): TGL_LOCID_GROUND+0x29,
    (0x5, 0x4 ): TGL_LOCID_GROUND+0x2a,
    (0x6, 0x80): TGL_LOCID_GROUND+0x37,
    (0x8, 0x2 ): TGL_LOCID_SHOP+112,

    # Area 5 
    (0x9, 0x10): TGL_LOCID_CORRIDOR+5,
    (0xA, 0x40): TGL_LOCID_CORRIDOR+15,
    (0x2, 0x20): TGL_LOCID_GROUND+0x15,
    (0x2, 0x40): TGL_LOCID_GROUND+0x16,
    (0x0, 0x2 ): TGL_LOCID_GROUND+0x01,
    (0x5, 0x8 ): TGL_LOCID_GROUND+0x2b,
    (0x5, 0x10): TGL_LOCID_GROUND+0x2c,

    # Area 6
    (0x9, 0x20): TGL_LOCID_CORRIDOR+6,
    (0xA, 0x80): TGL_LOCID_CORRIDOR+16,
    (0x2, 0x80): TGL_LOCID_GROUND+0x17,
    (0x3, 0x1 ): TGL_LOCID_GROUND+0x18,
    (0x5, 0x20): TGL_LOCID_GROUND+0x2d,
    (0x5, 0x40): TGL_LOCID_GROUND+0x2e,
    (0x0, 0x4 ): TGL_LOCID_GROUND+0x02,
    (0x1, 0x4 ): TGL_LOCID_GROUND+0x0a,

    # Area 7
    (0x9, 0x40): TGL_LOCID_CORRIDOR+7,
    (0xB, 0x1 ): TGL_LOCID_CORRIDOR+17,
    (0x3, 0x2 ): TGL_LOCID_GROUND+0x19,
    (0x3, 0x4 ): TGL_LOCID_GROUND+0x1a,
    (0x0, 0x8 ): TGL_LOCID_GROUND+0x03,
    (0x6, 0x1 ): TGL_LOCID_GROUND+0x30,
    (0x5, 0x80): TGL_LOCID_GROUND+0x2f,
    (0x8, 0x1 ): TGL_LOCID_SHOP+107,
    (0x8, 0x4 ): TGL_LOCID_SHOP+117,

    # Area 8
    (0x9, 0x80): TGL_LOCID_CORRIDOR+8,
    (0xB, 0x2 ): TGL_LOCID_CORRIDOR+18,
    (0x3, 0x8 ): TGL_LOCID_GROUND+0x1b,
    (0x3, 0x10): TGL_LOCID_GROUND+0x1c,
    (0x6, 0x2 ): TGL_LOCID_GROUND+0x31,
    (0x6, 0x4 ): TGL_LOCID_GROUND+0x32,
    (0x0, 0x10): TGL_LOCID_GROUND+0x04,
    (0x7, 0x1 ): TGL_LOCID_GROUND+0x38,

    # Area 9
    (0xA, 0x1 ): TGL_LOCID_CORRIDOR+9,
    (0xB, 0x4 ): TGL_LOCID_CORRIDOR+19,
    (0x3, 0x20): TGL_LOCID_GROUND+0x1d,
    (0x3, 0x40): TGL_LOCID_GROUND+0x1e,
    (0x6, 0x8 ): TGL_LOCID_GROUND+0x33,
    (0x6, 0x10): TGL_LOCID_GROUND+0x34,
    (0x0, 0x40): TGL_LOCID_GROUND+0x06,
    (0x0, 0x80): TGL_LOCID_GROUND+0x07,
    (0x1, 0x1 ): TGL_LOCID_GROUND+0x08,

    # Area 10
    (0xA, 0x2 ): TGL_LOCID_CORRIDOR+10,
    (0xB, 0x8 ): TGL_LOCID_CORRIDOR+20,
    (0x3, 0x80): TGL_LOCID_GROUND+0x1f,
    (0x4, 0x1 ): TGL_LOCID_GROUND+0x20,
    (0x1, 0x2 ): TGL_LOCID_GROUND+0x09,
    (0x8, 0x8 ): TGL_LOCID_SHOP+122,
}
'''


location_address_lookup: Dict[int, Tuple] = {
    # Area 0
    TGL_LOCID_CORRIDOR+1:  (0x9, 0x1 ),
    TGL_LOCID_GROUND+0x0b: (0x1, 0x8 ),
    TGL_LOCID_GROUND+0x0c: (0x1, 0x10),
    TGL_LOCID_GROUND+0x35: (0x6, 0x20),
    TGL_LOCID_GROUND+0x39: (0x7, 0x2 ),
    TGL_LOCID_GROUND+0x05: (0x0, 0x20),
    TGL_LOCID_GROUND+0x21: (0x4, 0x2 ),
    TGL_LOCID_SHOP+2:  (0x7, 0x4 ),
    TGL_LOCID_SHOP+5:  (0x7, 0x8 ),
    TGL_LOCID_SHOP+8:  (0x7, 0x10),
    TGL_LOCID_SHOP+14: (0x7, 0x40),
    TGL_LOCID_SHOP+11: (0x7, 0x20),

    # Area 1
    TGL_LOCID_CORRIDOR+11: (0xA, 0x4 ),
    TGL_LOCID_GROUND+0x0d: (0x1, 0x20),
    TGL_LOCID_GROUND+0x0e: (0x1, 0x40),
    TGL_LOCID_GROUND+0x24: (0x4, 0x10),
    TGL_LOCID_GROUND+0x23: (0x4, 0x8 ),
    TGL_LOCID_GROUND+0x26: (0x4, 0x40),

    # Area 2
    TGL_LOCID_CORRIDOR+2:  (0x9, 0x2 ),
    TGL_LOCID_CORRIDOR+12: (0xA, 0x8 ),
    TGL_LOCID_GROUND+0x0f: (0x1, 0x80),
    TGL_LOCID_GROUND+0x10: (0x2, 0x1 ),
    TGL_LOCID_GROUND+0x36: (0x6, 0x40),
    TGL_LOCID_GROUND+0x25: (0x4, 0x20),
    TGL_LOCID_SHOP+102:    (0x7, 0x80),

    # Area 3
    TGL_LOCID_CORRIDOR+3:  (0x9, 0x4 ),
    TGL_LOCID_CORRIDOR+13: (0xA, 0x10),
    TGL_LOCID_GROUND+0x11: (0x2, 0x2 ),
    TGL_LOCID_GROUND+0x12: (0x2, 0x4 ),
    TGL_LOCID_GROUND+0x27: (0x4, 0x80),
    TGL_LOCID_GROUND+0x28: (0x5, 0x1 ),
    
    # Area 4 
    TGL_LOCID_CORRIDOR+4:  (0x9, 0x8 ),
    TGL_LOCID_CORRIDOR+14: (0xA, 0x20),
    TGL_LOCID_GROUND+0x13: (0x2, 0x8 ),
    TGL_LOCID_GROUND+0x14: (0x2, 0x10),
    TGL_LOCID_GROUND+0x29: (0x5, 0x2 ),
    TGL_LOCID_GROUND+0x2a: (0x5, 0x4 ),
    TGL_LOCID_GROUND+0x37: (0x6, 0x80),
    TGL_LOCID_SHOP+112:    (0x8, 0x2 ),

    # Area 5 
    TGL_LOCID_CORRIDOR+5:  (0x9, 0x10),
    TGL_LOCID_CORRIDOR+15: (0xA, 0x40),
    TGL_LOCID_GROUND+0x15: (0x2, 0x20),
    TGL_LOCID_GROUND+0x16: (0x2, 0x40),
    TGL_LOCID_GROUND+0x01: (0x0, 0x2 ),
    TGL_LOCID_GROUND+0x2b: (0x5, 0x8 ),
    TGL_LOCID_GROUND+0x2c: (0x5, 0x10),

    # Area 6
    TGL_LOCID_CORRIDOR+6:  (0x9, 0x20),
    TGL_LOCID_CORRIDOR+16: (0xA, 0x80),
    TGL_LOCID_GROUND+0x17: (0x2, 0x80),
    TGL_LOCID_GROUND+0x18: (0x3, 0x1 ),
    TGL_LOCID_GROUND+0x2d: (0x5, 0x20),
    TGL_LOCID_GROUND+0x2e: (0x5, 0x40),
    TGL_LOCID_GROUND+0x02: (0x0, 0x4 ),
    TGL_LOCID_GROUND+0x0a: (0x1, 0x4 ),

    # Area 7
    TGL_LOCID_CORRIDOR+7:  (0x9, 0x40),
    TGL_LOCID_CORRIDOR+17: (0xB, 0x1 ),
    TGL_LOCID_GROUND+0x19: (0x3, 0x2 ),
    TGL_LOCID_GROUND+0x1a: (0x3, 0x4 ),
    TGL_LOCID_GROUND+0x03: (0x0, 0x8 ),
    TGL_LOCID_GROUND+0x30: (0x6, 0x1 ),
    TGL_LOCID_GROUND+0x2f: (0x5, 0x80),
    TGL_LOCID_SHOP+107:    (0x8, 0x1 ),
    TGL_LOCID_SHOP+117:    (0x8, 0x4 ),

    # Area 8
    TGL_LOCID_CORRIDOR+8:  (0x9, 0x80),
    TGL_LOCID_CORRIDOR+18: (0xB, 0x2 ),
    TGL_LOCID_GROUND+0x1b: (0x3, 0x8 ),
    TGL_LOCID_GROUND+0x1c: (0x3, 0x10),
    TGL_LOCID_GROUND+0x31: (0x6, 0x2 ),
    TGL_LOCID_GROUND+0x32: (0x6, 0x4 ),
    TGL_LOCID_GROUND+0x04: (0x0, 0x10),
    TGL_LOCID_GROUND+0x38: (0x7, 0x1 ),

    # Area 9
    TGL_LOCID_CORRIDOR+9:  (0xA, 0x1 ),
    TGL_LOCID_CORRIDOR+19: (0xB, 0x4 ),
    TGL_LOCID_GROUND+0x1d: (0x3, 0x20),
    TGL_LOCID_GROUND+0x1e: (0x3, 0x40),
    TGL_LOCID_GROUND+0x33: (0x6, 0x8 ),
    TGL_LOCID_GROUND+0x34: (0x6, 0x10),
    TGL_LOCID_GROUND+0x06: (0x0, 0x40),
    TGL_LOCID_GROUND+0x07: (0x0, 0x80),
    TGL_LOCID_GROUND+0x08: (0x1, 0x1 ),

    # Area 10
    TGL_LOCID_CORRIDOR+10: (0xA, 0x2 ),
    TGL_LOCID_CORRIDOR+20: (0xB, 0x8 ),
    TGL_LOCID_GROUND+0x1f: (0x3, 0x80),
    TGL_LOCID_GROUND+0x20: (0x4, 0x1 ),
    TGL_LOCID_GROUND+0x09: (0x1, 0x2 ),
    TGL_LOCID_SHOP+122:    (0x8, 0x8 ),
}

# Location names genericized for map randomization
# Assumes any given area can have up to 6 items and 3 minibosses
# ROM IDs and RAM flags will have to be provided by the map randomizer at generation time
# Note: For generic LOCID, 5000s is Ground drops and 6000s is Shops, 7000s is Corridors, 8000s for bonus Corridor items
# (see Rom.py)
location_table_generic: Dict[str, TGLLocationData] = {
    # Area 0 
    "A0 Corridor 1":        TGLLocationData("Area 0",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+1, (0x9, 0x1 )),
    "A0 Corridor 1 Bonus":  TGLLocationData("Area 0",  "Corridor", TGL_LOCID_BONUS_GENERIC+1),
    "A0 Miniboss A":        TGLLocationData("Area 0",  "Miniboss", TGL_LOCID_GROUND_GENERIC+0),
    "A0 Miniboss B":        TGLLocationData("Area 0",  "Miniboss", TGL_LOCID_GROUND_GENERIC+1),
    "A0 Miniboss C":        TGLLocationData("Area 0",  "Miniboss", TGL_LOCID_GROUND_GENERIC+2),
    "A0 Ground Item A":     TGLLocationData("Area 0",  "Ground",   TGL_LOCID_GROUND_GENERIC+3),
    "A0 Ground Item B":     TGLLocationData("Area 0",  "Ground",   TGL_LOCID_GROUND_GENERIC+4),
    "A0 Ground Item C":     TGLLocationData("Area 0",  "Ground",   TGL_LOCID_GROUND_GENERIC+5),
    "A0 Ground Item D":     TGLLocationData("Area 0",  "Ground",   TGL_LOCID_GROUND_GENERIC+6),
    "A0 Ground Item E":     TGLLocationData("Area 0",  "Ground",   TGL_LOCID_GROUND_GENERIC+7),
    "A0 Ground Item F":     TGLLocationData("Area 0",  "Ground",   TGL_LOCID_GROUND_GENERIC+8),
    "A0 50 Chip Shop":   TGLLocationData("Area 0",  "Shop", TGL_LOCID_SHOP_GENERIC+2,  (0x7, 0x4 )),
    "A0 100 Chip Shop":  TGLLocationData("Area 0",  "Shop", TGL_LOCID_SHOP_GENERIC+5,  (0x7, 0x8 )),
    "A0 150 Chip Shop":  TGLLocationData("Area 0",  "Shop", TGL_LOCID_SHOP_GENERIC+8,  (0x7, 0x10)),
    "A0 300 Chip Shop":  TGLLocationData("Area 0",  "Shop", TGL_LOCID_SHOP_GENERIC+14, (0x7, 0x40)),
    "A0 500 Chip Shop":  TGLLocationData("Area 0",  "Shop", TGL_LOCID_SHOP_GENERIC+11, (0x7, 0x20)),

    # Area 1
    "A1 Corridor 11":       TGLLocationData("Area 1",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+11, (0xA, 0x4 )),
    "A1 Corridor 11 Bonus": TGLLocationData("Area 1",  "Corridor", TGL_LOCID_BONUS_GENERIC+11),
    "A1 Miniboss A":        TGLLocationData("Area 1",  "Miniboss", TGL_LOCID_GROUND_GENERIC+10),
    "A1 Miniboss B":        TGLLocationData("Area 1",  "Miniboss", TGL_LOCID_GROUND_GENERIC+11),
    "A1 Miniboss C":        TGLLocationData("Area 1",  "Miniboss", TGL_LOCID_GROUND_GENERIC+12),
    "A1 Ground Item A":     TGLLocationData("Area 1",  "Ground",   TGL_LOCID_GROUND_GENERIC+13),
    "A1 Ground Item B":     TGLLocationData("Area 1",  "Ground",   TGL_LOCID_GROUND_GENERIC+14),
    "A1 Ground Item C":     TGLLocationData("Area 1",  "Ground",   TGL_LOCID_GROUND_GENERIC+15),
    "A1 Ground Item D":     TGLLocationData("Area 1",  "Ground",   TGL_LOCID_GROUND_GENERIC+16),
    "A1 Ground Item E":     TGLLocationData("Area 1",  "Ground",   TGL_LOCID_GROUND_GENERIC+17),
    "A1 Ground Item F":     TGLLocationData("Area 1",  "Ground",   TGL_LOCID_GROUND_GENERIC+18),

    # Area 2
    "A2 Corridor 2":        TGLLocationData("Area 2",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+2, (0x9, 0x2 )),
    "A2 Corridor 2 Bonus":  TGLLocationData("Area 2",  "Corridor", TGL_LOCID_BONUS_GENERIC+2),
    "A2 Corridor 12":       TGLLocationData("Area 2",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+12, (0xA, 0x8 )),
    "A2 Corridor 12 Bonus": TGLLocationData("Area 2",  "Corridor", TGL_LOCID_BONUS_GENERIC+12),
    "A2 Miniboss A":        TGLLocationData("Area 2",  "Miniboss", TGL_LOCID_GROUND_GENERIC+20),
    "A2 Miniboss B":        TGLLocationData("Area 2",  "Miniboss", TGL_LOCID_GROUND_GENERIC+21),
    "A2 Miniboss C":        TGLLocationData("Area 2",  "Miniboss", TGL_LOCID_GROUND_GENERIC+22),
    "A2 Ground Item A":     TGLLocationData("Area 2",  "Ground",   TGL_LOCID_GROUND_GENERIC+23),
    "A2 Ground Item B":     TGLLocationData("Area 2",  "Ground",   TGL_LOCID_GROUND_GENERIC+24),
    "A2 Ground Item C":     TGLLocationData("Area 2",  "Ground",   TGL_LOCID_GROUND_GENERIC+25),
    "A2 Ground Item D":     TGLLocationData("Area 2",  "Ground",   TGL_LOCID_GROUND_GENERIC+26),
    "A2 Ground Item E":     TGLLocationData("Area 2",  "Ground",   TGL_LOCID_GROUND_GENERIC+27),
    "A2 Ground Item F":     TGLLocationData("Area 2",  "Ground",   TGL_LOCID_GROUND_GENERIC+28),
    "A2 150 Chip Shop":     TGLLocationData("Area 2",  "Shop", TGL_LOCID_SHOP_GENERIC+102, (0x7, 0x80)),

    # Area 3
    "A3 Corridor 3":        TGLLocationData("Area 3",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+3, (0x9, 0x4 )),
    "A3 Corridor 3 Bonus":  TGLLocationData("Area 3",  "Corridor", TGL_LOCID_BONUS_GENERIC+3),
    "A3 Corridor 13":       TGLLocationData("Area 3",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+13, (0xA, 0x10)),
    "A3 Corridor 13 Bonus": TGLLocationData("Area 3",  "Corridor", TGL_LOCID_BONUS_GENERIC+13),
    "A3 Miniboss A":        TGLLocationData("Area 3",  "Miniboss", TGL_LOCID_GROUND_GENERIC+30),
    "A3 Miniboss B":        TGLLocationData("Area 3",  "Miniboss", TGL_LOCID_GROUND_GENERIC+31),
    "A3 Miniboss C":        TGLLocationData("Area 3",  "Miniboss", TGL_LOCID_GROUND_GENERIC+32),
    "A3 Ground Item A":     TGLLocationData("Area 3",  "Ground",   TGL_LOCID_GROUND_GENERIC+33),
    "A3 Ground Item B":     TGLLocationData("Area 3",  "Ground",   TGL_LOCID_GROUND_GENERIC+34),
    "A3 Ground Item C":     TGLLocationData("Area 3",  "Ground",   TGL_LOCID_GROUND_GENERIC+35),
    "A3 Ground Item D":     TGLLocationData("Area 3",  "Ground",   TGL_LOCID_GROUND_GENERIC+36),
    "A3 Ground Item E":     TGLLocationData("Area 3",  "Ground",   TGL_LOCID_GROUND_GENERIC+37),
    "A3 Ground Item F":     TGLLocationData("Area 3",  "Ground",   TGL_LOCID_GROUND_GENERIC+38),
    
    # Area 4
    "A4 Corridor 4":        TGLLocationData("Area 4",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+4, (0x9, 0x8 )),
    "A4 Corridor 4 Bonus":  TGLLocationData("Area 4",  "Corridor", TGL_LOCID_BONUS_GENERIC+4),
    "A4 Corridor 14":       TGLLocationData("Area 4",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+14, (0xA, 0x20)),
    "A4 Corridor 14 Bonus": TGLLocationData("Area 4",  "Corridor", TGL_LOCID_BONUS_GENERIC+14),
    "A4 Miniboss A":        TGLLocationData("Area 4",  "Miniboss", TGL_LOCID_GROUND_GENERIC+40),
    "A4 Miniboss B":        TGLLocationData("Area 4",  "Miniboss", TGL_LOCID_GROUND_GENERIC+41),
    "A4 Miniboss C":        TGLLocationData("Area 4",  "Miniboss", TGL_LOCID_GROUND_GENERIC+42),
    "A4 Ground Item A":     TGLLocationData("Area 4",  "Ground",   TGL_LOCID_GROUND_GENERIC+43),
    "A4 Ground Item B":     TGLLocationData("Area 4",  "Ground",   TGL_LOCID_GROUND_GENERIC+44),
    "A4 Ground Item C":     TGLLocationData("Area 4",  "Ground",   TGL_LOCID_GROUND_GENERIC+45),
    "A4 Ground Item D":     TGLLocationData("Area 4",  "Ground",   TGL_LOCID_GROUND_GENERIC+46),
    "A4 Ground Item E":     TGLLocationData("Area 4",  "Ground",   TGL_LOCID_GROUND_GENERIC+47),
    "A4 Ground Item F":     TGLLocationData("Area 4",  "Ground",   TGL_LOCID_GROUND_GENERIC+48),
    "A4 400 Chip Shop":     TGLLocationData("Area 4",  "Shop", TGL_LOCID_SHOP_GENERIC+112, (0x8, 0x2 )),

    # Area 5
    "A5 Corridor 5":        TGLLocationData("Area 5",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+5, (0x9, 0x10)),
    "A5 Corridor 5 Bonus":  TGLLocationData("Area 5",  "Corridor", TGL_LOCID_BONUS_GENERIC+5),
    "A5 Corridor 15":       TGLLocationData("Area 5",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+15, (0xA, 0x40)),
    "A5 Corridor 15 Bonus": TGLLocationData("Area 5",  "Corridor", TGL_LOCID_BONUS_GENERIC+15),
    "A5 Miniboss A":        TGLLocationData("Area 5",  "Miniboss", TGL_LOCID_GROUND_GENERIC+50),
    "A5 Miniboss B":        TGLLocationData("Area 5",  "Miniboss", TGL_LOCID_GROUND_GENERIC+51),
    "A5 Miniboss C":        TGLLocationData("Area 5",  "Miniboss", TGL_LOCID_GROUND_GENERIC+52),
    "A5 Ground Item A":     TGLLocationData("Area 5",  "Ground",   TGL_LOCID_GROUND_GENERIC+53),
    "A5 Ground Item B":     TGLLocationData("Area 5",  "Ground",   TGL_LOCID_GROUND_GENERIC+54),
    "A5 Ground Item C":     TGLLocationData("Area 5",  "Ground",   TGL_LOCID_GROUND_GENERIC+55),
    "A5 Ground Item D":     TGLLocationData("Area 5",  "Ground",   TGL_LOCID_GROUND_GENERIC+56),
    "A5 Ground Item E":     TGLLocationData("Area 5",  "Ground",   TGL_LOCID_GROUND_GENERIC+57),
    "A5 Ground Item F":     TGLLocationData("Area 5",  "Ground",   TGL_LOCID_GROUND_GENERIC+58),

    # Area 6
    "A6 Corridor 6":        TGLLocationData("Area 6",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+6, (0x9, 0x20)),
    "A6 Corridor 6 Bonus":  TGLLocationData("Area 6",  "Corridor", TGL_LOCID_BONUS_GENERIC+6),
    "A6 Corridor 16":       TGLLocationData("Area 6",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+16, (0xA, 0x80)),
    "A6 Corridor 16 Bonus": TGLLocationData("Area 6",  "Corridor", TGL_LOCID_BONUS_GENERIC+16),
    "A6 Miniboss A":        TGLLocationData("Area 6",  "Miniboss", TGL_LOCID_GROUND_GENERIC+60),
    "A6 Miniboss B":        TGLLocationData("Area 6",  "Miniboss", TGL_LOCID_GROUND_GENERIC+61),
    "A6 Miniboss C":        TGLLocationData("Area 6",  "Miniboss", TGL_LOCID_GROUND_GENERIC+62),
    "A6 Ground Item A":     TGLLocationData("Area 6",  "Ground",   TGL_LOCID_GROUND_GENERIC+63),
    "A6 Ground Item B":     TGLLocationData("Area 6",  "Ground",   TGL_LOCID_GROUND_GENERIC+64),
    "A6 Ground Item C":     TGLLocationData("Area 6",  "Ground",   TGL_LOCID_GROUND_GENERIC+65),
    "A6 Ground Item D":     TGLLocationData("Area 6",  "Ground",   TGL_LOCID_GROUND_GENERIC+66),
    "A6 Ground Item E":     TGLLocationData("Area 6",  "Ground",   TGL_LOCID_GROUND_GENERIC+67),
    "A6 Ground Item F":     TGLLocationData("Area 6",  "Ground",   TGL_LOCID_GROUND_GENERIC+68),

    # Area 7
    "A7 Corridor 7":        TGLLocationData("Area 7",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+7, (0x9, 0x40)),
    "A7 Corridor 7 Bonus":  TGLLocationData("Area 7",  "Corridor", TGL_LOCID_BONUS_GENERIC+7),
    "A7 Corridor 17":       TGLLocationData("Area 7",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+17, (0xB, 0x1 )),
    "A7 Corridor 17 Bonus": TGLLocationData("Area 7",  "Corridor", TGL_LOCID_BONUS_GENERIC+17),
    "A7 Miniboss A":        TGLLocationData("Area 7",  "Miniboss", TGL_LOCID_GROUND_GENERIC+70),
    "A7 Miniboss B":        TGLLocationData("Area 7",  "Miniboss", TGL_LOCID_GROUND_GENERIC+71),
    "A7 Miniboss C":        TGLLocationData("Area 7",  "Miniboss", TGL_LOCID_GROUND_GENERIC+72),
    "A7 Ground Item A":     TGLLocationData("Area 7",  "Ground",   TGL_LOCID_GROUND_GENERIC+73),
    "A7 Ground Item B":     TGLLocationData("Area 7",  "Ground",   TGL_LOCID_GROUND_GENERIC+74),
    "A7 Ground Item C":     TGLLocationData("Area 7",  "Ground",   TGL_LOCID_GROUND_GENERIC+75),
    "A7 Ground Item D":     TGLLocationData("Area 7",  "Ground",   TGL_LOCID_GROUND_GENERIC+76),
    "A7 Ground Item E":     TGLLocationData("Area 7",  "Ground",   TGL_LOCID_GROUND_GENERIC+77),
    "A7 Ground Item F":     TGLLocationData("Area 7",  "Ground",   TGL_LOCID_GROUND_GENERIC+78),
    "A7 1000 Chip Shop":  TGLLocationData("Area 7",  "Shop", TGL_LOCID_SHOP_GENERIC+107, (0x8, 0x1 )),
    "A7 600 Chip Shop":   TGLLocationData("Area 7",  "Shop", TGL_LOCID_SHOP_GENERIC+117, (0x8, 0x4 )),

    # Area 8
    "A8 Corridor 8":        TGLLocationData("Area 8",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+8, (0x9, 0x80)),
    "A8 Corridor 8 Bonus":  TGLLocationData("Area 8",  "Corridor", TGL_LOCID_BONUS_GENERIC+8),
    "A8 Corridor 18":       TGLLocationData("Area 8",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+18, (0xB, 0x2 )),
    "A8 Corridor 18 Bonus": TGLLocationData("Area 8",  "Corridor", TGL_LOCID_BONUS_GENERIC+18),
    "A8 Miniboss A":        TGLLocationData("Area 8",  "Miniboss", TGL_LOCID_GROUND_GENERIC+80),
    "A8 Miniboss B":        TGLLocationData("Area 8",  "Miniboss", TGL_LOCID_GROUND_GENERIC+81),
    "A8 Miniboss C":        TGLLocationData("Area 8",  "Miniboss", TGL_LOCID_GROUND_GENERIC+82),
    "A8 Ground Item A":     TGLLocationData("Area 8",  "Ground",   TGL_LOCID_GROUND_GENERIC+83),
    "A8 Ground Item B":     TGLLocationData("Area 8",  "Ground",   TGL_LOCID_GROUND_GENERIC+84),
    "A8 Ground Item C":     TGLLocationData("Area 8",  "Ground",   TGL_LOCID_GROUND_GENERIC+85),
    "A8 Ground Item D":     TGLLocationData("Area 8",  "Ground",   TGL_LOCID_GROUND_GENERIC+86),
    "A8 Ground Item E":     TGLLocationData("Area 8",  "Ground",   TGL_LOCID_GROUND_GENERIC+87),
    "A8 Ground Item F":     TGLLocationData("Area 8",  "Ground",   TGL_LOCID_GROUND_GENERIC+88),

    # Area 9
    "A9 Corridor 9":        TGLLocationData("Area 9",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+9, (0xA, 0x1 )),
    "A9 Corridor 9 Bonus":  TGLLocationData("Area 9",  "Corridor", TGL_LOCID_BONUS_GENERIC+9),
    "A9 Corridor 19":       TGLLocationData("Area 9",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+19, (0xB, 0x4 )),
    "A9 Corridor 19 Bonus": TGLLocationData("Area 9",  "Corridor", TGL_LOCID_BONUS_GENERIC+19),
    "A9 Miniboss A":        TGLLocationData("Area 9",  "Miniboss", TGL_LOCID_GROUND_GENERIC+90),
    "A9 Miniboss B":        TGLLocationData("Area 9",  "Miniboss", TGL_LOCID_GROUND_GENERIC+91),
    "A9 Miniboss C":        TGLLocationData("Area 9",  "Miniboss", TGL_LOCID_GROUND_GENERIC+92),
    "A9 Ground Item A":     TGLLocationData("Area 9",  "Ground",   TGL_LOCID_GROUND_GENERIC+93),
    "A9 Ground Item B":     TGLLocationData("Area 9",  "Ground",   TGL_LOCID_GROUND_GENERIC+94),
    "A9 Ground Item C":     TGLLocationData("Area 9",  "Ground",   TGL_LOCID_GROUND_GENERIC+95),
    "A9 Ground Item D":     TGLLocationData("Area 9",  "Ground",   TGL_LOCID_GROUND_GENERIC+96),
    "A9 Ground Item E":     TGLLocationData("Area 9",  "Ground",   TGL_LOCID_GROUND_GENERIC+97),
    "A9 Ground Item F":     TGLLocationData("Area 9",  "Ground",   TGL_LOCID_GROUND_GENERIC+98),

    # Area 10
    "A10 Corridor 10":       TGLLocationData("Area 10",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+10, (0xA, 0x2 )),
    "A10 Corridor 10 Bonus": TGLLocationData("Area 10",  "Corridor", TGL_LOCID_BONUS_GENERIC+10),
    "A10 Corridor 20":       TGLLocationData("Area 10",  "Corridor", TGL_LOCID_CORRIDOR_GENERIC+20, (0xB, 0x8 )),
    "A10 Corridor 20 Bonus": TGLLocationData("Area 10",  "Corridor", TGL_LOCID_BONUS_GENERIC+20),
    "A10 Miniboss A":        TGLLocationData("Area 10",  "Miniboss", TGL_LOCID_GROUND_GENERIC+100),
    "A10 Miniboss B":        TGLLocationData("Area 10",  "Miniboss", TGL_LOCID_GROUND_GENERIC+101),
    "A10 Miniboss C":        TGLLocationData("Area 10",  "Miniboss", TGL_LOCID_GROUND_GENERIC+102),
    "A10 Ground Item A":     TGLLocationData("Area 10",  "Ground",   TGL_LOCID_GROUND_GENERIC+103),
    "A10 Ground Item B":     TGLLocationData("Area 10",  "Ground",   TGL_LOCID_GROUND_GENERIC+104),
    "A10 Ground Item C":     TGLLocationData("Area 10",  "Ground",   TGL_LOCID_GROUND_GENERIC+105),
    "A10 Ground Item D":     TGLLocationData("Area 10",  "Ground",   TGL_LOCID_GROUND_GENERIC+106),
    "A10 Ground Item E":     TGLLocationData("Area 10",  "Ground",   TGL_LOCID_GROUND_GENERIC+107),
    "A10 Ground Item F":     TGLLocationData("Area 10",  "Ground",   TGL_LOCID_GROUND_GENERIC+108),
    "A10 2000 Chip Shop":    TGLLocationData("Area 10",  "Shop", TGL_LOCID_SHOP_GENERIC+122, (0x8, 0x8 )),
}

event_location_table: Dict[str, TGLLocationData] = {
    "Corridor 1":   TGLLocationData("Area 0",      "Event"),
    "Corridor 2":   TGLLocationData("Area 2",      "Event"),
    "Corridor 3":   TGLLocationData("Area 3",      "Event"),
    "Corridor 4":   TGLLocationData("Area 4",      "Event"),
    "Corridor 5":   TGLLocationData("Area 5",      "Event"),
    "Corridor 6":   TGLLocationData("Area 6",      "Event"),
    "Corridor 7":   TGLLocationData("Area 7",      "Event"),
    "Corridor 8":   TGLLocationData("Area 8",      "Event"),
    "Corridor 9":   TGLLocationData("Area 9",      "Event"),
    "Corridor 10":  TGLLocationData("Area 10",     "Event"),
    "Corridor 21":  TGLLocationData("Corridor 21", "Event"),
}
