from sys import argv
import math


def round_to_whole_no(n):
    return math.ceil(n)


class Borrower:
    def __init__(self, name):
        self.name = name


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
        return self.principal * self.no_of_years * (self.rate_of_interest / 100)

    def total_amount(self):
        return self.interest() + self.principal

    def emi_amount(self):
        return round_to_whole_no(self.total_amount() / (self.no_of_years * 12))

    def no_of_emi(self):
        return self.no_of_years * 12


class Payment:
    def __init__(self):
        pass

    def __init__(self, **kwargs):
        self.bank_loan = kwargs['bank_loan']
        self.lump_sum_amount = kwargs['lump_sum_amount']
        self.emi_no = kwargs['emi_no']


class LedgerEntry:
    def __init__(self, bank_loan=None, payment=None):
        self.bank_loan = bank_loan
        self.payment = payment

    def add_payment(self, payment):
        self.payment = payment

    def amount_paid(self, emi_no):
        if self.payment is None:
            return emi_no * self.bank_loan.emi_amount()
        else:
            if emi_no >= self.payment.emi_no:
                return self.payment.lump_sum_amount + (emi_no * self.bank_loan.emi_amount())
            else:
                return emi_no * self.bank_loan.emi_amount()

    def no_of_emi_left(self, emi_no):
        if self.payment is None:
            return self.bank_loan.no_of_emi() - emi_no
        else:
            remaining_principal = self.bank_loan.total_amount() - self.amount_paid(emi_no=emi_no)
            remaining_emi = round_to_whole_no(remaining_principal / self.bank_loan.emi_amount())
            return remaining_emi


class Ledger(dict):
    def __init__(self):
        super().__init__()

    def add_entry_to_ledger(self, borrower_name, ledger_entry):
        self[borrower_name] = ledger_entry


def main():
    ledger = Ledger()

    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    lines = f.readlines()

    for line in lines:
        if line.startswith("LOAN"):
            if line.split().__len__() == 6:
                bank_name, borrower_name, principal, no_of_years, rate_of_interest = line.split()[1:]

                bank = Bank(name=bank_name)
                borrower = Borrower(name=borrower_name)
                bank_loan = BankLoan(bank=bank,
                                     borrower=borrower,
                                     principal=float(principal),
                                     no_of_years=float(no_of_years),
                                     rate_of_interest=float(rate_of_interest))

                ledger_entry = LedgerEntry(bank_loan=bank_loan)
                ledger.add_entry_to_ledger(borrower_name=borrower_name,
                                           ledger_entry=ledger_entry)

            else:
                raise Exception("Incorrect number of arguments for LOAN command")

        if line.startswith("PAYMENT"):
            if line.split().__len__() == 5:
                bank_name, borrower_name, lump_sum_amount, emi_no = line.split()[1:]

                if borrower_name in ledger:
                    ledger_entry = ledger[borrower_name]
                    payment = Payment(bank_loan=ledger_entry.bank_loan,
                                      lump_sum_amount=float(lump_sum_amount),
                                      emi_no=float(emi_no))
                    ledger_entry.add_payment(payment)
                    ledger[borrower_name] = ledger_entry
                else:
                    Exception("No borrower by that name")
            else:
                Exception("Incorrect number of arguments for PAYMENT command")
        if line.startswith("BALANCE"):
            if line.split().__len__() == 4:
                bank_name, borrower_name, emi_no = line.split()[1:]

                if borrower_name in ledger:
                    ledger_entry = ledger[borrower_name]

                    amount_paid = int(ledger_entry.amount_paid(emi_no=float(emi_no)))
                    no_of_emis_left = int(ledger_entry.no_of_emi_left(emi_no=float(emi_no)))
                    print(bank_name + ' ' + borrower_name + ' ' + str(amount_paid) + ' ' + str(no_of_emis_left))
                else:
                    Exception("No borrower by that name")
            else:
                Exception("Incorrect number of arguments for BALANCE command")


if __name__ == "__main__":
    main()
