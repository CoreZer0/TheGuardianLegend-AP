from typing import TYPE_CHECKING, List, Tuple
from copy import deepcopy

from enum import IntFlag, IntEnum

if TYPE_CHECKING:
    from . import TGLWorld


area_template = [
    [ 1, 1, 1, 1,-1, 2, 2, 2, 2, 2, 2, 2,-1, 3, 3, 3, 3, 3, 3,-1, 4, 4, 4, 4],
    [ 1, 1, 1, 1,-1, 2, 2, 2, 2, 2, 2, 2,-1, 3, 3, 3, 3, 3, 3,-1, 4, 4, 4, 4],
    [ 1, 1, 1, 1,-1, 2, 2, 2, 2, 2, 2, 2,-1, 3, 3, 3, 3, 3, 3,-1, 4, 4, 4, 4],
    [ 1, 1, 1, 1,-1,-1,-1, 2, 2, 2, 2, 2,-1, 3, 3, 3, 3,-1,-1,-1, 4, 4, 4, 4],
    [ 1, 1, 1, 1, 1, 1,-1, 2, 2, 2, 2,-1,-1, 3, 3, 3, 3,-1, 4, 4, 4, 4, 4, 4],
    [ 1, 1, 1, 1, 1, 1,-1, 2, 2, 2, 2,-1, 3, 3, 3, 3, 3,-1, 4, 4, 4, 4, 4, 4],
    [ 1, 1, 1, 1, 1, 1,-1,-1,-1,-1, 2,-1, 3, 3,-1,-1,-1,-1, 4, 4, 4, 4, 4, 4],
    [-1,-1,-1,-1, 1, 1, 1, 1, 1,-1, 2,-1, 3, 3,-1, 4, 4, 4, 4, 4,-1,-1,-1,-1],
    [ 5, 5, 5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 6, 6, 6],
    [ 5, 5, 5, 5, 5, 5, 5,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1, 6, 6, 6, 6, 6, 6, 6],
    [ 5, 5, 5, 5, 5, 5, 5,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1, 6, 6, 6, 6, 6, 6, 6],
    [ 5, 5, 5, 5, 5, 5, 5,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1, 6, 6, 6, 6, 6, 6, 6],
    [ 5, 5, 5, 5, 5, 5, 5,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1, 6, 6, 6, 6, 6, 6, 6],
    [ 5, 5, 5, 5, 5, 5, 5,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1, 6, 6, 6, 6, 6, 6, 6],
    [ 5, 5, 5, 5, 5, 5, 5,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1, 6, 6, 6, 6, 6, 6, 6],
    [ 5, 5, 5,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 6, 6, 6],
    [-1,-1,-1,-1, 7, 7, 7, 7, 7,-1, 8,-1, 9, 9,-1,10,10,10,10,10,-1,-1,-1,-1],
    [ 7, 7, 7, 7, 7, 7,-1,-1,-1,-1, 8,-1, 9, 9,-1,-1,-1,-1,10,10,10,10,10,10],
    [ 7, 7, 7, 7, 7, 7,-1, 8, 8, 8, 8,-1, 9, 9, 9, 9, 9,-1,10,10,10,10,10,10],
    [ 7, 7, 7, 7, 7, 7,-1, 8, 8, 8, 8,-1, 9, 9, 9, 9, 9,-1,10,10,10,10,10,10],
    [ 7, 7, 7, 7,-1,-1,-1, 8, 8, 8, 8,-1,-1, 9, 9, 9, 9,-1,-1,-1,10,10,10,10],
    [ 7, 7, 7, 7,-1, 8, 8, 8, 8, 8, 8, 8,-1, 9, 9, 9, 9, 9, 9,-1,10,10,10,10],
    [ 7, 7, 7, 7,-1, 8, 8, 8, 8, 8, 8, 8,-1, 9, 9, 9, 9, 9, 9,-1,10,10,10,10],
    [ 7, 7, 7, 7,-1, 8, 8, 8, 8, 8, 8, 8,-1, 9, 9, 9, 9, 9, 9,-1,10,10,10,10],
]


room_blocksets = {
    "no_chips_no_transition": [0x6894,0x3D94,0x4694,0x5094,0x8794,0x3F94,0x8C94,0x5D94,0x5294,0xE394,0xDD94,0xDF94,
                               0xD994,0xD194,0xD794,0xD594],
    "with_chips_no_transition":       [0x6F94,0x4194,0x9D94],
    "no_chips_area_transition_up":    [0x1C95],
    "no_chips_area_transition_down":  [0x3C95,0x4995],
    "no_chips_area_transition_left":  [0xE994,0xF394,0xEB94],
    "no_chips_area_transition_right": [0x0895],
    "with_chips_area_transition_up":    [0x1795,0x2995,0x2495],
    "with_chips_area_transition_down":  [0x4495,0x3795],
    "with_chips_area_transition_left":  [0xFB94],
    "with_chips_area_transition_right": [0x0395,0x0D95],
    "corridor_transition_up":    [0x7A95,0x8595],
    "corridor_transition_down":  [0x9095,0x9B95],
    "corridor_transition_left":  [0x4E95,0x5995],
    "corridor_transition_right": [0x6495,0x6F95]
}

item_locations = [
    [0x21,0x05,0x39,0x35],
    [0x24,0x23,0x26],
    [0x36,0x25],
    [0x28,0x27],
    [0x29,0x2A,0x37],
    [0x01,0x2B,0x2C],
    [0x0A,0x2D,0x2E,0x02],
    [0x03,0x2F,0x30],
    [0x31,0x38,0x04,0x32],
    [0x06,0x33,0x34,0x08,0x07],
    [0x09]
]
    

class TGLRoomType(IntEnum):
    NORMAL = 0
    SAVE = 1
    CORRIDOR = 2
    TEXT = 3
    MULTISHOP = 4
    SINGLESHOP = 5
    MINIBOSS = 6
    ITEM = 7


class TGLRoomExits(IntFlag):
    NONE  = 0b0000  # Should be invalid
    DOWN  = 0b0001
    RIGHT = 0b0010
    LEFT  = 0b0100
    UP    = 0b1000


class TGLRoom:
    """Holds the various flags to determine room type and structure that will be used to generate the ROM code 
    for the map structure."""
    area: int  # In-game area, between 0 and 10, -1 and -2 are special flags
    is_accessible: bool
    is_startingpoint: bool  # If this room is a connection to Area 0
    exits: TGLRoomExits  # Bitflag, order (little-endian) Down Right Left Up (DRLU)
    avoid_special: bool
    room_type: TGLRoomType
    block_set: int  # For item rooms and normal rooms with blocks
    chip_tile: bool  # Are there chip boxes?
    content_id: int  # Item / Miniboss / Shop / Text id
    enemy_type: int  # 0 is no enemies, 1-47 represent enemy groups

    def __init__(self):
        self.is_accessible = False
        self.is_startingpoint = False
        self.exits = TGLRoomExits.NONE
        self.avoid_special = False
        self.room_type = TGLRoomType.NORMAL
        self.block_set = -1
        self.chip_tile = False
        self.enemy_type = 0

    def count_bytes(self) -> int:
        if not self.is_accessible:
            return 1
        elif (self.room_type == TGLRoomType.SAVE) or (self.room_type == TGLRoomType.CORRIDOR):
            return 3
        elif ((self.room_type == TGLRoomType.TEXT) 
              or (self.room_type == TGLRoomType.MULTISHOP)
              or (self.room_type == TGLRoomType.SINGLESHOP)
              or (self.room_type == TGLRoomType.MINIBOSS)):
            return 4
        else:
            bytecount = 3
            if (self.room_type == TGLRoomType.ITEM):
                bytecount += 1
            if self.block_set > 0:
                bytecount += 2
            if self.enemy_type != 0:
                bytecount += 1
            return bytecount
    
    def print_room(self):
        print("Room Data START:")
        if self.is_accessible:
            print("Accessible")
        else:
            print("Inaccessible")
        print("Area: " + str(self.area))
        print("Room Type: " + str(self.room_type))
        if self.is_startingpoint:
            print("Area starting point")
        if self.avoid_special:
            print("Avoid Special")
        if self.chip_tile:
            print("Has chips")
        if hasattr(self, "content_id"):
            print("Content ID: " + str(self.content_id))
        print("Block set: " + str(self.block_set))
        print("Enemy type: " + str(self.enemy_type))
        exits = ""
        if self.exits & TGLRoomExits.UP:
            exits += "U"
        if self.exits & TGLRoomExits.DOWN:
            exits += "D"
        if self.exits & TGLRoomExits.LEFT:
            exits += "L"
        if self.exits & TGLRoomExits.RIGHT:
            exits += "R"
        print("Room exits: " + exits + " " + str(bin(self.exits)))
        print("Room Data END")
        print("")

