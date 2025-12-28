test:
	python -m pytest goods_app/tests/test_products.py -v --nomigrations

server:
    python manage,py runserver

lint:
    pylint $(git ls-files '*.py')

coverage:
	pytest -s --cov --cov-report html --cov-fail-under 70