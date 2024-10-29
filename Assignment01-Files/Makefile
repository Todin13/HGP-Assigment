check:
	@echo "Running Black"
	poetry run black --check .
	# @echo "Running isort"
	# poetry run isort --check .
	@echo "Running mypy"
	poetry run mypy .
	@echo "Running Vulture"
	poetry run vulture StockTradeCalculator.py
	@echo ""
	@echo "All goods !!!"

format:
	poetry run black .

run:
	poetry run python StockTradeCalculator.py