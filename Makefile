.PHONY: all black lint typecheck build clean

all: black
	-$(MAKE) lint
	-$(MAKE) typecheck
	$(MAKE) build
	$(MAKE) clean

black:
	poetry run black src


lint:
	poetry run pylint src

typecheck:
	poetry run mypy src

build:
	poetry build

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	rm -rf .mypy_cache
	rm -rf dist/ build/ *.egg-info/