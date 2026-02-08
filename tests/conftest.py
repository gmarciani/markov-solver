import pytest
from pathlib import Path


@pytest.fixture
def resource_path_root() -> Path:
    """Return the path to the test resources' directory."""
    return Path(__file__).parent / "resources"
