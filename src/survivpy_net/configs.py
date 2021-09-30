constants = {}
mtypes = {}
gtypes = {}
map_defs = {}
materials = {}
animations = {}
anims = {}
proxies = {}
updated = False

mtypes_list = []
gtypes_list = []


def update_configs(force=False):
    from json import load

    global constants, mtypes, gtypes, map_defs, materials, anims, animations, proxies, updated, gtypes_list, mtypes_list

    if updated and not force:
        return

    constants_file = open("./configs/constants.json")
    constants = load(constants_file)
    constants_file.close()

    mtypes_data = load(open("./configs/objects.json"))
    mtypes = mtypes_data["objects"]
    materials = mtypes_data["materials"]
    del mtypes_data

    files = ("bullets", "crosshairs", "heal_effects", "emotes", "explosions", "nonweapons", "guns", "melee_weapons",
             "outfits", "quests", "perks", "passes", "pings", "roles", "throwables", "default_unlocks", "xp_sources",
             "death_effects", "lootbox_tables", "item_pools", "xp_boost_events", "market_min_values", "npcs")
    gtypes = {}
    for file in files:
        file = open(("./configs/" + file + ".json"))
        data = load(file)
        file.close()
        gtypes = gtypes | data
    del file, files

    map_defs = load(open("./configs/map_data.json"))

    anims = animations = load(open("./configs/anims.json"))

    proxies = load(open("./configs/proxies.json"))

    updated = True

    mtypes_list = [""] + list(mtypes.keys())
    gtypes_list = [""] + list(gtypes.keys())
