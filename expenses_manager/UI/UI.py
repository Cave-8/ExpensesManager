###########
# Imports #
###########
# Frontend
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Header, Footer, Button, Static, Input, DataTable, Select
from textual.containers import VerticalScroll, Container

# Backend
from ..backend.middleware import Middleware
from ..backend.backend import dumpDB, setup, insertExpense, insertIncome, retrieveExpenses, retrieveIncomes, \
    deleteExpense, deleteIncome

from datetime import datetime

mid = Middleware


###############
# Menu widget #
###############
# Options menu
class Menu(Widget):
    BORDER_TITLE = "Menu"

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="scroller"):
            yield Button("Register new expense", id="insertExpense", classes="menuButtons")
            yield Button("Register new income", id="insertIncome", classes="menuButtons")
            yield Button("See your expenses", id="showExpenses", classes="menuButtons")
            yield Button("See your incomes", id="showIncomes", classes="menuButtons")
            yield Button("Delete expense", id="deleteExpense", classes="menuButtons")
            yield Button("Delete income", id="deleteIncome", classes="menuButtons")
            yield Button("Dump JSON", id="dumpJSON", classes="menuButtons")


######################
# Operational window #
######################
class InsertExpense(Widget):

    def compose(self) -> ComposeResult:
        yield Container(Input(placeholder="Description of your expense", classes="inputForm", id="nameExpense"),
                        classes="inputContainer")
        yield Container(
            Input(placeholder="Amount of your expense", classes="inputForm", id="amountExpense", type="number"),
            classes="inputContainer")
        yield Button("Confirm expense", id="confirmExpense", classes="inputButton")


class InsertIncome(Widget):

    def compose(self) -> ComposeResult:
        yield Container(Input(placeholder="Description of your income", classes="inputForm", id="nameIncome"),
                        classes="inputContainer")
        yield Container(
            Input(placeholder="Amount of your income", classes="inputForm", id="amountIncome", type="number"),
            classes="inputContainer")
        yield Button("Confirm income", id="confirmIncome", classes="inputButton")


class ShowExpenses(Widget):

    def compose(self) -> ComposeResult:
        yield DataTable(id="expensesTable", classes="table")

    # Workaround to fit table width, no flexible columns available
    def on_refresh(self):
        table = self.query_one("#expensesTable", DataTable)
        table.disabled = True
        c_0, c_1 = 0, 0
        for c, i in zip(reversed(table.columns.values()), range(0, 3)):
            match i:
                case 0:
                    c.auto_width = True
                    c_0 = c.width
                case 1:
                    c.auto_width = True
                    c_1 = c.width
                case 2:
                    c.auto_width = False
                    c.width = int(table.size.width - 3 * c_0 - c_1)
        table.disabled = False

    def on_resize(self):
        table = self.query_one("#expensesTable", DataTable)
        table.disabled = True
        c_0, c_1 = 0, 0
        for c, i in zip(reversed(table.columns.values()), range(0, 3)):
            match i:
                case 0:
                    c.auto_width = True
                    c_0 = c.width
                case 1:
                    c.auto_width = True
                    c_1 = c.width
                case 2:
                    c.auto_width = False
                    c.width = int(table.size.width - 3 * c_0 - c_1)
        table.disabled = False

    def on_mount(self) -> None:
        expenses = [list(x.values())[1:] for x in retrieveExpenses(mid)]

        table = self.query_one("#expensesTable", DataTable)
        if len(expenses) == 0:
            table.disabled = True
        else:
            table.disabled = False
            table.zebra_stripes = 1
            table.add_column("Description", width=None)
            table.add_column("Amount", width=None)
            table.add_column("Timestamp", width=None)

            for x in expenses:
                table.add_row(x[0], x[1], x[2])

        table.refresh()


class ShowIncomes(Widget):

    def compose(self) -> ComposeResult:
        yield DataTable(id="incomesTable", classes="table")
        yield Static(id="sizer", expand=True)

    # Workaround to fit table width, no flexible columns available
    def on_refresh(self):
        table = self.query_one("#incomesTable", DataTable)
        table.disabled = True
        c_0, c_1 = 0, 0
        for c, i in zip(reversed(table.columns.values()), range(0, 3)):
            match i:
                case 0:
                    c.auto_width = True
                    c_0 = c.width
                case 1:
                    c.auto_width = True
                    c_1 = c.width
                case 2:
                    c.auto_width = False
                    c.width = int(table.size.width - 3 * c_0 - c_1)
        table.disabled = False

    def on_resize(self):
        table = self.query_one("#incomesTable", DataTable)
        table.disabled = True
        c_0, c_1 = 0, 0
        for c, i in zip(reversed(table.columns.values()), range(0, 3)):
            match i:
                case 0:
                    c.auto_width = True
                    c_0 = c.width
                case 1:
                    c.auto_width = True
                    c_1 = c.width
                case 2:
                    c.auto_width = False
                    c.width = int(table.size.width - 3 * c_0 - c_1)
        table.disabled = False

    def on_mount(self) -> None:
        incomes = [list(x.values())[1:] for x in retrieveIncomes(mid)]

        table = self.query_one("#incomesTable", DataTable)
        if len(incomes) == 0:
            table.disabled = True
        else:
            table.zebra_stripes = 1
            table.add_column("Description")
            table.add_column("Amount")
            table.add_column("Timestamp")

            for x in incomes:
                table.add_row(x[0], x[1], x[2])

            table.refresh()


