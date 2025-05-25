ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

def GetName(node):
    return ''.join(c if c in ALPHANUMERIC else f'FBXASC{ord(c):03}' for c in node.GetNameOnly().Buffer())

def mirrorX(skl=None, skn=None, anm=None):
    if skl != None:
        for joint in skl.joints:
            joint.local_translate.x = -joint.local_translate.x
            joint.local_rotate.y = -joint.local_rotate.y
            joint.local_rotate.z = -joint.local_rotate.z
            joint.ibind_translate.x = -joint.ibind_translate.x
            joint.ibind_rotate.y = -joint.ibind_rotate.y
            joint.ibind_rotate.z = -joint.ibind_rotate.z
    if skn != None:
        for vertex in skn.vertices:
            vertex.position.x = -vertex.position.x
            if vertex.normal != None:
                vertex.normal.y = -vertex.normal.y
                vertex.normal.z = -vertex.normal.z
    if anm != None:
        for track in anm.tracks:
            for time in track.poses:
                pose = track.poses[time]
                if pose.translate != None:
                    pose.translate.x = -pose.translate.x
                if pose.rotate != None:
                    pose.rotate.y = -pose.rotate.y
                    pose.rotate.z = -pose.rotate.z