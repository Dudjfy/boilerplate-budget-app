import math


class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        budget = [self.name.center(30, '*')]
        for item in self.ledger:
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
        return check_amount <= self.get_balance()


class SpendChart:
    filled_cell = 'o  '
    empty_cell = '   '
    cell_len = len(empty_cell)

    def __init__(self, categories):
        self.lines = []

        self.categories = categories
        self.cat_spaced_len = len(categories) * 3
        self.chart_width = 5 + self.cat_spaced_len

        self.cat_withdraws = []

        self.cat_percentages = []

    def add_top_text(self):
        self.lines.append("Percentage spent by category")

    def create_cat_withdraws(self):
        for cat in self.categories:
            cat_sum = 0
            for ledger_item in cat.ledger:
                if ledger_item["amount"] < 0:
                    cat_sum += abs(ledger_item["amount"])
            self.cat_withdraws.append(cat_sum)

    def create_cat_percentages(self):
        cat_withdraws_sum = sum(self.cat_withdraws)
        for cat_sum in self.cat_withdraws:
            raw_percentage = cat_sum / cat_withdraws_sum
            rounded_percentage = math.floor(raw_percentage * 100)
            self.cat_percentages.append(rounded_percentage)

    def add_percentage_rows_with_cat_bars(self):
        self.create_cat_withdraws()
        self.create_cat_percentages()

        chart_max = 100
        chart_min = -10
        chart_step = -10
        for cur_percentage in range(chart_max, chart_min, chart_step):
            percentages_str = ''
            for cat_percentage in self.cat_percentages:
                percentages_str += self.filled_cell if cat_percentage >= cur_percentage else self.empty_cell

            self.lines.append("{:>3}| {}".format(cur_percentage, percentages_str))

    def add_bottom_line(self):
        bottom_line_len = 1 + self.cat_spaced_len
        bottom_line = '-' * bottom_line_len
        bottom_line_row = bottom_line.rjust(self.chart_width)
        self.lines.append(bottom_line_row)

    def add_cat_columns(self):
        cat_names = [cat.name for cat in self.categories]
        cat_max_len = len(max(cat_names, key=len))
        for letter_i in range(cat_max_len):
            cat_str = ''
            for name in cat_names:
                letter_cell = self.empty_cell
                if letter_i < len(name):
                    letter = name[letter_i]
                    letter_cell = letter.ljust(self.cell_len)
                cat_str += letter_cell

            self.lines.append(cat_str.rjust(self.chart_width))


def create_spend_chart(categories):

    spend_chart = SpendChart(categories)

    spend_chart.add_top_text()
    spend_chart.add_percentage_rows_with_cat_bars()
    spend_chart.add_bottom_line()
    spend_chart.add_cat_columns()

    return '\n'.join(spend_chart.lines)
