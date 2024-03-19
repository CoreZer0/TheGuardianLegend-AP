from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import TGLLocation, location_table, get_locations_by_category, get_locations_by_areanum

class TGLRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    regions: Dict[str, TGLRegionData] = {
        "Menu":        TGLRegionData(None, ["Area 0"]),
        "Area 0":      TGLRegionData([], ["Area 1","Area 2","Area 3","Area 4","Area 5","Area 6","Area 7",
                                          "Area 8","Area 9","Area 10","Corridor 21"]),
        "Area 1":      TGLRegionData([], []),
        "Area 2":      TGLRegionData([], []),
        "Area 3":      TGLRegionData([], []),
        "Area 4":      TGLRegionData([], []),
        "Area 5":      TGLRegionData([], []),
        "Area 6":      TGLRegionData([], []),
        "Area 7":      TGLRegionData([], []),
        "Area 8":      TGLRegionData([], []),
        "Area 9":      TGLRegionData([], []),
        "Area 10":     TGLRegionData([], []),
        "Corridor 21": TGLRegionData([], None),
    }

    # Fill regions by Area number
    for areanum in range (0,11):
        areaname = "Area " + str(areanum)
        for locname in get_locations_by_areanum(areaname).keys():
            regions[areaname].locations.append(locname)

    # Victory location is in its own region
    regions["Corridor 21"].locations.append("Corridor 21")

    # Set up regions
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

    multiworld.get_entrance("Area 0", player).connect(multiworld.get_region("Area 0", player))
    multiworld.get_entrance("Area 1", player).connect(multiworld.get_region("Area 1", player))
    multiworld.get_entrance("Area 2", player).connect(multiworld.get_region("Area 2", player))
    multiworld.get_entrance("Area 3", player).connect(multiworld.get_region("Area 3", player))
    multiworld.get_entrance("Area 4", player).connect(multiworld.get_region("Area 4", player))
    multiworld.get_entrance("Area 5", player).connect(multiworld.get_region("Area 5", player))
    multiworld.get_entrance("Area 6", player).connect(multiworld.get_region("Area 6", player))
    multiworld.get_entrance("Area 7", player).connect(multiworld.get_region("Area 7", player))
    multiworld.get_entrance("Area 8", player).connect(multiworld.get_region("Area 8", player))
    multiworld.get_entrance("Area 9", player).connect(multiworld.get_region("Area 9", player))
    multiworld.get_entrance("Area 10", player).connect(multiworld.get_region("Area 10", player))
    multiworld.get_entrance("Corridor 21", player).connect(multiworld.get_region("Corridor 21", player))

def create_region(multiworld: MultiWorld, player: int, name: str, data: TGLRegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = TGLLocation(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region