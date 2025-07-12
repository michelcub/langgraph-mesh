from setuptools import setup, find_packages

setup(
    name="langgraph_server",
    version="0.1.0",
    description="Simple server framework for distributed LangGraph agents",
    author="Orestes Michel Lopez Perez",
    author_email="oreste.lopez@gmail.com",
    packages=find_packages(),
    install_requires=[
        "langgraph>=0.5.0",
        "fastapi>=0.115.14",
        "uvicorn>=0.35.0",
        "httpx>=0.28.1",
        "pydantic>=2.11.7",
    ],
    python_requires=">=3.11",
)