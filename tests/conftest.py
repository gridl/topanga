import pytest


@pytest.fixture(scope="session")
def application():
    from topanga.application import Application
    return Application('test')
