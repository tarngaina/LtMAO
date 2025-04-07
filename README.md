# LtMAO-hai
`LtMAO-hai` is my toolpack to help League modding.
![](https://i.imgur.com/Uffi4Hu.png)

# Installation
1. Download: [LtMAO-hai.zip](https://github.com/tarngaina/LtMAO/archive/refs/heads/hai.zip)
2. Extract: `LtMAO-hai.zip`
3. Run `LtMAO-hai/start.bat`

# Updates
1. LtMAO always check for latest version when you open the app. If there is a newer version, the app will display update message in title bar.
2. To fully update: re-download the whole app from github and extract it to same location.
3. To lazily update LtMAO: press "Update LtMAO" button from setting page. This is not recommended but if it works, it works.

# Documentation
## Shortcut
1. Launch shortcut: When running the app for first time, a `LtMAO.lnk` (shortcut file) will be created in same folder as `start.bat`.

![](https://i.imgur.com/5eIWMKJ.png)

2. Desktop shortcut: Can be created in setting tab.


## File Explorer Context menu
Can be added/removed in setting tab.
**Note**: You can to run `LtMAO` as Admin through shortcut if you encounter permission error. 

![](https://i.imgur.com/f3XIP4M.png)

## cslmao
Just `cslol-manager`, but different UI.

**Important**: Need to set League of Legends/Game folder in first to work.

![](https://i.imgur.com/up0fEir.png)

## hash_helper
![](https://i.imgur.com/YWRnz5e.png)

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
    - Custom Hashes is hashes that used with all LtMAO related functions: ritobin, wad_tool, no_skin,...
    - Custom Hashes = CDTB Hashes + Extracted Hashes + User Manually Added Hashes

Also has generate wad & bin hash function. Those generated hashes can be added to Custom Hashes with buttons.

## mask_viewer
Edit MaskData's weights inside animation BINs.

![](https://i.imgur.com/kDz95rM.png)

## hapiBin
An app with multiple functions related to BIN file:

![](https://i.imgur.com/DqQqodH.png)

## no_skin
Create NO SKIN mod: Replace **almost** every League skins to default.

`SKIPS.json`: Some skins cause League to crash when they get changed to base. This file tell the program to not change those skins to base.

Has 2 modes:
1. Full: make a full `NO SKIN.fantome` of all champions inside League of Legends/Game/DATA/FINAL/Champions folder.
2. Lite: Make all selected `skinx.bin` become `skin0.bin`.

![](https://i.imgur.com/pJ0ESnw.png)

![](https://i.imgur.com/AfQyzFN.png)

## wad_tool
Simple tool to unpack, pack WAD files.

Can bulk unpack multiple WADs into same output. 

![](https://i.imgur.com/moBB7nz.png)

## sborf
Fix skin based on rito files: moonwalk animations, layering animations,...
Can also adapt your custom animation bin MaskData base on riot original files.

![](https://i.imgur.com/aOCdjtT.png)

## lemon3d
To work with League 3d files.

1. fbx:
![](https://i.imgur.com/XW74g8T.png)

Convert League files to FBX and vice versa.
Support: SKN, SKL, ANM. Todo: SCO, SCB, MAPGEO

2. maya:
![](https://i.imgur.com/MdMjFwO.png)
![](https://i.imgur.com/BWuIm1y.png)

`lol_maya` but rewritten, plugin for maya 2022+ with 3d.
Support: SKN, SKL, ANM, SCO, SCB. Todo: MAPGEO


More information on lemon3d will be in a separated page soon.

## ddsmart
Convert League texture files.

![](https://i.imgur.com/SP8N2xp.png)

## bnk_tool
Copy of `bnk-extract-GUI`, but extract `.wav` instead of `.ogg`.

![](https://i.imgur.com/StqeP24.png)

## wiwawe
Convert `wav` to `wem` and vice versa.

![](https://i.imgur.com/7kpfGS4.png)

# Extra:
- [LeagueToolKit](https://github.com/LeagueToolkit/LeagueToolkit)
- [CDTB](https://github.com/CommunityDragon/CDTB)
- [cslol-manager](https://github.com/LeagueToolkit/cslol-manager)
- [ritobin](https://github.com/moonshadow565/ritobin)
- [Hacksaw](https://github.com/TheMartynasXS/Hacksaw)
- [Uvee](https://github.com/LeagueToolkit/Uvee)
- [Ritoddstex](https://github.com/Morilli/Ritoddstex)
- [bnk-extract-GUI](https://github.com/Morilli/bnk-extract-GUI)