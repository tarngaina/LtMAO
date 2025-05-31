# Lemon3d

## lemon_fbx 
This tool focus on `blender` more than maya, if you use maya use lemon_maya instead.

Here is some `required` blender fbx export settings:

![](https://i.imgur.com/0ikEMll.png)

- Scale 0.01: Scale in blender is 100x bigger compare to maya, this setting reduce scale 100 times back.
- Triangualate Faces: This setting is a must, because League use triangualated mesh.
- No Leaf Bones: "_end" bones that blender fbx plugin added for some reason, we don't wan those joints.
- First frame of animation: This frame need to be bindpose of the model. How: Go to bindpose -> Move to first frame -> press I to set keyframe.

`Bonus stuffs related to maya:` Some animation converted to fbx look very wrong in maya, to fix this problem: change all rotate curve to quaternion slerp by `Graph editor -> Select rotation curves -> Graph editor toolbar -> Change Rotation Interp -> Quaternion Slerp`.

![](https://i.imgur.com/QWVPuRM.png)

## lemon_maya

![](https://i.imgur.com/cRpMpYt.gif)

### File translators:

1. Misc:

- Export base on original file: This is very important, some data can't be loaded into maya and can only retrieve though original files.

- How to: have at least 1 of 2 files below in export directory:
    - `riot_{name of export file}.EXT` (take priority first)
    - `riot.EXT`

- File type support (`EXT`):
    - SKN: Fix incorrect transparent faces on champions.
    - SKL: Fix bad animation blending of champions that have animation layers.
    - MAPGEO: Always need otherwise map will crash.

- Example: If you want to export modified `yone_base.skl` base on original file, you must have either `riot_yone_base.skl` or `riot.skl` in export directory; if you have both of them, `riot_yone_base.skl` will take priority.

2. SKIN:

- A skin group of joints and meshes:
    
    ![](https://i.imgur.com/F75UyHQ.png)

- All meshes must:
    - Have materials and UVs assigned on all faces.
    - Have ll UVs in first UV set.
    - Have all face normals point inward. 
    - Bound with joints as a skin cluster and have weight painted on all vertices.

- To export: 
    - Select the skin group that contains skin meshes and joints -> export.
    - Both SKN and SKL will be export together.

- Limit vertices: 65535. (UVs count in `Display -> Head Ups Display -> PolyCount`)

3. ANM:

- Translate + Rotate + Scale keyframes of all joints in scene from animation start time + 1 to animation end time on Time Slider. 

- If the animation time range is -5 to 14 like in the below picture, keyframes will be exported from time -4 (-5+1) to 14.

    ![](https://i.imgur.com/T44RI0q.png)

- Import options:

    ![](https://i.imgur.com/HlKCKc7.png)

    - Reset scene channel, time, range before import: Delete existing scene animations (all channel) before load another ANM file.
    - Framerate import & Animation range: Override to Match Source: Make sure enable this to load fps and duration of anm file to scene.

- FPS support: 30/60.

- To export: No need to select anything -> export.

4. Static object:

- A single mesh must: 
    - Have UVs assigned on all faces and in first UV set.
    - Have all face normals point inward.
    
- Central point: is translate of mesh's transform.

- Pivot point (SCO only, optional): is translate of an additional joint that bound with mesh.

    ![](https://i.imgur.com/XZFvV3V.png)

- To export: Select the single static object mesh -> export.

- Export options: For `scb only`: Should always use `HasLocalOriginLocatorAndPivot` flag to prevent wrong scb position in game.

    ![](https://i.imgur.com/flRWkin.png)

5. Mapgeo:

- A group of meshes that must
    - Have materials and UVs assigned on all faces.
    - Have all face normals point inward.

    ![](https://i.imgur.com/3Gl705M.png)

- Material:
    - Material names in MAPGEO files or in BIN files are used with `/`, this character can't be used in Maya, so all `/` will be converted to `__` when import, and will be converted back to `/` when export. 
    - Example:
        - In mapgeo or bin: `Maps/KitPieces/Howling_Abyss/Materials/Keep_inst`
        - In Maya: `Maps__KitPieces__Howling_Abyss__Materials__Keep_inst`

- Layer: 
    - A map must have 8 layers, equal to 8 `set` in Maya.

        ![](https://i.imgur.com/uxlcYsw.png)

    - If a mesh is assigned to a layer, it will appear on that layer in game.
    - A mesh can be assigned to multiple layers, if it is assigned on all 8 layers, it will appear on all 8 layers.
    - Layer only important in Summoner Rift (SR):
        - Layer 1: Base 
        - Layer 2: Inferno drake map
        - Layer 3: Mountain drake map
        - Layer 4: Ocean drake map
        - Layer 5: Cloud drake map
        - Layer 6: Hextech drake map
        - Layer 7: Chemtech drake map
        - Layer 8: Unknown
        - Example in SR: if mesh assigned to `set2` -> that object will appear in layer 2 - Inferno map.
    - Layer in Aram, TFT and other maps: all meshes are always assigned to all 8 layers.

- Bushes:
    - Similar to Layers, a map also must have `setBushes` to indicate which mesh is a bush.
    
        ![](https://i.imgur.com/7Gn8C2v.png)
    
    - If a mesh is assigned to `setBushes`, it is bush. (yep)

- Bucket Hash:
    - All mesh imported to maya will have an extra attribute called `Bucket Hash` and this `Bucket Hash` tell which mesh will appear on 3 Baron specific area or Athakan area.

        ![](https://i.imgur.com/ypbAftg.png)
    
    - `Bucket Hash`: is a FNV1a hash value that can be found in `materials.bin`. When exporting, if your entered value that is not a correct hash, the mesh will be exported with default value: 0.

- Bucket Grid and Planar Reflector (Important):
    - These things can only be achieved by exporting base on original MAPGEO file. (aka `riot.mapgeo` method)
    - If you export without `riot.mapgeo`, the modified map will likely crash League or event worse, freeze you computer.

- Lightmap (Optional):
    - 2nd texture & 2nd UVs set to store light data, will blend with main texture (1st texture & 1st UVs set) in game.
    - Lightmap contains two things: Name and UVs

        ![](https://i.imgur.com/JLKRvQz.png)

    - Name: 
        - If there is no lightmap: The group name can be whatever it is.
        - If there is lightmap: The group name must be lightmap folder path and have `lm_` before it. Example: In Aram, keep this name if you want original lightmap work.
        
            ![](https://i.imgur.com/lNhQr7R.png)
            
            Example: Lightmap name of above image is in TFT `inkbiome_sky.mapgeo`: `ASSETS/Maps/Lightmaps/Maps/MapGeometry/Map22/InkBiome_Sky/2.dds`
    - UVs: 2nd UV set of mesh, can be generated by a button on shelf.
    - You don't need to have Lightmap if you can bake light straight into main texture, like Riot did with SR.   

- To export: select the group of map meshes -> export.
    - Limit vertices for each mesh: 65535.
    - Diffuse UVs must be in 1st UV set; if model uses Lightmap, Lightmap UVs must be in 2nd UV set.
- Export options:

    ![](https://i.imgur.com/Molq7GF.png)

    - Version: 17 for SR map and 13 for Aran, TFT maps,...
    - Half Float: Enable this for TFT maps only.

### Shelf buttons

1. General Shelf:

![](https://i.imgur.com/rxVetvM.png)

- Namespace buttons: Quickly add/remove a temporary namespace on selected objects.
- Separated mesh button: Separate selected mesh by materials, will delete weights.
- Fix shared vertices button, will delete weights.
- Martin UV helper: move selected UVs to specific corner of the main UV square.
- Update bind pose button: set current pose as bind pose for skin cluster, require: select single joint of the skin cluster.
- Freeze joints buttons: Freeze/bake selected/all joints rotation.
- Rebind button: Quickly unbind, delete history, rebind selected skin cluster.

2. Mapgeo Shelf:

![](https://i.imgur.com/T1leVkM.png)

- Rename selected objects with input prefix. 
- Rename path of selected objects with input prefix.
- Toggle on/off all layers on selected mesh.
- Toggle on/off layer 1 - 8 on selected mesh.
- Assigned to / remove from `setBushes` on selected mesh.
- Show and edit info on selected mesh such as layers, is bush and bucket hash.

    ![](https://i.imgur.com/5yd1AGG.png)

- Select all member that has non-zero `Bucket Hash` value.
- Select all faces of all meshes that have same assigned material as selected face.
- Fix shared vertices on all meshes in scene.
- Import materials: Read `materials.bin` and `WAD` folder to import textures.
- Export materials: Export all materials to a selected `materials.bin` file.
- Check if materials of selected meshes are not defined in `materials.bin`, if nothing get selected, this button will check all materials in scene instead.
- Generate Lightmap UVs on 2nd UV set of selected objects.
- Delete Lightmap UVs and 2nd UV set of selected objects.
- Bake texture: bake textures with [Arnold](https://arnoldrenderer.com/download/) on selected objects.
    
    ![](https://i.imgur.com/4bEXne8.png)
    
    - Output: Location of output baked textures.
    - No diffuse:
        - On: Bake only light - use 2nd UV set of selected objects and default material `standardSurface1` to bake.
        - Off: Bake with diffuse - use 1st UV set of selected objects and their own materials to bake.
    - Quality: You will want High quality bake for diffuse and Low quality bake for lightmap.
    - Resolution: Resolution of baked textures; integer input, should be 256, 512, 1024,...