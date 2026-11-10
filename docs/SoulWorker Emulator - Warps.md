# SoulWorker Emulator - Warps

> Complete warp and location database for the SoulWorker emulator
> Source: `warps.txt`

## Overview

This document contains all warp IDs, district locations, portal connections, and maze/dungeon entries for the SoulWorker emulator.

## Location Types

### Districts (Town Areas)
Main hub areas where players can socialize, access NPCs, and enter dungeons. Use `/tp <id>` to teleport.

### Mazes (Dungeons/Instances)
Combat instances including story chapters, raids, casual raids, and special events. Use `/maze <id>` to enter.

---

## Districts

| ID | Name | World File | Start Box | Teleport Command |
|----|------|------------|-----------|------------------|
| 10001 | My Room | F001_TESTFIELD | 1000101 | `/tp 10001` |
| 10002 | Eternal Promise | SM03_CLOUDYWEDDINGHALL | 1000201 | `/tp 10002` |
| 10003 | Rocco Town | F031_ROCCOTOWN | 1000301 | `/tp 10003` |
| 10004 | Serenus Spica | SM04_SERENUSSPICA | 1000201 | `/tp 10004` |
| 10005 | Operation Stratos | SM08_DOMINIONY | 1000501 | `/tp 10005` |
| 10007 | Havets Fyrste | SM10_PIRATE_SHIP | 1000201 | `/tp 10007` |
| 10008 | Band Studio | SM12_LIVE_HOUSE | 1000201 | `/tp 10008` |
| 10021 | Candus City | F021_CANDUSCITY | 1002101 | `/tp 10021` |
| 10031 | Grace City | F041_GRACECITY | 1003101 | `/tp 10031` |
| 10041 | Ruin Fortress | F051_RUINFORTRESS | 1004101 | `/tp 10041` |
| 10051 | Grasscover Camp | F061_GRASSCOVERCAMP | 1005101 | `/tp 10051` |
| 10061 | Dipluce Horizon | F071_DIPLUCEHORIZON | 1006101 | `/tp 10061` |
| 10071 | Tower of Lord | F081_TOWEROFLORD | 1007101 | `/tp 10071` |
| 10081 | Arcadia Realm | F091_ARCADIAREALM | 1008102 | `/tp 10081` |
| 10091 | Etheldreda | F101_ETHEDLREDA | 1008102 | `/tp 10091` |
| 11001 | Golden Citadel Entry | DF01_GOLDENCITADEL | 1100101 | `/tp 11001` |

### Special Districts
- **101** - SimpleWorld (test area)
- **1001** - LoginBackground
- **1101-1124** - ClassSelect screens

---

## Portal Connections

### My Room (10001) Portals
| Portal ID | Type | Destination | Destination Box |
|-----------|------|-------------|-----------------|
| 10001 | Field | Rocco Town (10003) | 1000311 |
| 10002 | Field | Candus City (10021) | 1002101 |
| 10003 | Field | Grace City (10031) | 1003101 |
| 10004 | Field | Ruin Fortress (10041) | 1004101 |
| 21011 | Maze | Casual Raid (21012) | 2101201 |
| 21012 | Maze | Casual Raid (21012) | 2101201 |
| 21013 | Maze | Casual Raid (21013) | 2101301 |
| 21014 | Maze | Casual Raid (21014) | 2101401 |
| 21051 | Maze | Golden Citadel (21051) | 2105101 |

### Grace City (10031) Portals
| Portal ID | Type | Destination | Destination Box |
|-----------|------|-------------|-----------------|
| 21013 | Maze | Casual Raid (21013) | 2101301 |
| 21017 | Maze | Violent Sun (21017) | 2101701 |
| 21018 | Maze | Broken Savior (21018) | 2101801 |
| 21202 | Maze | The Beyond (21202) | 2120201 |
| 24018 | Maze | Broken Savior [Solo] (24018) | 2401801 |
| 23017 | Maze | Violent Sun [Solo] (23017) | 2301701 |
| 21031 | Maze | Violent Sun Hero [Solo] (21031) | 2103101 |
| 21032 | Maze | Violent Sun Hero [Party] (21032) | 2103101 |

