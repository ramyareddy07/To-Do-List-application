import getpass
from database import Database
from app import App

if __name__ == '__main__':
    host = input('Host [localhost]: ').strip() or 'localhost'
    port_input = input('Port [3306]: ').strip() or '3306'
    try:
        port = int(port_input)
    except:
        port = 3306
    user = input('User [root]: ').strip() or 'root'
    password = getpass.getpass('Password: ')
    database = input('Database name [todo_app]: ').strip() or 'todo_app'
    db = Database(host, port, user, password, database)
    app = App(db)
    app.run()