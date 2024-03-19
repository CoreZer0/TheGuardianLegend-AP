from typing import TYPE_CHECKING, List, Tuple

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Items import TGLItem, TGLItemData, red_lander_thresholds, TGL_ITEMID_BASE, get_itemname_by_id
from .Locations import TGLLocation, TGLLocationData, TGL_LOCID_BASE, get_locationcode_by_bitflag

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

# Everything here shamelessly adapted from Pokemon Emerald :)

#TODO: Figure this out
EXPECTED_ROM_NAME = "TGL AP Hack"
ROM_CHIP_MAX = 0x87E6
ROM_RAPID_FIRE_LEVELS = 0x87CE

# RAM Address list

# 0x0178-0x017b *appear* to be unused

RAM_ITEMS_RECEIVED = 0x17a # ctx.items_received index

RAM_KEYS_RECEIVED = 0x17b # Remote Key items as sent by AP, in case in game value gets changed

# RAM Address for item locations grabbed bitmap (4A0-4A8, exact values stored in TGLLocationData)
RAM_LOCATIONS_CHECKED = 0x4A0

# RAM Address for cleared corridor bitmap (1-20 sequence over 3 bytes)
RAM_CORRIDORS_CLEARED = 0x4A9

RAM_CORRIDORS_OPENED = 0x4B1 # 2 bytes

# RAM Address for Subweapon levels (0-3 levels per weapon, 2 bits per weapon over 3 bytes)
RAM_SUBWEAPON_LEVELS = 0x4AC

# RAM Address for key bitmap (1-7 in sequence), checked by the game
RAM_KEYS_INGAME = 0x4B0

RAM_EE_COUNT = 0x4AF

RAM_RED_LANDER_COUNT = 0x46
RAM_CURRENT_CHIPS = 0x4C # 2 bytes
RAM_MAX_CHIPS = 0x4E # 2 bytes

RAM_MAX_HEALTH = 0x47
RAM_CURRENT_HEALTH = 0x48

RAM_ATTACK_LEVEL = 0x4A
RAM_DEFENSE_LEVEL = 0x4B
RAM_RAPID_FIRE_LEVEL = 0x6B
RAM_SHOT_SPEED = 0x39

RAM_GAME_STATE = 0x30
RAM_ROOM_NUMBER = 0x51
RAM_MUSIC_ID = 0x3DD
RAM_ENDING_FLAG = 0x1FF # usually this is 0xFF, but 0x82 in sound check and 0x8B during ending

