# Expenses manager
A small tool for expenses management with support for TUI and MongoDB. <br>
The basic idea was to develop a utility that simulate an old style application with modern functionalities.

## Building project
To obtain correct imports in various file run `pip install -e .` when in project folder (expenses_manager). <br>
Then the application can be started with `python3 ./path/main.py`. <br><br>
Project was developed with Linux Ubuntu 22.04 and Python 3.10. <br>
I did not test it on Windows/macOS (it should work, if the appropriate dependencies are installed). <br>
The main used libraries were PyMongo and Textual.

## Available functionalities
A brief list of currently available and WIP functionalities:
- [X] Insertion of income,
- [X] Insertion of expense,
- [X] View your expenses,
- [X] View your incomes,
- [X] Dump database in a JSON file,
- [X] Delete income(s),
- [X] Delete expense(s),
- [ ] Complete support for resize (right now it struggles on tiny windows).

## Customization
You can easily customize the look of your application by editing the (T)CSS in `expenses_manager/UI/styles` folder. <br>