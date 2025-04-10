from setuptools import setup, find_packages

setup(
    name="gudlft",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-caching",
    ],
    description="GUDLFT - Club Competition Booking System",
    author="OpenClassrooms Project",
    author_email="example@example.com",
    python_requires=">=3.6",
)
