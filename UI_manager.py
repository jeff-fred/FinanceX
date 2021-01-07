''' Object to control all UI useful functions. '''

# Imports 
import sys, os

from data_manager import DatabaseHandling
from data_manager import Transaction

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem
from PyQt5.QtWidgets import QAbstractItemView


# Database Initialization to use with windows
db = DatabaseHandling()

class MainWindow(QMainWindow):
    ''' Control of MAIN window of program. '''
    def __init__(self):
        super().__init__()

        windowUI = uic.loadUi('UIs/MainWindowUI.ui', self)

        # WIDGET CONTROLLING VARIABLES
        self.incomeAddButton = windowUI.addIncomeButton
        self.incomeRemoveButton = windowUI.removeIncomeButton
        self.expenseAddButton = windowUI.addExpenseButton
        self.expenseRemoveButton = windowUI.removeExpenseButton
        self.expenseTable = windowUI.expensesTable
        self.incomeTable = windowUI.incomeTable

        self.resize_table(self.incomeTable)
        self.resize_table(self.expenseTable)

        self.load_data(self.incomeTable, db.return_all('Income'))
        self.load_data(self.expenseTable, db.return_all('Expenses'))
        

    # Resize table columns > None
    def resize_table(self, tableObject):
        tableObject.setColumnWidth(0, 40) 
        tableObject.setColumnWidth(1, 70)
        tableObject.setColumnWidth(2, 85)


    # Load data into tables
    def load_data(self, tableObj, data):
        tableObj.setRowCount(len(data))
        row = 0
        for item in data:
            trans = Transaction(item[0], item[1], item[2], item[3])

            tableObj.setItem(row, 0, trans.get_id())
            tableObj.setItem(row, 1, trans.get_date())
            tableObj.setItem(row, 2, trans.get_type())
            tableObj.setItem(row, 3, trans.get_amount())

            row += 1
    

class RemoveTransactionWindow(QMainWindow):
    ''' GUI to allow user to remove transactions from table. '''
    def __init__(self, tableName):
        super().__init__()

        windowUI = uic.loadUi('UIs/TransactionRemovalWindow.ui', self)
       
        # WIDGET CONTROLLING VARIABLES
        self.removeButton = windowUI.removePushButton
        self.keepButton = windowUI.keepPullButton
        self.confirmButton = windowUI.confirmRemovalButton
        self.cancelButton = windowUI.cancelRemovalButton
        self.currentTable = windowUI.currentTransTable
        self.removalTable = windowUI.remTransTable
        self.widget_setup()


        self.resize_table(self.currentTable)
        self.resize_table(self.removalTable)

        self.load_data(self.currentTable, db.return_all(tableName))


    # Setup and connect widgets
    def widget_setup(self):
        self.removeButton.clicked.connect(self.remove_move)
        self.currentTable.setSelectionMode(QAbstractItemView.SelectionMode(1))
        self.currentTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior(1))
   
    # Resize table columns > None
    def resize_table(self, tableObject):
        tableObject.setColumnWidth(0, 40) 
        tableObject.setColumnWidth(1, 70)
        tableObject.setColumnWidth(2, 118)


    # Load data onto table
    def load_data(self, tableObj, data):
        tableObj.setRowCount(len(data))
        row = 0
        for item in data:
            trans = Transaction(item[0], item[1], item[2], item[3])

            tableObj.setItem(row, 0, trans.get_id())
            tableObj.setItem(row, 1, trans.get_type())
            tableObj.setItem(row, 2, trans.get_amount())

            row += 1


    # Move row from current into removal table
    def remove_move(self):
        print(self.currentTable.selectedItems())
    

class AddTransactionWindow(QMainWindow):
    ''' GUI to allow user to input a new transaction. '''
    def __init__(self, tableName):
        super().__init__()

        windowUI = uic.loadUi('UIs/TransactionAdditionWindow.ui', self)

        # Widgets
        self.cancelButton = windowUI.cancelButton
        self.cancelButton.clicked.connect(self.hide)