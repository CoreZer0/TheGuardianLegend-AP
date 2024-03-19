from typing import Dict

from . import TGLTestBase

from worlds.guardianlegend.Locations import TGLLocationData, location_table, get_locations_by_areanum

# Test that each location per Area has the correct Key lock
class TestAreaKeyAccess(TGLTestBase):
        def test_keys(self) -> None:
                # Going to hard code this for now, but should eventually have a helper list somewhere
                area_key_table: Dict[str, str] = {
                        "Area 1":  "Crescent Key",
                        "Area 2":  "Crescent Key",
                        "Area 3":  "Hook Key",
                        "Area 4":  "Wave Key",
                        "Area 5":  "Square Key",
                        "Area 6":  "Square Key",
                        "Area 7":  "Cross Key",
                        "Area 8":  "Cross Key",
                        "Area 9":  "Triangle Key",
                        "Area 10": "Rectangle Key",
                }

                for areaname in area_key_table.keys():
                        location_list = []
                        for location_name in get_locations_by_areanum(areaname).keys():
                                location_list.append(location_name)
                        key_list = [[area_key_table[areaname]]]
                        self.assertAccessDependency(location_list, key_list, True)