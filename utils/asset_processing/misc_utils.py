class DataNeededError(RuntimeError):
    """
    This is the error used when there isn't enough information to turn a function into a value

    This is only used by scripts in the json_processing folder
    """
    pass


def get_app(mode="r"):
    """
    :param mode: If the file object should be in read or write mode
    :return: File object for app.js
    """
    import os

    file = None
    for script in os.listdir(os.path.dirname(os.path.abspath(__file__))+".\\deobfuscated\\js"):
        if script.count("app"):
            if file is not None:
                raise RuntimeError("There must be exactly one app.js script in out/code/js")
            file = open(os.path.dirname(os.path.abspath(__file__))+".\\deobfuscated\\js\\" + script, mode, encoding="utf-8")
    if file is None:
        raise RuntimeError("There must be exactly one app.js script in out/code/js")
    return file


def check_servers_down():
    import requests
    resp = requests.get("https://surviv.io")
    if resp.status_code == 503:
        return True
    return False
