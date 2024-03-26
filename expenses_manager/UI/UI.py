###########
# Imports #
###########
# Frontend
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Header, Footer, Button, Static, Input
from textual.containers import VerticalScroll, Container

# Backend
from ..backend.middleware import Middleware
from ..backend.backend import dumpDB, setup
mid = Middleware
###############
# Menu widget #
###############
# Options menu
class Menu(Widget):
    BORDER_TITLE = "Menu"

    def compose(self) -> ComposeResult:
        with VerticalScroll():
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
        with VerticalScroll():
            yield Container(Input(placeholder="Description of your expense", classes="inputForm"), classes="inputContainer")
            yield Container(Input(placeholder="Amount of your expense", classes="inputForm"), classes="inputContainer")
            yield Button("Confirm expense", id="confirmExpense", classes="inputButtons")

class InsertIncome(Widget):

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Container(Input(placeholder="Description of your income", classes="inputForm"), classes="inputContainer")
            yield Container(Input(placeholder="Amount of your income", classes="inputForm"), classes="inputContainer")
            yield Button("Confirm income", id="confirmIncome", classes="inputButtons")

class OpWindow(Widget):
    BORDER_TITLE = "Action"
    # Attribute reactive to changes
    currTab = reactive("")

    # Update requested
    def watch_currTab(self) -> None:
        self.refresh(recompose=True)

    def compose(self) -> ComposeResult:
         with self.prevent():
             match self.currTab:
                case "t0":
                    yield InsertExpense()
                case "t1":
                    yield InsertIncome()
                case "t2":
                    yield Static("Test2", classes="actionWindow")
                case "t3":
                    yield Static("Test3", classes="actionWindow")
                case "dumpJSON":
                    yield Static("Dump created, visible in dumps folder!")
                case "confirmExpense" | "confirmIncome":
                    #TODO Insert actual database validation
                    yield Static("Operation confirmed ✓")
                case _:
                    yield Static()

############
# Main expenses_manager #
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
        # Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("ctrl+q", "quit", "Quit application"),
    ]

    #################
    # Create layout #
    #################
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield Menu(classes="windowMenu")
        yield OpWindow(classes="windowActive")

        #yield ActiveScene(classes="window")
        yield Footer()

    #####################
    # Events management #
    #####################
    # This will manage button pressed in Menu and update attribute in OpWindow
    @on(Button.Pressed)
    def menu_button_pressed(self, event: Button.Pressed):
        for w in self.query(OpWindow):
            with w.prevent():
                w.currTab = event.button.id

    # Confirm insertion of a new expense
    @on(Button.Pressed, "#confirmExpense")
    def expense_confirm(self, event: Button.Pressed):
        for w in self.query(OpWindow):
            with w.prevent():
                # TODO Execute insert
                w.currTab = event.button.id

    # Confirm insertion of a new income
    @on(Button.Pressed, "#confirmIncome")
    def income_confirm(self, event: Button.Pressed):
        for w in self.query(OpWindow):
            with w.prevent():
                # TODO Execute insert
                w.currTab = event.button.id

    # Dump database
    @on(Button.Pressed, "#dumpJSON")
    def create_dump(self, event: Button.Pressed):
        for w in self.query(OpWindow):
            with w.prevent():
                dumpDB(mid)


    # Toggle dark mode
    # def action_toggle_dark(self) -> None:
    #     self.dark = not self.dark

    # Close application
    def action_quit(self) -> None:
        self.exit()


def boot():
    (exp, inc) = setup()
    global mid
    mid = Middleware(exp, inc)

    app = ExpensesManager()
    app.run()