class TGLClient(BizHawkClient):
    game = "The Guardian Legend"
    system = "NES"
    patch_suffix = ".aptgl"

    opened_corridors: bool
    message_interval_set: bool
    

    def __init__(self) -> None:
        super().__init__()
        self.opened_corridors = False
        self.message_interval_set = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        # TODO: Everything
        
        try:
            # Currently validating ROM against the first 4 bytes in the MAX CHIPs table
            # TODO: Probaby want a longer string (like the full chip table)
            # NOTE: if randomized MAX CHIPs added, this will have to be changed/adapted 
            rom_valid_bytes = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(ROM_CHIP_MAX, 4, "PRG ROM")]
            )
            # reading as one long number in byte order, so need big-endian in this caw
            rom_valid_num = int.from_bytes(rom_valid_bytes[0], 'big')
            if not rom_valid_num == 0xA00F7017:
                logger.info("ERROR: This is not a valid The Guardian Legend ROM file.")
                return False
        except bizhawk.RequestFailedError:
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b011

        return True


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        
        # main watch loop
        try:
            # Check it's safe to receive items (probably just in game, not on title screen or save room?)
            # - Music Player channel ids (0x03DD-0x3DF), should be 01 on title only
            # - The game state bitflags (0x0030) set bit 8 (0x80) for demo mode
            # - And there's a sound check so we need to make sure we're not in that either
            check_safety_bytes = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (RAM_GAME_STATE, 1, "RAM"),
                    (RAM_MUSIC_ID, 1, "RAM"),
                    (RAM_ENDING_FLAG, 1, "RAM")
                ]
            )
            check_demo_byte = int.from_bytes(check_safety_bytes[0], 'little')
            check_music_id = int.from_bytes(check_safety_bytes[1], 'little')
            check_ending_flag = int.from_bytes(check_safety_bytes[2], 'little')

            check_demo_bit = (check_demo_byte & (1 << 7)) >> 7

            if not self.message_interval_set:
                await bizhawk.set_message_interval(ctx.bizhawk_ctx, 2)
                self.message_interval_set = True
            
            # If we're in title screen or demo mode or sound check, skip this loop
            if (check_music_id == 1) or (check_demo_bit == 1) or (check_ending_flag == 0x82):
                self.opened_corridors = False
                return
            
            # Check and send game clear - Music code 0F (at 0x3DD)
            if (not ctx.finished_game) and (check_music_id == 0xF) and (check_ending_flag == 0x8B):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                return 
            
            # Set the flags to open all Corridors - should reset any time we go to title screen
            if not self.opened_corridors:
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [(RAM_CORRIDORS_OPENED, int(0x03FF).to_bytes(2, 'little'), "RAM")]
                )
                self.opened_corridors = True

            # Handle giving the player items from the received items list
            # save index of received items array to RAM
            read_item_count = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(RAM_ITEMS_RECEIVED, 1, "RAM")]
            )
            if read_item_count is None:
                raise Exception("Failed to read stored item count.")
            
            num_new_items = int.from_bytes(read_item_count[0], 'little')
            granted_item = bool(False)
            
            if num_new_items < len(ctx.items_received):
                next_item_id = ctx.items_received[num_new_items].item

                # remote items (including this client's Keys) always get processed
                is_remote_item = not ctx.slot_concerns_self(ctx.items_received[num_new_items].player)

                # location id < 0 indicates cheat console or server item, we always need to process those
                # location id in 4000s indicated bonus corridor item that also needs to be handled
                item_loc = ctx.items_received[num_new_items].location
                is_special_item = (item_loc < 0) or (item_loc - TGL_LOCID_BASE >= 4000) 
                next_item_type:Tuple = divmod(next_item_id - TGL_ITEMID_BASE, 1000)

                # Determine how to handle the item based on type:
                if (next_item_type[0] == 1) and (is_remote_item or is_special_item):
                    ap_item_message = f"AP: You received your {get_itemname_by_id(next_item_id)}!"
                    await bizhawk.display_message(ctx.bizhawk_ctx, ap_item_message)
                    
                    # Drop item
                    # Subweapons are 2 bits per, stored over 3 bytes - need to add 1 level if less than 3 total
                    if next_item_type[1] <= 10:
                        item_index = next_item_type[1] * 2
                        item_mask = 0b11 << item_index
                        read_item_bytes = await bizhawk.read(
                            ctx.bizhawk_ctx, 
                            [(RAM_SUBWEAPON_LEVELS, 3, "RAM")]
                            )
                        itemlevel_bytes = int.from_bytes(read_item_bytes[0], 'little')
                        current_itemlevel_count = (itemlevel_bytes & item_mask) >> item_index
                        if current_itemlevel_count < 3:
                            add_one_itemlevel = itemlevel_bytes + (1 << item_index)
                            granted_item = await bizhawk.guarded_write(
                                ctx.bizhawk_ctx,
                                [(RAM_SUBWEAPON_LEVELS, add_one_itemlevel.to_bytes(3, 'little'), "RAM")],
                                [(RAM_SUBWEAPON_LEVELS, read_item_bytes[0], "RAM")]
                            )
                        else:
                            granted_item = bool(True)
                       
                    elif next_item_type[1] == 11:
                        # Enemy Eraser is one byte - add 20 (TODO: or option value) to a max of 255 
                        # - also need to set subweapon bit (see above)
                        item_mask = 1 << 6
                        read_item_bytes = await bizhawk.read(
                            ctx.bizhawk_ctx, 
                            [
                                (RAM_SUBWEAPON_LEVELS + 2, 1, "RAM"),
                                (RAM_EE_COUNT, 1, "RAM")]
                            )
                        add_ee_count = (int.from_bytes(read_item_bytes[1])) + 20
                        if add_ee_count > 255:
                            add_ee_count = 255
                        itemlevel_bytes = int.from_bytes(read_item_bytes[0], 'little')
                        # Enemy Eraser only has one level, but player can't use unless this bit is set
                        has_ee = ((itemlevel_bytes & item_mask) == item_mask)
                        set_ee = itemlevel_bytes
                        if not has_ee:
                             set_ee += item_mask
                        granted_item = await bizhawk.guarded_write(
                            ctx.bizhawk_ctx,
                            [
                                (RAM_SUBWEAPON_LEVELS + 2, set_ee.to_bytes(1, 'little'), "RAM"),
                                (RAM_EE_COUNT, add_ee_count.to_bytes(1, 'little'), "RAM")
                            ],
                            [(RAM_EE_COUNT, read_item_bytes[1], "RAM")]
                        )
                    elif (next_item_type[1] == 12) or (next_item_type[1] == 13):
                        # Energy Tank is max health - read Max, set Current to Max
                        read_item_bytes = await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(RAM_MAX_HEALTH, 1, "RAM")]
                        )
                        # Blue Lander add +8 to max health and refill
                        max_health = int.from_bytes(read_item_bytes[0])
                        if (next_item_type[1] == 13) and (max_health < 240):
                            max_health += 8
                        granted_item = await bizhawk.guarded_write(
                            ctx.bizhawk_ctx,
                            [
                                (RAM_MAX_HEALTH, max_health.to_bytes(1,'little'), "RAM"),
                                (RAM_CURRENT_HEALTH, max_health.to_bytes(1,'little'), "RAM")
                            ],
                            [(RAM_MAX_HEALTH, read_item_bytes[0], "RAM")]
                        )
                    elif next_item_type[1] == 14:
                        # Attack up - read current, check against max, add 1 if < max (4)
                        read_item_bytes = await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(RAM_ATTACK_LEVEL, 1, "RAM")]
                        )
                        stat_level = int.from_bytes(read_item_bytes[0], 'little')
                        if stat_level < 4:
                            stat_level += 1
                            granted_item = await bizhawk.guarded_write(
                                ctx.bizhawk_ctx,
                                [(RAM_ATTACK_LEVEL, stat_level.to_bytes(1, 'little'), "RAM")],
                                [(RAM_ATTACK_LEVEL, read_item_bytes[0], "RAM")]
                            )
                        else:
                            granted_item = bool(True)
                    elif next_item_type[1] == 15:
                        # Defense up - read current, check against max, add 1 if < max (7)
                        read_item_bytes = await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(RAM_DEFENSE_LEVEL, 1, "RAM")]
                        )
                        stat_level = int.from_bytes(read_item_bytes[0], 'little')
                        if stat_level < 7:
                            stat_level += 1
                            granted_item = await bizhawk.guarded_write(
                                ctx.bizhawk_ctx,
                                [(RAM_DEFENSE_LEVEL, stat_level.to_bytes(1, 'little'), "RAM")],
                                [(RAM_DEFENSE_LEVEL, read_item_bytes[0], "RAM")]
                            )
                        else:
                            granted_item = bool(True)
                    elif next_item_type[1] == 16:
                        # Rapid Fire up - read current, check against max, add 1 if < max (5)
                        # Also need to manually set shot speed
                        read_item_bytes = await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(RAM_RAPID_FIRE_LEVEL, 1, "RAM")]
                        )
                        stat_level = int.from_bytes(read_item_bytes[0], 'little')
                        if stat_level < 5:
                            stat_level += 1
                            read_rapid_fire_level = await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(ROM_RAPID_FIRE_LEVELS+stat_level, 1, "PRG ROM")]
                            )
                            shot_speed = int.from_bytes(read_rapid_fire_level[0], 'little')
                            granted_item = await bizhawk.guarded_write(
                                ctx.bizhawk_ctx,
                                [
                                    (RAM_RAPID_FIRE_LEVEL, stat_level.to_bytes(1, 'little'), "RAM"),
                                    (RAM_SHOT_SPEED, shot_speed.to_bytes(1, "little"), "RAM")
                                ],
                                [(RAM_RAPID_FIRE_LEVEL, read_item_bytes[0], "RAM")]
                            )
                        else:
                            granted_item = bool(True)  
                    elif next_item_type[1] == 17:
                        # Red Landers increase Max Chips 
                        # - read current count, add one, set chip max to correct value, set Current to new Max 
                        read_item_bytes = await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(RAM_RED_LANDER_COUNT, 1, "RAM")]
                        )
                        red_lander_count = int.from_bytes(read_item_bytes[0])
                        if red_lander_count < 10:
                            red_lander_count += 1
                            chip_max = red_lander_thresholds[red_lander_count]
                            granted_item = await bizhawk.guarded_write(
                                ctx.bizhawk_ctx,
                                [
                                    (RAM_RED_LANDER_COUNT, red_lander_count.to_bytes(1,'little'), "RAM"),
                                    (RAM_MAX_CHIPS, chip_max.to_bytes(2, 'little'), "RAM"),
                                    (RAM_CURRENT_CHIPS, chip_max.to_bytes(2, 'little'), "RAM")
                                ],
                                [(RAM_RED_LANDER_COUNT, read_item_bytes[0], "RAM")]
                            )
                        # If there are 10 Red Landers in pool this should never be hit
                        else:
                            granted_item = bool(True)
                        
                    else:
                        raise Exception("Invalid item number ID sent to The Guardian Legend.")
                
                # For non-key items, these don't need to be received from server so just note it and skip it    
                elif (next_item_type[0] == 1) and not is_remote_item:
                    granted_item = bool(True)

                # Keys item - we save what keys we think the player should have,
                # - and write that value over the key bitmap in game
                elif next_item_type[0] == 2:
                    ap_item_message = f"AP: You received your {get_itemname_by_id(next_item_id)}!"
                    await bizhawk.display_message(ctx.bizhawk_ctx, ap_item_message)

                    if next_item_type[1] < 7:
                        read_key_data = await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(RAM_KEYS_RECEIVED, 1, "RAM")]
                        )
                        add_key_bit = 1 << next_item_type[1]
                        new_key_flags = int.from_bytes(read_key_data[0], 'little') | add_key_bit
                        granted_item = await bizhawk.guarded_write(
                            ctx.bizhawk_ctx,
                            [
                                (RAM_KEYS_RECEIVED, new_key_flags.to_bytes(1, 'little'), "RAM"),
                                (RAM_KEYS_INGAME, new_key_flags.to_bytes(1, 'little'), "RAM")
                            ],
                            [(RAM_KEYS_RECEIVED, read_key_data[0], "RAM")]
                        )
                    else:
                        raise Exception("Invalid Key flag sent to The Guardian Legend.")
                else:
                    raise Exception("Invalid item type ID sent to The Guardian Legend.")
                
            # if we managed to make a successful write, increment the item counter
            if granted_item:
                num_new_items += 1
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [(RAM_ITEMS_RECEIVED, num_new_items.to_bytes(1, 'little'), "RAM")],
                )
            # Area Key overwrite failsafe
            # Overwrite key flags in case the game gives us a key before AP thinks we should have it
            read_key_data = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (RAM_KEYS_RECEIVED, 1, "RAM"),
                    (RAM_KEYS_INGAME, 1, "RAM")
                ]
            )
            if not (read_key_data[0] == read_key_data[1]):
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [(RAM_KEYS_INGAME, read_key_data[0], "RAM")]
                )

            # Send local checked locations
            # Read the RAM for location checks
            read_location_flags = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (RAM_LOCATIONS_CHECKED, 9, "RAM"),
                    (RAM_CORRIDORS_CLEARED, 3, "RAM")
                ]
            )
            location_flag_bits = int.from_bytes(read_location_flags[0], 'little')
            corridor_flag_bits = int.from_bytes(read_location_flags[1], 'little')
            # Figure out what the new locations are, send to AP
            for i in range(68):
                if (location_flag_bits & (1 << i)) !=0:
                    locbits = divmod(i, 8)
                    locid = get_locationcode_by_bitflag((locbits[0], 1 << locbits[1]))
                    if locid not in ctx.checked_locations:
                        ctx.locations_checked.add(locid)
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [locid]}])

            # Corridors 1-20
            # Send 2 location IDs per corridor, one is a bonus item for game balance 
            for j in range(20):
                if (corridor_flag_bits & (1 << j)) !=0:
                    locbits = divmod(j, 8)
                    locid = get_locationcode_by_bitflag((locbits[0] + 9, 1 << locbits[1]))
                    locid_bonus = locid + 1000
                    checks_out: List[int] = []
                    if locid not in ctx.checked_locations:
                        ctx.locations_checked.add(locid)
                        checks_out.append(locid)
                    if locid_bonus not in ctx.checked_locations:
                        ctx.locations_checked.add(locid_bonus)
                        checks_out.append(locid_bonus)
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checks_out}])

        except bizhawk.RequestFailedError:
            pass
