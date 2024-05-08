import os
from typing import TYPE_CHECKING, Tuple, Dict, Optional

import Utils
import settings
from BaseClasses import ItemClassification as IC
from worlds.Files import APProcedurePatch, APTokenTypes, APTokenMixin
from .Items import TGL_ITEMID_BASE, balanced_rapid_fire
from .Locations import TGL_LOCID_BASE
from .Options import TGLOptions
from .Map import TGLMap

if TYPE_CHECKING:
    from . import TGLWorld

#TGL_ITEMID_BASE = 8471760000
AP_ITEM_CODE = 21    # Red Chips
SHOP_JUNK_ITEM = 22  # Blue Chips

TEXT_NEWLINE = 0x0D
TEXT_BLANKSPACE = 0x0B
TEXT_NEXTPAGE = 0x01
TEXT_END_MESSAGE = 0x0

corridor_hints_addresses = {
    11: 0x15A30,
    12: 0x15CA0,
    13: 0x15CD8,
    14: 0x15D3C,
    15: 0x15DB3,
    16: 0x15DF2,
    17: 0x15E36,
    18: 0x15E8D,
    19: 0x15EC5,
    20: 0x15EF4
}

# Hint text can be 16 characters long per line
corridor_hints_junk = {
    "short":  [
        ("xx49 48z61?", "76.65 46o61!", "69z6Ci45-64xyzx"),
        ("Do not go to", "Corridor 21,", "it smells bad.")
    ],
    "medium": [
        ("Why are you", "here? It is not", "after dark", "yet!"),
        ("Hint text can", "be up to 16", "characters", "long per line!")
    ],
    "long":   [
        ("This Blue Lander@", "text is brought", "to you by", "Archipelago@", "in association", "with BK@."),
        ("I will tell you", "where to find", "the key", "you are missing,", "please pay 9999", "Power Chips.")
    ]
}

corridor_hints_filler = {
    "short":  [
        ("C-# holds", "nothing of", "great value."),
        ("None of the", "items in C-#", "are worth much.")
    ],
    "medium": [
        ("C-# holds an", "item that", "no one really", "cares about."),
        ("If you clear", "out C-#,", "there will", "be nothing of", "value.")
    ],
    "long":   [
        ("Corridor-#", "does not have", "anything that", "will bring you", "closer to saving", "the worlds."),
        ("When I hid", "items to help", "you on your", "quest, I did not", "put anything", "important", "in C-#.")
    ]
}

corridor_hints_useful = {
    "short":  [
        ("C-# holds a", "useful item", "for someone."),
        ("At least one", "item in C-#", "is useful.")
    ],
    "medium": [
        ("C-# holds an", "item that some", "have said is", "useful."),
        ("If you clear", "out C-#, you", "may find a", "useful item!")
    ],
    "long":   [
        ("Corridor-#", "may be of some", "use to you or", "your friends", "in trying to", "save the worlds."),
        ("When I hid", "items to help", "you on your", "quest, I put", "something useful", "in Corridor-#.")
    ]
}

corridor_hints_progression = {
    "short":  [
        ("C-# holds an", "important item", "for someone!"),
        ("At least one", "item in C-#", "is progression!")
    ],
    "medium": [
        ("C-# holds an", "item that some", "have said", "brings progress"),
        ("If you clear", "out C-#, you", "may find an", "important item!")
    ],
    "long":   [
        ("Corridor-# is", "an important", "place for you", "to explore if", "you want to", "save the worlds!"),
        ("When I hid", "items to help", "you on your", "quest, I put", "something", "important in", "Corridor-#!")
    ]
}

# Short = 43 characters max (52 bounded) 
# Medium = 56 characters max (68 bounded)
# Long = 87 characters max (112 bounded)
corridor_hints_length = {
    "short":  [11, 19, 20],
    "medium": [12, 15, 16, 18],
    "long":   [13, 14, 17]
}


class TGLProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = "5acfc9d45b94f82f97e04c4434adbf36"
    game = "The Guardian Legend"
    patch_file_ending = ".aptgl"
    result_file_ending = ".nes"

    procedure = [("apply_tokens", ["tgl_token_data.bin"])]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

 
def write_tokens(world: "TGLWorld", options: TGLOptions, patch: TGLProcedurePatch) -> None:
    corridor_hint_items: Dict[int, IC] = {}
    for location in world.multiworld.get_filled_locations(world.player):

        if location.address is not None:
            
            # Determine location type: Ground drop, Shop, Corridor Drop, or Key/Boss
            location_data: Tuple = divmod(get_internal_loc_id(location.address), 1000)
            location_rom_address = 0x0
            if location_data[0] == 1:
                # Ground or Miniboss drop 
                location_rom_address = 0x16388 + location_data[1] - 1
            
            # Triple Item Shop
            elif location_data[0] == 2:
                # Fill in 3-item shops with junk
                if location_data[1] > 100:
                    # middle shop location will hold the item, left and right get junk
                    location_rom_address = (0x1605e + (location_data[1] - 100)) + 1
                    patch.write_token(
                        APTokenTypes.WRITE, 
                        location_rom_address-1,
                        SHOP_JUNK_ITEM.to_bytes(1, 'big')
                    )
                    patch.write_token(
                        APTokenTypes.WRITE, 
                        location_rom_address+1,
                        SHOP_JUNK_ITEM.to_bytes(1, 'big')
                    )
                else:
                    location_rom_address = 0x16077 + location_data[1]
                
            # Corridor Item 
            elif location_data[0] == 3:
                location_rom_address = 0x1ef51 + location_data[1] - 1
                if location_data[1] > 10:
                    corridor_hint_items[location_data[1]] = location.item.classification

            # Corridor bonus items, these are remote and not displayed in-game
            elif location_data[0] == 4:
                if location_data[1] > 10:
                    # Store the classification for Corridor 11-20 items for hints
                    corridor_hint_items[location_data[1]+100] = location.item.classification
            else:
                raise Exception('Invalid location ID found for The Guardian Legend.')
            
            # This should only be skipped if case 4 hit above because this is a Corridor item never shown in game
            # - Prevents the ROM header being edited and ROM failing to load 
            if location_rom_address != 0:
                # Local item: can change directly
                if location.item and location.item.player == world.player:
                    item_data: Tuple = divmod(get_internal_item_id(location.item.code), 1000)
            
                    # Check whether this is a drop item or a key
                    if item_data[0] == 1:
                        # Drop item
                        patch.write_token(
                            APTokenTypes.WRITE, 
                            location_rom_address,
                            item_data[1].to_bytes(1, 'big')
                        )    
                    elif item_data[0] == 2:
                        # Key item - treat as remote item
                        patch.write_token(
                            APTokenTypes.WRITE, 
                            location_rom_address,
                            AP_ITEM_CODE.to_bytes(1, 'big')
                        )
                    else:
                        raise Exception('Invalid item ID found for The Guardian Legend.')

                # APItem: Set sprite to Red Chip in-game
                else:
                    patch.write_token(
                        APTokenTypes.WRITE, 
                        location_rom_address,
                        AP_ITEM_CODE.to_bytes(1, 'big')
                    )

    ## Core changes ##

    # Remove the YOU GOT KEY popup in Corridors (TODO: Add to all Corridors, change message)
    # 0xEA is No-OP, removing the branch to the YOU GOT ITEM subroutine
    corridor_reward_popup_byte = 0x1F552
    patch.write_token(
        APTokenTypes.WRITE, 
        corridor_reward_popup_byte,
        0xEAEA.to_bytes(2, 'big')
    )

    # Edit 3-item shops to only have one item, change Lander text accordingly
    left_shop_item_jump = 0x15FFD   # JSR, 3 bytes
    right_shop_item_jump = 0x16015  # JSR, 3 bytes
    shop_item_counter = 0x1603A     # static 06, 1 byte
    item_data_pointer = 0x1603C     # LDA (B9 50), 1 byte
    branch_to_load_items = 0x1604F  # BNE, 2 bytes
    shop_message_start = 0x15C16

    # No-op loading left item sprite data
    patch.write_token(
        APTokenTypes.WRITE,
        left_shop_item_jump,
        0xEAEAEA.to_bytes(3, 'big')
    )
    # No-op loading right item sprite data
    patch.write_token(
        APTokenTypes.WRITE,
        right_shop_item_jump,
        0xEAEAEA.to_bytes(3, 'big')
    )
    # Bump the compare counter by one, start on 2nd item
    patch.write_token(
        APTokenTypes.WRITE,
        shop_item_counter,
        0x07.to_bytes(1, 'big')
    )
    # Bump the item data pointer by one, start on 2nd item
    patch.write_token(
        APTokenTypes.WRITE,
        item_data_pointer,
        0x51.to_bytes(1, 'big')
    )
    # No-op the loop branch so only one item's data loads
    patch.write_token(
        APTokenTypes.WRITE,
        branch_to_load_items,
        0xEAEA.to_bytes(2, 'big')
    )
    
    # Overwrite the three-item shop text
    new_shop_text = ("Yum yum,", "Power Chips,", "gimme gimme!")
    new_shop_bytes = encode_text_to_bytes(new_shop_text)
    new_shop_bytes.append(TEXT_END_MESSAGE)
    patch.write_token(
        APTokenTypes.WRITE,
        shop_message_start,
        bytes(new_shop_bytes)
    )

    # change saveroom text
    save_room_text_data = 0x15B7F
    new_save_room_text = (
        "If you want", "to save your", "progress,",
        "please use", "a savestate.", "Passwords", "do not work."
    )
    new_save_room_bytes = encode_text_to_bytes(new_save_room_text)
    new_save_room_bytes.append(TEXT_END_MESSAGE) 
    patch.write_token(
        APTokenTypes.WRITE,
        save_room_text_data,
        bytes(new_save_room_bytes)
    )

    # Remove the password menu option
    game_start_jump = 0x458
    # Changes the cursor handler to an empty loop, can never select PASSWORD screen
    patch.write_token(
        APTokenTypes.WRITE,
        game_start_jump,
        0x4C3D84.to_bytes(3, 'big')
    )

    # Change the PASSWORD CONTINUE text to the player's slot name (mostly...)
    password_continue_text_data = 0x88D
    player_slotname_limited = world.multiworld.player_name[world.player][:17].upper()
    for _ in range(17 - len(player_slotname_limited)):
        player_slotname_limited += " "
    player_slotname_bytes = bytearray()
    for c in player_slotname_limited:
        if (ord(c) in range(0x30, 0x3A)) or (ord(c) in range(0x41, 0x5B)):
            player_slotname_bytes.append(ord(c))
        elif (c == " ") or (c == "-") or (c == "_"):
            player_slotname_bytes.append(0x20)
        else:
            # Any character we can't display gets a nice star sprite :)
            player_slotname_bytes.append(0x25)
    patch.write_token(
        APTokenTypes.WRITE,
        password_continue_text_data,
        bytes(player_slotname_bytes)
    )

    # Disable the password screen in save rooms, no-op branch on pressing 'A'
    saveroom_branch_to_password = 0x162D3
    patch.write_token(
        APTokenTypes.WRITE,
        saveroom_branch_to_password,
        0xEAEA.to_bytes(2, 'big')
    )

    # Change the Corridor 4 Blue Lander text
    helpful_lander_text_data = 0x15C53
    helpful_lander_new_text = (
        "Why are you", "doing this?", "The door to",
        "Corridor-4", "has already", "opened,", "now go! "
    )
    helpful_lander_new_bytes = encode_text_to_bytes(helpful_lander_new_text)
    helpful_lander_new_bytes.append(TEXT_END_MESSAGE)

    patch.write_token(
        APTokenTypes.WRITE,
        helpful_lander_text_data,
        bytes(helpful_lander_new_bytes)
    )

    # NOTE: Need to double check Fireball's work for safety
    # Remove screen flashes from EE use and Naju explosion cutscene (from Fireball87 rando)
    ee_flash = 0x18BBD
    end_flash = 0x894C
    patch.write_token(
        APTokenTypes.WRITE,
        ee_flash,
        0x0F.to_bytes(1, 'big')
    )
    patch.write_token(
        APTokenTypes.WRITE,
        end_flash,
        0x0F.to_bytes(1, 'big')
    )
    
    ## Options-based changes ##

    # Map Randomization
    # Call Map rando to get the map bytestring and write
    # TODO: Fill empty space with 0s? Also double check the 1916 figure
    # TODO: Future version may affect item distribution
    if options.randomize_map:
        map_data_start = 0x14A7E
        random_map = TGLMap()
        random_map.randomizeMap(world)
        random_map.print_maps() # For testing, should be a logging option?
        map_hex: bytearray = random_map.writehex()
        print(map_hex.hex(" ", 1))
        patch.write_token(
            APTokenTypes.WRITE,
            map_data_start,
            bytes(map_hex)
        )


    # Balanced Rapid fire
    if options.balanced_rapid_fire:
        rapid_fire_byte = 0x87DE
        for i in range(6):
            patch.write_token(
                APTokenTypes.WRITE, 
                rapid_fire_byte+i,
                balanced_rapid_fire[i].to_bytes(1, 'big')
            )
        
    # Corridor hints
    corridor_hint_main_text_data = 0x159C6
    # This text has to be exact length because it flows into another line
    corridor_hint_main_new_text = (
        "The corridor", "locks are now", "broken!    ",
        "Defeat the", "monsters that", "are infesting",
        "them to get", "valuable items."
    )
    corridor_hint_main_new_bytes = encode_text_to_bytes(corridor_hint_main_new_text)
    corridor_hint_main_new_bytes.append(TEXT_NEXTPAGE)
    patch.write_token(
        APTokenTypes.WRITE,
        corridor_hint_main_text_data,
        bytes(corridor_hint_main_new_bytes)
    )

    # Determine which corridors get "real" hints
    corridor_hint_selections = world.random.sample(range(11, 21), options.corridor_hints.value)

    # For each corridor, determine which hint to give 
    for cnum in range(11, 21):
        corridor_hint_text_choice: Tuple[str]
        corridor_hint_size_choice: str = ""
        if cnum in corridor_hints_length["long"]:
            corridor_hint_size_choice = "long"
        elif cnum in corridor_hints_length["medium"]:
            corridor_hint_size_choice = "medium"
        else:
            corridor_hint_size_choice = "short"

        if cnum in corridor_hint_selections:
            # Determine hint level
            if (((corridor_hint_items[cnum] & IC.progression) == IC.progression) 
                  or ((corridor_hint_items[cnum+100] & IC.progression) == IC.progression)):
                corridor_hint_text_choice = world.random.choice(corridor_hints_progression[corridor_hint_size_choice])
            elif (((corridor_hint_items[cnum] & IC.useful) == IC.useful)
                    or ((corridor_hint_items[cnum+100] & IC.useful) == IC.useful)):
                corridor_hint_text_choice = world.random.choice(corridor_hints_useful[corridor_hint_size_choice])
            else:
                # Traps may cause text to appear as "useful" rather than "filler"
                if (((corridor_hint_items[cnum] & IC.trap) == IC.trap)
                      or ((corridor_hint_items[cnum+100] & IC.trap) == IC.trap)):
                    if world.random.randint(0, 1) == 1:
                        corridor_hint_text_choice = world.random.choice(
                            corridor_hints_useful[corridor_hint_size_choice])
                    else:
                        corridor_hint_text_choice = world.random.choice(
                            corridor_hints_filler[corridor_hint_size_choice])
                else:
                    corridor_hint_text_choice = world.random.choice(
                        corridor_hints_filler[corridor_hint_size_choice])   
        else:
            # Junk text
            corridor_hint_text_choice = world.random.choice(corridor_hints_junk[corridor_hint_size_choice])

        # Write hint text to corresponding corridor hint location
        hintbytes = encode_text_to_bytes(corridor_hint_text_choice, cnum)
        hintbytes.append(TEXT_END_MESSAGE)
        patch.write_token(
            APTokenTypes.WRITE,
            corridor_hints_addresses[cnum],
            bytes(hintbytes)
        )

    # Finish, write patch file
    patch.write_file("tgl_token_data.bin", patch.get_token_binary())
    
    
