def flatten_dict(to_flatten: dict, name: str, output: dict):
    """
    Turns
    .. code-block::

        {
            "a": {
                "b": 1
            },
            "c": 2
        }

    into
    .. code-block::

        {'a_b': 1, 'c': 2}

    :param to_flatten:
    :param name: Used for recursion, should be an empty string
    :param output: output dict, also returned
    :return:
    """
    for key, value in to_flatten.items():
        if name:
            sub_name = name + "_" + key
        else:
            sub_name = key
        if type(value) == dict:
            flatten_dict(value, sub_name, output)
        else:
            output[sub_name] = value
    return output


def make_table(infile: str, defaults: dict):
    """
    Makes a list of dicts, one from each dict in infile

    :param infile: the json file to read
    :param defaults: If a dict doesn't have a key in defaults, it will use the default
    :return:
    """
    from json import load
    import os

    with open(os.path.join(os.path.dirname(__file__), infile)) as file:
        data = load(file)

    list_of_dicts = []
    for key, value in data.items():
        list_of_dicts.append(defaults | flatten_dict(value, "", {"internalName": key}))

    out = []
    for dict_ in list_of_dicts:
        sorted_dict = {}
        for key in sorted(dict_.keys()):
            sorted_dict[key] = dict_[key]
        out.append(sorted_dict)
    return out


def write_table(table: list, fname: str):
    """
    Small write macro

    :param table: List to write
    :param fname: File name
    :return:
    """
    from csv import DictWriter
    import os

    file = open(os.path.join(os.path.dirname(__file__), fname), "w", newline="")
    fields = table[0].keys()
    writer = DictWriter(file, fields)
    writer.writeheader()
    writer.writerows(table)
    file.close()


if __name__ == '__main__':
    categories = [
        {"defaults": {
            "burstCount": 1,
            "burstDelay": None,
            "sound_fallOff": None,
            "worldImg_gunOffset_y": 0,
            "worldImg_gunOffset_x": 0,
            "isBullpup": False,
            "worldImg_magImg_pos_x": 0,
            "worldImg_magImg_pos_y": 0,
            "worldImg_magImg_sprite": None,
            "aimDelay": False,
            "pullDelay": 0,
            "sound_cycle": None,
            "weaponClass": None,
            "sound_pull": None,
            "particle_customParticle": None,
            "noPotatoSwap": False,
            "burstSounds": None,
            "worldImg_magImg_top": None,
            "particle_shellReverse": None,
            "reloadTimeAlt": None,
            "maxReloadAlt": None,
            "extendedReloadAlt": None,
            "sound_reloadAlt": None,
            "sound_shootLast": None,
            "deployGroup": None,
            "jitter": None,
            "toMouseHit": None,
            "noSplinter": False,
            "pistol": None,
            "dualWieldType": None,
            "isDual": False,
            "dualOffset": None,
            "noDrop": False,
            "ammoInfinite": False,
            "worldImg_loadingBullet_pos_x": 0,
            "lootImg_noTint": None,
            "speed_load": None,
            "worldImg_handsBelow": None,
            "worldImg_magImg_max_height_adj": None,
            "worldImg_loadingBullet_MaxScale": None,
            "worldImg_loadingBullet_sprite": None,
            "projType": None,
            "loadTime": None,
            "particle_amount": None,
            "worldImg_onLoadComplete": None,
            "worldImg_loadingBullet_pos_y": None,
            "worldImg_loadingBullet_maxScale": None,
            "ignoreEndlessAmmo": False,
            "outsideOnly": False,
            "isLauncher": False,
            "particle_shellOffsetY": 0,
            "particle_shellForward": None,
            "sound_shootTeam_1": None,
            "ignoreDetune": False,
            "sound_shootAlt": None,
            "sound_shootTeam_2": None,
            "worldImg_rightHandOffset_y": None,
            "worldImg_rightHandOffset_x": None,
        }, "source": "guns.json", "out": "guns.csv"},
        {"defaults": {
            "isSkin": False,
            "speed_attack": None,
            "lootImg_border": None,
            "sound_pickup": None,
            "worldImg_rot": None,
            "worldImg_sprite": None,
            "worldImg_pos_x": None,
            "lootImg_rot": None,
            "noPotatoSwap": None,
            "lootImg_borderTint": None,
            "worldImg_pos_y": None,
            "worldImg_scale_y": None,
            "worldImg_scale_x": None,
            "noDropOnDeath": False,
            "worldImg_tint": None,
            "lootImg_mirror": False,
            "cleave": False,
            "sound_playerHit2": None,
            "worldImg_leftHandOntop": False,
            "armorPiercing": False,
            "attack_poseTime": None,
            "anim_poseAnims": None,
            "reflectArea_offset_x": None,
            "reflectArea_offset_y": None,
            "reflectArea_rad": None,
            "stonePiercing": False,
            "worldImg_renderOnHand": None,
            "reflectSurface_equipped_p0_y": None,
            "hipImg_scale_x": None,
            "reflectSurface_unequipped_p1_x": None,
            "hipImg_pos_x": None,
            "sound_bullet": None,
            "hipImg_sprite": None,
            "reflectSurface_unequipped_p0_x": None,
            "reflectSurface_equipped_p1_x": None,
            "reflectSurface_equipped_p1_y": None,
            "reflectSurface_unequipped_p1_y": None,
            "hipImg_pos_y": None,
            "hipImg_tint": None,
            "reflectSurface_equipped_p0_x": None,
            "reflectSurface_unequipped_p0_y": None,
            "hipImg_rot": None,
            "hipImg_scale_y": None,
            "scale_x": 1,
            "scale_y": 1,
            "handSprites_spriteL": None,
            "handSprites_spriteR": None,
            "flip": None,
        }, "source": "melee_weapons.json", "out": "melees.csv"},
        {"defaults": {
            "onHit": None,
            "suppressed": False,
            "skipCollision": False,
            "maxFlareScale": 1,
            "flareColor": 0,
            "addFlare": False,
        }, "source": "bullets.json", "out": "bullets.csv"},
        {"defaults": {
            "teamDamage": True
        }, "source": "explosions.json", "out": "explosives.csv", },
    ]

    try:
        from os import mkdir

        mkdir("./ csvs")
        del mkdir
    except FileExistsError:
        pass

    for category in categories:
        print("Writing " + category["out"])
        category_table = make_table("./jsons/" + category["source"], category["defaults"])
        write_table(category_table, "./csvs/" + category["out"])

    print("Done")
