def array_cutout(array, x, y, w, h):
    """
    Creates a cutout of a big array

    :param array: input array
    :param x: x of top left corner of cutout
    :param y: y of top left corner of cutout
    :param w: width of cutout
    :param h: height of cutout
    :return: cutout
    """
    return [array[i][x:x+w] for i in range(y, y+h)]


def grab_pngs(to_parse):
    """
    Takes in a image map string from the JS source, downloads the big images and cuts them up into smaller images
    """
    import json
    import os
    import multiprocessing

    try:
        os.mkdir("out")
    except FileExistsError:
        pass
    try:
        os.mkdir("out/pngs")
    except FileExistsError:
        pass

    from shutil import rmtree
    rmtree("out/pngs")
    del rmtree
    os.mkdir("out/pngs")
    os.mkdir("out/pngs/raw")

    if type(to_parse) == str:
        parsed = json.loads(to_parse)
    elif type(to_parse) == dict:
        parsed = to_parse
    else:
        raise TypeError("Input must be either string or dict")

    with multiprocessing.Pool() as pool:
        pool.starmap(write_bigimage, tuple(parsed.items()))


def write_bigimage(key, parse_data):
    from requests import get
    import png
    from os import mkdir, listdir

    if key == "raw":
        raise RuntimeError("Very unlikely name collision")

    try:
        mkdir("./out/pngs/" + key)
    except FileExistsError:
        pass

    for bigimage_number in range(len(parse_data)):
        bigimage = parse_data[bigimage_number]
        bigimage_name = bigimage["meta"]["image"]

        cwd = "./out/pngs/" + key + "/" + str(bigimage_number)

        try:
            mkdir(cwd)
        except FileExistsError:
            pass

        if listdir(path=cwd):
            continue
        print(bigimage_name + ": Downloading")
        with open("./out/pngs/raw/" + bigimage_name, "bw") as file:
            resp = get("https://surviv.io/assets/" + bigimage_name, stream=True)
            length = resp.headers.get("content-length")

            if length is None:
                file.write(resp.content)
            else:
                for data in resp.iter_content(chunk_size=(2 ^ 25)):
                    file.write(data)

        # Get big image

    for bigimage_number in range(len(parse_data)):
        bigimage = parse_data[bigimage_number]
        bigimage_name = bigimage["meta"]["image"]
        frames = bigimage["frames"]

        file = open("./out/pngs/raw/" + bigimage_name, "br")
        reader = png.Reader(file=file)
        bigimage_data = reader.asRGBA()

        bigimage_bitdepth = bigimage_data[3]["bitdepth"]
        bigimage_alpha = bigimage_data[3]["alpha"]

        if bigimage_data[0] != bigimage["meta"]["size"]["w"]:
            raise RuntimeError("Expected and actual image width differ.\nExpected: " + str(
                bigimage["meta"]["size"]["w"]) + "\n Actual: " + str(bigimage_data[0]))
        if bigimage_data[1] != bigimage["meta"]["size"]["h"]:
            raise RuntimeError("Expected and actual image height differ.\nExpected: " + str(
                bigimage["meta"]["size"]["w"]) + "\n Actual: " + str(bigimage_data[0]))

        if bigimage["meta"]["scale"] != 1:
            print(bigimage_name + ": scale expected to be 1, is actually " + str(bigimage["meta"]["scale"]))

        # Generator to list
        img_data = []
        for line in bigimage_data[2]:
            img_data.append(line)
        file.close()
        print(bigimage_name + ": Processing")

        channels = 3 + bigimage_alpha
        for i in frames:
            x = frames[i]["frame"]["x"]
            y = frames[i]["frame"]["y"]
            w = frames[i]["frame"]["w"]
            h = frames[i]["frame"]["h"]
            name = i.replace(".img", ".png")
            smallimage_organised = array_cutout(img_data, x*channels, y, w*channels, h)

            if bigimage_alpha:
                image = png.from_array(smallimage_organised, "RGBA;" + str(bigimage_bitdepth))
            else:
                image = png.from_array(smallimage_organised, "RGB;" + str(bigimage_bitdepth))
            # convert image back into format png lib can understand
            image.save("./out/pngs/" + key + "/" + str(bigimage_number) + "/" + name)
        print(bigimage_name + ": Finished")