def generate_output(world: "TGLWorld", output_directory: str, options: TGLOptions) -> None:
    patch = TGLProcedurePatch()
    player = world.player
    multiworld = world.multiworld
    write_tokens(world, options, patch)

    # Write output to patch file
    outfile_player_name = f"_P{player}"
    outfile_player_name += f"_{multiworld.get_file_safe_player_name(player).replace(' ', '_')}" \
        if multiworld.player_name[player] != f"Player{player}" else ""
    output_path = os.path.join(
                    output_directory, 
                    f"AP_{multiworld.seed_name}{outfile_player_name}{patch.patch_file_ending}"
                  )
    patch.write(output_path)

        
def get_internal_item_id(item_id: int) -> int:
    return (item_id - TGL_ITEMID_BASE)


def get_internal_loc_id(loc_id: int) -> int:
    return (loc_id - TGL_LOCID_BASE)


def get_base_rom_as_bytes() -> bytes:
    options = settings.get_settings()
    file_name = options["guardianlegend_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    with open(file_name, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes


# Take a message in String-Tuple format and encode as a TGL-friendly string.
# Messages have 3 lines per page, but can have 4 if it's the last page.
# TGL uses mostly ASCII but has some outliers, so special encoding is performed.
def encode_text_to_bytes(textdata: Tuple[str], corridor_number: Optional[int] = 99) -> bytearray:
    tgl_special_chars = {
        " ": 0x0B,
        ";": 0x3B,
        ",": 0x3C,
        "-": 0x3D,
        "?": 0x3F,
        "@": 0x40,
        ".": 0x5B,
        "!": 0x5D,
    }
    newtext_bytes = bytearray()
    pages = divmod(len(textdata), 3)
    pagecount = pages[0]
    if pages[1] == 1:
        # Allow 4 lines of text if no next page
        pagecount = pages[0] - 1
    
    linecount = 0
    for textline in textdata:
        linecount += 1

        for c in textline:
            if (ord(c) in range(0x30, 0x3A)) or (ord(c) in range(0x41, 0x5B)) or (ord(c) in range(0x61, 0x7B)):
                newtext_bytes.append(ord(c))
            elif c == "#":
                # Using the pound sign as a stand in for "insert relevant Corridor number here"
                # Always 2 characters for hints
                newtext_bytes.append(ord(str(corridor_number)[0]))
                newtext_bytes.append(ord(str(corridor_number)[1]))
            elif c in tgl_special_chars.keys():
                newtext_bytes.append(tgl_special_chars[c])
            else:
                # Handle non-standard characters, replace with '?'
                newtext_bytes.append(0x3F)
        
        if linecount == len(textdata):
            # Some messages need different end of message handling, do this outside of call
            pass
        elif (linecount % 3 == 0) and (pagecount != 0):
            # Change text page after 3 lines if there are at least 2 more lines to write
            pagecount -= 1
            newtext_bytes.append(TEXT_NEXTPAGE)     
        else:
            newtext_bytes.append(TEXT_NEWLINE)
    return newtext_bytes
