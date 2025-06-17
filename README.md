# LtMAO-hai
`LtMAO-hai` is my toolpack to help League modding.
![](https://i.postimg.cc/W4HnKJXs/screenshot-14.png)

# Installation
1. Download: [LtMAO-hai.zip](https://github.com/tarngaina/LtMAO/archive/refs/heads/hai.zip)
2. Extract: `LtMAO-hai.zip`
3. Run `LtMAO-hai/start.bat`

# Updates
1. LtMAO-hai always check for latest version when you open the app. If there is a newer version, the app will display update message in title bar.
2. To fully update: re-download the whole app from github and extract it to same location.
3. To lazily update LtMAO: press "Redownload LtMAO" button from setting page. This is not recommended but if it works, it works.

# Documentation
## Shortcut
1. Launch shortcut: When running the app for first time, a `LtMAO.lnk` (shortcut file) will be created in same folder as `start.bat`.

![](https://i.imgur.com/5eIWMKJ.png)

2. Desktop shortcut: Can be created in setting tab.

## Theme
You can create your custom theme by making a new folder in `LtMAO-hai/res/themes`.

Your custom image sizes must be same ratio as original images.

The accent color of the app will be the dominant color of your `background.gif`.

If there is "_" in theme name, the accent color will be a gradient between the most 2 dominant colors.

![](https://i.imgur.com/Gn9bz17.png)

## cslmao
Just `cslol-manager`, but different UI.

**Important**: To make cslmao work -> Click `Show settings` in the top right cornet -> Set `League of Legends/Game` folder.

![](https://i.postimg.cc/BZdzbR5J/screenshot-0.png)

## hash_helper

![](https://i.postimg.cc/7Y0W2XX0/screenshot-1.png)

**Important:** Please wait for all syncing/updating/loading hashes finished before process with any `LtMAO` functions.

1. CDTB Hashes: Auto sync [CommunityDragon](https://github.com/CommunityDragon/CDTB/tree/master/cdragontoolbox) hashes. Can also be manually downloaded at mentioned link. 
2. Extracted Hashes: Extract personally by user. Hashes that can be extracted:
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

`hash_helper` also has generate wad & bin hash tool. Those generated hashes can be added to Custom Hashes with buttons.

## mask_viewer
Edit MaskData's weights inside animation BINs.

![](https://i.postimg.cc/TPY7BxxJ/screenshot-2.png)

## hapiBin
An app with multiple functions related to BIN file.

![](https://i.postimg.cc/kgChF8hZ/screenshot-3.png)

## no_skin
Create NO SKIN mod: Replace **almost** every League skins to default.

![](https://i.imgur.com/AfQyzFN.png)

`SKIPS.json`: Some skins cause League to crash when they get changed to base. This file tell the program to not change those skins to base.

Has 2 modes:
1. Full: make a full `NO SKIN.fantome` of all champions inside `League of Legends/Game/DATA/FINAL/Champions` folder.

![](https://i.postimg.cc/ht0ZCjkG/screenshot-4.png)

2. Lite: Make all selected `skinx.bin` become `skin0.bin`.

![](https://i.postimg.cc/c18DpTp2/screenshot-7.png)

## wad_tool
Simple tool to unpack, pack WAD files.

Can bulk unpack multiple WADs into same output with filter. 

![](https://i.postimg.cc/qRNmMGzt/screenshot-5.png)

## sborf
Fix skin based on rito files: moonwalk animations, layering animations,...

Can also adapt your custom animation bin MaskData base on riot original files.

![](https://i.postimg.cc/KzC0KgM0/screenshot-6.png)

## lemon3d
Tool to work with League 3d files.

1. fbx:
![](https://i.postimg.cc/q7bbTFMV/screenshot-8.png)

Convert League files to FBX and vice versa.

This tool mainly support `blender`, for maya please use the maya plugin.

Support: SKN, SKL, ANM. Todo: SCO, SCB, MAPGEO

2. maya:
![](https://i.postimg.cc/L6Ky2LRX/screenshot-9.png)

![](https://i.imgur.com/BWuIm1y.png)

`lol_maya` but rewritten, plugin for maya 2023+ with 3d.

Support: SKN, SKL, ANM, SCO, SCB, MAPGEO.


[Click here to read full document of lemon3d](src/LtMAO/lemon3d/README.md)

## texsmart
Convert League texture files.

![](https://i.postimg.cc/pXfsTrXB/screenshot-10.png)

## bnk_tool
Copy of `bnk-extract-GUI`, but extract `.wav` instead of `.ogg`.

![](https://i.postimg.cc/Dw55rNGJ/screenshot-11.png)

## wiwawe
Convert audio files.

![](https://i.postimg.cc/6Q3cYhVH/screenshot-12.png)

## winLT
Custom LtMAO explorer context menu.

![](https://i.imgur.com/f3XIP4M.png)

**Important**: You must run `LtMAO` as Admin through shortcut to bypass permission error. 

![](https://i.postimg.cc/W3qnPbHg/screenshot-13.png)

# Extra:
- [LeagueToolKit](https://github.com/LeagueToolkit/LeagueToolkit)
- [CDTB](https://github.com/CommunityDragon/CDTB)
- [cslol-manager](https://github.com/LeagueToolkit/cslol-manager)
- [ritobin](https://github.com/moonshadow565/ritobin)
- [Hacksaw](https://github.com/TheMartynasXS/Hacksaw)
- [Uvee](https://github.com/LeagueToolkit/Uvee)
- [Ritoddstex](https://github.com/Morilli/Ritoddstex)
- [bnk-extract-GUI](https://github.com/Morilli/bnk-extract-GUI)