install:
	pip install .

uninstall:
	pip uninstall -y opendir-dl-web

reinstall: uninstall install

run:
	python ./opendir_dl_web
