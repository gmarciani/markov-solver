from assertpy import assert_that

from markov_solver.constants import __version__


class TestConstants:
    def test_version_exists(self) -> None:
        assert_that(__version__).is_not_none()
        assert_that(__version__).is_not_empty()
