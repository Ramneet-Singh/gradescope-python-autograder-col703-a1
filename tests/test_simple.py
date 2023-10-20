import unittest
from gradescope_utils.autograder_utils.decorators import weight, visibility, number

class TestComplex(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.05)
    @number("1.1.1")
    def test_and_in(self):
        """Unit test - and-in rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-and-in.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.2")
    def test_and_e1(self):
        """Unit test - and-e1 rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-and-e1.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.3")
    def test_and_e2(self):
        """Unit test - and-e2 rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-and-e2.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.4")
    def test_or_in1(self):
        """Unit test - or-in1 rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-or-in1.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.5")
    def test_or_in2(self):
        """Unit test - or-in2 rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-or-in2.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.6")
    def test_mp(self):
        """Unit test - mp rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-mp.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.7")
    def test_mt(self):
        """Unit test - mt rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-mt.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.8")
    def test_dneg_el(self):
        """Unit test - dneg-el rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-dneg-el.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.9")
    def test_dneg_in(self):
        """Unit test - dneg-in rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-dneg-in.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.10")
    def test_impl_in(self):
        """Unit test - impl-in rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-impl-in.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.11")
    def test_neg_in(self):
        """Unit test - neg-in rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-neg-in.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.12")
    def test_neg_el(self):
        """Unit test - neg-el rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-neg-el.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.13")
    def test_bot_el(self):
        """Unit test - bot-el rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-bot-el.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.14")
    def test_or_el(self):
        """Unit test - or-el rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-or-el.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.15")
    def test_pbc(self):
        """Unit test - pbc rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-pbc.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.05)
    @number("1.1.16")
    def test_lem(self):
        """Unit test - lem rule."""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/unit-lem.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.2)
    @number("1.2.1")
    def test_scope_incorrect(self):
        """Incorrect Proof Test - Scope Issue"""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/scope_incorrect_1.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "incorrect")

    @weight(0.2)
    @number("1.2.2")
    def test_incorrect(self):
        """Incorrect Proof Test"""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/incorrect_1.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "incorrect")

    @weight(0.4)
    @number("1.3.1")
    def test_big_1(self):
        """Big Test 1"""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/big_1.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")

    @weight(0.4)
    @number("1.3.2")
    def test_big_2(self):
        """Big Test 2"""
        from checkProof import checkProof
        proofFilePath = "/autograder/source/inputProofFiles/big_2.txt"
        output = checkProof(proofFilePath)
        self.assertEqual(output, "correct")
