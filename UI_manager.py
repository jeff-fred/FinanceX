''' Object to control all UI useful functions. '''

# Imports 
import sys, os

from data_manager import DatabaseHandling

from PyQt5 import QtWidgets, uic, QtGui
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
        self.currentTable = windowUI.currentTransTable
        self.removalTable = windowUI.remTransTable

        self.widget_setup()

        self.resize_table(self.currentTable)
        self.resize_table(self.removalTable)
        self.load_data(self.currentTable, db.return_all(tableName))

    
    # Widget connection
    def widget_setup(self):
        self.cancelButton.clicked.connect(self.hide)
        self.confirmButton.clicked.connect(self.confirm_removal)
        self.removeButton.clicked.connect(self.removal_move)
        self.keepButton.clicked.connect(self.keep_move)


    # Move selected widgets to removal table > None
    def removal_move(self):
        pass
        

    # Move selected widgets back to current trans table > None     
    def keep_move(self):
        pass


    # Remove from MAIN table and exit window
    def confirm_removal(self):
        pass
    

    # Resize table columns > None
    def resize_table(self, tableObject):
        tableObject.setColumnWidth(0, 40) 
        tableObject.setColumnWidth(1, 70)
        tableObject.setColumnWidth(2, 118)


    # Load tables with correct data > None
    def load_data(self, tableObject, data):
        tableObject.setRowCount(len(data))
        row = 0
        for i in data:
            tableObject.setItem(row, 0, QTableWidgetItem(str(data[row][0])))
            tableObject.setItem(row, 1, QTableWidgetItem(str(data[row][2])))
            tableObject.setItem(row, 2, QTableWidgetItem(str(data[row][3])))
            row += 1


class AddTransactionWindow(QMainWindow):
    ''' GUI to allow user to input a new transaction. '''
    def __init__(self, tableName):
        super().__init__()

        windowUI = uic.loadUi('UIs/TransactionAdditionWindow.ui', self)

        # Widgets
        self.cancelButton = windowUI.cancelButton
        self.cancelButton.clicked.connect(self.hide)