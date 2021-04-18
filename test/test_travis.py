import unittest


class TestCI(unittest.TestCase):
    @staticmethod
    def test_always_passes():
        assert True

    # @staticmethod
    # def test_always_fails():
    #     assert False
