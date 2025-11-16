from datetime import datetime
from database import Database

class App:
    def __init__(self, db):
        self.db = db

    def run(self):
        while True:
            print('\n1) Add task')
            print('2) List tasks')
            print('3) List pending tasks')
            print('4) Update task')
            print('5) Delete task')
            print('6) Mark task complete')
            print('7) Mark task incomplete')
            print('8) View task')
            print('9) Exit')
            choice = input('Choose an option: ').strip()
            if choice == '1':
                self._add_task()
            elif choice == '2':
                self._list_tasks(show_all=True)
            elif choice == '3':
                self._list_tasks(show_all=False)
            elif choice == '4':
                self._update_task()
            elif choice == '5':
                self._delete_task()
            elif choice == '6':
                self._mark_task(True)
            elif choice == '7':
                self._mark_task(False)
            elif choice == '8':
                self._view_task()
            elif choice == '9':
                print('Goodbye')
                break
            else:
                print('Invalid option')

    def _add_task(self):
        title = input('Title: ').strip()
        if not title:
            print('Title required')
            return
        description = input('Description: ').strip()
        task_id = self.db.add_task(title, description)
        print('Added task id', task_id)

    def _list_tasks(self, show_all=True):
        tasks = self.db.list_tasks(show_all=show_all)
        if not tasks:
            print('No tasks')
            return
        for t in tasks:
            status = '✓' if t.completed else ' '
            created = t.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(t, 'created_at') else str(t.created_at)
            print(f"[{status}] {t.id}: {t.title} (created: {created})")
            if t.description:
                print('    ', t.description)

    def _update_task(self):
        try:
            task_id = int(input('Task id to update: ').strip())
        except:
            print('Invalid id')
            return
        task = self.db.get_task(task_id)
        if not task:
            print('Task not found')
            return
        title = input(f'New title (leave blank to keep "{task.title}"): ').strip()
        description = input('New description (leave blank to keep current): ').strip()
        title_val = title if title else None
        description_val = description if description else None
        if title_val is None and description_val is None:
            print('Nothing to update')
            return
        ok = self.db.update_task(task_id, title=title_val, description=description_val)
        print('Updated' if ok else 'Update failed')

    def _delete_task(self):
        try:
            task_id = int(input('Task id to delete: ').strip())
        except:
            print('Invalid id')
            return
        ok = self.db.delete_task(task_id)
        print('Deleted' if ok else 'Delete failed')

    def _mark_task(self, completed=True):
        try:
            task_id = int(input('Task id: ').strip())
        except:
            print('Invalid id')
            return
        ok = self.db.mark_complete(task_id, completed=completed)
        print('Marked' if ok else 'Operation failed')

    def _view_task(self):
        try:
            task_id = int(input('Task id to view: ').strip())
        except:
            print('Invalid id')
            return
        task = self.db.get_task(task_id)
        if not task:
            print('Task not found')
            return
        status = 'Complete' if task.completed else 'Pending'
        created = task.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(task, 'created_at') else str(task.created_at)
        print('Id:', task.id)
        print('Title:', task.title)
        print('Description:', task.description)
        print('Status:', status)
        print('Created at:', created)