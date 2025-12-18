.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
	@echo ""
	@echo "Release commands:"
	@echo "  notes - consume towncrier newsfragments and update release notes (requires bump=patch|minor|major)"
	@echo "  release - package and upload a release (requires bump=patch|minor|major)"
	@echo "  validate-newsfragments - validate newsfragments and show draft changelog"

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +
	rm -rf .tox/.pkg/ 2>/dev/null || true

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with ruff
	ruff check cid tests

typecheck: ## run type checking with mypy and pyrefly
	pre-commit run mypy-local --all-files && pre-commit run pyrefly-local --all-files

test: ## run tests quickly with the default Python
	py.test --cov=cid/ --cov-report=html --cov-report=term-missing --cov-branch

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source cid -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/cid.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ --separate cid
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

check-docs-ci: ## check documentation for CI
	rm -f docs/cid.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ --separate cid
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst;*.py' -c '$(MAKE) -C docs html' -R -D .

verify_description: ## verify the long description is valid RST
	python -c "from docutils.core import publish_string; result = publish_string(open('README.rst').read(), writer_name='html'); print('RST validation successful')" 2>&1 | grep -E "(ERROR|WARNING)" && exit 1 || echo "RST validation passed"


dist: clean ## builds source and wheel package
	python -m build
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	pip install .

install-dev: clean ## install the package in development mode
	pip install -e ".[dev]"

pr: clean lint typecheck test ## run clean, lint, typecheck, and test - everything needed before creating a PR

# release commands

notes: check-bump validate-newsfragments ## consume towncrier newsfragments and update release notes - requires bump to be set
	# Let UPCOMING_VERSION be the version that is used for the current bump
	$(eval UPCOMING_VERSION=$(shell bump-my-version bump --dry-run $(bump) -v | awk -F"'" '/New version will be / {print $$2}'))
	# Now generate the release notes to have them included in the release commit
	towncrier build --yes --version $(UPCOMING_VERSION)
	# Before we bump the version, make sure that the towncrier-generated docs will build
	make check-docs-ci
	git commit -m "Compile release notes for v$(UPCOMING_VERSION)"

release: check-bump check-git clean ## package and upload a release (does not run notes target) - requires bump to be set
	# verify that notes command ran correctly
	./newsfragments/validate_files.py is-empty
	CURRENT_SIGN_SETTING=$(git config commit.gpgSign)
	git config commit.gpgSign true
	bump-my-version bump $(bump)
	python -m build
	git config commit.gpgSign "$(CURRENT_SIGN_SETTING)"
	git push upstream && git push upstream --tags
	twine upload dist/*

# release helpers

validate-newsfragments: ## validate newsfragments and show draft changelog
	python ./newsfragments/validate_files.py
	towncrier build --draft --version preview

check-bump: ## check that bump parameter is set
ifndef bump
	$(error bump must be set, typically: major, minor, patch, or devnum)
endif

check-git: ## check that upstream remote is configured correctly
	# require that upstream is configured for ipld/py-cid
	@if ! git remote -v | grep "upstream[[:space:]]git@github.com:ipld/py-cid.git (push)\|upstream[[:space:]]https://github.com/ipld/py-cid (push)"; then \
		echo "Error: You must have a remote named 'upstream' that points to 'ipld/py-cid'"; \
		exit 1; \
	fi
