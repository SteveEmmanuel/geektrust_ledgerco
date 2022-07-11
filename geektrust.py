from sys import argv
from src.models import (Bank, BankLoan, Borrower,
                        Payment, Ledger, LedgerEntry)
from src import constants


def main():
    ledger = Ledger()

    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    lines = f.readlines()

    for line in lines:
        if line.startswith(constants.LOAN):
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

        if line.startswith(constants.PAYMENT):
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
        if line.startswith(constants.BALANCE):
            if line.split().__len__() == 4:
                bank_name, borrower_name, emi_no = line.split()[1:]

                if borrower_name in ledger:
                    ledger_entry = ledger[borrower_name]

                    amount_paid = int(ledger_entry.amount_paid(emi_no=float(emi_no)))
                    no_of_emis_left = int(ledger_entry.no_of_emi_left(emi_no=float(emi_no)))
                    print(bank_name, borrower_name, str(amount_paid), str(no_of_emis_left))
                else:
                    Exception("No borrower by that name")
            else:
                Exception("Incorrect number of arguments for BALANCE command")


if __name__ == "__main__":
    main()
