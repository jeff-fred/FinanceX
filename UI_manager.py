''' Object to control all UI useful functions. '''

# Imports 
import sys, os

from data_manager import DatabaseHandling

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem


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
        self.incomeTable = windowUI.incomeTable
        self.expenseAddButton = windowUI.addExpenseButton
        self.expenseRemoveButton = windowUI.removeExpenseButton
        self.expenseTable = windowUI.expensesTable

        self.setup_tables()
        

    # MainWindow table setup
    def setup_tables(self):
        self.resize_table(self.incomeTable)
        self.resize_table(self.expenseTable)
        self.load_data(self.incomeTable, db.return_all('Income'))
        self.load_data(self.expenseTable, db.return_all('Expenses'))
        

    # Resize table columns > None
    def resize_table(self, tableObject):
        tableObject.setColumnWidth(0, 40) 
        tableObject.setColumnWidth(1, 70)
        tableObject.setColumnWidth(2, 85)

    
    # Load the data into the table columns > None
    def load_data(self, tableObject, data):
        tableObject.setRowCount(len(data))
        row = 0
        for i in data:
            tableObject.setItem(row, 0, QTableWidgetItem(str(data[row][0])))
            tableObject.setItem(row, 1, QTableWidgetItem(str(data[row][1])))
            tableObject.setItem(row, 2, QTableWidgetItem(str(data[row][2])))
            tableObject.setItem(row, 3, QTableWidgetItem(str(data[row][3])))
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
        self.currentList = windowUI.currentTransList
        self.removalList = windowUI.removalTransList
        self.widget_setup()

        self.load_list_data(tableName)


    # Widget connection setup
    def widget_setup(self):
        self.removeButton.clicked.connect(self.removal)


    # Fill CURRENT list with tableName data
    def load_list_data(self, tableName):
        data = db.return_all(tableName)
       
        row = 0
        for i in data:
            self.currentList.addItem(QListWidgetItem(str(data[row])))
            row += 1
        

    # Function for removal button
    def removal(self):
        the_object = self.currentList.selectedItems()
        
        object_methods = [method_name for method_name in dir(the_object)
                  if callable(getattr(the_object, method_name))]
        print(object_methods)
        the_object.pop()

class AddTransactionWindow(QMainWindow):
    ''' GUI to allow user to input a new transaction. '''
    def __init__(self, tableName):
        super().__init__()

        windowUI = uic.loadUi('UIs/TransactionAdditionWindow.ui', self)

        # Widgets
        self.cancelButton = windowUI.cancelButton
        self.cancelButton.clicked.connect(self.hide)