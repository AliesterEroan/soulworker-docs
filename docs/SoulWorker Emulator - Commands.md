# SoulWorker Emulator - Commands

> Complete command reference for the SoulWorker emulator
> Source: `cmd sw.txt`

## Overview

This document provides a comprehensive reference for all available GM/admin commands in the SoulWorker emulator, including syntax, parameters, and usage examples.

---

## Command List

### Help
```
/help
```
Displays the command list.

---

## Item Commands

### Spawn Item
```
/item <id or name> [count]
```

Spawn an item by ID or name, optionally specifying quantity.

**Examples:**
- `/item 101161` - Spawn 1 Peta Brooch: First Blade
- `/item "Peta Brooch: Sky High" 5` - Spawn 5 Sky High brooches
- `/item 1085106 99` - Spawn 99 Excalibur swords

### Find Item
```
/find <name>
```

Search for an item by name and display its ID.

**Examples:**
- `/find Excalibur` - Find Excalibur's ID
- `/find "Peta Brooch"` - List all Peta Brooches

---

## Currency Commands

### Give Currency
```
/gold [0 | 1 | 2 | 3] <amount>
```

Add currency to your character. Use negative values to remove.

**Currency Types:**
- `0` - Zenny (main currency)
- `1` - Ether
- `2` - BP (Battle Points)
- `3` - Cash

**Examples:**
- `/gold 0 1000000` - Add 1,000,000 Zenny
- `/gold 1 5000` - Add 5,000 Ether
- `/gold 2 100` - Add 100 BP
- `/gold 3 10000` - Add 10,000 Cash
- `/gold 0 -50000` - Remove 50,000 Zenny

### Set Gold
```
/setgold <amount>
```

Set your Zenny to a specific amount (absolute value).

**Examples:**
- `/setgold 999999999` - Set Zenny to 999,999,999

### Give Ether
```
/ether <amount>
```

Add Ether to your character. Use negative values to remove.

**Examples:**
- `/ether 10000` - Add 10,000 Ether
- `/ether -500` - Remove 500 Ether

---

## Character Commands

### Set Level
```
/level <1-85>
```

Set your character level.

**Examples:**
- `/level 85` - Set to max level
- `/level 1` - Reset to level 1
- `/level 50` - Set to level 50

### Set Awakening
```
/awaken <0-3>
```

Set your advancement/awakening state.

**Advancement Levels:**
- `0` - Base class (no advancement)
- `1` - First advancement
- `2` - Desireworker (second advancement)
- `3` - Second advancement (includes all previous)

**Examples:**
- `/awaken 0` - Reset to base class
- `/awaken 1` - First advancement
- `/awaken 2` - Desireworker
- `/awaken 3` - Full second advancement

### Set Family Points
```
/fp <FP> [bonus FP]
```

Set your Family Points. Optionally set bonus FP.

**Examples:**
- `/fp 1000000` - Set FP to 1,000,000
- `/fp 500000 100000` - Set FP to 500,000 with 100,000 bonus

---

## Combat Commands

### Set Attack Speed
```
/aspd <1-250 | off>
```

Set attack speed percentage. 100 = normal speed.

**Examples:**
- `/aspd 100` - Normal attack speed
- `/aspd 200` - Double attack speed
- `/aspd 250` - Maximum attack speed
- `/aspd off` - Reset to default

### Set Movement Speed
```
/mspd <1-250 | off>
```

Set movement speed percentage. Same as aspd.

**Examples:**
- `/mspd 150` - 1.5x movement speed
- `/mspd off` - Reset to default

### Set Cooldown Reduction
```
/cooldown <0-100 | off>
```

Reduce skill cooldowns by percentage.

**Examples:**
- `/cooldown 50` - 50% cooldown reduction
- `/cooldown 100` - Instant skills (no cooldown)
- `/cooldown off` - Reset to default

### God Mode
```
/god [on | off]
```

Toggle god mode - no HP loss, no stuns or crowd control effects.

**Examples:**
- `/god on` - Enable god mode
- `/god off` - Disable god mode

### Set Soul Vapor
```
/sv <amount | max>
```

Set Soul Vapor (break skills gauge).

**Examples:**
- `/sv 5000` - Set SV to 5,000
- `/sv max` - Set SV to maximum

---

## Equipment & Buff Commands

### Add Buff
```
/buff <tb_Buff id>
```

Apply a buff by its table ID.

**Examples:**
- `/buff 1001` - Apply buff ID 1001

### Add Booster
```
/booster <tb_Booster id> | clear
```

Apply a booster or clear all boosters.

**Examples:**
- `/booster 500` - Apply booster ID 500
- `/booster clear` - Remove all boosters

### Set Durability
```
/durability <n>
```

