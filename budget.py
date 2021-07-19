import math


class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        budget = [self.name.center(30, '*')]
        for item in self.ledger:
            # budget.append(item["description"].ljust(23) + f"{item['amount']: 5.2f}")
            # budget.append(f'{item["description"]:<23.23}{item["amount"]:>7.2f}')
            budget.append('{:<23.23}{:>7.2f}'.format(item["description"], item["amount"]))
        budget.append(f'Total: {self.get_balance()}')
        return '\n'.join(budget)

    def deposit(self, deposit_amount, deposit_description=''):
        self.ledger.append({"amount": deposit_amount, "description": deposit_description})

    def withdraw(self, withdraw_amount, withdraw_description=''):
        if self.check_funds(withdraw_amount):
            self.ledger.append({"amount": -withdraw_amount, "description": withdraw_description})
            return True
        return False

    def get_balance(self):
        return sum([item["amount"] for item in self.ledger])

    def transfer(self, transfer_amount, transfer_category):
        if self.check_funds(transfer_amount):
            self.withdraw(transfer_amount, f"Transfer to {transfer_category.name}")
            transfer_category.deposit(transfer_amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, check_amount):
        return False if check_amount > self.get_balance() else True


def create_spend_chart(categories):
    spend_chart = ["Percentage spent by category"]

    item_withdraws = []
    for cat_item in categories:
        item_withdraws.append(sum([abs(ledger_item["amount"]) for ledger_item in cat_item.ledger if ledger_item["amount"] < 0]))

    item_percentages = [int(math.floor(((item / sum(item_withdraws)) * 100))) for item in item_withdraws]
    for percentage in range(100, -10, -10):
        percentages_string = ''.join([('o' + ' ' * 2 if item >= percentage else ' ' * 3) for item in item_percentages])
        spend_chart.append(f"{percentage:>3}| " + percentages_string)

        # spend_chart.append(f"{percentage:>3}| ")
        # for item in item_percentages:
        #     if item <= percentage:
        #         spend_chart[i] += 'o  '
        #     else:
        #         spend_chart[i] += '   '

    spend_chart.append(' ' * 4 + '-' * ((len(categories) * 3) + 1))

    cat_names = [item.name for item in categories]
    cat_max_len = len(max(cat_names, key=len))
    for i in range(cat_max_len):
        cat_string = ''.join([(name[i] + ' ' * 2) if i < len(name) else ' ' * 3 for name in cat_names])
        spend_chart.append(' ' * 5 + cat_string)

    # return spend_chart
    return '\n'.join(spend_chart)
