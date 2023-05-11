# LtMAO
LtMAO is a toolpack to help League modding.
![](https://i.imgur.com/6rygiM7.png)

# Installation
1. Download: [LtMAO-master.zip](https://github.com/tarngaina/LtMAO/archive/refs/heads/master.zip)
2. Extract: `LtMAO-master.zip`
3. Run `LtMAO/start.bat`
4. Another `LtMAO.lnk` (launch shortcut) will be created in the same folder of `start.bat`. Next time, you can use `LtMAO.lnk` to launch `LtMAO` instead of `start.bat`.

# Documentation
## File Explorer Context menu
Can be added in LtMAO setting tab.

![](https://i.imgur.com/FqegQos.png)

## cslmao
Just [cslol-manager](https://github.com/LeagueToolkit/cslol-manager), but different UI.

![](https://i.imgur.com/EwbPaQW.png)

## leaguefile_inspector
View League files infomations.

![](https://i.imgur.com/2w9yyKH.png)

## animask_viewer
Edit MaskData's weights inside animation bins.

![](https://i.imgur.com/a0x8dQE.png)

## hash_manager
![](https://i.imgur.com/IeXNfKF.png)

- CDTB Hashes: Auto sync [CommunityDragon](https://github.com/CommunityDragon/CDTB/blob/master/cdragontoolbox/binfile.py) hashes.
- Extracted Hashes: Extract personally by user.
    - VfxSystemDefinitionData <-> particlePath from bin.
    - StaticMaterialDef <-> name from bin.
    - Joint hashes <-> names from skl.
    - Submesh hashes <-> names from skn.
- Custom Hashes:
    - Custom Hashes = CDTB Hashes + Extracted Hashes + User Manually Added Hashes
    - Hashes that used with all LtMAO related functions: leaguefile_inspector, ritobin, wad extract,...
    
## vo_helper
Make fantome work on all langs by cloning it.

![](https://i.imgur.com/YEafCGc.png)

## no_skin
Create NO SKIN mod: Replace **almost** every League skins to default.

![](https://i.imgur.com/wONCNnj.png)

![](https://i.imgur.com/AfQyzFN.png)


## uvee
[This app](https://github.com/LeagueToolkit/Uvee) but rewritten.
Extract UVs from skn/sco/scb as png files.

![](https://i.imgur.com/c9FZz8C.png)

## shrum
Rename joints in ANM using old names & new names input.
Can load SKL as inputs.

![](https://i.imgur.com/eOAOkbX.png)

## wad_tool
Simple tool to unpack, pack WAD files.
Can bulk unpack multiple WADs into same output.

![](https://i.imgur.com/bMV57O7.png)


# Extra:
- [LeagueToolKit](https://github.com/LeagueToolkit/LeagueToolkit)
- [CDTB](https://github.com/CommunityDragon/CDTB)
- [cslol-manager](https://github.com/LeagueToolkit/cslol-manager)
- [ritobin](https://github.com/moonshadow565/ritobin)
- [Uvee](https://github.com/LeagueToolkit/Uvee)

