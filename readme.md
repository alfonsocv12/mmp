# mpip

[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/release/python-3)
[![Upload Python Package](https://github.com/alfonsocv12/mpip/actions/workflows/python-publish.yml/badge.svg)](https://github.com/alfonsocv12/mpip/actions/workflows/python-publish.yml)

This is a cli solution for an easier and faster way to handle you python modules
with your projects.

## Inspiration

The inspiration and the goal to deliver its a similar way of handling node modules
but off course not losing the simplicity of the python programing language, taking
into consideration the difference in use cases between both programming languages.

## Quickstart

To start using mpip, first install the program, at this early stages we just have
the installation by pip so its required for you to have that also the app just works
with python 3 and up so you need to use pip3 in the case that you have python 2 as
your default python version.

```bash
$ pip3 install mpip
```

After you install the program, go to the proyect that you want to use mpip and
start installing dependencies with this simple command

```bash
$ mpip install [module_name]
```

To run your project/script its ass simple to use the run command, this command defaults
to a run.py file but you can specify the file that you want to run by adding the file
full name at the end like this

```bash
$ mpip run my_perfect_script.py
```

In the case that you want to know a little more off the commands that you can run
with the program just ask for help with the -h on every section of the program for
example.

```bash
$ mpip -h
$ mpip run -h
```
