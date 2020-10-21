import mysql.connector


class Database:
    # THIS API IS FOR MYSQL DATA BASE SETUP ON MY LOCAL COMPUTER
    # HERE QUERIES FOR DIFFERENT TYPES OF OPERATIONS WILL BE EXECUTED.
    def __init__(self, dbconfig: dict):
        # THIS IS CONFIGURATION OF DATABASE TO OPERATE
        
        self.config = dbconfig

    def __enter__(self):
        # THIS PART IS FOR CONNECTING WITH THE MYSQL SERVER ANF DATABASE AND RETURNING
        # CORRECT RESULTS OF QUERIES MADE BY USER OR OTHER FUNCTIONS.\

        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # AFTER EXECUTION OF QUERY, THE CONNECTION HAS TO BE CLOSED BETWEEN THIS AOI AND
        # DATABASE OR SERVER.

        self.conn.commit()
        self.cursor.close()
        self.conn.close()
