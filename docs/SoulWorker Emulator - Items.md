# SoulWorker Emulator - Items

> Comprehensive item database for the SoulWorker emulator (global 2026-09-17)
> Source: `items.txt`

## Overview

This document contains the complete item database from the client `tb_Item` table. Items are organized by ID, name, group type, bag slot, and stack limit.

## Item Structure

| Column | Description |
|--------|-------------|
| **id** | Unique item identifier |
| **name** | Item name (English) |
| **group** | Item category/type |
| **bag** | Inventory bag slot type |
| **stack** | Maximum stackable quantity |

## Item Groups

- **Main_Weapon** - Primary weapons for characters
- **Gear** - Armor and equipment pieces
- **Accessory** - Accessories (rings, earrings, pendants)
- **Equip_Reg** - Regular equipment/Peta Brooches
- **Title** - Character titles
- **Money** - Currency items
- **Func** - Functional items/consumables

## Key Item Categories

### Peta Brooches (Skill Brooches)
Peta Brooches are skill-enhancing items with the following pattern:
- **Format**: `Peta Brooch: [Skill Name]`
- **Bound Version**: `Bound Peta Brooch: [Skill Name]`
- **Stack Limit**: 99
- **Bag Type**: 13

Examples:
- `101161` - Peta Brooch: First Blade
- `201161` - Peta Brooch: Sky High
- `301161` - Peta Brooch: Evil Slash

### Character-Specific Equipment Sets

#### Haru (Sword Class)
- Supportive Nostalgic Vanguard (1079101)
- Sealed weapons (1085101-1085113)
- Voidsteel armor sets (1085201-1085255)

#### Erwin (Gun Class)
- Supportive Nostalgic Dualist (1179101)
- Sealed weapons (1185101-1185113)

#### Lily (Scythe Class)
- Supportive Nostalgic Executor (1279101)
- Sealed weapons (1285101-1285113)

#### Stella (Fist Class)
- Supportive Nostalgic Infighter (1379101)
- Sealed weapons (1385101-1385113)

#### Jin (Guitar Class)
- Supportive Nostalgic Minstrel (1479101)
- Sealed weapons (1485101-1485113)

#### Iris (Cannon Class)
- Supportive Nostalgic Crusader (1579101)
- Sealed weapons (1585101-1585113)

#### Chii (Sword Class)
- Supportive Nostalgic Warlord (1679101)
- Sealed weapons (1685101-1685113)

#### Ephnel (Spear Class)
- Supportive Nostalgic Phalanx (1779101)
- Sealed weapons (1785101-1785113)

#### Tenebris (Sword Class)
- Supportive Nostalgic Skirmisher (1879101)
- Sealed weapons (1885101-1885113)

#### Nabi (Fan Class)
- Supportive Nostalgic Tailor (1979101)
- Sealed weapons (1985101-1985113)

### Re-Tag Chips (Titles)
Title modification items:
- `61001` - Re-Tag Chip: Rebellious
- `61002` - Re-Tag Chip: Informative
- `61003` - Re-Tag Chip: Annoying
- `61004` - Re-Tag Chip: Playful

### Currency Items
- `700001` - [EV] Blooming Wildflowers (Money)

### Event & Functional Items
Various event packages and functional items (IDs 2000001+)

## Usage Notes

### Finding Items
Use the command:
```
/find <item name>
```

### Spawning Items
Use the command:
```
/item <id or name> [count]
```

**Examples:**
- `/item 101161` - Spawn Peta Brooch: First Blade
- `/item "Peta Brooch: Sky High" 5` - Spawn 5 of Sky High brooch
- `/item 1085106 1` - Spawn Excalibur

## Related Documentation

- [[SoulWorker Emulator - Warps]] - Warp locations and maps
- [[SoulWorker Emulator - Commands]] - Complete command reference

## Data Source

- **File**: `items.txt`
- **Date**: 2026-09-17
- **Region**: Global
- **Source**: Client `tb_Item` table
