def get_surviv_changelog():
    """
    Gets the changelog from https://surviv.io/changelog.html.
    Raises an error if resp.ok is not true.

    :return: {
              * "time": time the changelog was received,
              * "last_modified": the last_modified field in the headers,
              * "content": resp.content except the html has been stripped out
              }
    """

    from requests import get
    from time import time
    from re import findall, DOTALL

    resp = get("https://surviv.io/changelog.html")
    if not resp.ok:
        raise RuntimeError("Non ok response: " + str(resp.content))
    result = {
        "time": time(),
        "last_modified": resp.headers.get("last-modified")
    }
    content = resp.content.decode("utf-8")
    pre_content_regex = "(?<=<pre style=\"word-wrap: break-word; white-space: pre-wrap;\">).*(?=\n {4}</pre>)"
    content = findall(pre_content_regex, content, DOTALL)[0]
    result["content"] = content
    return result


def get_json_changelog():
    """
    Loads and returns changelogs/changelog_changelog.json
    """

    from json import load
    from os.path import join, dirname

    try:
        file = open(join(dirname(__file__), "changelogs/changelog_changelog.json"), "r")
        data = load(file)
        file.close()
    except FileNotFoundError:
        return {
            "chunks": [],
            "updates": {}
        }

    return data


def write_json_changelog(data):
    """
    Writes data to changelogs/changelog_changelog.json
    """

    from json import dump
    from os.path import join, dirname

    file = open(join(dirname(__file__), "./changelogs/changelog_changelog.json"), "w")
    dump(data, file, indent=4)
    file.close()


def update_changelog(changelog_dict, content):
    """
    :param changelog_dict: Old changelog_changelog.json
    :param content: Data to merge into changelog_changelog.jso
    :return: New changelog_changelog.json
    """

    from hashlib import sha3_256

    source_string = "\n".join(content["content"])
    # Merge back into a single string
    encoded = source_string.encode("utf-8")
    str_hash = sha3_256(encoded).hexdigest()

    if str_hash in changelog_dict["updates"]:
        changelog_dict["updates"][str_hash]["last_seen"] = content["time"]
        if content["last_modified"] != changelog_dict["updates"][str_hash]["last_modified"]:
            raise RuntimeError("Conflicting last_modified times")

    else:
        changelog_dict["updates"][str_hash] = {
            "new_chunks": [],
            "first_seen": content["time"],
            "last_seen": content["time"],
            "last_modified": content["last_modified"]
        }
        for chunk in content["content"]:
            if chunk not in changelog_dict["chunks"]:
                changelog_dict["chunks"].append(chunk)
                changelog_dict["updates"][str_hash]["new_chunks"].append(chunk)

    return changelog_dict


def main():
    from re import split

    sv_changelog = get_surviv_changelog()
    sv_changelog["content"] = split(r"(?=## \[[\d.]{3,6}[a-f]?] - \w{2,9}\.? \d{1,2}, \d{4}\n)", sv_changelog["content"])
    # Split the main string at the new version/date lines
    json_changelog = get_json_changelog()
    json_changelog = update_changelog(json_changelog, sv_changelog)
    write_json_changelog(json_changelog)


if __name__ == "__main__":
    main()
