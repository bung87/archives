import pytest
import os


@pytest.fixture
def loadFixture():
    def _loadFixture(name):
        content = None
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, "fixtures", name)
        with open(path) as f:
            content = f.read()
        return content

    return _loadFixture
