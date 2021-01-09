''' Application to track your finances and view the latest data on them. '''

# Imports
import sys, os

from data_manager import DatabaseHandling
from UI_manager import MainWindow, RemoveTransactionWindow
from UI_manager import AddTransactionWindow

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem



if __name__ == '__main__':
    # Application creation   
    application = QApplication(sys.argv)

    # Window Objects
    mainWindow = MainWindow()
    
    incomeRemWindow = RemoveTransactionWindow('Income')  
    expensesRemWindow = RemoveTransactionWindow('Expenses')

    incomeAddWindow = AddTransactionWindow('Income')
    expensesAddWindow = AddTransactionWindow('Expenses')

    mainWindow.incomeRemoveButton.clicked.connect(incomeRemWindow.show)
    mainWindow.expenseRemoveButton.clicked.connect(expensesRemWindow.show)
    mainWindow.addIncomeButton.clicked.connect(incomeAddWindow.show)

    mainWindow.show()
    sys.exit(application.exec_())