prepare:
	@echo "Preparing the set up"
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	@echo "Starting the app"
	poetry run python main.py

check:
	@echo "Running Black"
	poetry run black --check .
	@echo "Running mypy"
	poetry run mypy .
	@echo "Running Vulture"
	poetry run vulture main.py
	@echo ""
	@echo "All goods !!!"

style:
	@echo "Running Black"
	poetry run black .
	@echo ""
	@echo "All goods !!!"

black:
	poetry run black .
