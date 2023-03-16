format:
	black aichattelegrambot/ bot.py

lint:
	pylint aichattelegrambot/ bot.py

typecheck:
	mypy aichattelegrambot/

pre-commit: format lint typecheck

tmp-remove: 
	rm -rf .mypy_cache
	rm -rf aichattelegrambot/__pycache__
	rm -rf aichattelegrambot/utils/__pycache__
	rm -rf bot_logger.log