### Candus City (10021) Portals
| Portal ID | Type | Destination | Destination Box |
|-----------|------|-------------|-----------------|
| 21012 | Maze | Casual Raid (21012) | 2101201 |
| 10061 | Field | Dipluce Horizon (10061) | 1006101 |

### Dipluce Horizon (10061) Portals
| Portal ID | Type | Destination | Destination Box |
|-----------|------|-------------|-----------------|
| 21016 | Maze | Hidden Hideout (21016) | 2101601 |
| 22061 | Maze | Lunar Fall (22061) | 2206101 |
| 22062 | Maze | Lunafall Hero [Party] (22062) | 2206201 |
| 22144 | Maze | Hidden Hideout Hero (22144) | 2214401 |

---

## Mazes (Dungeons)

### Story Chapters (Steel Grave)
| ID | Name | World File |
|----|------|------------|
| 20101-20125 | CHAPTER 1-5 | S01_STEELGRAVE |
| 20201-20210 | CHAPTER 6-7 | S02_STEELGRAVE |
| 20211-20215 | CHAPTER 8-10 | S02_STEELGRAVE |
| 20301-20325 | CHAPTER 11-15 | S03_STEELGRAVE |

### Casual Raids
| ID | Name | World File |
|----|------|------------|
| 21011 | Free Match | B03_BATTLECOURT |
| 21012 | Casual Raid | C02_JUNKHIVE |
| 21013 | Casual Raid | C03_BANDITSHIGHWAY |
| 21014 | Casual Raid | C04_IRONCASTLE |

### Major Raids
| ID | Name | World File |
|----|------|------------|
| 21015 | Altar of Void | C05_ALTAROFVOID |
| 21016 | Hidden Hideout | C06_HIDDENHIDEOUT |
| 21017 | Violent Sun | C08_VIOLENTSUN |
| 21018 | Broken Savior | C09_BROKENSAVIOR |
| 21019 | Tragic Fairy [HARD] | C10_TRAGEDYFAIRY |
| 21020 | Vile Predator [Guide] | C11_DOMINIONV |
| 21021-21022 | Collateral Damage [Party] | C12_COLLATERAL_DAMAGE |
| 21023-21028 | Rebellious Star | C10_RUGMAN / C10_RUGMAN_Party |

### Hero/Difficulty Variants
| ID | Name | World File |
|----|------|------------|
| 21031-21034 | Violent Sun Hero | C08_VIOLENTSUN_HERO |
| 21041-21046 | Broken Savior Hero | C09_BROKENSAVIOR_HERO |
| 21047 | Reckless Bravery | C09_BROKENSAVIOR_Awaken_A |
| 21048 | Inner Peace | E05_RUMBLEVACATION_Awaken_A |

### Golden Citadel
| ID | Name | World File |
|----|------|------------|
| 21051 | Golden Citadel | DR01_GOLDENCITADEL |
| 21061-21062 | The Primal | AR01_THEPRIMAL |
| 21071-21072 | Innocent Daydream | SM01_INNOCENTDAYDREAM |
| 21074 | Scary Daydream | SM01_INNOCENTDAYDREAM_THIRD |
| 21141-21142 | Skyclock Palace | E03_SKYCLOCKPALACE |

### Event Mazes
| ID | Name | World File |
|----|------|------------|
| 21115 | Break Room | T05_RESTROOM |
| 21121-21123 | Gruton World | E01_GLUTONWORLD |
| 21131 | Lonely Christmas | E02_LONELYCHRISTMAS |
| 21171 | Rumble Vacation | E05_RUMBLEVACATION |
| 21173-21174 | Strange Holiday | E09_LATESUMMERHOLIDAY |
| 21175 | Fireworks Festival | E10_FIREWORKSFESTIVAL |
| 21176 | Melodious Aurora | E11_MELODIOUSAURORA |
| 21177 | Void of Magic | E12_VOIDOFMAGIC |
| 21178 | Horizon of The Void | E13_HORIZONOFVOID |
| 21181 | Soul Jumper | E07_SOULJUMPER_N |
| 21191 | Moonlight Party | E08_MOONLIGHTPARTY |

