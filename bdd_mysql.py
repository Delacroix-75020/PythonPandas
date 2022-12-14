import pymysql.cursors
import pymysql
import json


class Database:
    def __init__(self) -> None:
        with open("conf.json") as openfile:
            conf = json.load(openfile)
        # Connect to the database
        self.__connection = pymysql.connect(host=conf["connect"],
                                            user=conf["user"],
                                            password=conf["password"],
                                            database=conf["database"],
                                            cursorclass=pymysql.cursors.DictCursor)

    def __getitem__(self):
        with self.__connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM airlines"
            cursor.execute(sql)
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


db = Database()
db.__getitem__()
