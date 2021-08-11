from requests import get
from json import load
from os.path import isfile


def handle_sounds_dict(sounds):
    for key, value in sounds.items():
        if key in ['fallOff', "shootTeam"]:
            continue
        if not isfile("./out/mp3s/guns/"+value+".mp3") and value:
            print("Downloading "+value+".mp3")
            resp = get("https://surviv.io/audio/guns/"+value+".mp3")
            with open("../out/mp3s/guns/"+value+".mp3", "bw") as file:
                file.write(resp.content)


def main():
    print("Loading weapon definitions...")
    with open("../../survivpy_net/configs/guns.json") as file:
        data = load(file)
    del file

    print("Downloading files")
    for each in data.values():
        handle_sounds_dict(each["sound"])

    print("Done getting MP3s")


if __name__ == '__main__':
    main()
