import sqlite3


class DB:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO `users` (`user`) VALUES(?)', (user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute('SELECT `user` FROM `users`').fetchall()

    def remove_user(self, user_id):
        with self.connection:
            return self.cursor.execute(f'DELETE FROM `users` WHERE `user`= {user_id}')

    def close(self):
        self.connection.close()

