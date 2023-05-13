# LtMAO
`LtMAO` is my toolpack to help League modding.
![](https://i.imgur.com/2V04RbW.png)

# Installation
1. Download: [LtMAO-master.zip](https://github.com/tarngaina/LtMAO/archive/refs/heads/master.zip)
2. Extract: `LtMAO-master.zip`
3. Run `LtMAO/start.bat`

# Documentation
## Shortcut & How to Run as Admin
1. Launch shortcut: When running the app for first time, a `LtMAO.lnk` (shortcut file) will be created in same folder as `start.bat`. You can run `LtMAO` as Admin through `LtMAO.lnk`.

![](https://i.imgur.com/YRsKEVm.png)

2. Desktop shortcut: Can be created inside setting tab.

## File Explorer Context menu
Can be added in setting tab.

![](https://i.imgur.com/LVJ2Cfw.png)

## cslmao
Just [cslol-manager](https://github.com/LeagueToolkit/cslol-manager), but different UI.
Need to set Game folder inside setting tab first to work.

![](https://i.imgur.com/EwbPaQW.png)

## leaguefile_inspector
View League files infomations.

![](https://i.imgur.com/2w9yyKH.png)

## animask_viewer
Edit MaskData's weights inside animation bins.

![](https://i.imgur.com/a0x8dQE.png)

## hash_manager
![](https://i.imgur.com/IeXNfKF.png)

Important: Wait for finish syncing/updating/loading all hashes before process with any LtMAO functions.
1. CDTB Hashes: Auto sync [CommunityDragon](https://github.com/CommunityDragon/CDTB/tree/master/cdragontoolbox) hashes. Can also be manually downloaded at mentioned link. 
2. Extracted Hashes: Extract personally by user.
    Hashes that can be extracted:
        - VfxSystemDefinitionData <-> particlePath from bin.
        - StaticMaterialDef <-> name from bin.
        - Joint hashes <-> names from skl.
        - Submesh hashes <-> names from skn.
        - All file path that starts with `assets/` or `data/`.
3. Custom Hashes:
    - Custom Hashes = CDTB Hashes + Extracted Hashes + User Manually Added Hashes
    - Custom Hashes is hashes that used with all LtMAO related functions: leaguefile_inspector, ritobin, wad_tool,...
    
## vo_helper
Make fantome work on all langs by cloning it.

![](https://i.imgur.com/YEafCGc.png)

## no_skin
Create NO SKIN mod: Replace **almost** every League skins to default.
`SKIPS.json`: Some skins cause League to crash when they get changed to base. This file tell the program to not change them back to base.

![](https://i.imgur.com/wONCNnj.png)

![](https://i.imgur.com/AfQyzFN.png)


## uvee
[Uvee](https://github.com/LeagueToolkit/Uvee) but rewritten.
Extract UVs from skn/sco/scb as png files.

![](https://i.imgur.com/c9FZz8C.png)

## shrum
Rename joints in ANM using old names & new names input.
Can load SKL as inputs.

![](https://i.imgur.com/eOAOkbX.png)

## wad_tool
Simple tool to unpack, pack WAD files.
Can bulk unpack multiple WADs into same output. Example: Bulk unpacking all voiced wad then throw into vo_helper is a fast way to create a champion langue voice mod.

![](https://i.imgur.com/bMV57O7.png)


# Extra:
- [LeagueToolKit](https://github.com/LeagueToolkit/LeagueToolkit)
- [CDTB](https://github.com/CommunityDragon/CDTB)
- [cslol-manager](https://github.com/LeagueToolkit/cslol-manager)
- [ritobin](https://github.com/moonshadow565/ritobin)
- [Uvee](https://github.com/LeagueToolkit/Uvee)

