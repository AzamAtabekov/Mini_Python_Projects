from setuptools import setup, find_packages

setup(
    name="site-analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "httpx[http2]",
        "beautifulsoup4",
        "lxml",
        "tldextract",
    ],
    entry_points={
        "console_scripts": [
            "site-analyzer = site_analyzer.cli:main",
        ],
    },
)
