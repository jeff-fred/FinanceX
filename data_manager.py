''' Data handling and management of formats, table, and results. '''

# Imports
import sqlite3, datetime, os



# Returns {month}{year} as a STRING
def month_and_year():
    return datetime.date.today().strftime('%B%Y')


class DatabaseHandling:
    ''' Control and modification functions of the database. '''
    def __init__(self):
        super().__init__()

        # Name for file
        date = month_and_year()

        # === OS HANDLE ===
        currentPath = os.getcwd()
        try:
            os.mkdir(os.path.join(os.getcwd(), 'Data'))
        except FileExistsError:
            pass
        os.chdir(os.path.join(os.getcwd(), 'Data'))


        # Creating database for current month
        # === SQLite3 Components ===
        self.connection = sqlite3.connect(month_and_year() +'.db')
        self.cursor = self.connection.cursor()
        # ==========================


        # Tables in db
        self.tables = ['Expenses', 'Income']
        self.tranTypes = ['WORK', 'NEED', 'FUN', 'CREDIT', 'OTHER', 'INV']

        self.create_table('Expenses')
        self.create_table('Income')

        # Exit path
        os.chdir(currentPath)

        
    # Create tableName table > None
    def create_table(self, tableName):
        query = '''
            CREATE TABLE IF NOT EXISTS ''' + tableName + '''(
                TransID INTEGER PRIMARY KEY,
                Day INTEGER,
                Type TEXT,
                Amount DOUBLE)
            '''
        with self.connection:
            self.cursor.execute(query)
            self.connection.commit()

    
    # Return all items in table under tableName > LIST
    def return_all(self, tableName):
        query = 'SELECT * FROM ' + tableName
        try:
            with self.connection:
                self.cursor.execute(query)
                return [list(i) for i in self.cursor.fetchall()]
        except Exception as e:
            return e

    
    # Add item to specified table > None
    def add_to_table(self, tableName, transDay, transType, amount):
        query = 'INSERT INTO ' + tableName + '(Day, Type, Amount) VALUES(?,?,?)'
        values = (transDay, transType, amount)
        with self.connection:
            self.cursor.execute(query, (values))
            self.connection.commit()


    # Remove from table by ITEM ID > None
    def remove_from_table(self, tableName, itemID):
        query = 'DELETE FROM ' + tableName + ' Where TransID=?'
        with self.connection:
            self.cursor.execute(query, (itemID,))
            self.connection.commit()


    # Return the total balance for {tableName} > INT
    def return_total(self, tableName):
        with self.connection:
            self.cursor.execute('SELECT Amount FROM ' + tableName)
            return sum([i[0] for i in self.cursor.fetchall()])

 
 