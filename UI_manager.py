''' Object to control all UI useful functions. '''

# Imports 
import sys, os

from data_manager import DatabaseHandling
from data_manager import Transaction

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QListWidgetItem, QAbstractItemView


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

        self.tableName = tableName
       
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

        self.load_data(self.currentTable, db.return_all(self.tableName))


    # Setup and connect widgets
    def widget_setup(self):
        self.removeButton.clicked.connect(self.remove_action)
        self.cancelButton.clicked.connect(self.cancel_action)
        self.keepButton.clicked.connect(self.keep_action)
        self.confirmButton.clicked.connect(self.confirm_action)
   
        self.currentTable.setSelectionMode(QAbstractItemView.SelectionMode(1))
        self.currentTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior(1))
        self.removalTable.setSelectionMode(QAbstractItemView.SelectionMode(1))
        self.removalTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior(1))
   

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
    

    # Cancel, close and reset window > None
    def cancel_action(self):
        self.removalTable.clearContents()
        self.removalTable.setRowCount(0)
        self.currentTable.clearContents()
        self.currentTable.setRowCount(0)
        self.load_data(self.currentTable, db.return_all(self.tableName))
        self.close()


    # Move row from current into removal table
    def remove_action(self):
        transSelected = self.currentTable.selectedItems()
        selectedID = transSelected[0].clone()
        selectedType = transSelected[1].clone()
        selectedAmount = transSelected[2].clone()

        self.removalTable.insertRow(self.removalTable.rowCount())
        self.removalTable.setItem(self.removalTable.rowCount()-1, 0, selectedID)
        self.removalTable.setItem(self.removalTable.rowCount()-1, 1, selectedType)
        self.removalTable.setItem(self.removalTable.rowCount()-1, 2, selectedAmount)

        self.currentTable.removeRow(transSelected[0].row())


    # Keep action
    def keep_action(self):
        transSelected = self.removalTable.selectedItems()
        selectedID = transSelected[0].clone()
        selectedType = transSelected[1].clone()
        selectedAmount = transSelected[2].clone()

        row = self.currentTable.rowCount()

        self.currentTable.insertRow(row)
        self.currentTable.setItem(row, 0, selectedID)
        self.currentTable.setItem(row, 1, selectedType)
        self.currentTable.setItem(row, 2, selectedAmount)

        self.removalTable.removeRow(transSelected[0].row())

    
    # Confirm removal action > None
    def confirm_action(self):
        rows = self.removalTable.rowCount()
        for row in range(0, rows):
            transID = int(self.removalTable.item(row, 0).text())
            db.remove_from_table(self.tableName, transID)
        
        MainWindow().incomeTable.update()
        self.cancel_action()


class AddTransactionWindow(QMainWindow):
    ''' GUI to allow user to input a new transaction. '''
    def __init__(self, tableName):
        super().__init__()

        windowUI = uic.loadUi('UIs/TransactionAdditionWindow.ui', self)

        # Widgets
        self.cancelButton = windowUI.cancelButton
        self.cancelButton.clicked.connect(self.hide)