Set durability of worn gear (capped at item's max durability).

**Examples:**
- `/durability 100` - Set gear durability to 100

### Set Desire Crystal
```
/core <level 0-9> [tb_Core_Skill id per slot ...]
```

Configure the worn Desire Crystal (Akashic Record core).

**Parameters:**
- `level` - Crystal level (0-9)
- Slot IDs - Core skill IDs for each slot

**Examples:**
- `/core 9` - Set level 9 crystal
- `/core 5 1001 1002 1003` - Level 5 crystal with specific skills

### Configure Akashic Records
```
/akashic <card id ... | all | pages <1-5> | reset>
```

Configure the Akashic Records book.

**Options:**
- `card id ...` - Add specific card IDs
- `all` - Unlock all cards for your class
- `pages <1-5>` - Unlock specific pages
- `reset` - Reset all cards

**Examples:**
- `/akashic all` - Unlock all cards
- `/akashic pages 1 2 3` - Unlock pages 1-3
- `/akashic reset` - Reset Akashic Records
- `/akashic 1001 1002 1003` - Add specific cards

---

## Pet Commands

### Configure Pet
```
/pet <group ... | all> [step=<1-50>] [level=<1-30>] | pieces <group> <n> | colorless <n> | reset
```

Configure pet stats and evolution.

**Options:**
- `group ...` - Specify pet group(s)
- `all` - All pets
- `step=<1-50>` - Set evolution step
- `level=<1-30>` - Set pet level
- `pieces <group> <n>` - Add evolution pieces
- `colorless <n>` - Add colorless pieces
- `reset` - Reset pet

**Examples:**
- `/pet all step=50 level=30` - Max all pets
- `/pet 1001 step=25 level=15` - Set specific pet
- `/pet pieces 1001 10` - Add 10 pieces for pet 1001
- `/pet colorless 50` - Add 50 colorless pieces
- `/pet reset` - Reset pet

---

## Title Commands

### Manage Titles
```
/title <title id ... | all | clear | del <id ...> | open <id ...>>
```

Manage character titles.

**Options:**
- `title id ...` - Add specific titles
- `all` - Unlock all titles for your class
- `clear` - Remove all titles
- `del <id ...>` - Delete specific titles
- `open <id ...>` - Open specific titles

**Examples:**
- `/title all` - Unlock all class titles
- `/title 1001 1002 1003` - Add specific titles
- `/title clear` - Remove all titles
- `/title del 1001` - Delete title 1001
- `/title open 1001` - Open title 1001

---

## NPC Commands

### Set NPC Credit/Loyalty
```
/credit <NPC group> <points>
```

Set NPC loyalty/credit points.

**NPC Groups:**
- `1004` - Trisha

**Examples:**
- `/credit 1004 5000` - Set Trisha loyalty to 5,000

---

## Inventory Commands

### Reset Inventory
```
/resetinven [bag | costume | cash | all]
```

Reset/clear inventory slots.

**Options:**
- `bag` - Clear main inventory
- `costume` - Clear costume inventory
- `cash` - Clear cash inventory
- `all` - Clear all inventories

**Examples:**
- `/resetinven bag` - Clear main inventory
- `/resetinven all` - Clear everything

---

## Teleportation Commands

### Teleport to District
```
/tp <town name or district id>
```

Teleport to a district/town area.

**Examples:**
- `/tp 10031` - Teleport to Grace City
- `/tp Grace City` - Teleport to Grace City
- `/tp 10061` - Teleport to Dipluce Horizon

### Enter Maze
```
/maze <maze id>
```

Enter a dungeon/instance by ID.

**Examples:**
- `/maze 21051` - Enter Golden Citadel
- `/maze 21017` - Enter Violent Sun
- `/maze 20101` - Enter Chapter 1

### Leave Maze
```
/leave
```

Leave the current maze/dungeon and return to town.

### Clear Maze
```
/clear
```

Instantly complete/clear the current maze run.

### View Location
```
/where
```

Display your current location (district and coordinates).

### Maze Entry Management
```
/entry [<maze id> | reset]
```

Check or reset maze entry counts.

**Options:**
- No argument - Show remaining entries for current maze
- `<maze id>` - Show entries for specific maze
- `reset` - Clear all entry counts

**Examples:**
- `/entry` - Check current maze entries
- `/entry 21051` - Check Golden Citadel entries
- `/entry reset` - Reset all entry counts

---

## Quest Commands

### Quest Management
```
/quest <list | accept | complete | force | giveup | cond | reset | skip> [id]
```

Manage quests.

**Options:**
- `list` - List available quests
- `accept [id]` - Accept a quest
- `complete [id]` - Complete a quest
- `force [id]` - Force complete a quest
- `giveup [id]` - Abandon a quest
- `cond [id]` - Show quest conditions
- `reset [id]` - Reset a quest (no ID = all)
- `skip [id]` - Skip a quest

**Examples:**
- `/quest list` - List quests
- `/quest accept 1001` - Accept quest 1001
- `/quest complete 1001` - Complete quest 1001
- `/quest force 1001` - Force complete quest 1001
- `/quest reset` - Reset all quests
- `/quest reset 1001` - Reset quest 1001
- `/quest skip 1001` - Skip quest 1001

---

## Account Commands

### PIN Management
```
/pin [reset]
```

Manage your account's second password (PIN).

**Options:**
- No argument - Show current PIN status
- `reset` - Remove PIN and unblock account

**Examples:**
- `/pin` - Check PIN status
- `/pin reset` - Remove PIN

---

## Quick Reference Tables

### Currency Types
| Type | Name | Command |
|------|------|---------|
| 0 | Zenny | `/gold 0 <amount>` |
| 1 | Ether | `/gold 1 <amount>` or `/ether <amount>` |
| 2 | BP | `/gold 2 <amount>` |
| 3 | Cash | `/gold 3 <amount>` |

### Awakening Stages
| Level | State | Command |
|-------|-------|---------|
| 0 | Base Class | `/awaken 0` |
| 1 | First Advancement | `/awaken 1` |
| 2 | Desireworker | `/awaken 2` |
| 3 | Second Advancement | `/awaken 3` |

### Inventory Resets
| Option | Description |
|--------|-------------|
| `bag` | Main inventory |
| `costume` | Costume inventory |
| `cash` | Cash shop inventory |
| `all` | All inventories |

---

## Related Documentation

- [[SoulWorker Emulator - Items]] - Item database and IDs
- [[SoulWorker Emulator - Warps]] - Warp locations and maze IDs

## Data Source

- **File**: `cmd sw.txt`
- **Date**: 2026-09-17
- **Region**: Global
