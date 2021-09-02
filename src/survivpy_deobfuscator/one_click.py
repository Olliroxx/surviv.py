_DESCRIPTION = "Download and deobfuscate .js files used by https://surviv.io. Also generates .json files."
_USE_OLD = "Do not download new .js files. Will still download assets if --assets is used."
_NO_CODE = "Do not re-deobfuscate code. Not compatible with --assets."
_NO_JSONS = "Do not generate new jsons."
_ASSETS = "Grab all assets (requires code)"


def _parse_args(args=None):
    from argparse import ArgumentParser

    parser = ArgumentParser(description=_DESCRIPTION)
    parser.add_argument("--use-old", help=_USE_OLD, action="store_true")
    parser.add_argument("--no-code", help=_NO_CODE, action="store_true")
    parser.add_argument("--assets", help=_ASSETS, action="store_true")
    parser.add_argument("--no-jsons", help=_NO_JSONS, action="store_true")

    return parser.parse_args(args)


def one_click_deob(args=None):
    args = _parse_args(args)

    if args.assets and args.no_code:
        raise ValueError("Incompatible arguments")

    from survivpy_deobfuscator.deobfuscate import main
    from survivpy_deobfuscator.json_processing.create_jsons import create_jsons
    from survivpy_deobfuscator.json_processing.grab_svgs import grab_svgs
    from survivpy_deobfuscator.json_processing.grab_mp3s import grab_mp3s

    if not args.no_code:
        main(dl_assets=args.assets, redownload=not args.use_old)

    if not args.no_jsons:
        create_jsons()

    if args.assets:
        grab_svgs()
        grab_mp3s()


if __name__ == '__main__':
    one_click_deob()
