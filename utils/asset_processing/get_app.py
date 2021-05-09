def get_app(mode="r"):
    """
    :param mode: If the file object should be in read or write mode
    :return: File object for app.js
    """
    import os

    file = None
    for script in os.listdir(".\\deobfuscated\\js"):
        if script.count("app"):
            if file is not None:
                raise RuntimeError("There must be exactly one app.js script in out/code/js")
            file = open(".\\deobfuscated\\js\\" + script, mode, encoding="utf-8")
    if file is None:
        raise RuntimeError("There must be exactly one app.js script in out/code/js")
    return file
