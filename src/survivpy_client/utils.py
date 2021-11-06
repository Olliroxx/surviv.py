from math import sin, cos, sqrt
from arcade import Texture
from arcade import load_texture as get_tex_data
import survivpy_client


def load_texture(name: str, rotation=0, scale=(1, 1), *args, **kwargs):
    if name.endswith(".img"):
        name = name[:-4] + ".png"
    tex = get_tex_data(survivpy_client.ASSET_ROOT + name, *args, **kwargs)
    if rotation:
        tex = Texture(tex.name + "-rot" + str(rotation), tex.image.rotate(rotation, expand=True))

    if scale != (1, 1):
        raw = tex.image
        new_size = (i * j for i, j in zip(scale, tex.size))
        new = raw.resize(new_size)
        tex = Texture(tex.name + "-scale" + str(scale), new)

    return tex


def scale_texture(tex: Texture, x, y):
    raw = tex.image
    new_size = [round(i * j) for i, j in zip([x, y], raw.size)]
    new = raw.resize(new_size)
    tex = Texture(tex.name + "-scale" + str((x, y)), new)
    return tex


def rotate_vector(x, y, angle):
    new_x = x * cos(angle) - y * sin(angle)
    new_y = y * cos(angle) + x * sin(angle)
    return new_x, new_y


def normalise_vec(x, y, center=(400, 300)):
    mx, my = x - center[0], y - center[1]
    mag = sqrt(mx ** 2 + my ** 2)

    if not mag:
        return -1, 0

    return mx / mag, my / mag


def num_to_colour(num) -> tuple[int, int, int]:
    """
    In surviv, colours are stored as a single number, the decimal representation of the hex colour code. This function
    reverses that

    :param num:
    :return:
    """

    all_ones = (1 << 8) - 1
    return (num & (all_ones << 16)) >> 16, (num & (all_ones << 8)) >> 8, num & all_ones
