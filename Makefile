install:
	pip install .

setup-azure:
	bash scripts/configure_azure.sh

run:
	streamlit run streamlit_app/app.py
