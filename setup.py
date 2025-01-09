from setuptools import setup, find_packages

setup(
    name="nlp_frontend_azure",
    version="1.0.0",
    description="NLP frontend for Azure automation using ACI",
    author="Fabio Saito",
    author_email="fabiosaito@microsoft.com",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "azure-cli",
        "autogen",
    ],
    entry_points={
        "console_scripts": [
            "nlp-frontend=npl_frontend_v2.streamlit_app.app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
