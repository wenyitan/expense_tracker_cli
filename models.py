class Transaction:
    def __init__(self, amount, date, category, remarks) -> None:
        self.amount = amount
        self.date = date
        self.category = category
        self.remarks = remarks

    def get_amount(self):
        return self.amount
    
    def get_date(self):
        return self.date
    
    def get_category(self):
        return self.category
    
    def get_remarks(self):
        return self.remarks
    
class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name