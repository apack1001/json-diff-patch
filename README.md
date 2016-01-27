JSON tools
==========

Manipulate JSON documents using ["JSON patch" format][1].

This software is available under the [MIT License](http://opensource.org/licenses/MIT)

Installation
------------

TBD

Release notes
-------------
TBD

Running tests
-------------

Just run `nosetests` from the repo root.


Usage
-----

There are two ways of using *json_tools*:

 1. As a CLI utilty.
 2. As a Python module.

### CLI interface

After you've installed *json_tools* you can access it via `json` command in the
shell. It provides a pretty simple yet powerful interface to manipulate JSON
documents:

 *  `print [input_file]`

    Pretty-print a JSON file with syntax highlighting and keys sorting.

    If `input_file` is omitted or equals `-`, reads JSON from STDIN.

    **Example:**

        $ echo '{"Hello": ["w", "o", "r", "l", "d", "!"]}' | json print
        {
            "Hello": [
                "w",
                "o",
                "r",
                "l",
                "d",
                "!"
            ]
        }

 *  `diff [file1] [file2]`

    Calculate difference between two JSON documents and output it in JSON patch format.

    Either `file1` or `file2` can be set to `-`, in order to read JSON from STDIN.

    **Example:**

        $ json diff doc1.json doc2.json
        [
            {
                "add": "/lol",
                "value": "wut"
            },
            {
                "remove": "/some/field",
                "prev": {
                    "compound": "value"
                }
            }
        ]

 *  `patch [options] input [patch [patch ...]]`

    Modify the JSON file `input` using a series of JSON `patch`es.

    If `patch` is omitted or equals `-`, its content is read from STDIN.

    **Options:**

    `-i, --inplace`

    Modify `source_file` inplace instead of printing it to STDOUT.


### Pythonic interface

TBD


Planned features
----------------

 1. Support more JSON patch options: currently *json_tools* only supports
    *add*, *remove* and *replace*.
 1. Make **diff** output more human readable (not JSONish).
 1. Improve documentation.


  [1]: http://tools.ietf.org/html/draft-ietf-appsawg-json-patch-02
