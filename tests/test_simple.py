import unittest
from gradescope_utils.autograder_utils.decorators import weight, visibility, number
from checkProof import checkProof


class TestComplex(unittest.TestCase):
    def setUp(self):
        pass

    @weight(1)
    #@visibility('after_published')
    @number("1.1")
    def test_and_intro(self):
        """Unit test - and introduction rule."""
        proofFilePath = "/autograder/source/inputProofFiles/unit_and_intro.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")