### Control Zone 43
| ID | Name | World File |
|----|------|------------|
| 21211-21213 | Control Zone 43 EP01 | M03_CONTROLZONE43_EP01 |
| 21221-21223 | Control Zone 43 EP02 | M03_CONTROLZONE43_EP02 |
| 21231-21233 | Control Zone 43 EP03 | M03_CONTROLZONE43_EP03 |
| 21241-21243 | Control Zone 43 EP04 | M03_CONTROLZONE43_EP04 |
| 21244 | Control Zone 43 HERO | M03_CONTROLZONE43_HERO |

### Infinity Tower (Advancing Helix)
| ID | Name | World File |
|----|------|------------|
| 21401-21410 | Advancing Helix F1-10 | SM07_INFINITY_TOWER_01-10 |
| 21501-21510 | Advancing Helix F11-20 | SM07_INFINITY_TOWER_11-20 |
| 21601-21620 | Advancing Helix F21-40 | SM07_INFINITY_TOWER_21-40 |

### District 6 Episodes
| ID | Name | World File |
|----|------|------------|
| 21311-21343 | R Square EP01-04 | M04_RSQUARE_EP_01-04 |
| 21411-21444 | Best Showtime EP01-04 | M05_BESTSHOWTIME_EP_01-04 |
| 21511-21544 | Tower of Greed EP01-04 | M06_TOWEROFGREED_EP_01-04 |

### Lunar Fall
| ID | Name | World File |
|----|------|------------|
| 22061 | Lunar Fall | C07_LUNARFALL |
| 22062-22065 | Lunafall Hero | C07_LUNARFALL_HERO |

### Episode Dungeons (EP01-04)
| ID | Name | World File |
|----|------|------------|
| 22111-22143 | Concrete Jungle | M07_CONCRETEJUNGLE_EP_01-04 |
| 22211-22245 | Junk Pool | M08_JUNKPOOL_EP_01-04 |
| 22311-22343 | The Big Mouth | M09_THEBIGMOUTH_EP_01-04 |
| 22411-22443 | N102 Shelter | M10_N102SHELTER_EP_01-04 |
| 22511-22543 | Breakout | M11_BREAKOUT_EP_01-04 |
| 23111-23143 | Front Line | M12_FRONTLINE_EP_01-04 |
| 23211-23243 | NED Company | M13_NEDCOMPANY_EP_01-04 |
| 23311-23343 | Wolf Cry | M14_WOLFCRY_EP_01-04 |
| 23411-23443 | Cold Rain | M15_COLDRAIN_EP_01-04 |
| 23511-23543 | Flame Breaker | M16_FLAMEBREAKER_EP_01-04 |
| 23611-23643 | Area 9 | M17_AREA9_EP_01-04 |
| 24111-24143 | Control Base | M18_CONTROLBASE_EP_01-04 |
| 24211-24243 | Buster Core | M19_BUSTERCORE_EP_01-04 |
| 24311-24343 | Cold Revenge | M20_COLDREVENGE_EP_01-04 |
| 24411-24444 | Forgotten Armory | M21_FORGOTTENARMORY_EP_01-04 |
| 24511-24544 | Deep Core | M22_DEEPCORE_EP_01-04 |
| 24611-24644 | Acheron | M23_ACHERON_EP_01-04 |
| 24711-24744 | Ark Ship | M24_ARKSHIP_EP_01-04 |
| 25111-25143 | Dreadful Echo | M25_DREADFULECHO_EP_01-04 |
| 25211-25243 | Perforated Street | M26_PERFORATEDSTREET_EP_01-04 |
| 25311-25343 | Man Eater Garden | M27_MANEATERGARDEN_EP_01-04 |
| 25411-25443 | Dead Meat Factory | M28_DEADMEATFACTORY_EP_01-04 |
| 25511-25631 | Corrupted Record EP01-13 | M29_CORRUPTEDRECORD_EP_01-13 |
| 26111-26143 | Sky Walker | M32_SKYWALKER_EP_01-04 |
| 26211-26243 | Transport Fleet | M33_TRANSPORTFLEET_EP_01-04 |
| 26311-26343 | Betrayers' Army | M34_BETRAYERSARMY_EP_01-04 |
| 26411-26443 | Holy Ground | M35_HOLYGROUND_EP_01-04 |
| 26511-26543 | S303 Shelter | M36_S303SHELTER_EP_01-04 |
| 26611-26643 | Unholy Sanatarium | M37_UNHOLYSANATORIUM_EP_01-04 |
| 26711-26743 | Dawn of Fate | M38_DAWNOFFATE_EP_01-04 |
| 27111-27143 | White Out | M39_WHITEOUT_EP_01-04 |
| 27211-27243 | Project Resurrection | M40_RESURRECTIONPROJECT_EP_01-04 |
| 27311-27343 | Untouchable Pass | M41_UNTOUCHABLEPASS_EP_01-04 |
| 27411-27443 | Hell City | M42_HELLCITY_EP_01-04 |
| 27511-27543 | Blooming Road | M45_BLOOMINGROAD_EP_01-04 |
| 27611-27643 | Day Dreamer | M46_DAYDREAMER_EP_01-04 |
| 27711-27743 | Emergency Call | M47_EMERGENCYCALL_EP_01-04 |
| 27811-27843 | Doom of West | M48_DOOMOFWEST_EP_01-04 |
| 27911-27991 | Recapture Esseldreda EP01-09 | M56_RECAPTUREESSELDREDA_EP_01-09 |
| 28001-28009 | Undertown EP01-S03 | M58_UNDERTOWN_EP_01-S03 |
| 28011-28015 | Undertown 2 EP01-05 | M59_UNDERTOWN2_EP_01-05 |
| 28111-28131 | Cloud Border EP01-03 | M43_CLOUDBORDER_EP_01-03 |

