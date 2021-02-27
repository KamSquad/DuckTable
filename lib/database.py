import sqlite3

from lib import strings
from lib import config


class LocalDB:
    """
    CLASS FOR WORKING WITH LOCAL DB BASED ON SQLITE
    """
    def __init__(self):
        self.db_path = config.get_argument('table_database_path')
        try:
            """
            CONNECT TO DB
            """
            self.db_connection = sqlite3.connect(self.db_path)
            self.db_cursor = self.db_connection.cursor()
            if LocalDB.local_db_is_empty(self):
                LocalDB.init_empty_db(self)
        except Exception as ex:
            print('[!] Error:\t' + str(ex))
            print('[!] Debug Warning:\tlocal db connection failed, running first init...')
            self.db_connection = sqlite3.connect(self.db_path)
            self.db_cursor = self.db_connection.cursor()
            LocalDB.init_empty_db(self)

    def init_empty_db(self):
        """
        FUNCTION FOR FIRST INIT OF DB
        """
        self.db_cursor.executescript(strings.database_init_script)
        self.db_connection.commit()  # save changes

    def local_db_is_empty(self):
        tables = ['tables']
        for table in tables:
            if not self.db_cursor.execute('SELECT COUNT(*) FROM {table}'.format(table=table)).fetchone():
                return True

    def save_local_records(self, records):
        for rec in records:
            self.add_table_record(rec)

    def add_table_record(self, record):
        self.db_cursor.executescript(
            """
            INSERT OR IGNORE INTO tables (msg_id, datetime, univer, fak, in_queue) 
            VALUES ('{msg_id}', '{datetime}', '{univer}', '{fak}', '{queue}');
            """.format(msg_id=record.msg_id,
                       datetime=record.date.strftime('%d %b %Y %H:%M:%S'),
                       univer=record.univer,
                       fak=record.fak,
                       queue='opened'))
        self.db_connection.commit()  # save changes

    def get_table_records(self):
        # column_names = ['id', 'msg_id', 'object', 'in_queue']
        local_news = self.db_cursor.execute('SELECT * FROM tables').fetchall()
        return local_news


if __name__ == "__main__":
    db = LocalDB()
    # print()  # uncomment for #debug
