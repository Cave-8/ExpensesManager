###########
# Imports #
###########
# Frontend
from datetime import datetime
import pprint

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Header, Footer, Button, Static, Input, DataTable
from textual.containers import VerticalScroll, Container

# Backend
from ..backend.middleware import Middleware
from ..backend.backend import dumpDB, setup, insertExpense, insertIncome, retrieveExpenses, retrieveIncomes

mid = Middleware


###############
# Menu widget #
###############
# Options menu
class Menu(Widget):
    BORDER_TITLE = "Menu"

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="scroller"):
            yield Button("Register new expense", id="t0", classes="menuButtons")
            yield Button("Register new income", id="t1", classes="menuButtons")
            yield Button("See your expenses", id="t2", classes="menuButtons")
            yield Button("See your incomes", id="t3", classes="menuButtons")
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

    def on_mount(self) -> None:
        expenses = [list(x.values())[1:] for x in retrieveExpenses(mid)]

        table = self.query_one('#expensesTable', DataTable)
        table.zebra_stripes = 1
        table.add_columns("Description", "Amount", "Timestamp")

        for x in expenses:
            table.add_row(x[0], x[1], x[2])


class ShowIncomes(Widget):

    def compose(self) -> ComposeResult:
        yield DataTable(id="incomesTable", classes="table")

    def on_mount(self) -> None:
        expenses = [list(x.values())[1:] for x in retrieveIncomes(mid)]

        table = self.query_one('#incomesTable', DataTable)
        table.zebra_stripes = 1
        table.add_columns("Description", "Amount", "Timestamp")

        for x in expenses:
            table.add_row(x[0], x[1], x[2])


class OpWindow(Widget):
    BORDER_TITLE = "Action"
    # Attribute reactive to changes
    currTab = reactive("")

    # Update requested
    def watch_currTab(self) -> None:
        self.refresh(recompose=True)

    def compose(self) -> ComposeResult:
        match self.currTab:
            case "t0":
                yield InsertExpense()
            case "t1":
                yield InsertIncome()
            case "t2":
                yield ShowExpenses()
            case "t3":
                yield ShowIncomes()
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
    BINDINGS = [
        #    Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("ctrl+q", "quit", "Quit application"),
    ]

    #################
    # Create layout #
    #################
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield Menu(classes="windowMenu")
        yield OpWindow(classes="windowActive")

    #    yield Footer()

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
            nameExp = self.query_one('#nameExpense', Input)
            amount = self.query_one('#amountExpense', Input)
            ts = datetime.now().strftime("%Y%m%d-%H%M")
            insertExpense(mid, nameExp.value, amount.value, ts)
            w.currTab = event.button.id

    # Confirm insertion of a new income
    @on(Button.Pressed, "#confirmIncome")
    def income_confirm(self, event: Button.Pressed):
        for w in self.query(OpWindow):
            nameInc = self.query_one('#nameIncome', Input)
            amount = self.query_one('#amountIncome', Input)
            ts = datetime.now().strftime("%Y%m%d-%H%M")
            insertIncome(mid, nameInc.value, amount.value, ts)
            w.currTab = event.button.id

    # Dump database
    @on(Button.Pressed, "#dumpJSON")
    def create_dump(self):
        dumpDB(mid)

    # Toggle dark mode
    # def action_toggle_dark(self) -> None:
    #    self.dark = not self.dark

    # Close application
    def action_quit(self) -> None:
        self.exit()


def boot():
    (exp, inc) = setup()
    global mid
    mid = Middleware(exp, inc)

    app = ExpensesManager()
    app.run()