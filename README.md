## DEPRECATED

The project got superseded by the [CodeImageGenerator](https://github.com/peitek/CodeImageGenerator) project, which creates generally usable images instead of Presentation-specific output.

# PresentationCodeFormatter

PresentationCodeFormatter is a Python script, which converts Java files/functions to a text file, which is readable by [Presentation](http://www.neurobs.com/).
This includes a rough custom syntax highlighting with [Pygments](http://pygments.org/).

I personally use this to convert short code snippets for empirical research on program comprehension (see [Brains on Code](https://github.com/brains-on-code)).
This means the script is personalized to my specific usage and probably not directly useful to you without changes.

Disclaimer: I am not a Python programmer. I'm always grateful for feedback on how to improve my code.

## Features

The main feature is to read all files from a directory and attempting to add syntax highlighting compatible with the syntax of Presentation to the output file(s).

Implemented so far:

* Reads all files from a directory, and parses one at a time
* Extracts just the function code from the file (and ignores the class, comments, etc around it)
* Uses Pygments to create syntax highlighting for each function
* Parses Pygments syntax highlighting to a Presentation-compatible format (still may be incomplete)
* Wraps code into a Presentation variable for seamless integration
* Output in separate files, or one large file


## Roadmap

Things I still want to add:

* Command line support
* Better configuration (in particular the output color scheme)
* Allow multiple functions per file
* Allow functions besides `public int`, `public String`, `public boolean`
* Only read Java files
* Support for more languages than just Java


## Setup ##

The project should run in any Python environment. It was developed and tested with the [PyCharms IDE](https://www.jetbrains.com/pycharm/).


# License #

```
MIT License

Copyright (c) 2017 Norman Peitek
```