class TGLMap:
    """Contains a List of Lists of Rooms representing the map data for the TGL ROM.
    The Map in ROM is represented as a continuous string, starting at X0 Y0 and proceeding row by row to X23 Y23."""
    areakeys_other: List = [0,1,1,2,3,4,4,5,5,6,7]  # used in room data to determine which panel locks exist
    areakeys_mostrooms: List = [8,9,9,10,11,12,12,13,13,14,15] # "KeyForAreaForRoomsThatCouldHaveEnemiesButDont"

    def __init__(self):
        self.mapdata: List[List[TGLRoom]] = [[TGLRoom() for _ in range(24)] for _ in range(24)]

    def writehex(self) -> bytearray:
        outbytes = bytearray()
        for ycoord in self.mapdata:
            for xcoord in ycoord:
                if xcoord.is_accessible:
                    # Each room has a unique string length and values based on contents
                    # Most rooms are constructed from nybbles of data, represented in comments by (x + y)
                    if xcoord.area < 0:
                        # No room in Area -1 should be accessible. Print it and fail
                        xcoord.print_room()
                        raise Exception("TGL Map Rando: Accessible room with Area < 0 generated.") 
                    exits_shift = xcoord.exits << 4
                    if xcoord.room_type == TGLRoomType.NORMAL:
                        # (roomtype + length) + (exits + roomkey) + (0 + area) + (enemy) + (blocks)
                        roomlength = 2
                        roomkey = self.areakeys_other[xcoord.area]
                        roomtype = 0
                        if xcoord.enemy_type != 0:
                            roomkey = self.areakeys_mostrooms[xcoord.area]
                            roomlength += 1
                        if xcoord.block_set >= 0:
                            roomlength += 2
                            if xcoord.chip_tile:
                                roomtype = 7 << 4
                            else:
                                roomtype = 1 << 4
                        outbytes.append(roomtype + roomlength)
                        outbytes.append(exits_shift + roomkey)
                        outbytes.append(xcoord.area)
                        if xcoord.enemy_type != 0:
                            outbytes.append(xcoord.enemy_type)
                        if xcoord.block_set > 0:
                            # Block sets are 2 bytes
                            block_bytes = xcoord.block_set.to_bytes(2, "big")
                            outbytes.append(block_bytes[0])
                            outbytes.append(block_bytes[1])
                    elif xcoord.room_type == TGLRoomType.SAVE:
                        # (82) + (exits + roomkey) + (01)
                        outbytes.append(0x82)
                        outbytes.append(exits_shift + self.areakeys_mostrooms[xcoord.area])
                        outbytes.append(0x01)
                    elif xcoord.room_type == TGLRoomType.CORRIDOR:
                        # (82) + (exits + roomkey) + (corridor)
                        roomkey = self.areakeys_mostrooms[xcoord.area]
                        if xcoord.content_id == 1:
                            roomkey = 0
                        outbytes.append(0x82)
                        outbytes.append(exits_shift + roomkey)
                        outbytes.append(0x80 + xcoord.content_id)
                    elif xcoord.room_type == TGLRoomType.TEXT:
                        # (A3) + (exits + roomkey) + (03) + (textid)
                        outbytes.append(0xA3)
                        outbytes.append(exits_shift + self.areakeys_other[xcoord.area])
                        outbytes.append(0x03)
                        outbytes.append(xcoord.content_id)
                    elif xcoord.room_type == TGLRoomType.MULTISHOP:
                        # (A3) + (exits + roomkey) + (02) + (shopid)
                        outbytes.append(0xA3)
                        outbytes.append(exits_shift + self.areakeys_other[xcoord.area])
                        outbytes.append(0x02)
                        outbytes.append(xcoord.content_id)
                    elif xcoord.room_type == TGLRoomType.SINGLESHOP:
                        # (A3) + (exits + roomkey) + (06) + (shopid)
                        outbytes.append(0xA3)
                        outbytes.append(exits_shift + self.areakeys_other[xcoord.area])
                        outbytes.append(0x06)
                        outbytes.append(xcoord.content_id)
                    elif xcoord.room_type == TGLRoomType.MINIBOSS:
                        # (43) + (exits + roomkey) + (1 + area) + (contents)
                        outbytes.append(0x43)
                        outbytes.append(exits_shift + self.areakeys_mostrooms[xcoord.area])
                        outbytes.append(0x10 + xcoord.area)
                        outbytes.append(xcoord.content_id)
                    elif xcoord.room_type == TGLRoomType.ITEM:
                        # (3 + length) + (exits + roomkey) + (0 + area) + (contents) + (enemy) + (blocks)
                        roomkey = self.areakeys_other[xcoord.area]
                        roomlength = 5
                        if xcoord.enemy_type != 0:
                            roomkey = self.areakeys_mostrooms[xcoord.area]
                            roomlength += 1
                        outbytes.append(0x30 + roomlength)
                        outbytes.append(exits_shift + roomkey)
                        outbytes.append(xcoord.area)
                        outbytes.append(xcoord.content_id)
                        if xcoord.enemy_type != 0:
                            outbytes.append(xcoord.enemy_type)
                        # Block sets are 2 bytes
                        block_bytes = xcoord.block_set.to_bytes(2, "big")
                        outbytes.append(block_bytes[0])
                        outbytes.append(block_bytes[1])
                    else:
                        # Something went wrong...
                        raise Exception("TGL Map Rando: writehex() failed, Invalid Room Type found.")
                else:
                    # Inaccessible rooms in array are noted with 0x80 single byte
                    outbytes.append(0x80)
        outbytes.append(0x0) # End the room data table with a null terminator 
        return outbytes
    
    def print_maps(self):
        print(" List of Areas START:")
        for ycoord in self.mapdata:
            row: str = ""
            for xcoord in ycoord:
                if (xcoord.area < 0):
                    row += "X "
                elif (xcoord.area == 10):
                    row += "A "
                else:
                    row += str(xcoord.area) + " "
            print(row)
        print(" List of Areas END")
        print("")
        print("In-game (accessibility) map START:")
        for ycoord in self.mapdata:
            row: str = ""
            for xcoord in ycoord:
                if xcoord.is_accessible:
                    row += "O "
                else:
                    row += "X "
            print(row)
        print("In-game (accessibility) map END")
        print("")
        print("Visual map START:")
        for ycoord in self.mapdata:
            for i in range(3):
                row = ""
                for xcoord in ycoord:
                    if i == 0:
                        row += "╔═"
                        if (xcoord.exits & TGLRoomExits.UP):
                            row += "░░"
                        else: 
                            row += "══"
                        row += "═╗"
                    if i == 1:
                        if (xcoord.exits & TGLRoomExits.LEFT):
                            row += "░░"
                        else:
                            row += "║║"
                        if xcoord.is_accessible:
                            if xcoord.room_type == 1:
                                row += "SV"
                            elif xcoord.room_type == 2:
                                if xcoord.content_id < 10:
                                    row += "X" + str(xcoord.content_id)
                                elif xcoord.content_id == 10:
                                    row += "XA"
                                elif xcoord.content_id == 20:
                                    row += "xA"
                                elif xcoord.content_id == 21:
                                    row += "XF"
                                else:
                                    row += "x" + str(xcoord.content_id - 10)
                            elif xcoord.room_type == 3:
                                row += "TX"
                            elif xcoord.room_type == 4:
                                row += "S" + str(xcoord.content_id - 0x3F)
                            elif xcoord.room_type == 5:
                                row += "s" + str(xcoord.content_id - 0x3A)
                            elif (xcoord.room_type == 6) or (xcoord.room_type == 7):
                                if xcoord.content_id < 10:
                                    row += "0" + str(xcoord.content_id)
                                else:
                                    row += str(xcoord.content_id)
                            else:
                                row += "░░"
                        else:
                            row += "╬╬"
                        if (xcoord.exits & TGLRoomExits.RIGHT):
                            row += "░░"
                        else:
                            row += "║║"
                    if i == 2:
                        row += "╚═"
                        if (xcoord.exits & TGLRoomExits.DOWN):
                            row += "░░"
                        else: row += "══"
                        row += "═╝"
                print(row)        
        print("Visual map END")
        print("")

    
    # This is the core function to DO ALL THE THINGS to the map, proceed through helper functions to randomize map
    def randomizeMap(self, world: "TGLWorld"):
        # Subdivide the map into areas from A0, and shuffle them
        choose_flip: bool = world.random.choice([True, False])
        choose_rotation: int = world.random.randint(0,3)
        areas = list(range(1,11))
        world.random.shuffle(areas)
        self.__shuffle_areas(choose_flip, choose_rotation, areas)

        # Need to place cardinal direction rooms before starting points to not break calculations (from Fireball)
        self.__grow_area_zero()
        self.__place_cardinal_points()
        self.__find_starting_points(world)

        # Fill in each area
        for area in areas:
            areasize = world.random.randint(18,25)
            self.__grow_area(world, area, areasize)
            self.__add_connections(world, area, 3, False, False)
            self.__add_connections(world, area, 0, True, False)

        # Fill in A0
        self.__grow_area(world, 0, 50)
        self.__add_connections(world, 0, 6, False, False)
        self.__add_connections(world, 0, 0, True, False)

        # Fill in non-item stuff
        self.__place_starting_points()
        self.__place_area_decorations(world)

        # Starting room (and connecting rooms)
        self.__place_starting_text_room()

        for area in range(11):
            self.__place_important_rooms(world, area)
            self.__place_item_locations(world, area)
            self.__place_safe_rooms(world, area)

        self.__place_corridor_decorations(world)
        self.__place_random_decorations(world)

        self.__populate_enemies(world)
        mapsize: int = self.__count_bytes()
        print("Map Size: " + str(mapsize))
        if mapsize > 1916:
            raise Exception("TGL Map Rando: Map size in Bytes is too large to fit in ROM.")

    def __count_bytes(self) -> int:
        bytecount: int = 0
        for ycoord in self.mapdata:
            for xcoord in ycoord:
                bytecount += xcoord.count_bytes()
        return bytecount

    def __shuffle_areas(self, flip: bool, rotate: int, shuffled_areas: List[int]):
        # Optionally flip and rotate vanilla map layout, then shuffle area numbers
        division: List[List[int]] = deepcopy(area_template)
        
        if flip:
            # Flip the map across Y-axis (mirrored)
            for ycoord in division:
                ycoord.reverse()
        rotation = 0
        while rotation < rotate:
            # Rotate map counter-clockwise up to 3 times
            # https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
            division = list(reversed(list(zip(*division))))
            rotation += 1
        ykey = 0
        for ycoord in self.mapdata:
            xkey = 0
            for xcoord in ycoord:
                # For all areas except 0 (and -1), set the areanum to a shuffled number
                if division[ykey][xkey] > 0:
                    xcoord.area = shuffled_areas[division[ykey][xkey] - 1]
                else:
                    xcoord.area = division[ykey][xkey]
                xkey += 1
            ykey += 1

    def __find_starting_points(self, world: "TGLWorld"):
        possible_entrances = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10:[]
        }
        ykey = 0
        for ycoord in self.mapdata:
            xkey = 0
            for xcoord in ycoord:
                if xcoord.area == -1:
                    up_block = None
                    down_block = None
                    left_block = None
                    right_block = None
                    if ykey > 0:
                        up_block = self.mapdata[ykey-1][xkey]
                    if ykey < 23:
                        down_block = self.mapdata[ykey+1][xkey]
                    if xkey > 0:
                        left_block = self.mapdata[ykey][xkey-1]
                    if xkey < 23:
                        right_block = self.mapdata[ykey][xkey+1]

                    # Check each neighboring block to a border. If it connects Area 0 to a different Area, 
                    # add it to the possible entry points for the Area 
                    if up_block is not None:
                        if up_block.area == 0:
                            if down_block is not None:
                                if down_block.area > 0:
                                    possible_entrances[down_block.area].append((ykey,xkey,TGLRoomExits.UP))
                    if down_block is not None:
                        if down_block.area == 0:
                            if up_block is not None:
                                if up_block.area > 0:
                                    possible_entrances[up_block.area].append((ykey,xkey,TGLRoomExits.DOWN))
                    if left_block is not None:
                        if left_block.area == 0:
                            if right_block is not None:
                                if right_block.area > 0:
                                    possible_entrances[right_block.area].append((ykey,xkey,TGLRoomExits.LEFT))
                    if right_block is not None:
                        if right_block.area == 0:
                            if left_block is not None:
                                if left_block.area > 0:
                                    possible_entrances[left_block.area].append((ykey,xkey,TGLRoomExits.RIGHT))
                xkey += 1
            ykey += 1                    

        for areanum in possible_entrances:
            if not possible_entrances[areanum]:
                # This is an error, we generated a map with no possible entry points to an area
                raise Exception(f"TGL Map Rando: No valid entrance point for Area {areanum}.")
            else:
                entrance: Tuple = world.random.choice(possible_entrances[areanum])
                thisroom: TGLRoom = self.mapdata[entrance[0]][entrance[1]]

                thisroom.area = 0
                thisroom.is_startingpoint = True
                thisroom.is_accessible = True
                ykey: int = entrance[0]
                xkey: int = entrance[1]

                # Set the neighboring rooms correctly to act as area connectors
                if entrance[2] == TGLRoomExits.DOWN:
                    thisroom.exits |= TGLRoomExits.DOWN
                    thisroom.exits |= TGLRoomExits.UP
                    self.mapdata[ykey-1][xkey].exits |= TGLRoomExits.DOWN
                    self.mapdata[ykey-1][xkey].is_startingpoint = True
                    self.mapdata[ykey-1][xkey].is_accessible = True
                    self.mapdata[ykey+1][xkey].exits |= TGLRoomExits.UP
                    self.mapdata[ykey+1][xkey].is_accessible = True
                if entrance[2] == TGLRoomExits.UP:
                    thisroom.exits |= TGLRoomExits.DOWN
                    thisroom.exits |= TGLRoomExits.UP
                    self.mapdata[ykey+1][xkey].exits |= TGLRoomExits.UP
                    self.mapdata[ykey+1][xkey].is_startingpoint = True
                    self.mapdata[ykey+1][xkey].is_accessible = True
                    self.mapdata[ykey-1][xkey].exits |= TGLRoomExits.DOWN
                    self.mapdata[ykey-1][xkey].is_accessible = True
                if entrance[2] == TGLRoomExits.RIGHT:
                    thisroom.exits |= TGLRoomExits.RIGHT
                    thisroom.exits |= TGLRoomExits.LEFT
                    self.mapdata[ykey][xkey-1].exits |= TGLRoomExits.RIGHT
                    self.mapdata[ykey][xkey-1].is_startingpoint = True
                    self.mapdata[ykey][xkey-1].is_accessible = True
                    self.mapdata[ykey][xkey+1].exits |= TGLRoomExits.LEFT
                    self.mapdata[ykey][xkey+1].is_accessible = True
                if entrance[2] == TGLRoomExits.LEFT:
                    thisroom.exits |= TGLRoomExits.RIGHT
                    thisroom.exits |= TGLRoomExits.LEFT
                    self.mapdata[ykey][xkey+1].exits |= TGLRoomExits.LEFT
                    self.mapdata[ykey][xkey+1].is_startingpoint = True
                    self.mapdata[ykey][xkey+1].is_accessible = True
                    self.mapdata[ykey][xkey-1].exits |= TGLRoomExits.RIGHT
                    self.mapdata[ykey][xkey-1].is_accessible = True


    def __grow_area(self, world: "TGLWorld", area: int, total_size: int):
        grow_points = []
        ykey = 0
        size_grown = 0
        for ycoord in self.mapdata:
            xkey = 0
            for xcoord in ycoord:
                if (xcoord.area == area) and (xcoord.is_accessible == True):
                    new_point = (ykey,xkey)
                    grow_points.append(new_point)
                xkey += 1
            ykey += 1
        while (total_size > size_grown) and (len(grow_points) > 0):
            # Choose a random existing room, attempt to grow
            # Choose a random order of directions to grow and attempt in sequence
            # Stop when a grow point is reached
            # If growth fails, remove the point from the list
            choose_point = world.random.choice(grow_points)
            ykey: int = choose_point[0]
            xkey: int = choose_point[1]
            sequence = world.random.sample(range(4), 4)
            grow_success = False
            for i in sequence:
                if not grow_success:
                    direction = 1 << i
                    if (direction == TGLRoomExits.UP) and (ykey > 0):
                        nextroom = self.mapdata[ykey - 1][xkey]
                        if (nextroom.area == area) and (nextroom.is_accessible == False):
                            self.mapdata[ykey][xkey].exits |= TGLRoomExits.UP
                            nextroom.exits |= TGLRoomExits.DOWN
                            nextroom.is_accessible = True
                            new_point = (ykey - 1, xkey)
                            grow_points.append(new_point)
                            grow_success = True
                    if (direction == TGLRoomExits.LEFT) and (xkey > 0):
                        nextroom = self.mapdata[ykey][xkey - 1]
                        if (nextroom.area == area) and (nextroom.is_accessible == False):
                            self.mapdata[ykey][xkey].exits |= TGLRoomExits.LEFT
                            nextroom.exits |= TGLRoomExits.RIGHT
                            nextroom.is_accessible = True
                            new_point = (ykey, xkey - 1)
                            grow_points.append(new_point)
                            grow_success = True
                    if (direction == TGLRoomExits.RIGHT) and (xkey < 23):
                        nextroom = self.mapdata[ykey][xkey + 1]
                        if (nextroom.area == area) and (nextroom.is_accessible == False):
                            self.mapdata[ykey][xkey].exits |= TGLRoomExits.RIGHT
                            nextroom.exits |= TGLRoomExits.LEFT
                            nextroom.is_accessible = True
                            new_point = (ykey, xkey + 1)
                            grow_points.append(new_point)
                            grow_success = True
                    if (direction == TGLRoomExits.DOWN) and (ykey < 23):
                        nextroom = self.mapdata[ykey + 1][xkey]
                        if (nextroom.area == area) and (nextroom.is_accessible == False):
                            self.mapdata[ykey][xkey].exits |= TGLRoomExits.DOWN
                            nextroom.exits |= TGLRoomExits.UP
                            nextroom.is_accessible = True
                            new_point = (ykey + 1, xkey)
                            grow_points.append(new_point)
                            grow_success = True
            if grow_success:
                size_grown += 1
            else:
                grow_points.remove(choose_point)


    def __grow_area_zero(self):
        # Form outside ring
        ykey = 0
        for ycoord in self.mapdata:
            xkey = 0
            for xcoord in ycoord:
                if xcoord.area == 0:
                    # See if next to a wall
                    if (self.mapdata[ykey - 1][xkey].area < 0) or (self.mapdata[ykey + 1][xkey].area < 0):
                        self.mapdata[ykey][xkey].is_accessible = True
                        self.mapdata[ykey][xkey].avoid_special = True
                        if self.mapdata[ykey][xkey - 1].area == 0:
                            # Grow left
                            self.mapdata[ykey][xkey].exits |= TGLRoomExits.LEFT
                            self.mapdata[ykey][xkey - 1].is_accessible = True
                            self.mapdata[ykey][xkey - 1].avoid_special = True
                            self.mapdata[ykey][xkey - 1].exits |= TGLRoomExits.RIGHT
                        if self.mapdata[ykey][xkey + 1].area == 0:
                            # Grow right
                            self.mapdata[ykey][xkey].exits |= TGLRoomExits.RIGHT
                            self.mapdata[ykey][xkey + 1].is_accessible = True
                            self.mapdata[ykey][xkey + 1].avoid_special = True
                            self.mapdata[ykey][xkey + 1].exits |= TGLRoomExits.LEFT
                    if (self.mapdata[ykey][xkey - 1].area < 0) or (self.mapdata[ykey][xkey + 1].area < 0):
                        self.mapdata[ykey][xkey].is_accessible = True
                        self.mapdata[ykey][xkey].avoid_special = True
                        if self.mapdata[ykey - 1][xkey].area == 0:
                            # Grow up
                            self.mapdata[ykey][xkey].exits |= TGLRoomExits.UP
                            self.mapdata[ykey - 1][xkey].is_accessible = True
                            self.mapdata[ykey - 1][xkey].avoid_special = True
                            self.mapdata[ykey - 1][xkey].exits |= TGLRoomExits.DOWN
                        if self.mapdata[ykey + 1][xkey].area == 0:
                            # Grow down
                            self.mapdata[ykey][xkey].exits |= TGLRoomExits.DOWN
                            self.mapdata[ykey + 1][xkey].is_accessible = True
                            self.mapdata[ykey + 1][xkey].avoid_special = True
                            self.mapdata[ykey + 1][xkey].exits |= TGLRoomExits.UP
                xkey += 1
            ykey += 1

    # Place items and minibosses which hold items
    # Unlike the standalone rando, we have to keep these in their original area for AP location rules
    def __place_item_locations(self, world: "TGLWorld", area: int):
        locations = self.__create_suitable_list(area, False, False)

        # We need lists of items to place per area, 2 minibosses per area, and blocksets
        # TODO: Can minibosses be randomized in any way without screwing up Area logic 
        #       (or, can we note the locations of minibosses for logic?) 
        item_list = item_locations[area]
        miniboss_list = [0x0B + (area * 2), 0x0C + (area * 2)]
        item_blocks = [0xAE94,0xC994,0xBE94,0xB394]

        for item in item_list:
            if len(locations) > 0:
                item_room = world.random.choice(locations)
                item_room.room_type = TGLRoomType.ITEM
                item_room.content_id = item
                item_room.block_set = world.random.choice(item_blocks)
                locations.remove(item_room)
            else:
                raise Exception("TGL Map Rando: Not enough suitable locations for placing items.") 
        
        for miniboss in miniboss_list:
            if len(locations) > 0:
                item_room = world.random.choice(locations)
                item_room.room_type = TGLRoomType.MINIBOSS
                item_room.content_id = miniboss
                locations.remove(item_room)
            else:
                raise Exception("TGL Map Rando: Not enough suitable locations for placing minibosses.")

    def __place_starting_text_room(self):
        coord = [12, 11]
        starting_room: TGLRoom = self.mapdata[coord[0]][coord[1]]
        starting_room.room_type = TGLRoomType.TEXT
        starting_room.content_id = 0x0
        starting_room.exits = 0b1111
        # Set neighboring rooms to accessible and with exits
        self.mapdata[coord[0] + 1][coord[1]].is_accessible = True
        self.mapdata[coord[0] + 1][coord[1]].exits |= TGLRoomExits.UP
        self.mapdata[coord[0] - 1][coord[1]].is_accessible = True
        self.mapdata[coord[0] - 1][coord[1]].exits |= TGLRoomExits.DOWN
        self.mapdata[coord[0]][coord[1] + 1].is_accessible = True
        self.mapdata[coord[0]][coord[1] + 1].exits |= TGLRoomExits.LEFT
        self.mapdata[coord[0]][coord[1] - 1].is_accessible = True
        self.mapdata[coord[0]][coord[1] - 1].exits |= TGLRoomExits.RIGHT

    # Corridors, shops
    def __place_important_rooms(self, world: "TGLWorld", area: int):
        suitable_rooms = self.__create_suitable_list(area, True, True)
        if not suitable_rooms:
            raise Exception(f"TGL Map Rando: Not enough suitable rooms available for Area {area}.")
        # Corridors
        if area == 0:
            c_room = world.random.choice(suitable_rooms)
            c_room.room_type = TGLRoomType.CORRIDOR
            c_room.content_id = 21
            suitable_rooms.remove(c_room)
            # Single Shops - for now putting in same areas as vanilla
            for shopnum in range(0x3A, 0x3F):
                shoproom = world.random.choice(suitable_rooms)
                shoproom.room_type = TGLRoomType.SINGLESHOP
                shoproom.content_id = shopnum
                suitable_rooms.remove(shoproom)
        elif area == 1:
            c_room = world.random.choice(suitable_rooms)
            c_room.room_type = TGLRoomType.CORRIDOR
            c_room.content_id = 11
            suitable_rooms.remove(c_room)
        else:
            c_room = world.random.choice(suitable_rooms)
            c_room.room_type = TGLRoomType.CORRIDOR
            c_room.content_id = area
            suitable_rooms.remove(c_room)
            c_room = world.random.choice(suitable_rooms)
            c_room.room_type = TGLRoomType.CORRIDOR
            c_room.content_id = area + 10
            suitable_rooms.remove(c_room)
        
        
        # "Multi" shops - for now placing in vanilla zones
        if area == 2:
            shopnum = 0x3F
            shoproom = world.random.choice(suitable_rooms)
            shoproom.room_type = TGLRoomType.MULTISHOP
            shoproom.content_id = shopnum
            suitable_rooms.remove(shoproom)
        if area == 4:
            shopnum = 0x41
            shoproom = world.random.choice(suitable_rooms)
            shoproom.room_type = TGLRoomType.MULTISHOP
            shoproom.content_id = shopnum
            suitable_rooms.remove(shoproom)
        if area == 10:
            shopnum = 0x43
            shoproom = world.random.choice(suitable_rooms)
            shoproom.room_type = TGLRoomType.MULTISHOP
            shoproom.content_id = shopnum
            suitable_rooms.remove(shoproom)
        if area == 7:
            # There are 2 shops in Area 7
            shopnum = 0x40
            shoproom = world.random.choice(suitable_rooms)
            shoproom.room_type = TGLRoomType.MULTISHOP
            shoproom.content_id = shopnum
            suitable_rooms.remove(shoproom)
            shopnum = 0x42
            shoproom = world.random.choice(suitable_rooms)
            shoproom.room_type = TGLRoomType.MULTISHOP
            shoproom.content_id = shopnum
            suitable_rooms.remove(shoproom)

    # Saves, text, power chip refill
    def __place_safe_rooms(self, world: "TGLWorld", area: int):
        suitable_rooms = self.__create_suitable_list(area, True, True)
        
        if area == 0:
            # "Power Chip" refill room - Area 0
            chiproom = world.random.choice(suitable_rooms)
            chiproom.block_set = 0xEA95
            chiproom.chip_tile = True
            suitable_rooms.remove(chiproom)
            # Text rooms for Area 0, skip text 0 because we place that in the start room
            for textnum in range(1,4):
                textroom = world.random.choice(suitable_rooms)
                textroom.room_type = TGLRoomType.TEXT
                textroom.content_id = textnum
                suitable_rooms.remove(textroom)
        # Save room
        saveroom = world.random.choice(suitable_rooms)
        saveroom.room_type = TGLRoomType.SAVE
        suitable_rooms.remove(saveroom)
        # Text rooms non-Area 0
        # Unlike vanilla we're putting each hint room in the area it belongs to
        # Corridor 1 hint is in Area 0 as well, start at 2
        if area > 1:
            textroom = world.random.choice(suitable_rooms)
            textroom.room_type = TGLRoomType.TEXT
            textroom.content_id = area + 10

    # N E S W box rooms
    # NOTE: I hate this, and this code was buggy in original. This should be vastly simplified.
    def __place_cardinal_points(self):
        rooms_on_ring: List[Tuple] = []
        ykey: int = 0
        for ycoord in self.mapdata:
            xkey: int = 0
            for xcoord in ycoord:
                if (xcoord.area == 0) and xcoord.avoid_special and (xcoord.room_type == 0) and xcoord.is_accessible:
                    room_coord = (ykey, xkey)
                    rooms_on_ring.append(room_coord)
                xkey += 1
            ykey += 1
        north_y = None
        south_y = None
        west_x = None
        east_x = None
        for room in rooms_on_ring:
            if (north_y is None) or (room[0] < north_y):
                north_y = room[0]
            if (south_y is None) or (room[0] > south_y):
                south_y = room[0]
            if (west_x is None) or (room[1] < west_x):
                west_x = room[1]
            if (east_x is None) or (room[1] > east_x):
                east_x = room[1]
        north_sum = 0
        north_tiles = 0
        south_sum = 0
        south_tiles = 0
        west_sum = 0
        west_tiles = 0
        east_sum = 0
        east_tiles = 0
        for room in rooms_on_ring:
            if (room[0] == north_y):
                north_sum += room[1]
                north_tiles += 1
            if (room[0] == south_y):
                south_sum += room[1]
                south_tiles += 1
            if (room[1] == west_x):
                west_sum += room[0]
                west_tiles += 1
            if (room[1] == east_x):
                east_sum += room[0]
                east_tiles += 1
        north_avg = north_sum / north_tiles
        south_avg = south_sum / south_tiles
        west_avg = west_sum / west_tiles
        east_avg = east_sum / east_tiles
        north_room = None
        north_distance = None
        south_room = None
        south_distance = None
        west_room = None
        west_distance = None
        east_room = None
        east_distance = None
        for room in rooms_on_ring:
            if (room[0] == north_y):
                distance = abs(north_avg - room[1])
                if (north_distance is None) or (distance <= north_distance):
                    north_room = room
                    north_distance = distance
            if (room[0] == south_y):
                distance = abs(south_avg - room[1])
                if (south_distance is None) or (distance <= south_distance):
                    south_room = room
                    south_distance = distance
            if (room[1] == west_x):
                distance = abs(west_avg - room[0])
                if (west_distance is None) or (distance <= west_distance):
                    west_room = room
                    west_distance = distance
            if (room[1] == east_x):
                distance = abs(east_avg - room[0])
                if (east_distance is None) or (distance <= east_distance):
                    east_room = room
                    east_distance = distance
        self.mapdata[north_room[0]][north_room[1]].block_set = 0xA695
        self.mapdata[south_room[0]][south_room[1]].block_set = 0xB495
        self.mapdata[west_room[0]][west_room[1]].block_set = 0xD995
        self.mapdata[east_room[0]][east_room[1]].block_set = 0xC895

            
    '''
    # NOTE: This selects a random room from a list of rooms to be a corridor, may not need this or can simplify
    def __place_corridor(self, corridor: int, room: TGLRoom):
        pass
    '''

    def __place_starting_points(self):
        for ycoord in self.mapdata:
            for xcoord in ycoord:
                if xcoord.area > 0 and xcoord.is_startingpoint:
                    if xcoord.area == 1:
                        xcoord.room_type = TGLRoomType.CORRIDOR
                        xcoord.content_id = 1
                    else:
                        xcoord.room_type = TGLRoomType.SAVE


    def __populate_enemies(self, world: "TGLWorld"):
        for ycoord in self.mapdata:
            for xcoord in ycoord:
                if xcoord.is_accessible:
                    if (xcoord.room_type == TGLRoomType.NORMAL) or (xcoord.room_type == TGLRoomType.ITEM):
                        # Sets the % chance there is an enemy (currently ~90%)
                        if world.random.random() > 0.1:
                            xcoord.enemy_type = (world.random.choice(range(47))) + 1

    def __place_area_decorations(self, world: "TGLWorld"):
        starting_rooms: List[Tuple] = []
        ykey: int = 0
        for ycoord in self.mapdata:
            xkey: int = 0
            for xcoord in ycoord:
                if xcoord.is_startingpoint and (xcoord.area != 0):
                    new_room = (ykey,xkey)
                    starting_rooms.append(new_room)
                xkey += 1
            ykey += 1
        for room in starting_rooms:
            ykey = room[0]
            xkey = room[1]
            if (self.mapdata[ykey][xkey].exits & TGLRoomExits.UP):
                room_up = self.mapdata[ykey - 1][xkey]
                if (room_up.room_type == TGLRoomType.NORMAL) and (room_up.block_set == -1):
                    if (world.random.random() < 0.5):
                        room_up.block_set = world.random.choice(room_blocksets["no_chips_area_transition_down"])
                        room_up.chip_tile = False
                    else:
                        room_up.block_set = world.random.choice(room_blocksets["with_chips_area_transition_down"])
                        room_up.chip_tile = True
            if (self.mapdata[ykey][xkey].exits & TGLRoomExits.DOWN):
                room_down = self.mapdata[ykey + 1][xkey]
                if (room_down.room_type == TGLRoomType.NORMAL) and (room_down.block_set == -1):
                    if (world.random.random() < 0.5):
                        room_down.block_set = world.random.choice(room_blocksets["no_chips_area_transition_up"])
                        room_down.chip_tile = False
                    else:
                        room_down.block_set = world.random.choice(room_blocksets["with_chips_area_transition_up"])
                        room_down.chip_tile = True
            if (self.mapdata[ykey][xkey].exits & TGLRoomExits.LEFT):
                room_left = self.mapdata[ykey][xkey - 1]
                if (room_left.room_type == TGLRoomType.NORMAL) and (room_left.block_set == -1):
                    if (world.random.random() < 0.5):
                        room_left.block_set = world.random.choice(room_blocksets["no_chips_area_transition_right"])
                        room_left.chip_tile = False
                    else:
                        room_left.block_set = world.random.choice(room_blocksets["with_chips_area_transition_right"])
                        room_left.chip_tile = True
            if (self.mapdata[ykey][xkey].exits & TGLRoomExits.RIGHT):
                room_right = self.mapdata[ykey][xkey + 1]
                if (room_right.room_type == TGLRoomType.NORMAL) and (room_right.block_set == -1):
                    if (world.random.random() < 0.5):
                        room_right.block_set = world.random.choice(room_blocksets["no_chips_area_transition_left"])
                        room_right.chip_tile = False
                    else:
                        room_right.block_set = world.random.choice(room_blocksets["with_chips_area_transition_left"])
                        room_right.chip_tile = True


    def __place_corridor_decorations(self, world: "TGLWorld"):
        corridor_rooms: List[Tuple] = []
        ykey: int = 0
        for ycoord in self.mapdata:
            xkey: int = 0
            for xcoord in ycoord:
                if xcoord.is_startingpoint and (xcoord.area != 0):
                    new_room = (ykey,xkey)
                    corridor_rooms.append(new_room)
                xkey += 1
            ykey += 1
        for room in corridor_rooms:
            ykey = room[0]
            xkey = room[1]
            if (self.mapdata[ykey][xkey].exits & TGLRoomExits.UP):
                room_up = self.mapdata[ykey - 1][xkey]
                if (room_up.room_type == TGLRoomType.NORMAL) and (room_up.block_set == -1):
                    room_up.block_set = world.random.choice(room_blocksets["corridor_transition_down"])
                    room_up.chip_tile = False
            if (self.mapdata[ykey][xkey].exits & TGLRoomExits.DOWN):
                room_down = self.mapdata[ykey + 1][xkey]
                if (room_down.room_type == TGLRoomType.NORMAL) and (room_down.block_set == -1):
                    room_up.block_set = world.random.choice(room_blocksets["corridor_transition_up"])
                    room_up.chip_tile = False
            if (self.mapdata[ykey][xkey].exits & TGLRoomExits.LEFT):
                room_left = self.mapdata[ykey][xkey - 1]
                if (room_left.room_type == TGLRoomType.NORMAL) and (room_left.block_set == -1):
                    room_up.block_set = world.random.choice(room_blocksets["corridor_transition_right"])
                    room_up.chip_tile = False
            if (self.mapdata[ykey][xkey].exits & TGLRoomExits.RIGHT):
                room_right = self.mapdata[ykey][xkey + 1]
                if (room_right.room_type == TGLRoomType.NORMAL) and (room_right.block_set == -1):
                    room_up.block_set = world.random.choice(room_blocksets["corridor_transition_left"])
                    room_up.chip_tile = False

    def __place_random_decorations(self, world: "TGLWorld"):
        decoration_chance = 5 # 1/x chance to have decorations
        chip_chance = 3 # 1/x chance to have chips if have decorations
        for ycoord in self.mapdata:
            for xcoord in ycoord:
                if xcoord.is_accessible and (xcoord.room_type == TGLRoomType.NORMAL) and (xcoord.block_set == -1):
                    if world.random.choice(range(decoration_chance)) == 0:
                        if world.random.choice(range(chip_chance)) == 0:
                            xcoord.block_set = world.random.choice(room_blocksets["with_chips_no_transition"])
                            xcoord.chip_tile = True
                        else:
                            xcoord.block_set = world.random.choice(room_blocksets["no_chips_no_transition"])
                            xcoord.chip_tile = False

    def __create_suitable_list(self, area: int, discard_special: bool, allow_overwrite: bool) -> List[TGLRoom]:
        locations: List[TGLRoom] = []
        for ycoord in self.mapdata:
            for xcoord in ycoord:
                if (xcoord.area == area) and xcoord.is_accessible and (xcoord.block_set == -1):
                    if (xcoord.room_type == TGLRoomType.NORMAL) or \
                        ((area != 0) and allow_overwrite and 
                         (xcoord.room_type == TGLRoomType.SAVE) and xcoord.is_startingpoint):
                        if not discard_special or not xcoord.avoid_special:
                            if (area != 0) or not xcoord.is_startingpoint:
                                locations.append(xcoord)
        #print("Area " + str(area) + " suitable: " + str(len(locations)))
        return locations


    # Build a list of the rooms in an area, and test where connections can be made
    def __add_connections(self, world: "TGLWorld", area: int, connection_count: int, oneway: bool, portal_only: bool):
        rooms_in_area: List[Tuple] = []
        connections_made: int = 0
        ykey = 0
        for ycoord in self.mapdata:
            xkey = 0
            for xcoord in ycoord:
                if (xcoord.area == area) and (xcoord.is_accessible):
                    new_room = (ykey,xkey)
                    rooms_in_area.append(new_room)
                xkey += 1
            ykey += 1
        while (connections_made < connection_count) and (len(rooms_in_area) > 1):
            room_loc = world.random.choice(rooms_in_area)
            ykey: int = room_loc[0]
            xkey: int = room_loc[1]
            room: TGLRoom = self.mapdata[ykey][xkey]
            direction_shift = world.random.choice(range(4))
            direction = (1 << direction_shift) # choose one random direction to connect to
            go_up: bool = ((ykey > 0) 
                           and (self.mapdata[ykey - 1][xkey].area == area) 
                           and (self.mapdata[ykey - 1][xkey].is_accessible) 
                           and (room.exits & TGLRoomExits.UP == 0))
            go_down: bool = ((ykey < 23) 
                             and (self.mapdata[ykey + 1][xkey].area == area) 
                             and (self.mapdata[ykey + 1][xkey].is_accessible) 
                             and (room.exits & TGLRoomExits.DOWN == 0))
            go_left: bool = ((xkey > 0) 
                             and (self.mapdata[ykey][xkey - 1].area == area) 
                             and (self.mapdata[ykey][xkey - 1].is_accessible) 
                             and (room.exits & TGLRoomExits.LEFT == 0))
            go_right: bool = ((xkey < 23) 
                              and (self.mapdata[ykey][xkey + 1].area == area) 
                              and (self.mapdata[ykey][xkey + 1].is_accessible) 
                              and (room.exits & TGLRoomExits.RIGHT == 0))
            if portal_only:
                room_type = room.room_type
                good_rooms = list(range(1,6))
                if go_up:
                    other_room_type = self.mapdata[ykey - 1][xkey].room_type
                    go_up = (room_type in good_rooms) or (other_room_type in good_rooms)
                if go_down:
                    other_room_type = self.mapdata[ykey + 1][xkey].room_type
                    go_down = (room_type in good_rooms) or (other_room_type in good_rooms)
                if go_left:
                    other_room_type = self.mapdata[ykey][xkey - 1].room_type
                    go_left = (room_type in good_rooms) or (other_room_type in good_rooms)
                if go_right:
                    other_room_type = self.mapdata[ykey][xkey + 1].room_type
                    go_right = (room_type in good_rooms) or (other_room_type in good_rooms)
            if not (go_up or go_down or go_right or go_left):
                rooms_in_area.remove(room_loc)
            if (direction == TGLRoomExits.UP) and go_up:
                room.exits |= TGLRoomExits.UP
                if not oneway:
                    self.mapdata[ykey - 1][xkey].exits |= TGLRoomExits.DOWN
                connections_made += 1
            if (direction == TGLRoomExits.DOWN) and go_down:
                room.exits |= TGLRoomExits.DOWN
                if not oneway:
                    self.mapdata[ykey + 1][xkey].exits |= TGLRoomExits.UP
                connections_made += 1
            if (direction == TGLRoomExits.LEFT) and go_left:
                room.exits |= TGLRoomExits.LEFT
                if not oneway:
                    self.mapdata[ykey][xkey - 1].exits |= TGLRoomExits.RIGHT
                connections_made += 1
            if (direction == TGLRoomExits.RIGHT) and go_right:
                room.exits |= TGLRoomExits.RIGHT
                if not oneway:
                    self.mapdata[ykey][xkey + 1].exits |= TGLRoomExits.LEFT
                connections_made += 1
            
                

        