class DeleteExpense(Widget):
    def compose(self) -> ComposeResult:
        incomes = [list(x.values())[1:] for x in retrieveExpenses(mid)]
        options = [(x[0], x[1], x[2]) for x in incomes]

        yield Select.from_values(options, id="selectDelExpense", prompt="Select expense to delete")
        yield Button("Delete expense", id="confirmDeleteExpense", classes="inputButton")


class DeleteIncome(Widget):
    def compose(self) -> ComposeResult:
        incomes = [list(x.values())[1:] for x in retrieveIncomes(mid)]
        options = [(str(x[0]), x[1], x[2]) for x in incomes]

        yield Select.from_values(options, id="selectDelIncome", prompt="Select income to delete")
        yield Button("Delete income", id="confirmDeleteIncome", classes="inputButton")


class OpWindow(Widget):
    BORDER_TITLE = "Action"
    # Attribute reactive to changes
    currTab = reactive("")

    # Update requested
    def watch_currTab(self) -> None:
        self.refresh(recompose=True)

    def compose(self) -> ComposeResult:
        match self.currTab:
            case "insertExpense":
                yield InsertExpense()
            case "insertIncome":
                yield InsertIncome()
            case "showExpenses":
                yield ShowExpenses()
            case "showIncomes":
                yield ShowIncomes()
            case "deleteExpense":
                yield DeleteExpense()
            case "deleteIncome":
                yield DeleteIncome()
            case "dumpJSON":
                yield Static("Dump created, visible in dumps folder!", classes="outputWindowActive")
            case "confirmExpense" | "confirmIncome":
                # TODO Insert actual database validation
                yield Static("Operation confirmed ✓", classes="outputWindowActive")
            case _:
                yield Static()


############
# Main App #
############
class ExpensesManager(App):
    ############
    # Preamble #
    ############

    # Style
    CSS_PATH = "styles/app.tcss"
    dark = False

    ###################
    # Footer commands #
    ###################

    # (Key, action, description)
    BINDINGS = [Binding("ctrl+q", "quit", "Quit application")]

    #################
    # Create layout #
    #################
    def compose(self) -> ComposeResult:

        yield Menu(id="menu", classes="windowMenu")
        yield OpWindow(id="opWindow", classes="windowActive")

        yield Footer()

    #####################
    # Events management #
    #####################
    # This will manage button pressed in Menu and update attribute in OpWindow
    @on(Button.Pressed)
    def menu_button_pressed(self, event: Button.Pressed):
        for w in self.query(OpWindow):
            w.currTab = event.button.id

    # Confirm insertion of a new expense
    @on(Button.Pressed, "#confirmExpense")
    def expense_confirm(self, event: Button.Pressed):
        for w in self.query(OpWindow):
            nameExp = w.query_one('#nameExpense', Input)
            amount = w.query_one('#amountExpense', Input)
            ts = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
            insertExpense(mid, nameExp.value, amount.value, ts)
            w.currTab = ""

    # Confirm insertion of a new income
    @on(Button.Pressed, "#confirmIncome")
    def income_confirm(self, event: Button.Pressed):
        for w in self.query(OpWindow):
            nameInc = w.query_one('#nameIncome', Input)
            amount = w.query_one('#amountIncome', Input)
            ts = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
            insertIncome(mid, nameInc.value, amount.value, ts)
            w.currTab = ""

    # Dump database
    @on(Button.Pressed, "#dumpJSON")
    def create_dump(self):
        dumpDB(mid)

    # Manage selection between options to delete
    @on(Select.Changed, "#selectDelIncome")
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)

    @on(Select.Changed, "#selectDelExpense")
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)

    @on(Button.Pressed, "#confirmDeleteExpense")
    def delete_expense(self):
        for w in self.query(OpWindow):
            query = w.query_one('#selectDelExpense', Select)
            if not query.is_blank():
                (desc, val, ts) = query.value
                deleteExpense(mid, desc, val, ts)
            w.currTab = ""

    @on(Button.Pressed, "#confirmDeleteIncome")
    def delete_income(self):
        for w in self.query(OpWindow):
            query = w.query_one('#selectDelIncome', Select)
            if not query.is_blank():
                (desc, val, ts) = query.value
                print(desc, val, ts)
                deleteIncome(mid, desc, val, ts)
            w.currTab = ""

    # Close application
    def action_quit(self) -> None:
        self.exit()


def boot():
    (exp, inc) = setup()
    global mid
    mid = Middleware(exp, inc)

    app = ExpensesManager()
    app.run()
