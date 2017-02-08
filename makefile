install:
	pip install .

uninstall:
	pip uninstall -y opendir-dl-web

reinstall: uninstall install
