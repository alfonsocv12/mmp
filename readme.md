<p align="center">
  <a href="https://mmp-y.com">
    <img src="https://mmp-y.com/owl.svg">
  </a>
  <p align="center">
    <span>mmp</span>
  </p>
  <p align=center>
    <a href="https://www.python.org/downloads/release/python-3">
      <img src="https://img.shields.io/badge/python-3-blue.svg">
    </a>
    <a href="https://github.com/alfonsocv12/mmp/actions/workflows/python-publish.yml">
      <img src="https://github.com/alfonsocv12/mmp/actions/workflows/python-publish.yml/badge.svg">
    </a>
  </p>
</p>


Module manager python  is a cli solution for an easier and faster way to handle you python modules
with your projects.

---

### [Documentation](https://mmp-y.com)

### [Source code](https://github.com/alfonsocv12/mmp)

---

## Inspiration

The inspiration and the goal to deliver its a similar way of handling node modules
but off course not losing the simplicity of the python programing language, taking
into consideration the difference in use cases between both programming languages.

I know that the name its wrong but mmp was taken by the time that i build this
solution.

## Quickstart

To start using PyMm, first install the program, at this early stages we just have
the installation by pip so its required for you to have that also the app just works
with python 3 and up so you need to use pip3 in the case that you have python 2 as
your default python version.

```bash
$ pip3 install mmp
```

After you install the program, go to the proyect that you want to use mmp and
start installing dependencies with this simple command

```bash
$ mmp install [module_name]
```

To run your project/script its ass simple to use the run command, this command defaults
to a run.py file but you can specify the file that you want to run by adding the file
full name at the end like this

```bash
$ mmp run my_perfect_script.py
```

In the case that you want to know a little more off the commands that you can run
with the program just ask for help with the -h on every section of the program for
example.

```bash
$ mmp -h
$ mmp run -h
```
