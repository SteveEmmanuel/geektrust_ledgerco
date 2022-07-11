from ..utils import round_to_whole_no
from .. import constants

class Bank:
    def __init__(self, name):
        self.name = name


class BankLoan:
    def __init__(self, **kwargs):
        self.bank = kwargs['bank']
        self.principal = kwargs['principal']
        self.rate_of_interest = kwargs['rate_of_interest']
        self.no_of_years = kwargs['no_of_years']
        self.borrower = kwargs['borrower']

    def interest(self):
        return self.principal * self.no_of_years * (self.rate_of_interest / constants.HUNDRED)

    def total_amount(self):
        return self.interest() + self.principal

    def emi_amount(self):
        return round_to_whole_no(self.total_amount() / (self.no_of_years * constants.MONTHS_IN_A_YEAR))

    def no_of_emi(self):
        return self.no_of_years * constants.MONTHS_IN_A_YEAR