### Special Mazes
| ID | Name | World File |
|----|------|------------|
| 25051-25052 | Golden Labyrinth | DR02-DR03_GOLDENCITADEL |
| 21100 | Abandoned Grave | Q01_ABANDONEDGRAVE |
| 21103 | Abandoned Grave (DW) | Q01_ABANDONEDGRAVE_DW |
| 21102 | Battle of the Void | Q02_BATTLEOFVOID |
| 21037 | Lost Number Laboratory | Q1_DanaQuest_01 |
| 21040 | Project Omega Headquarters | Q1_DanaQuest_02 |
| 21200 | Broken Savior | Q03_BROKENSAVIOR |
| 21201 | Epilogue | Q04_EPILOGUE |
| 21205 | The World's End | Q03_BROKENSAVIOR_D |
| 21301 | Prayers' Cloister | Q05_S2_PROLOGUE |
| 21202 | The Beyond | SM05_THEBEYOND |
| 21203-21204 | Parallel Metronome | SM06_PARALLELMETRONOME |

---

## Usage Commands

### Teleport to District
```
/tp <district id or name>
```

**Examples:**
- `/tp 10031` - Teleport to Grace City
- `/tp Grace City` - Teleport to Grace City
- `/tp 10061` - Teleport to Dipluce Horizon

### Enter Maze/Dungeon
```
/maze <maze id>
```

**Examples:**
- `/maze 21051` - Enter Golden Citadel
- `/maze 21017` - Enter Violent Sun
- `/maze 20101` - Enter Chapter 1

### View Current Location
```
/where
```

### Leave Current Maze
```
/leave
```

### Clear Current Maze
```
/clear
```

### Check Maze Entry Counts
```
/entry
```

### Reset Maze Entry Counts
```
/entry reset
```

---

## Portal Types

| Type | Description |
|------|-------------|
| **Field** | Teleports to another district/town |
| **Maze** | Enters a dungeon/instance |
| **JumpPos** | Teleports within the same district |
| **District6** | Special portal for District 6 content |

---

## Related Documentation

- [[SoulWorker Emulator - Items]] - Item database and spawning
- [[SoulWorker Emulator - Commands]] - Complete command reference

## Data Source

- **File**: `warps.txt`
- **Date**: 2026-09-17
- **Region**: Global
- **Source**: Client tables
