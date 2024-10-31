run:
	@echo "Starting the app"
	poetry run python PictionaryGame.py

check:
	@echo "Running Black"
	poetry run black --check .
	@echo "Running mypy"
	poetry run mypy .
	@echo "Running Vulture"
	poetry run vulture PictionaryGame.py
	@echo ""
	@echo "All goods !!!"

style:
	@echo "Running Black"
	poetry run black .
	@echo ""
	@echo "All goods !!!"

black:
	poetry run black .
