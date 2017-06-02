# PresentationCodeFormatter

PresentationCodeFormatter is a Python script, which converts Java files/functions to a text file, which is readable by [Presentation](http://www.neurobs.com/).
This includes a rough custom syntax highlighting with [Pygments](http://pygments.org/).

I personally use this to convert [small code snippets](#TODO) for empirical research on program comprehension (see [Brains on Code](https://github.com/brains-on-code)).
This means the script is very personalized to my usage, and probably not directly useful to you without changes.

**Disclaimer: I am not a Python programmer and don't really know what I'm doing.**


## Features

The main feature is to read all files from a directory and attempts to add syntax highlighting compatible with the syntax of Presentation to the output file(s).

Implemented so far:

* Reads all files from a directory, and parses one at a time
* Extracts just the function code from the file (and ignores the class, comments, etc around it)
* Uses Pygments to create syntax highlighting for the code
* Parses Pygments syntax highlighting to a Presentation-compatible format
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

Things you could add:

* Better Python code...


## Setup ##

The project should run in any Python IDE. It was developed and tested with [PyCharms](https://www.jetbrains.com/pycharm/).


# Contributing #

Do you want to fix my horrible Python code? Feel free to create a pull request :)

Thank you!


# License #

```
MIT License

Copyright (c) 2017 Norman Peitek
```