def grab_svgs(big_string: str):
    import re
    import requests
    from os import mkdir

    print("\n\nWARNING: This script DOES NOT get all SVGs, look in json_processing for that\n")
    print("Finding SVGs")
    svg_links = []
    for svg in re.findall(r"img/[a-z\d/-_]*\.svg", big_string):
        if svg not in svg_links:
            svg_links.append(svg)
    del svg

    print("Making Folders")
    svg_folders = ["./out/svgs", "./out/svgs/gui", "./out/svgs/loot", "./out/svgs/emotes", "./out/svgs/modals"]

    try:
        mkdir("out")
    except FileExistsError:
        pass

    from shutil import rmtree
    try:
        rmtree("out/svgs")
    except FileNotFoundError:
        pass
    del rmtree

    for folder in svg_folders:
        try:
            mkdir(folder)
        except FileExistsError:
            pass

    print("Downloading SVGs")
    for link in svg_links:
        link_trimmed = link[4:]
        resp = requests.get("https://surviv.io/" + link)
        file = open("./out/svgs/" + link_trimmed, "bw")
        file.write(resp.content)
        file.close()
    print("Done grabbing SVGs\n")


def grab_mp3s(big_list: list):
    import re
    import requests
    from os import mkdir

    print("\n\nWARNING: This script DOES NOT get all MP3s, look in json_processing for that\n")
    print("Finding MP3s")
    mp3_links = []
    for string in big_list:
        for mp3 in re.findall(r"audio/[a-z\d/_-]*\.mp3", string):
            if mp3 not in mp3_links:
                mp3_links.append(mp3)
    del string, mp3

    print("Making folders")
    mp3_folders = ["./out/mp3s/", "./out/mp3s/guns", "./out/mp3s/ui", "./out/mp3s/sfx", "./out/mp3s/hits",
                   "./out/mp3s/ambient", "./out/mp3s/reverb"]

    try:
        mkdir("out")
    except FileExistsError:
        pass

    from shutil import rmtree
    try:
        rmtree("out/mp3s")
    except FileNotFoundError:
        pass
    del rmtree

    for folder in mp3_folders:
        try:
            mkdir(folder)
        except FileExistsError:
            pass

    print("Downloading MP3s")
    for link in mp3_links:
        link_trimmed = link[6:]
        resp = requests.get("https://surviv.io/" + link)
        file = open("./out/mp3s/" + link_trimmed, "bw")
        file.write(resp.content)
        file.close()
    print("Done grabbing MP3s\n")


def grab_assets(grab_all, mp3s=False, svgs=False, pngs=False):
    """
    uses
    :param grab_all: overrides other args
    :param mp3s:
    :param svgs:
    :param pngs:
    :return:
    """

    import ast
    from survivpy_deobfuscator.misc_utils import get_app

    if grab_all:
        mp3s = True
        svgs = True
        pngs = True
    del grab_all

    file = get_app()
    file.readline()
    line = file.readline()[16:][:-2]
    file.close()
    del file
    big_list = ast.literal_eval(line)
    del line

    if mp3s:
        grab_mp3s(big_list)
    del mp3s

    if svgs:
        file = get_app()
        big_string = file.read()
        grab_svgs(big_string)
    del svgs

    if pngs:
        big_string = None
        for x in big_list:
            if x.count("sourceSize"):  # and x.count("-100-"):
                # The mapping strings are the only strings in the big list to have "sourceSize" in them
                # There seems to be a set of half size/resolution assets, but they have -50- instead of -100-
                big_string = x
        del x

        if big_string is None:
            raise RuntimeError("Full-size mapping string not found")

        grab_pngs(big_string)
        print("PNGs done")

    print("Assets done!\n")


if __name__ == "__main__":
    grab_assets(False, pngs=True)
