def get_app(mode="r"):
    import os

    file = None
    for script in os.listdir(".\\deobfuscated\\js"):
        if script.count("app"):
            if file is not None:
                raise RuntimeError("There must be exactly one app.js script in overrides/surviv.io/js")
            file = open(".\\deobfuscated\\js\\" + script, mode, encoding="utf-8")
    if file is None:
        raise RuntimeError("There must be exactly one app.js script in overrides/surviv.io/js")
    return file
