prepare:
	@echo "Preparing the set up"
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

check:
	@echo "Running Black"
	poetry run black --check .
	@echo "Running isort"
	poetry run isort --check .
	@echo "Running mypy"
	poetry run mypy .
	@echo "Running Vulture"
	poetry run vulture main.py
	@echo ""
	@echo "All goods !!!"
