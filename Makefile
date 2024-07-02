init::
	python -m pip install --upgrade pip
	python -m pip install pip-tools
	python -m piptools compile requirements/dev-requirements.in
	python -m piptools compile requirements/requirements.in
	python -m piptools sync requirements/dev-requirements.txt requirements/requirements.txt
	python -m pre_commit install
	npm install


sync-reqs::
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


build::
	npm run build

watch::
	npm run watch:scss

render::
	python render.py

gwg:: build render

serve:
	python -m http.server 8080 --bind 127.0.0.1 --directory docs
