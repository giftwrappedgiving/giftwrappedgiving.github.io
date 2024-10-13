# current git branch
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

init::
	python -m pip install --upgrade pip
	python -m pip install pip-tools
	python -m piptools compile requirements/dev-requirements.in
	python -m piptools compile requirements/requirements.in
	python -m piptools sync requirements/dev-requirements.txt requirements/requirements.txt
	python -m pre_commit install
	npm install


sync-reqs::
	python -m pip install --upgrade pip
	python -m piptools compile requirements/dev-requirements.in
	python -m piptools compile requirements/requirements.in
	python -m piptools sync requirements/requirements.txt requirements/dev-requirements.txt


black:
	black bin

black-check:
	black --check bin

flake8:
	flake8 .

isort:
	isort --profile black .

lint: black flake8 isort

clean::
	rm -r docs/*

copy-imgs:
	cp -r src/images docs/static/

build::
	npm run build

watch::
	npm run watch:scss

render::
	python render.py

guides::	copy-imgs render

gwg:: copy-imgs build render

serve:
	python -m http.server 8080 --bind 127.0.0.1 --directory docs


commit-package::
	git add docs/
	git diff --quiet && git diff --staged --quiet || (git commit -m "Rebuilt gwg $(shell date +%F)"; git push origin $(BRANCH))
