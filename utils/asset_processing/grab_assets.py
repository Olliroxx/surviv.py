def split(to_split, n):
    from itertools import zip_longest
    if not len(to_split) % n == 0:
        raise ValueError("Array must be multiple of " + n)

    end_list = []

    args = [iter(to_split)] * n
    for i in zip_longest(*args):
        end_list.append(i)

    return end_list


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
    cutout = []
    for iy in range(y, y + h):
        cutout_row = []
        for ix in range(x, x + w):
            cutout_row.append(array[iy][ix])
        cutout.append(cutout_row)

    return cutout


def grab_pngs(to_parse):
    """
    Takes in a image map string from the JS source, downloads the big images and cuts them up into smaller images
    """
    import json
    import os
    import png
    import requests
    from array import array

    clean_run = True
    print_completed_file = False
    print_dl_progress = False

    if clean_run:
        autoclean_out = True
        redownload_pngs = True
    else:
        autoclean_out = False
        redownload_pngs = False

    try:
        os.mkdir("./out")
    except FileExistsError:
        pass
    try:
        os.mkdir("./out/pngs")
    except FileExistsError:
        pass

    if autoclean_out:
        from shutil import rmtree
        rmtree("./out/pngs")
        del rmtree
        os.mkdir("./out/pngs")
        os.mkdir("./out/pngs/raw")

    if type(to_parse) == str:
        parsed = json.loads(to_parse)
    elif type(to_parse) == dict:
        parsed = to_parse
    else:
        raise TypeError("Input must be either string or dict")

    for key in parsed:

        if key == "raw":
            raise RuntimeError("Very unlikely name collision")

        try:
            os.mkdir("./out/pngs/" + key)
        except FileExistsError:
            pass

        for bigimage_number in range(len(parsed[key])):
            bigimage = parsed[key][bigimage_number]
            bigimage_name = bigimage["meta"]["image"]

            cwd = "./out/pngs/" + key + "/" + str(bigimage_number)

            try:
                os.mkdir(cwd)
            except FileExistsError:
                pass

            if os.listdir(path=cwd):
                continue
            # If dir is not empty, skip this bigimage

            if redownload_pngs:
                print("Downloading PNG: " + bigimage_name)
                with open("./out/pngs/raw/" + bigimage_name, "bw") as file:
                    resp = requests.get("https://surviv.io/assets/" + bigimage_name, stream=True)
                    length = resp.headers.get("content-length")

                    if length is None:
                        file.write(resp.content)
                    else:
                        dl = 0
                        length = int(length)
                        last_percent = 0

                        for data in resp.iter_content(chunk_size=(2 ^ 25)):
                            dl += len(data)
                            file.write(data)
                            done = int(100 * dl / length)
                            if print_dl_progress and done > last_percent:
                                last_percent = done
                                print(
                                    str(done) + "% complete (" + str(dl // (2 ^ 15)) + "/" + str(
                                        length // (2 ^ 15)) + "k)")
                        if print_dl_progress:
                            print()
                    # Progress updates
            # Get big image

    for key in parsed:
        for bigimage_number in range(len(parsed[key])):
            bigimage = parsed[key][bigimage_number]
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
                print("Scale expected to be 1, is actually " + str(bigimage["meta"]["scale"]))
                print(bigimage_name)
                print()

            print("Processing " + bigimage_name)

            bigimage_organised = []
            for i in bigimage_data[2]:
                if str(type(i)) != "<class 'array.array'>":
                    i = array("B", i)
                split_array = split(i, 3 + bigimage_alpha)
                bigimage_organised.append(split_array)
            file.close()

            for i in frames:
                if frames[i]["rotated"]:
                    print(i + " is rotated")
                if not i.endswith(".img"):
                    print(i + " does not end with img")
                # if frames[i]["trimmed"]:
                #    print(i + " is trimmed")
                # They have these values, but all of them are false, I want to be notified if they introduce one which is different

                x = frames[i]["frame"]["x"]
                y = frames[i]["frame"]["y"]
                w = frames[i]["frame"]["w"]
                h = frames[i]["frame"]["h"]
                name = i.replace(".img", ".png")

                smallimage_organised = array_cutout(bigimage_organised, x, y, w, h)

                smallimage = []
                for row in smallimage_organised:
                    smallimage_row = []
                    for pixel in row:
                        for channel in pixel:
                            smallimage_row.append(channel)
                    smallimage.append(smallimage_row)
                del smallimage_row, row, pixel, channel

                if bigimage_alpha:
                    image = png.from_array(smallimage, "RGBA;" + str(bigimage_bitdepth))
                else:
                    image = png.from_array(smallimage, "RGB;" + str(bigimage_bitdepth))
                # convert image back into format png lib can understand

                image.save("./out/pngs/" + key + "/" + str(bigimage_number) + "/" + name)

                if print_completed_file:
                    print(name + " written to disk")

            print(bigimage_name + " mapped\n")


def grab_svgs(big_string: str):
    import re
    import requests
    import os

    print("\n\nWARNING: This script DOES NOT get all SVGs, look in json_processing for that\n")
    print("Finding SVGs")
    svg_links = []
    for svg in re.findall("img/[a-z0-9/-_]*\\.svg", big_string):
        if svg not in svg_links:
            svg_links.append(svg)
    del svg

    print("Making Folders")
    svg_folders = ["./out/svgs", "./out/svgs/gui", "./out/svgs/loot", "./out/svgs/emotes", "./out/svgs/modals"]

    try:
        os.mkdir("./out")
    except FileExistsError:
        pass

    from shutil import rmtree
    try:
        rmtree("./out/svgs")
    except FileNotFoundError:
        pass
    del rmtree

    for folder in svg_folders:
        try:
            os.mkdir(folder)
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
    import os

    print("Finding MP3s")
    mp3_links = []
    for string in big_list:
        for mp3 in re.findall("audio/[a-z0-9/_-]*\\.mp3", string):
            if mp3 not in mp3_links:
                mp3_links.append(mp3)
    del string, mp3

    print("Making folders")
    mp3_folders = ["./out/mp3s/", "./out/mp3s/guns", "./out/mp3s/ui", "./out/mp3s/sfx", "./out/mp3s/hits",
                   "./out/mp3s/ambient", "./out/mp3s/reverb"]

    try:
        os.mkdir("./out")
    except FileExistsError:
        pass

    from shutil import rmtree
    try:
        rmtree("./out/mp3s")
    except FileNotFoundError:
        pass
    del rmtree

    for folder in mp3_folders:
        try:
            os.mkdir(folder)
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
    from misc_utils import get_app

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
