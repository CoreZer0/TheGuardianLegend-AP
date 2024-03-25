import os
from typing import TYPE_CHECKING, Tuple

import Utils
from BaseClasses import MultiWorld
from worlds.Files import APProcedurePatch, APTokenTypes, APTokenMixin
from .Items import TGL_ITEMID_BASE, balanced_rapid_fire
from .Locations import TGL_LOCID_BASE
from .Options import TGLOptions


#TGL_ITEMID_BASE = 8471760000
AP_ITEM_CODE = 21 # Red Chips
SHOP_JUNK_ITEM = 22 # Blue Chips

#class TGLDeltaPatch(APDeltaPatch):
class TGLProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = "5acfc9d45b94f82f97e04c4434adbf36"
    game = "The Guardian Legend"
    patch_file_ending = ".aptgl"
    result_file_ending = ".nes"

    procedure = [("apply_tokens", ["token_data.bin"])]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()
    
def write_tokens(multiworld: MultiWorld, player: int, options: TGLOptions, patch: TGLProcedurePatch) -> None:
    for location in multiworld.get_filled_locations(player):

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
                    location_rom_address = 0x1605e + (location_data[1] - 100)
                    patch.write_token(
                        APTokenTypes.WRITE, 
                        location_rom_address+1,
                        SHOP_JUNK_ITEM.to_bytes(1, 'little')
                    )
                    patch.write_token(
                        APTokenTypes.WRITE, 
                        location_rom_address+2,
                        SHOP_JUNK_ITEM.to_bytes(1, 'little')
                    )
                    #_set_bytes_little_endian(base_patch_rom, location_rom_address+1, 1, SHOP_JUNK_ITEM)
                    #_set_bytes_little_endian(base_patch_rom, location_rom_address+2, 1, SHOP_JUNK_ITEM)

                else:
                    location_rom_address = 0x16077 + location_data[1]
                

            # Corridor Item 
            elif location_data[0] == 3:
                location_rom_address = 0x1ef51 + location_data[1] - 1

                # Corridor bonus items, these are remote and not displayed in-game
            elif location_data[0] == 4:
                pass
            else:
                raise Exception('Invalid location ID found for The Guardian Legend.')
            
            # This should only be skipped if case 4 hit above because this is a Corridor item never shown in game
            # - Prevents the ROM header being edited and ROM failing to load 
            if location_rom_address != 0:
                # Local item: can change directly
                if location.item and location.item.player == player:
                    item_data: Tuple = divmod(get_internal_item_id(location.item.code), 1000)
            
                    # Check whether this is a drop item or a key
                    if item_data[0] == 1:
                        # Drop item
                        patch.write_token(
                            APTokenTypes.WRITE, 
                            location_rom_address,
                            item_data[1].to_bytes(1, 'little')
                        )
                         #_set_bytes_little_endian(base_patch_rom, location_rom_address, 1, item_data[1])
                
                        # Key item - treat as remote item
                    elif item_data[0] == 2:
                        patch.write_token(
                            APTokenTypes.WRITE, 
                            location_rom_address,
                            AP_ITEM_CODE.to_bytes(1, 'little')
                        )
                        #_set_bytes_little_endian(base_patch_rom, location_rom_address, 1, AP_ITEM_CODE)
                    else:
                        raise Exception('Invalid item ID found for The Guardian Legend.')

                # APItem: Set sprite to Red Chip in-game
                else:
                    patch.write_token(
                        APTokenTypes.WRITE, 
                        location_rom_address,
                        AP_ITEM_CODE.to_bytes(1, 'little')
                    )
                    #_set_bytes_little_endian(base_patch_rom, location_rom_address, 1, AP_ITEM_CODE)

    # Core changes
    # Remove the YOU GOT KEY popup in Corridors (TODO: Add to all Corridors, change message)
    # 0xEA is No-OP, removing the branch to the YOU GOT ITEM subroutine
    corridor_reward_popup_byte = 0x1F552
    patch.write_token(
        APTokenTypes.WRITE, 
        corridor_reward_popup_byte,
        0xEAEA.to_bytes(2, 'little')
    )
    #_set_bytes_little_endian(base_patch_rom, corridor_reward_popup_byte, 2, 0xEAEA)

    # Options-based changes
    if options.balanced_rapid_fire:
        rapid_fire_byte = 0x87DE
        for i in range(6):
            patch.write_token(
                APTokenTypes.WRITE, 
                rapid_fire_byte+i,
                balanced_rapid_fire[i].to_bytes(1, 'little')
            )
            #_set_bytes_little_endian(base_patch_rom, rapid_fire_byte+i, 1, balanced_rapid_fire[i])
        
    patch.write_file("token_data.bin", patch.get_token_binary())
    
    
def generate_output(multiworld: MultiWorld, player: int, output_directory: str, options: TGLOptions) -> None:
    patch = TGLProcedurePatch()
    write_tokens(multiworld, player, options, patch)

    #base_rom = get_base_rom_as_bytes()

    # Write output to patch file
    outfile_player_name = f"_P{player}"
    outfile_player_name += f"_{multiworld.get_file_safe_player_name(player).replace(' ', '_')}" \
        if multiworld.player_name[player] != f"Player{player}" else ""
    output_path = os.path.join(
                    output_directory, 
                    f"AP_{multiworld.seed_name}{outfile_player_name}{patch.patch_file_ending}"
                  )
    patch.write(output_path)

    '''
    with open(output_path, "wb") as outfile:
        outfile.write(base_patch_rom)
    patch = TGLDeltaPatch(os.path.splitext(output_path)[0] + ".aptgl", player=player,
                          player_name=multiworld.player_name[player], patched_path=output_path)
    patch.write()
    '''

'''
def _set_bytes_little_endian(byte_array: bytearray, address: int, size: int, value: int) -> None:
    offset = 0
    while size > 0:
        byte_array[address + offset] = value & 0xFF
        value = value >> 8
        offset += 1
        size -= 1
'''
        
def get_internal_item_id(item_id: int) -> int:
    return (item_id - TGL_ITEMID_BASE)

def get_internal_loc_id(loc_id: int) -> int:
    return (loc_id - TGL_LOCID_BASE)
    
def get_base_rom_as_bytes() -> bytes:
    options = Utils.get_options()
    file_name = options["guardianlegend_options"]["rom_file"]
    with open(file_name, "rb") as infile:
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes