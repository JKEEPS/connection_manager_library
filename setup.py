from setuptools import setup, find_packages

setup(
    name="connection_manager",
    version="1.1.0",
    description="Unified library for managing connections to Tableau, Oracle, AWS, and Redshift",
    author="JKEEPS",
    packages=find_packages(),
    install_requires=[
        "tableauserverclient",
        "tableauhyperapi",
        "cx_Oracle",
        "boto3==1.34.69",
        "psycopg2",
        "pyyaml",
    ],
)