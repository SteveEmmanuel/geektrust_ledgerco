class Payment:
    def __init__(self):
        pass

    def __init__(self, **kwargs):
        self.bank_loan = kwargs['bank_loan']
        self.lump_sum_amount = kwargs['lump_sum_amount']
        self.emi_no = kwargs['emi_no']
