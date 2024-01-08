from .pyRitoFile import SKLJoint, read_skl, read_skn, write_skl, write_skn, read_bin, write_bin
from .pyRitoFile.hash import Elf
from .pyRitoFile.structs import Vector, Quaternion
from shutil import copy
import os.path
from .animask_viewer import find_mMaskDataMap, get_weights, set_weights

LOG = print


def skin_fix(skl_path, skn_path, riotskl_path, riotskn_path='', backup=True, dont_add_joint_back=False):
    # read skin
    LOG(f'sborf: Running: Read SKIN.')
    skl = read_skl(skl_path)
    riotskl = read_skl(riotskl_path)
    skn = read_skn(skn_path)
    riotskn = None
    if riotskn_path != '':
        riotskn = read_skn(riotskn_path)
    LOG(f'sborf: Done: Read SKIN.')

    # sort joint
    new_joint_id_by_old_joint_id = {}
    new_joint_id_by_old_joint_id[-1] = -1  # for parent
    LOG(f'sborf: Running: Sort joints.')
    new_joints = []
    extra_joints = [True] * len(skl.joints)
    # sort with riot skl
    for riotjoint_id, riotjoint in enumerate(riotskl.joints):
        found = False
        riotjoint_name_lower = riotjoint.name.lower()
        for joint_id, joint in enumerate(skl.joints):
            if joint.name.lower() == riotjoint_name_lower:
                new_id = len(new_joints)
                new_joint_id_by_old_joint_id[joint_id] = new_id
                new_joints.append(joint)
                LOG(
                    f'sborf: Sorted: [{new_id}] {joint.name} <- [{joint_id}]')
                extra_joints[joint_id] = False
                found = True
                break

        # fill removed rito joint back
        if not found:
            if dont_add_joint_back:
                LOG(
                    f'sborf: Missing: {joint.name}')
            else:
                joint = SKLJoint()
                joint.name = riotjoint.name
                joint.hash = Elf(joint.name)
                joint.radius = 2.1
                joint.parent = -1
                joint.local_translate = Vector(0.0, 0.0, 0.0)
                joint.local_rotate = Quaternion(0.0, 0.0, 0.0, 1.0)
                joint.local_scale = Vector(0.0, 0.0, 0.0)
                joint.ibind_translate = Vector(0.0, 0.0, 0.0)
                joint.ibind_rotate = Quaternion(0.0, 0.0, 0.0, 1.0)
                joint.ibind_scale = Vector(0.0, 0.0, 0.0)
                new_id = len(new_joints)
                new_joints.append(joint)
                LOG(
                    f'sborf: Filled back: [{new_id}] {joint.name}')
    # extra joints
    for joint_id, joint in enumerate(skl.joints):
        if extra_joints[joint_id]:
            new_id = len(new_joints)
            new_joint_id_by_old_joint_id[joint_id] = new_id
            new_joints.append(joint)
            LOG(
                f'sborf: Moved new: [{new_id}] {joint.name} <- [{joint_id}]')
    skl.joints = new_joints
    # sort parent
    for joint in skl.joints:
        joint.parent = new_joint_id_by_old_joint_id[joint.parent]
    if len(skl.joints) > 256:
        raise Exception(
            f'sborf: Failed: Sort joints: Too many joints after sort: {len(skn.joints)}(>256), please check if Riot SKL is correct.')
    LOG(f'sborf: Done: Sort joints.')

    # update influences
    LOG(f'sborf: Running: Update influences.')
    for vertex in skn.vertices:
        vertex.influences = [new_joint_id_by_old_joint_id[inf]
                             for inf in vertex.influences]
    LOG(f'sborf: Done: Update influences.')

    # sort materials
    if riotskn != None:
        LOG(f'sborf: Running: Sort materials.')
        new_submeshes = []
        flags = [True] * len(skn.submeshes)
        # sort with riot skn
        for riotsubmesh_id, riotsubmesh in enumerate(riotskn.submeshes):
            found = False
            riotsubmesh_name_lower = riotsubmesh.name.lower()
            for submesh_id, submesh in enumerate(skn.submeshes):
                if submesh.name.lower() == riotsubmesh_name_lower:
                    flags[submesh_id] = False
                    found = True
                    new_submeshes.append(submesh)
                    LOG(
                        f'sborf: Sorted: [{len(new_submeshes)-1}] {submesh.name} <- [{submesh_id}]')
                    break
            if not found:
                LOG(
                    f'sborf: Missing submesh: {riotsubmesh.name}')
        # extra submeshes
        for submesh_id, submesh in enumerate(skn.submeshes):
            if flags[submesh_id]:
                flags[submesh_id] = False
                new_submeshes.append(submesh)
                LOG(
                    f'sborf: Moved new: [{len(new_submeshes)-1}] {submesh.name} <- [{submesh_id}]')
        skn.submeshes = new_submeshes
        LOG(f'sborf: Done: Sort materials.')

    # backup skin
    if backup:
        LOG(f'sborf: Running: Backup SKIN.')
        backup_skl_path = os.path.join(
            os.path.dirname(skl_path),
            'sborf_backup_' + os.path.basename(skl_path)
        )
        copy(skl_path, backup_skl_path)
        backup_skn_path = os.path.join(
            os.path.dirname(skn_path),
            'sborf_backup_' + os.path.basename(skn_path)
        )
        copy(skn_path, backup_skn_path)
        LOG(f'sborf: Done: Backup SKIN.')
    # write skin
    LOG(f'sborf: Running: Write SKIN.')
    write_skl(skl_path, skl)
    write_skn(skn_path, skn)
    LOG(f'sborf: Done: Write SKIN.')
    LOG(f'sborf: Done: Fix SKIN.')


