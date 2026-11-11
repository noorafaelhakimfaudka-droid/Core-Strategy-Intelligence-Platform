.PHONY: help reproduce verify test lint docs-check app-test app clean

help:
	@echo "CSIP V17 Master Makefile Commands:"
	@echo "  make reproduce   Run full end-to-end reproduction pipeline"
	@echo "  make test        Run entire automated pytest test suite"
	@echo "  make verify      Run test suite + release quality gate verifier"
	@echo "  make lint        Run static code lint checks"
	@echo "  make docs-check  Verify anti-overclaim rules across all files"
	@echo "  make app-test    Run automated Streamlit AppTest page suite"
	@echo "  make app         Launch Streamlit interactive dashboard"
	@echo "  make clean       Remove temporary python cache files"

reproduce:
	python scripts/reproduce_all.py

test:
	python -m pytest -v --tb=short

verify: test
	python tools/verify_release.py

lint:
	python -m flake8 src tests scripts tools --count --select=E9,F63,F7,F82 --show-source --statistics || true

docs-check:
	python tools/check_claims.py

app-test:
	python -m pytest tests/test_app_pages.py -v

app:
	streamlit run app/streamlit_app.py

clean:
	python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
