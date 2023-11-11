from LtMAO.pyRitoFile import SKLJoint, read_skl, read_skn, write_skl, write_skn
from LtMAO.pyRitoFile.hash import Elf
from LtMAO.pyRitoFile.structs import Vector, Quaternion
from shutil import copy
import os.path

LOG = print


def skin_fix(skl_path, skn_path, riotskl_path, riotskn_path='', backup=True):
    # read skin
    LOG(f'sborf: Running: Read SKIN.')
    skl = read_skl(skl_path)
    riotskl = read_skl(riotskl_path)
    skn = read_skn(skn_path)
    riotskn = None
    if riotskn_path != '':
        riotskn = read_skn(riotskn_path)
    LOG(f'sborf: Done: Read SKIN.')

    new_joint_id_by_old_joint_id = {}
    new_joint_id_by_old_joint_id[-1] = -1  # for parent

    def joints_sort():
        LOG(f'sborf: Running: Sort joints.')
        new_joints = []
        flags = [True] * len(skl.joints)
        # sort with riot skl
        for riotjoint_id, riotjoint in enumerate(riotskl.joints):
            found = False
            riotjoint_name_lower = riotjoint.name.lower()
            for joint_id, joint in enumerate(skl.joints):
                if joint.name.lower() == riotjoint_name_lower:
                    old_id = joint.id
                    new_id = riotjoint_id
                    new_joint_id_by_old_joint_id[old_id] = new_id

                    joint.id = new_id
                    flags[joint_id] = False
                    found = True
                    new_joints.append(joint)
                    LOG(
                        f'sborf: Sorted: [{joint.id}] {joint.name} <- [{old_id}]')
                    break
            # fill removed rito joint back
            if not found:
                joint = SKLJoint()
                joint.id = riotjoint_id
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
                new_joints.append(joint)
                LOG(
                    f'sborf: Filled back: [{joint.id}] {joint.name}')
        # extra joints
        for joint_id, joint in enumerate(skl.joints):
            if flags[joint_id]:
                old_id = joint.id
                new_id = len(new_joints)
                new_joint_id_by_old_joint_id[old_id] = new_id
                joint.id = new_id
                flags[joint_id] = False
                new_joints.append(joint)
                LOG(
                    f'sborf: Moved new: [{joint.id}] {joint.name} <- [{old_id}]')
        skl.joints = new_joints
        # sort parent
        for joint in skl.joints:
            joint.parent = new_joint_id_by_old_joint_id[joint.parent]
        if len(skl.joints) > 256:
            raise Exception(
                f'sborf: Failed: Sort joints: Too many joints after sort: {len(skn.joints)}(>256), please check if Riot SKL is correct.')
        LOG(f'sborf: Done: Sort joints.')

    def influences_update():
        LOG(f'sborf: Running: Update influences.')
        for vertex in skn.vertices:
            vertex.influences = [new_joint_id_by_old_joint_id[inf]
                                 for inf in vertex.influences]
        LOG(f'sborf: Done: Update influences.')

    def materials_sort():
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

    joints_sort()
    influences_update()
    if riotskn != None:
        materials_sort()

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


def prepare(_LOG):
    global LOG
    LOG = _LOG
