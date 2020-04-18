import sqlite3


class Connect(object):
    """Create/Connect with database"""

    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error:
            return False

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        """Close connection"""
        if self.conn:
            self.conn.close()


class CrawlerDb(object):
    """That class represent the the Crawler tables: investing and currency"""

    def __init__(self):
        self.db = Connect('crawler.db')

    def close_connection(self):
        self.db.close_db()

    def close_db(self):
        if self.db.conn:
            self.db.conn.close()

    def create_schema(self):
        self.db.conn.execute('''CREATE TABLE IF NOT EXISTS 
                                investing(investing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          name TEXT,
                                          last_rs NUMERIC,
                                          high_rs NUMERIC,
                                          low_rs NUMERIC,
                                          last_usd NUMERIC,
                                          high_usd NUMERIC,
                                          low_usd NUMERIC,
                                          chg TEXT,
                                          chg_percent TEXT,
                                          vol TEXT,
                                          time timestamp);''')

        self.db.conn.execute('''CREATE TABLE IF NOT EXISTS 
                                currency(currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                         currency TEXT,
                                         value NUMERIC, 
                                         perc NUMERIC,
                                         timestamp timestamp);''')

        self.db.commit_db()

    def insert_currency(self, currency):
        """
        Insert currency model into currency table.
        :param currency: Models.currency
        :return:
        """
        self.db.cursor.execute("""
                    INSERT INTO currency (currency, value, perc, timestamp)
                    VALUES (?,?,?,?)
                    """, (currency.currency, currency.value, currency.percent, currency.timestamp))

        self.db.commit_db()

    def insert_ibovespa_list(self, ibovespa_data_frame):
        """
        Insert a DataFrame of ibovespa equities into Investing table.
        :param ibovespa_data_frame: DataFrame of IBovespa Equities
        """
        for row in ibovespa_data_frame.itertuples():
            insert_table = """
            INSERT INTO investing(name, last_rs, high_rs, low_rs, chg, chg_percent, vol, time) 
            VALUES (?,?,?,?,?,?,?,?)
            """
            self.db.cursor.execute(insert_table, row[1:])

        self.db.commit_db()

    def insert_nasdaq_list(self, nasdaq_data_frame):
        """
        Insert a DataFrame of Nasdaq equities into Investing table.
        :param nasdaq_data_frame: DataFrame of Nasdaq Equities
        """
        for row in nasdaq_data_frame.itertuples():
            insert_table = """
            INSERT INTO investing(name, last_usd, high_usd, low_usd, chg, chg_percent, vol, time, 
                                  last_rs, high_rs, low_rs) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """
            self.db.cursor.execute(insert_table, row[1:])

        self.db.commit_db()
