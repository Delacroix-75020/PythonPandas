import pymysql.cursors
import pymysql


class Database:
    def __init__(self) -> None:
        # Connect to the database
        self.__connection = pymysql.connect(host='localhost',
                                    user='user',
                                    password='passwd',
                                    database='db',
                                    cursorclass=pymysql.cursors.DictCursor)
    
    def __getitem__(self, key):
        with self.__connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, (key,))
            result = cursor.fetchone()
            print(result)
            
    def __setitem__(self, key, value):
        with self.__connection:
            with self.__connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`key`, `value`) VALUES (%s, %s)"
                cursor.execute(sql, (key, value))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.__connection.commit()

        