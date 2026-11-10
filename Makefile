.PHONY: help test clean lint app

help:
	@echo "CSIP Makefile Commands:"
	@echo "  make test      Run automated pytest test suite"
	@echo "  make app       Launch Streamlit Decision Showcase app"
	@echo "  make clean     Remove temporary python cache files"

test:
	python -m pytest tests -v

app:
	streamlit run app/streamlit_app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

