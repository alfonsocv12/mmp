<p align="center">
  <a href="https://mmp.alfonsocvu.me">
    <img src="https://mmp.alfonsocvu.me/owl.svg">
  </a>
  <p align="center">
    <h1 align="center">mmp</h1>
  </p>
  <p align=center>
    <a href="https://www.python.org/downloads/release/python-3">
      <img src="https://img.shields.io/badge/python-3-blue.svg">
    </a>
    <a href="https://github.com/alfonsocv12/mmp/actions/workflows/python-publish.yml">
      <img src="https://github.com/alfonsocv12/mmp/actions/workflows/python-publish.yml/badge.svg">
    </a>
    <a href="https://pypi.org/project/mmp/">
      <img src="https://img.shields.io/pypi/dm/mmp">
    </a>
  </p>
</p>


Module manager python  is a cli solution for an easier and faster way to handle you python modules.

---

### [Documentation page](https://mmp.alfonsocvu.me)
### [Update docs here](https://github.com/alfonsocv12/mmpDocs)
### [Source code git repo](https://github.com/alfonsocv12/mmp)

---

## Inspiration

The inspiration and the goal to deliver its a similar way of handling node modules
but off course not losing the simplicity of the python programing language, taking
into consideration the difference in use cases between both programming languages.

I know that the name its wrong but mmp was taken by the time that i build this
solution.

## Quickstart

### Installation

##### Requirements

Python 3.6+

* [virtualenv](https://virtualenv.pypa.io/en/latest/) for the envs
* [docopt](http://docopt.org/) for command handling and docs

To install mmp:

```bash
$ pip3 install mmp
```

### First commands

For installing modules into your project

```bash
$ mmp install [module_name]
```

This is how you run your scripts.

```bash
$ mmp run my_perfect_script.py
```

**by the way** if your script file name is run.py run this instead.

```bash
$ mmp run
```

### Help

If you need help, just add -h to whatever you want to know about

```bash
$ mmp -h
$ mmp run -h
```

[The docs are here if you have some more problems with the library](https://mmp.alfonsocvu.me/)
