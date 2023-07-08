from setuptools import setup, find_packages

setup(
    name="UrlChecker",
    version="1.0",
    author="Máté Pázmándi",
    author_email="matepazy@proton.me",
    description="",
    packages=find_packages(),
    install_requires=[
        "tkinter",
        "requests",
    ],
)