def maskdata_adapt(skl_path, riotskl_path, bin_path, riotbin_path, backup=True):
    # read skl and bin
    LOG(f'sborf: Running: Read SKL and Animation BIN.')
    skl = read_skl(skl_path)
    riotskl = read_skl(riotskl_path)
    bin = read_bin(bin_path)
    riotbin = read_bin(riotbin_path)
    LOG(f'sborf: Done: Read SKL and Animation BIN.')

    # get joints order
    new_joint_id_by_old_joint_id = {}
    new_joint_id_by_old_joint_id[-1] = -1  # for parent
    extra_joints = [True] * len(skl.joints)
    for riotjoint_id, riotjoint in enumerate(riotskl.joints):
        riotjoint_name_lower = riotjoint.name.lower()
        for joint_id, joint in enumerate(skl.joints):
            if joint.name.lower() == riotjoint_name_lower:
                new_joint_id_by_old_joint_id[joint_id] = riotjoint_id
                extra_joints[joint_id] = False

    # adapt mask_data
    LOG(f'sborf: Running: Adapt animation BIN MaskData.')
    binMDM = find_mMaskDataMap(bin)
    riotbinMDM = find_mMaskDataMap(riotbin)
    binMDM.data = riotbinMDM.data
    mask_data = {}
    riot_mask_data = get_weights(riotbin)
    for riot_mask_name in riot_mask_data:
        mask_data[riot_mask_name] = [0.0] * len(skl.joints)
        for joint_id, joint in enumerate(skl.joints):
            if not extra_joints[joint_id]:
                mask_data[riot_mask_name][joint_id] = riot_mask_data[riot_mask_name][new_joint_id_by_old_joint_id[joint_id]]
    set_weights(bin, mask_data)
    LOG(f'sborf: Done: Adapt animation BIN MaskData.')

    # backup skin
    if backup:
        LOG(f'sborf: Running: Backup Animation BIN.')
        backup_bin_path = os.path.join(
            os.path.dirname(bin_path),
            'sborf_backup_' + os.path.basename(bin_path)
        )
        copy(bin_path, backup_bin_path)
        LOG(f'sborf: Running: Backup Animation BIN.')
    # write skin
    LOG(f'sborf: Running: Write Animation BIN.')
    write_bin(bin_path, bin)
    LOG(f'sborf: Done: Write Animation BIN.')
    LOG(f'sborf: Done: Adapt MaskData.')


def prepare(_LOG):
    global LOG
    LOG = _LOG
