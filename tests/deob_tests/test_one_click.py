from unittest import TestCase
from os import mkdir, listdir
from shutil import rmtree, copyfile
from survivpy_deobfuscator import one_click


def get_file(target):
    with open(target) as file:
        data = file.read()
    return data


def chunk_split(string):
    """
    Splits the script into chunks, with the "'00000000': function....." lines at the boundaries

    :param string:
    :return:
    """
    from re import split
    regex = r" {8}'[\da-f]{8}': function"
    return split(regex, string)


class test_one_click(TestCase):
    def test_code(self):

        try:
            mkdir("./deobfuscated")
        except FileExistsError:
            pass
        try:
            mkdir("./deobfuscated/js")
        except FileExistsError:
            pass
        copyfile("./tests/deob_tests/code_test.js", "./deobfuscated/js/app.12345678.js")

        one_click.one_click_deob(["--use-old", "--no-jsons"])

        for expected, actual in zip(chunk_split(get_file("./tests/deob_tests/code_expected.js")),
                                    chunk_split(get_file("./deobfuscated/js/app.12345678.js"))):
            self.assertEqual(expected, actual)
        self.assertEqual(get_file("./tests/deob_tests/code_expected.js"), get_file("./deobfuscated/js/app.12345678.js"))

        rmtree("./deobfuscated")

    def test_jsons(self):
        try:
            mkdir("./deobfuscated")
        except FileExistsError:
            pass
        try:
            mkdir("./deobfuscated/js")
        except FileExistsError:
            pass
        copyfile("./tests/deob_tests/json_test.js", "./deobfuscated/js/app.12345678.js")

        one_click.one_click_deob(["--no-code"])

        for file in listdir("./tests/deob_tests/expected_jsons"):
            target = open("./tests/deob_tests/expected_jsons/"+file)
            actual = open("./jsons/"+file)
            target_content = target.read()
            actual_content = actual.read()
            target.close()
            actual.close()

            self.assertEqual(target_content, actual_content)

        self.assertEqual(listdir("./tests/deob_tests/expected_jsons"), listdir("./jsons/"))

        rmtree("./deobfuscated")
        rmtree("./jsons")
