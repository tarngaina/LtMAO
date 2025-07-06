import os, os.path
from . import lepath, pyRitoFile
from PIL import Image, ImageDraw

TEXTURE_SIZE = 1024
UV_COLOR = 0xFFFFFFFF

def uvee_skn(path):
    imgs = []
    # read file
    skn = pyRitoFile.skn.SKN().read(path)
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
        base = lepath.ext(os.path.basename(path), '.skn', '')
        uvee_dir = dir+f'/uvee_{base}'
        os.makedirs(uvee_dir, exist_ok=True)
        img_path = lepath.join(
            uvee_dir, f'{submesh.name}.png')
        img.save(img_path)
        print(f'uvee: Finish: Extract UV: {img_path}')
        imgs.append((submesh.name, img))


def uvee_so(path):
    # read file
    if path.endswith('.sco'):
        so = pyRitoFile.so.SO().read_sco(path)
    else:
        so = pyRitoFile.so.SO().read_scb(path)
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
    base = lepath.ext(lepath.ext(os.path.basename(path), '.sco', ''), '.scb', '')
    img_path = lepath.join(dir, f'uvee_{base}.png')
    img.save(img_path)
    print(f'uvee: Finish: Extract UV: {img_path}')


def uvee_file(path):
    if path.endswith('.skn'):
        uvee_skn(path)
    elif path.endswith('.scb') or path.endswith('.sco'):
        uvee_so(path)


