format:
	black aichattelegrambot/ financeanalysis/ bot.py

lint:
	pylint aichattelegrambot/ financeanalysis/ bot.py

typecheck:
	mypy aichattelegrambot/ financeanalysis/

pre-commit: format lint typecheck

tmp-remove: 
	rm -rf .mypy_cache
	rm -rf aichattelegrambot/__pycache__
	rm -rf aichattelegrambot/utils/__pycache__
	rm -rf financeanalysis/__pycache__
	rm -rf bot_logger.log