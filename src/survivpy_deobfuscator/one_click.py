_DESCRIPTION = "Download and deobfuscate .js files used by https://surviv.io. Also generates .json files."
_USE_OLD = "Do not download new .js files. Will still download assets if --assets is used."
_CODE_ONLY = "Do not generate .json files. Cannot be used with --assets."
_ASSETS = "Grab all assets as well. Cannot be used with --code-only."


def _parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser(description=_DESCRIPTION)
    parser.add_argument("--use-old", help=_USE_OLD, action="store_true")
    parser.add_argument("--code-only", help=_CODE_ONLY, action="store_true")
    parser.add_argument("--assets", help=_ASSETS, action="store_true")

    return parser.parse_args()


def one_click_deob():
    args = _parse_args()

    from .deobfuscate import main
    from .json_processing.create_jsons import create_jsons
    from .json_processing.grab_svgs import grab_svgs

    if args.code_only and args.assets:
        raise ValueError("Incompatible arguments")

    main(dl_assets=args.assets, redownload=not args.use_old)

    if not args.code_only:
        create_jsons()

    if args.assets:
        grab_svgs()


if __name__ == '__main__':
    one_click_deob()
