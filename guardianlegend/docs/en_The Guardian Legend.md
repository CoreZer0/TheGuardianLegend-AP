# The Guardian Legend (NES)

## Summary

A hybrid top-down exploration-adventure game like The Legend of Zelda, with scrolling shoot-em-up segments.

Developed by Compile, published by Irem/Broderbund in 1988.

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and
export a config file.

## What items and locations get shuffled?

All locations with one-time-only items are shuffled. More formally:

- All subweapons and upgrades, including Enemy Erasers
- Red Landers (ammo) and Blue Landers (health)
- Stat upgrades for attack power, defense power, and firing speed
- Keys for accessing later Areas

## What does another world's item look like in The Guardian Legend?

Items from other games will look like a Red Chip. Note that only static items (item boxes in rooms, and miniboss drops)
are shuffled. Enemies will still drop the regular Red Chip items and these are not part of Archipelago.

Items from TGL will look as usual, except for keys, which due to sprite limitations will also look like Red Chips as if
belonging to a different world.

## Are there any other changes made?

- Corridors no longer grant keys and these are shuffled in the item pool. Clearing Corridors will grant 2 item checks.
- Shops that have 3 items will always show one "good" item and 2 Blue Chips. Because of how shops work in TGL,
  Archipelago will always ensure the unique item is considered checked.

## Special Thanks

- Fireball87 for developing the map and enemy randomizer, which formed the basis of a lot of what's here.
- TailsMK4 for large amounts of research into RAM and ROM item and text data, and significant playtesting.
- Facet, Farren Bronaugh, MeowingKitty, Crypt1cmeta4, and others on the AP discord for feedback and playtesting.
