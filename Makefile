reinstall:
	./pip_modules/bin/pip uninstall mmp -y
	rm -rf build
	rm -rf dist
	rm -rf mmp.egg-info
	./pip_modules/bin/python setup.py install
