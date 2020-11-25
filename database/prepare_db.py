import pymysql
from pymysql.cursors import DictCursor


class MysqlConnection(object):

    def __init__(self, user, password, db_name, host, port, charset='utf8'):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = host
        self.port = port
        self.charset = charset
        self.connection = self.connect()

    def get_connection(self, db_created=False):
        return pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                               db=self.db_name if db_created else None,
                               charset=self.charset, cursorclass=DictCursor, autocommit=True)

    def connect(self):
        connection = self.get_connection()
        print(1)
        connection.query(f'DROP DATABASE IF EXISTS {self.db_name}')
        connection.query(f'CREATE DATABASE {self.db_name}')
        connection.close()
        print(2)
        return self.get_connection(db_created=True)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == '__main__':
    connection = MysqlConnection('root', 'pass', 'MYSQL_DB', host='0.0.0.0', port=3306)
    query = """
        CREATE TABLE `test_users` (
        `id` int NOT NULL AUTO_INCREMENT,
        `username` varchar(16) DEFAULT NULL,
        `password` varchar(255) NOT NULL,
        `email` varchar(64) NOT NULL,
        `access` smallint DEFAULT NULL,
        `active` smallint DEFAULT NULL,
        `start_active_time` datetime DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `email` (`email`),
        UNIQUE KEY `ix_test_users_username` (`username`)
    )
    """
    print(3)
    connection.execute_query(query)

