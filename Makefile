.PHONY: install project build publish package package-install clean

install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package:
	python3 -m build

package-install:
	python3 -m pip install dist/*.whl