APPLICATION_NAME = webtronics
TEST = pytest -c pytest.ini $(APPLICATION_NAME)/tests/  --verbosity=2 --showlocals --log-level=DEBUG

test:
	$(TEST)

test-cov:  ##@Testing Test application with pytest and create coverage report
	$(TEST) --cov=$(APPLICATION_NAME) --cov-fail-under=70

format:
	isort .

lint:
	isort --check . && \
	flake8 . --count --statistics

env:
	cp .env.example .env
