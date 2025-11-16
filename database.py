
import mysql.connector
from mysql.connector import errorcode
from models import Task
import sys

class Database:
    def __init__(self, host, port, user, password, database):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'autocommit': True
        }
        self.database = database
        self.conn = None
        self._connect()

    def _connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
            cursor.close()
            self.conn.database = self.database
            self._ensure_table()
        except mysql.connector.Error as err:
            print('Database connection error:', err)
            sys.exit(1)

    def _ensure_table(self):
        create_table_sql = (
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "title VARCHAR(255) NOT NULL,"
            "description TEXT,"
            "completed TINYINT(1) DEFAULT 0,"
            "created_at DATETIME DEFAULT CURRENT_TIMESTAMP"
            ") ENGINE=InnoDB"
        )
        cursor = self.conn.cursor()
        cursor.execute(create_table_sql)
        cursor.close()

    def add_task(self, title, description):
        cursor = self.conn.cursor()
        sql = "INSERT INTO tasks (title, description) VALUES (%s, %s)"
        cursor.execute(sql, (title, description))
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def get_task(self, task_id):
        cursor = self.conn.cursor()
        sql = "SELECT id, title, description, completed, created_at FROM tasks WHERE id = %s"
        cursor.execute(sql, (task_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Task(*row)
        return None

    def list_tasks(self, show_all=True):
        cursor = self.conn.cursor()
        if show_all:
            sql = "SELECT id, title, description, completed, created_at FROM tasks ORDER BY created_at DESC"
            cursor.execute(sql)
        else:
            sql = "SELECT id, title, description, completed, created_at FROM tasks WHERE completed = 0 ORDER BY created_at DESC"
            cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        return [Task(*r) for r in rows]

    def update_task(self, task_id, title=None, description=None):
        parts = []
        params = []
        if title is not None:
            parts.append('title = %s')
            params.append(title)
        if description is not None:
            parts.append('description = %s')
            params.append(description)
        if not parts:
            return False
        params.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(parts)} WHERE id = %s"
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(params))
        affected = cursor.rowcount
        cursor.close()
        return affected > 0

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        sql = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(sql, (task_id,))
        affected = cursor.rowcount
        cursor.close()
        return affected > 0

    def mark_complete(self, task_id, completed=True):
        cursor = self.conn.cursor()
        sql = "UPDATE tasks SET completed = %s WHERE id = %s"
        cursor.execute(sql, (1 if completed else 0, task_id))
        affected = cursor.rowcount
        cursor.close()
        return affected > 0
