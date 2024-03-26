class Expense:
    def __init__(self, desc, amount, timestamp):
        self.desc = desc
        self.amount = amount
        self.timestamp = timestamp

    def to_dict(self):
        return {'desc': self.desc, 'amount': self.amount, 'timestamp': self.timestamp}
