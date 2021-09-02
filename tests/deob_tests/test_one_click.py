from unittest import TestCase
from os import mkdir, listdir
from shutil import rmtree, copyfile
from survivpy_deobfuscator import one_click


def get_file(target):
    with open(target) as file:
        data = file.read()
    return data


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
