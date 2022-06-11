import unittest

from geektrust import Borrower, Bank, BankLoan


class TestBorrower(unittest.TestCase):
    def test_init_ok(self):
        borrower = Borrower(name="name")
        self.assertEqual(borrower.name, "name")

