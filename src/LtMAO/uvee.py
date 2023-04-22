import os
import os.path
from LtMAO.pyRitoFile import read_skn, read_scb, read_sco
from PIL import Image, ImageDraw

TEXTURE_SIZE = 1024
UV_COLOR = 0xFFFFFFFF
LOG = print


def uvee_skn(path):
    imgs = []
    # read file
    skn = read_skn(path)
    for submesh in skn.submeshes:
        # init values
        vertex_start = submesh.vertex_start
        vertex_end = vertex_start+submesh.vertex_count
        index_start = submesh.index_start
        index_end = index_start+submesh.index_count
        # get vertices, indices of this submesh
        vertices = skn.vertices[vertex_start:vertex_end]
        indices = skn.indices[index_start:index_end]
        # normalize indices
        min_index = min(indices)
        indices = [index-min_index for index in indices]
        index_count = len(indices)
        face_count = index_count // 3
        # create pil image
        img = Image.new('RGBA', (TEXTURE_SIZE, TEXTURE_SIZE))
        draw = ImageDraw.Draw(img)
        for i in range(face_count):
            vertex1 = vertices[indices[i*3]]
            vertex2 = vertices[indices[i*3+1]]
            vertex3 = vertices[indices[i*3+2]]
            draw.line((TEXTURE_SIZE * vertex1.uv.x, TEXTURE_SIZE * vertex1.uv.y, TEXTURE_SIZE *
                      vertex2.uv.x, TEXTURE_SIZE * vertex2.uv.y), fill=UV_COLOR)
            draw.line((TEXTURE_SIZE * vertex2.uv.x, TEXTURE_SIZE * vertex2.uv.y, TEXTURE_SIZE *
                      vertex3.uv.x, TEXTURE_SIZE * vertex3.uv.y), fill=UV_COLOR)
            draw.line((TEXTURE_SIZE * vertex3.uv.x, TEXTURE_SIZE * vertex3.uv.y, TEXTURE_SIZE *
                      vertex1.uv.x, TEXTURE_SIZE * vertex1.uv.y), fill=UV_COLOR)
        # save pil image
        dir = os.path.dirname(path)
        base = os.path.basename(path).replace('.skn', '')
        uvee_dir = dir+f'/uvee_{base}'
        if not os.path.exists(uvee_dir):
            os.makedirs(uvee_dir)
        img_path = os.path.join(
            uvee_dir, f'{submesh.name}.png').replace('\\', '/')
        img.save(img_path)
        LOG(f'Done: Extract UV: {img_path}')
        imgs.append((submesh.name, img))
    return imgs


def uvee_so(path):
    # read file
    if path.endswith('.sco'):
        so = read_sco(path)
    else:
        so = read_scb(path)
    # init values
    uvs = so.uvs
    face_count = len(uvs) // 3
    # create pil image
    img = Image.new('RGBA', (TEXTURE_SIZE, TEXTURE_SIZE))
    draw = ImageDraw.Draw(img)
    for i in range(face_count):
        uv1 = uvs[i*3]
        uv2 = uvs[i*3+1]
        uv3 = uvs[i*3+2]
        draw.line((TEXTURE_SIZE * uv1.x, TEXTURE_SIZE * uv1.y, TEXTURE_SIZE *
                   uv2.x, TEXTURE_SIZE * uv2.y), fill=UV_COLOR)
        draw.line((TEXTURE_SIZE * uv2.x, TEXTURE_SIZE * uv2.y, TEXTURE_SIZE *
                   uv3.x, TEXTURE_SIZE * uv3.y), fill=UV_COLOR)
        draw.line((TEXTURE_SIZE * uv3.x, TEXTURE_SIZE * uv3.y, TEXTURE_SIZE *
                   uv1.x, TEXTURE_SIZE * uv1.y), fill=UV_COLOR)
    # save pil image
    dir = os.path.dirname(path)
    base = os.path.basename(path).replace('.sco', '').replace('.scb', '')
    img_path = os.path.join(dir, f'uvee_{base}.png').replace('\\', '/')
    img.save(img_path)
    LOG(f'Done: Extract UV: {img_path}')
    return [(so.material, img)]


def uvee_file(path):
    if path.endswith('.skn'):
        try:
            return uvee_skn(path)
        except Exception as e:
            e.__repr__
            LOG(f'Failed: Extract UV: {path}: {e}')
    elif path.endswith('.scb') or path.endswith('.sco'):
        try:
            return uvee_so(path)
        except Exception as e:
            LOG(f'Failed: Extract UV: {path}: {e}')
    return None


def prepare(_LOG):
    global LOG
    LOG = _LOG
