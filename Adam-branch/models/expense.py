class Expense:
    def __init__(self, date, account, category, note, amount):
        self.date = date
        self.account = account
        self.category = category
        self.note = note
        self.amount = amount

    def to_tuple(self):
        """Convert to a format suitable for DB insertion."""
        return (self.date, self.account, self.category, self.note, self.amount)
