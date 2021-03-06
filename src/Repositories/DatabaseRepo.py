from sqlite3.dbapi2 import Connection
from sqlite3 import Error

class DatabaseRepo:
    conn: Connection
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def create_tables(self):
        # create client table if it does not exist
        tb_create = '''CREATE TABLE User (Id INTEGER PRIMARY KEY, UserName TEXT NOT NULL UNIQUE,Password TEXT NOT NULL UNIQUE,PrivateKey TEXT NOT NULL UNIQUE, PublicKey TEXT NOT NULL UNIQUE, LastLogin TEXT)'''
        try:
            self.cur.execute(tb_create)
            self.conn.commit()
        except Error as e:
            return

        tb_create = '''create table Block
                        (
                                Id  INTEGER PRIMARY KEY,
                                BlockHash TEXT,
                                BlockNonce integer,
                                TransactionsData TEXT,
                                MinedUserId
                                referencing User,
                                PreviousBlockId
                                referencing Block,
                                verified boolean,
                                pending boolean,
                                Modified TEXT,
                                Created TEXT
                        );
                        '''
        try:
            self.cur.execute(tb_create)
            self.conn.commit()
        except Error as e:
            return


        tb_create = '''create table Transactions
                    (
                        Id  INTEGER PRIMARY KEY,
                        Sender    integer
                            constraint Transactions_Users_Id_fk
                                references User,
                        Receiver    integer
                        constraint Transactions_Users_Id_fk
                            references User,
                        TxValue  decimal,
                        TxFee  decimal,
                        TransactionSignature TEXT,
                        FalseTransaction boolean,
                        Created TEXT,
                        Modified TEXT
                    );'''
        try:
            self.cur.execute(tb_create)
            self.conn.commit()
        except Error as e:
            return

        tb_create = '''create table BlockCheck
                        (
                                Id  INTEGER PRIMARY KEY,
                                BlockId integer
                                references Block,
                                validatedUserId
                                references User,
                                BlockCorrect BOOLEAN,
                                Created TEXT
                        );
                        '''
        try:
            self.cur.execute(tb_create)
            self.conn.commit()
        except Error as e:
            return