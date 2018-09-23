.PHONY: docs test build publish clean

init:
	pip install -r requirements/dev.txt

test:
	detox

coverage:
	pytest --cov=hubql --cov-report html --cov-report term --cov-fail-under 100

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	python setup.py clean --all

docs:
	make -C docs/ html
