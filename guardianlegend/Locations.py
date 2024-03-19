from typing import Dict, NamedTuple, Optional, Tuple

from BaseClasses import Location, MultiWorld


class TGLLocation(Location):
    game = "The Guardian Legend"


class TGLLocationData(NamedTuple):
    areanum: str # In-game Area number
    category: str # Corridor / Ground / Miniboss / Shop / Event
    code: Optional[int] = None # AP Location code (ROM location offsets)
    bitflag: Optional[Tuple] = None # RAM address for item flag + bit flag offset

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

    # I think it's fine to return event locations here as well, makes creating region logic simpler
    for name, data in event_location_table.items():
        if data.areanum == areanum:
            location_dict.setdefault(name, data)

    return location_dict

def get_locationcode_by_bitflag(bitflag: Tuple) -> int:
    for name, data in location_table.items():
        if data.bitflag == bitflag:
            return data.code


# ID code base 8471765000 = 'TGL' in ASCII decimal + 5000
TGL_LOCID_BASE = 8471760000
TGL_LOCID_GROUND_BASE = TGL_LOCID_BASE + 1000

# Future concerns: Boss/Miniboss names probably need to be genericized in case of enemy rando
#                  Same with Shop names and cost/chip rando 
# Note: For LOCID, 1000s is Ground drops, 2000s is Shops, 3000s is Corridors, 4000s for double Corridor (see Rom.py)
# Total locations: 106
location_table: Dict[str, TGLLocationData] = {
    # Area 0 - 12 locs
    "A0 Corridor 1 (X6 Y10)":      TGLLocationData("Area 0",  "Corridor",  TGL_LOCID_BASE+3001, (0x9, 0x1 )),
    #"Corridor 1 Fleepa (X6 Y10)":  TGLLocationData("Area 0",  "Corridor",  TGL_LOCID_BASE+1002),
    "A0 Corridor 1 Bonus":         TGLLocationData("Area 0",  "Corridor",  TGL_LOCID_BASE+4001),
    "A0 Crab Walker (X8 Y13)":     TGLLocationData("Area 0",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x0b, (0x1, 0x8 )),
    "A0 Headcrawler (X14 Y9)":     TGLLocationData("Area 0",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x0c, (0x1, 0x10)),
    "A0 (X12 Y12)":                TGLLocationData("Area 0",  "Ground",    TGL_LOCID_GROUND_BASE+0x35, (0x6, 0x20)),
    "A0 (X9 Y14)":                 TGLLocationData("Area 0",  "Ground",    TGL_LOCID_GROUND_BASE+0x39, (0x7, 0x2 )),
    "A0 (X8 Y11)":                 TGLLocationData("Area 0",  "Ground",    TGL_LOCID_GROUND_BASE+0x05, (0x0, 0x20)),
    "A0 (X8 Y9)":                  TGLLocationData("Area 0",  "Ground",    TGL_LOCID_GROUND_BASE+0x21, (0x4, 0x2 )),
    "A0 50 Chip Shop (X13 Y11)":   TGLLocationData("Area 0",  "Shop",      TGL_LOCID_BASE+2002, (0x7, 0x4 )),
    "A0 100 Chip Shop (X13 Y10)":  TGLLocationData("Area 0",  "Shop",      TGL_LOCID_BASE+2005, (0x7, 0x8 )),
    "A0 150 Chip Shop (X12 Y10)":  TGLLocationData("Area 0",  "Shop",      TGL_LOCID_BASE+2008, (0x7, 0x10)),
    "A0 300 Chip Shop (X10 Y11)":  TGLLocationData("Area 0",  "Shop",      TGL_LOCID_BASE+2014, (0x7, 0x40)),
    "A0 500 Chip Shop (X10 Y10)":  TGLLocationData("Area 0",  "Shop",      TGL_LOCID_BASE+2011, (0x7, 0x20)),

    # Area 1 - 6 locs
    "A1 Corridor 11 (X1 Y8)":      TGLLocationData("Area 1",  "Corridor",  TGL_LOCID_BASE+3011,        (0xA, 0x4 )),
    "A1 Corridor 11 Bonus":        TGLLocationData("Area 1",  "Corridor",  TGL_LOCID_BASE+4011),
    "A1 Claw Launcher (X4 Y11)":   TGLLocationData("Area 1",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x0d, (0x1, 0x20)),
    "A1 Crab Walker (X0 Y6)":      TGLLocationData("Area 1",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x0e, (0x1, 0x40)),
    "A1 (X3 Y10)":                 TGLLocationData("Area 1",  "Ground",    TGL_LOCID_GROUND_BASE+0x24, (0x4, 0x10)),
    "A1 (X4 Y12)":                 TGLLocationData("Area 1",  "Ground",    TGL_LOCID_GROUND_BASE+0x23, (0x4, 0x8 )),
    "A1 (X0 Y9)":                  TGLLocationData("Area 1",  "Ground",    TGL_LOCID_GROUND_BASE+0x26, (0x4, 0x40)),

    # Area 2 - 7 locs
    "A2 Corridor 2 (X2 Y16)":         TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_BASE+3002, (0x9, 0x2 )),
    "A2 Corridor 2 Bonus":            TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_BASE+4002),
    #"Corridor 2 Crawdaddy (X2 Y16)":  TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_BASE+1202),
    "A2 Corridor 12 (X4 Y15)":        TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_BASE+3012, (0xA, 0x8 )),
    "A2 Corridor 12 Bonus":           TGLLocationData("Area 2",  "Corridor",  TGL_LOCID_BASE+4012, (0xA, 0x8 )),
    "A2 Claw Launcher (X5 Y17)":      TGLLocationData("Area 2",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x0f, (0x1, 0x80)),
    "A2 Crab Walker (X1 Y14)":        TGLLocationData("Area 2",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x10, (0x2, 0x1 )),
    "A2 (X2 Y17)":                    TGLLocationData("Area 2",  "Ground",    TGL_LOCID_GROUND_BASE+0x36, (0x6, 0x40)),
    "A2 (X3 Y14)":                    TGLLocationData("Area 2",  "Ground",    TGL_LOCID_GROUND_BASE+0x25, (0x4, 0x20)),
    "A2 150 Chip Shop A (X1 Y18)":    TGLLocationData("Area 2",  "Shop",      TGL_LOCID_BASE+2102, (0x7, 0x80)),
    #"A2 150 Chip Shop B (X1 Y18)":    TGLLocationData("Area 2",  "Shop",      TGL_LOCID_BASE+1222),

    # Area 3 - 6 locs
    "A3 Corridor 3 (X4 Y20)":         TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_BASE+3003, (0x9, 0x4 )),
    "A3 Corridor 3 Bonus":            TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_BASE+4003),
    #"Corridor 3 Optomon (X4 Y20)":    TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_BASE+1302),
    "A3 Corridor 13 (X5 Y20)":        TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_BASE+3013, (0xA, 0x10)),
    "A3 Corridor 13 Bonus":           TGLLocationData("Area 3",  "Corridor",  TGL_LOCID_BASE+4013),
    "A3 HeadCrawler (X1 Y20)":        TGLLocationData("Area 3",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x11, (0x2, 0x2 )),
    "A3 Leech Flower (X6 Y23)":       TGLLocationData("Area 3",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x12, (0x2, 0x4 )),
    "A3 (X0 Y22)":                    TGLLocationData("Area 3",  "Ground",    TGL_LOCID_GROUND_BASE+0x27, (0x4, 0x80)),
    "A3 (X6 Y22)":                    TGLLocationData("Area 3",  "Ground",    TGL_LOCID_GROUND_BASE+0x28, (0x5, 0x1 )),
    
    # Area 4 - 8 locs
    "A4 Corridor 4 (X20 Y0)":         TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_BASE+3004, (0x9, 0x8 )),
    "A4 Corridor 4 Bonus":            TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_BASE+4004),
    #"Corridor 4 Teramute (X20 Y0)":   TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_BASE+1402),
    "A4 Corridor 14 (X17 Y4)":        TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_BASE+3014, (0xA, 0x20)),
    "A4 Corridor 14 Bonus":           TGLLocationData("Area 4",  "Corridor",  TGL_LOCID_BASE+4014),
    "A4 Crab Walker (X16 Y3)":        TGLLocationData("Area 4",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x13, (0x2, 0x8 )),
    "A4 Leech Flower (X18 Y1)":       TGLLocationData("Area 4",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x14, (0x2, 0x10)),
    "A4 (X19 Y6)":                    TGLLocationData("Area 4",  "Ground",    TGL_LOCID_GROUND_BASE+0x29, (0x5, 0x2 )),
    "A4 (X17 Y2)":                    TGLLocationData("Area 4",  "Ground",    TGL_LOCID_GROUND_BASE+0x2a, (0x5, 0x4 )),
    "A4 (X16 Y0)":                    TGLLocationData("Area 4",  "Ground",    TGL_LOCID_GROUND_BASE+0x37, (0x6, 0x80)),
    "A4 400 Chip Shop A (X18 Y0)":    TGLLocationData("Area 4",  "Shop",      TGL_LOCID_BASE+2112, (0x8, 0x2 )),
    #"A4 400 Chip Shop B (X18 Y0)":    TGLLocationData("Area 4",  "Shop",      TGL_LOCID_BASE+1422),

    # Area 5 - 7 locs
    "A5 Corridor 5 (X23 Y4)":         TGLLocationData("Area 5",  "Corridor",  TGL_LOCID_BASE+3005, (0x9, 0x10)),
    "A5 Corridor 5 Bonus":            TGLLocationData("Area 5",  "Corridor",  TGL_LOCID_BASE+4005),
    "A5 Corridor 15 (X21 Y8)":        TGLLocationData("Area 5",  "Corridor",  TGL_LOCID_BASE+3015, (0xA, 0x40)),
    "A5 Corridor 15 Bonus":           TGLLocationData("Area 5",  "Corridor",  TGL_LOCID_BASE+4015),
    "A5 Crab Walker (X19 Y8)":        TGLLocationData("Area 5",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x15, (0x2, 0x20)),
    "A5 Crystal Chaser (X21 Y4)":     TGLLocationData("Area 5",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x16, (0x2, 0x40)),
    "A5 (X23 Y8)":                    TGLLocationData("Area 5",  "Ground",    TGL_LOCID_GROUND_BASE+0x01, (0x0, 0x2 )),
    "A5 (X23 Y6)":                    TGLLocationData("Area 5",  "Ground",    TGL_LOCID_GROUND_BASE+0x2b, (0x5, 0x8 )),
    "A5 (X23 Y3)":                    TGLLocationData("Area 5",  "Ground",    TGL_LOCID_GROUND_BASE+0x2c, (0x5, 0x10)),

    # Area 6 - 8 locs
    "A6 Corridor 6 (X16 Y11)":        TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_BASE+3006, (0x9, 0x20)),
    "A6 Corridor 6 Bonus":            TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_BASE+4006),
    #"Corridor 6 Glider (X16 Y11)":    TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_BASE+1602),
    "A6 Corridor 16 (X18 Y13)":       TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_BASE+3016, (0xA, 0x80)),
    "A6 Corridor 16 Bonus":           TGLLocationData("Area 6",  "Corridor",  TGL_LOCID_BASE+4016),
    "A6 Headcrawler (X18 Y10)":       TGLLocationData("Area 6",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x17, (0x2, 0x80)),
    "A6 Claw Launcher (X17 Y16)":     TGLLocationData("Area 6",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x18, (0x3, 0x1 )),
    "A6 (X18 Y12)":                   TGLLocationData("Area 6",  "Ground",    TGL_LOCID_GROUND_BASE+0x2d, (0x5, 0x20)),
    "A6 (X20 Y10)":                   TGLLocationData("Area 6",  "Ground",    TGL_LOCID_GROUND_BASE+0x2e, (0x5, 0x40)),
    "A6 (X21 Y13)":                   TGLLocationData("Area 6",  "Ground",    TGL_LOCID_GROUND_BASE+0x02, (0x0, 0x4 )),
    "A6 (X16 Y12)":                   TGLLocationData("Area 6",  "Ground",    TGL_LOCID_GROUND_BASE+0x0a, (0x1, 0x4 )),

    # Area 7 - 9 locs
    "A7 Corridor 7 (X19 Y23)":        TGLLocationData("Area 7",  "Corridor",  TGL_LOCID_BASE+3007, (0x9, 0x40)),
    "A7 Corridor 7 Bonus":            TGLLocationData("Area 7",  "Corridor",  TGL_LOCID_BASE+4007),
    "A7 Corridor 17 (X18 Y19)":       TGLLocationData("Area 7",  "Corridor",  TGL_LOCID_BASE+3017, (0xB, 0x1 )),
    "A7 Corridor 17 Bonus":           TGLLocationData("Area 7",  "Corridor",  TGL_LOCID_BASE+4017),
    "A7 Headcrawler (X16 Y18)":       TGLLocationData("Area 7",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x19, (0x3, 0x2 )),
    "A7 Claw Launcher (X22 Y20)":     TGLLocationData("Area 7",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x1a, (0x3, 0x4 )),
    "A7 (X17 Y23)":                   TGLLocationData("Area 7",  "Ground",    TGL_LOCID_GROUND_BASE+0x03, (0x0, 0x8 )),
    "A7 (X22 Y23)":                   TGLLocationData("Area 7",  "Ground",    TGL_LOCID_GROUND_BASE+0x30, (0x6, 0x1 )),
    "A7 (X19 Y19)":                   TGLLocationData("Area 7",  "Ground",    TGL_LOCID_GROUND_BASE+0x2f, (0x5, 0x80)),
    "A7 1000 Chip Shop A (X23 Y21)":  TGLLocationData("Area 7",  "Shop",      TGL_LOCID_BASE+2107, (0x8, 0x1 )),
    #"A7 1000 Chip Shop B (X23 Y21)":  TGLLocationData("Area 7",  "Shop",      TGL_LOCID_BASE+1722),
    "A7 600 Chip Shop A (X15 Y12)":   TGLLocationData("Area 7",  "Shop",      TGL_LOCID_BASE+2117, (0x8, 0x4 )),
    #"A7 600 Chip Shop B (X15 Y12)":   TGLLocationData("Area 7",  "Shop",      TGL_LOCID_BASE+1724),

    # Area 8 - 8 locs
    "A8 Corridor 8 (X10 Y16)":        TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_BASE+3008, (0x9, 0x80)),
    "A8 Corridor 8 Bonus":            TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_BASE+4008),
    #"Corridor 8 Grimgrin (X10 Y16)":  TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_BASE+1802),
    "A8 Corridor 18 (X11 Y19)":       TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_BASE+3018, (0xB, 0x2 )),
    "A8 Corridor 18 Bonus":           TGLLocationData("Area 8",  "Corridor",  TGL_LOCID_BASE+4018),
    "A8 Leech Flower (X12 Y18)":      TGLLocationData("Area 8",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x1b, (0x3, 0x8 )),
    "A8 Crab Walker (X12 Y22)":       TGLLocationData("Area 8",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x1c, (0x3, 0x10)),
    "A8 (X10 Y18)":                   TGLLocationData("Area 8",  "Ground",    TGL_LOCID_GROUND_BASE+0x31, (0x6, 0x2 )),
    "A8 (X14 Y20)":                   TGLLocationData("Area 8",  "Ground",    TGL_LOCID_GROUND_BASE+0x32, (0x6, 0x4 )),
    "A8 (X12 Y23)":                   TGLLocationData("Area 8",  "Ground",    TGL_LOCID_GROUND_BASE+0x04, (0x0, 0x10)),
    "A8 (X9 Y19)":                    TGLLocationData("Area 8",  "Ground",    TGL_LOCID_GROUND_BASE+0x38, (0x7, 0x1 )),

    # Area 9 - 9 locs
    "A9 Corridor 9 (X2 Y2)":          TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_BASE+3009, (0xA, 0x1 )),
    "A9 Corridor 9 Bonus":            TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_BASE+4009),
    #"Corridor 9 Eyegore (X2 Y2)":     TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_BASE+1902),
    "A9 Corridor 19 (X4 Y4)":         TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_BASE+3019, (0xB, 0x4 )),
    "A9 Corridor 19 Bonus":           TGLLocationData("Area 9",  "Corridor",  TGL_LOCID_BASE+4019),
    "A9 Crab Walker (X5 Y3)":         TGLLocationData("Area 9",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x1d, (0x3, 0x20)),
    "A9 Headcrawler (X2 Y0)":         TGLLocationData("Area 9",  "Miniboss",  TGL_LOCID_GROUND_BASE+0x1e, (0x3, 0x40)),
    "A9 (X3 Y6)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND_BASE+0x33, (0x6, 0x8 )),
    "A9 (X3 Y3)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND_BASE+0x34, (0x6, 0x10)),
    "A9 (X6 Y3)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND_BASE+0x06, (0x0, 0x40)),
    "A9 (X0 Y3)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND_BASE+0x07, (0x0, 0x80)),
    "A9 (X1 Y0)":                     TGLLocationData("Area 9",  "Ground",    TGL_LOCID_GROUND_BASE+0x08, (0x1, 0x1 )),

    # Area 10 - 6 locs
    "A10 Corridor 10 (X11 Y0)":        TGLLocationData("Area 10", "Corridor",  TGL_LOCID_BASE+3010, (0xA, 0x2 )),
    "A10 Corridor 10 Bonus":           TGLLocationData("Area 10", "Corridor",  TGL_LOCID_BASE+4010),
    "A10 Corridor 20 (X11 Y5)":        TGLLocationData("Area 10", "Corridor",  TGL_LOCID_BASE+3020, (0xB, 0x8 )),
    "A10 Corridor 20 Bonus":           TGLLocationData("Area 10", "Corridor",  TGL_LOCID_BASE+4020),
    "A10 Dino Skull (X11 Y3)":         TGLLocationData("Area 10", "Miniboss",  TGL_LOCID_GROUND_BASE+0x1f, (0x3, 0x80)),
    "A10 Glider (X12 Y0)":             TGLLocationData("Area 10", "Miniboss",  TGL_LOCID_GROUND_BASE+0x20, (0x4, 0x1 )),
    "A10 (X12 Y4)":                    TGLLocationData("Area 10", "Ground",    TGL_LOCID_GROUND_BASE+0x09, (0x1, 0x2 )),
    "A10 2000 Chip Shop A (X12 Y5)":   TGLLocationData("Area 10", "Shop",      TGL_LOCID_BASE+2122, (0x8, 0x8 )),
    #"A10 2000 Chip Shop B (X12 Y5)":   TGLLocationData("Area 10", "Shop",      TGL_LOCID_BASE+2022),
    
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