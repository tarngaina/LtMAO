# LtMAO
`LtMAO` is my toolpack to help League modding.
![](https://i.imgur.com/S6fEl1f.png)

# Installation
1. Download: [LtMAO-master.zip](https://github.com/tarngaina/LtMAO/archive/refs/heads/master.zip)
2. Extract: `LtMAO-master.zip`
3. Run `LtMAO/start.bat`

# Updates
If you see [new commit here](https://github.com/tarngaina/LtMAO/commits/master), that means there is new update. You can check the commit description to see what changed.
To update new version: re-download the app and extract it to same location.

# Documentation
## Shortcut & How to Run as Admin
1. Launch shortcut: When running the app for first time, a `LtMAO.lnk` (shortcut file) will be created in same folder as `start.bat`.

![](https://i.imgur.com/YRsKEVm.png)

2. Desktop shortcut: Can be created in setting tab.

 You can run `LtMAO` as Admin through shortcut.

## File Explorer Context menu
Can be added/removed in setting tab.

![](https://i.imgur.com/LVJ2Cfw.png)

## cslmao
Just [cslol-manager](https://github.com/LeagueToolkit/cslol-manager), but different UI.

**Important**: Need to set Game folder in setting tab first to work.

![](https://i.imgur.com/GcjDQcs.png)

## leaguefile_inspector
View League files infomations.

![](https://i.imgur.com/l5VvEWu.png)

## animask_viewer
Edit MaskData's weights inside animation BINs.

![](https://i.imgur.com/m9YkgeB.png)

## hash_manager
![](https://i.imgur.com/2KTMiET.png)

**Important:** Please wait for all syncing/updating/loading hashes finished before process with any `LtMAO` functions.
1. CDTB Hashes: Auto sync [CommunityDragon](https://github.com/CommunityDragon/CDTB/tree/master/cdragontoolbox) hashes. Can also be manually downloaded at mentioned link. 
2. Extracted Hashes: Extract personally by user.
    
    Hashes that can be extracted:
    - binentries:
        - VfxSystemDefinitionData -> particlePath in BIN.
        - StaticMaterialDef -> name in BIN.
    - binhashes: 
        - Joint hashes -> joint names in SKL.
        - Submesh hashes -> submesh names in SKN.
    - game:
        - File path that starts with `assets/` or `data/` in BIN. If file type is `.dds`, extract 2x, 4x dds too.
3. Custom Hashes:
    - Custom Hashes is hashes that used with all LtMAO related functions: leaguefile_inspector, ritobin, wad_tool,...
    - Custom Hashes = CDTB Hashes + Extracted Hashes + User Manually Added Hashes

Also has generate wad & bin hash function. Those generated hashes can be added to Custom Hashes with `->` buttons.
## vo_helper
Make fantome work on all langs by cloning it.

**Important**: The audio inside fantome must also come with events file to make it work on other langs.

![](https://i.imgur.com/fhXoShs.png)

## no_skin
Create NO SKIN mod: Replace **almost** every League skins to default.

`SKIPS.json`: Some skins cause League to crash when they get changed to base. This file tell the program to not change those skins to base.

![](https://i.imgur.com/YHWYuwP.png)

![](https://i.imgur.com/AfQyzFN.png)


## uvee
[Uvee](https://github.com/LeagueToolkit/Uvee) but rewritten.
Extract UVs from skn/sco/scb as png files.

![](https://i.imgur.com/qYtVMge.png)

## shrum
Rename joints in ANM using old names & new names input.

Can load SKL as inputs.

![](https://i.imgur.com/PQrU5eO.png)

## hapiBin
An app with multiple functions related to updating BIN file:
- Copy linked list.
- Copy vfx colors.


![](https://i.imgur.com/eYyYNhO.png)

## wad_tool
Simple tool to unpack, pack WAD files.

Can bulk unpack multiple WADs into same output. 
**Example:** Bulk unpacking all voiced wad then throw into [vo_helper](https://github.com/tarngaina/LtMAO#vo_helper) is a fast way to create a champion voicepack for specific language mod.

![](https://i.imgur.com/61wpQJ3.png)


## pyntex
[Hacksaw/bintex](https://github.com/TheMartynasXS/Hacksaw) but rewritten.
Print out mentioned & missing files in all BINs inside a WAD or a Folder.

![](https://i.imgur.com/Tj5GPV6.png)


## sborf
Fix skin based on rito files: moonwalk animations, layering animations,...

![](https://i.imgur.com/kAPOapL.png)


## lol2fbx
Convert League files to FBX and vice versa.

![](https://i.imgur.com/lIpTpdJ.png)

# Extra:
- [LeagueToolKit](https://github.com/LeagueToolkit/LeagueToolkit)
- [CDTB](https://github.com/CommunityDragon/CDTB)
- [cslol-manager](https://github.com/LeagueToolkit/cslol-manager)
- [ritobin](https://github.com/moonshadow565/ritobin)
- [Hacksaw](https://github.com/TheMartynasXS/Hacksaw)
- [Uvee](https://github.com/LeagueToolkit/Uvee)
- [Ritoddstex](https://github.com/Morilli/Ritoddstex)