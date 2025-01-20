import sqlite3

class TaskManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            due_date TEXT DEFAULT NULL,
            priority INTEGER DEFAULT 0,
            status TEXT DEFAULT 'open'
        );
        ''')
        self.db_connection.commit()

    def get_total_task_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM tasks')
        return self.cursor.fetchone()[0]

    def get_tasks_page(self, page_number=1, tasks_per_page=10):
        offset = (page_number - 1) * tasks_per_page
        self.cursor.execute('''
        SELECT * FROM tasks 
        LIMIT ? OFFSET ?''', (tasks_per_page, offset))
        return self.cursor.fetchall()

    def add_task(self, title, description, due_date, priority):
        self.cursor.execute('''
        INSERT INTO tasks (title, description, due_date, priority, status)
        VALUES (?, ?, ?, ?, 'open')''', (title, description, due_date, priority))
        self.db_connection.commit()

    def mark_task_completed(self, task_id):
        self.cursor.execute('''
        UPDATE tasks SET status = 'completed' WHERE id = ?''', (task_id,))
        self.db_connection.commit()

    def edit_task(self, task_id, new_title, new_description, new_due_date, new_priority):
        self.cursor.execute('''
        UPDATE tasks SET title = ?, description = ?, due_date = ?, priority = ? WHERE id = ?''',
                            (new_title, new_description, new_due_date, new_priority, task_id))
        self.db_connection.commit()

    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.db_connection.commit()

def main():
    
    db_connection = sqlite3.connect('tasks.db')
    
    task_manager = TaskManager(db_connection)
    
    while True:
        print("Меню:")
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Завершить задачу")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Выход")
        
        choice = input("Выберите опцию: ")
        
        if choice == '1':
            show_tasks_with_pagination(task_manager)
        elif choice == '2':
            add_task(task_manager)
        elif choice == '3':
            mark_task_completed(task_manager)
        elif choice == '4':
            edit_task(task_manager)
        elif choice == '5':
            delete_task(task_manager)
        elif choice == '6':
            break
        else:
            print("Неверная опция. Попробуйте снова.")
    
    db_connection.close()

def show_tasks_with_pagination(task_manager):
    total_tasks = task_manager.get_total_task_count()
    tasks_per_page = 10
    total_pages = (total_tasks // tasks_per_page) + (1 if total_tasks % tasks_per_page else 0)
    
    print(f"Всего задач: {total_tasks}. Страниц: {total_pages}.")
    
    page_number = 1
    
    while True:
        tasks = task_manager.get_tasks_page(page_number, tasks_per_page)
        
        if tasks:
            print(f"Задачи на странице {page_number}:")
            for task in tasks:
                print_task(task)
        
        # Пагинация
        print(f"\nСтраница {page_number} из {total_pages}.")
        print("1. Следующая страница")
        print("2. Предыдущая страница")
        print("3. Выйти")
        
        choice = input("Выберите опцию: ")
        
        if choice == '1' and page_number < total_pages:
            page_number += 1
        elif choice == '2' and page_number > 1:
            page_number -= 1
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def print_task(task):
    print(f'ID: {task[0]}, Название: {task[1]}, Описание: {task[2]}, Приоритет: {task[4]}, Статус: {task[5]}')

def add_task(task_manager):
    title = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")
    due_date = input("Введите дату выполнения задачи (YYYY-MM-DD): ")
    priority = input("Введите приоритет задачи: ")
    task_manager.add_task(title, description, due_date, priority)
    print("Задача добавлена.")

def mark_task_completed(task_manager):
    task_id = int(input("Введите ID задачи для завершения: "))
    task_manager.mark_task_completed(task_id)
    print("Задача завершена.")

def edit_task(task_manager):
    task_id = int(input("Введите ID задачи для редактирования: "))
    new_title = input("Введите новое название задачи: ")
    new_description = input("Введите новое описание задачи: ")
    new_due_date = input("Введите новую дату выполнения задачи (YYYY-MM-DD): ")
    new_priority = input("Введите новый приоритет задачи: ")
    task_manager.edit_task(task_id, new_title, new_description, new_due_date, new_priority)
    print("Задача отредактирована.")

def delete_task(task_manager):
    task_id = int(input("Введите ID задачи для удаления: "))
    task_manager.delete_task(task_id)
    print("Задача удалена.")

if __name__ == "__main__":
    main()
