Asset processing
================

.. toctree::

    deobfuscate
    get_app
    grab_assets
    json_processing

Shorter explanation:

.. image:: diagram.svg

``deobfuscate.py`` either uses the ``grab_code`` function to download the code and copy it to /out/code and /deobfuscated or copies the code from /out/code to /deobfuscated.
``autoindent`` uses the ``jsbeautifier`` library to indent all app.js, vendor.js and manifest.js.
This is all of the processing applied to vendor and manifest.js.
If ``dl_assets`` is ``true``, ``grab_assets.py`` is run and some of the mp3s and svgs and all of the pngs are downloaded.
After this, ``solve_hex`` is used to convert hex to integers, and a few other number related things.
At the start of the file, there is a massive list of strings.
This contains most of the strings used in the code, although a function is used to shift by an amount that changes every update.
``fill_strings`` gets the first line, turns it into a list, shifts it and replaces the usages with the actual values.
Instead of ``true`` and ``false``, ``!![]`` and ``![]`` are used, ``add_bools`` undoes this.
In a couple of places, massive strings with ``Json['parse']`` at the start are used instead of dictionaries (this helps with deployment automation).
``process_jsons`` undoes this.

After ``deobfuscate.py`` has finished, ``create_jsons.py`` can run.
It has a fair bit of logic, but also uses other files (``create_objects_json.py``, ``create_constants_json.py`` and ``create_gamemodes_json.py``).
There is a function (that is easy to find with regex) that contains the names of other functions (that have the data used to make the .json files).
There is a list of 3-tuples, each containing a filter string, a threshold and a handler function.
If a function has more of the filter string in it than the threshold, the handler is called with the function text as an argument.
After this, all of the jsons have been written except for ``gamemodes.json``, ``constants.json`` and ``objects.json``, which are each made by the relevant script.

``grab_svgs.py``, ``grab_mp3s.py`` and ``create_csv.py`` all use the json files to generate or download another set of files.
