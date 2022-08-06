from ..utils import round_to_whole_no


class LedgerEntry:
    def __init__(self, bank_loan=None, payment=None):
        self.bank_loan = bank_loan
        self.payment = payment

    def add_payment(self, payment):
        self.payment = payment

    def balance(self):
        if self.payment is None:
            return self.bank_loan.total_amount()
        else:
            return self.bank_loan.total_amount() - self.payment.lump_sum_amount

    def amount_paid(self, emi_no):
        if self.payment is None:
            return emi_no * self.bank_loan.emi_amount()
        else:
            if emi_no >= self.payment.emi_no:
                return self.payment.lump_sum_amount +\
                       (self.balance()
                        if ((emi_no * self.bank_loan.emi_amount()) + self.payment.lump_sum_amount) >
                           self.bank_loan.total_amount()
                        else emi_no * self.bank_loan.emi_amount())
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

    def add_entry_to_ledger(self, bank_name, borrower_name, ledger_entry):
        self[bank_name] = {}
        self[bank_name][borrower_name] = ledger_entry
