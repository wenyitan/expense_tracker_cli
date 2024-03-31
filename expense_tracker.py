from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.rule import Rule
from rich.table import Table
from rich import box
import datetime
from models import Transaction, Category
from db import Db

class Expense_Tracker:
    def __init__(self):
        self.console = Console()
        self.db = Db()
        self.started = True

    def print_options(self, options):
        for option in options.keys():
            self.console.print(f"{option}. {options[option]['option']}.")
    
    def double_confirm_choices(self, options, choice):
        confirmation = Confirm.ask(f"You have chosen {choice}. {options[choice]['option']}. Yes or no?")
        return confirmation
    
    def prompt_action(self, options):
        self.print_options(options)
        return options
    
    def prompt_choice_return_choice(self, options):
        return IntPrompt.ask("What is your choice?", choices=[str(option) for option in options.keys()])
    
    def double_confirm_input(self, input):
        return Confirm.ask(input)
    
    def start_add_transaction(self):
        spending = FloatPrompt.ask("Okay, how much did you spend?")
        category_options = self.db.get_all_categories()
        self.console.print(f"Okay, you have spent ${spending}. What did you spend it on?")
        self.prompt_action(options=category_options)
        category_choice = self.prompt_choice_return_choice(category_options)
        category_name = category_options[category_choice]["option"]        
        remarks = Prompt.ask("Do you have any remarks regarding this transaction?")
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        if self.double_confirm_input(f"Okay, you have spent ${spending} on {category_name}. Is that correct?"):
            print("Log transaction")
            category = Category(category_choice, category_name)
            transaction = Transaction(amount=spending, date=now, remarks=remarks, category=category)
            if self.db.save_transaction(transaction=transaction):
                print("Transaction logged!")
            else:
                print("Log transaction failed")
        else:
            self.start_add_transaction()

    def view_monthly_transaction(self):
        now = datetime.datetime.now()
        table = Table(title=f"Transactions for {now.strftime('%B-%Y')}")
        table.add_column("Id", style="cyan")
        table.add_column("Amount ($)", style="green", justify="right")
        table.add_column("Category", style="red")
        table.add_column("Date")
        table.add_column("Remarks", style="magenta")
        transactions = self.db.get_months_transactions(now.month, now.year)
        total = 0
        for transaction in transactions:
            id, amount, category, date, remark = (map(lambda x: str(x) if not isinstance(x, datetime.date) else x.strftime('%d-%b-%Y'), transaction.values()))
            total += float(amount)
            table.add_row(id+".", amount, category, date, remark)
        table.add_section()
        table.add_row("Total", str(total), "", "")
        self.console.print(table)
    
    def stop(self):
        self.started = False
        self.console.print("Bye bye!")

    def prompt_base_actions(self):
        reprompt = False
        while not reprompt:
            self.console.print("What would you like to do?")
            options = {
                1: {"option": "Add a transaction", "callback": self.start_add_transaction}, 
                2: {"option": "View month's transactions", "callback": self.view_monthly_transaction}, 
                3: {"option": "Exit", "callback": self.stop}
            }
            self.prompt_action(options=options)
            choice = self.prompt_choice_return_choice(options)
            if self.double_confirm_choices(options, choice):
                reprompt = True
                options[choice]["callback"]()

    def start(self):
        top_rule = Rule(title="Expense [blue]Tracker")
        self.console.print(top_rule)
        self.console.print("Welcome [blue]Wen Yi[/blue]!")
        while self.started:
            self.prompt_base_actions()