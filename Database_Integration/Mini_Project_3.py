import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk


class TaskManager:
    def __init__(self, db="tasks.db"):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT CHECK(priority IN ('low','medium','high')) DEFAULT 'medium',
            due_date TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()
    
    def create(self, title, desc="", priority="medium", due_date=None):
        self.c.execute(
            'INSERT INTO tasks (title,description,priority,due_date) VALUES (?,?,?,?)',
            (title, desc, priority, due_date)
        )
        self.conn.commit()
        return self.c.lastrowid
    
    def read_all(self):
        self.c.execute('SELECT * FROM tasks ORDER BY due_date')
        return self.c.fetchall()
    
    def read_one(self, task_id):
        self.c.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
        return self.c.fetchone()
    
    def update(self, task_id, **kwargs):
        fields = ', '.join([f"{k}=?" for k in kwargs.keys()])
        self.c.execute(
            f'UPDATE tasks SET {fields} WHERE id=?',
            (*kwargs.values(), task_id)
        )
        self.conn.commit()
    
    def delete(self, task_id):
        self.c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        self.conn.commit()
    
    def stats(self):
        self.c.execute('SELECT COUNT(*) FROM tasks')
        total = self.c.fetchone()[0]
        self.c.execute('SELECT COUNT(*) FROM tasks WHERE status="completed"')
        completed = self.c.fetchone()[0]
        pending = total - completed
        rate = round((completed / total * 100), 2) if total > 0 else 0
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'rate': rate
        }
    
    def close(self):
        self.conn.close()


# =========================
# GUI TABLE VIEW (NEW)
# =========================
def show_table_gui():
    tm = TaskManager()
    tasks = tm.read_all()

    root = tk.Tk()
    root.title("Task Manager – Table View")
    root.geometry("950x400")

    columns = ("ID", "Title", "Description", "Priority", "Due Date", "Status", "Created")

    tree = ttk.Treeview(root, columns=columns, show="headings")
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    for task in tasks:
        tree.insert("", tk.END, values=task)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()
    tm.close()


# =========================
# SIMPLE CLI
# =========================
def simple_cli():
    tm = TaskManager()
    
    while True:
        print("\n" + "="*50)
        print("TASK MANAGER")
        print("="*50)
        print("1. Add Task")
        print("2. List All Tasks")
        print("3. View Task Details")
        print("4. Update Task")
        print("5. Complete Task")
        print("6. Delete Task")
        print("7. View Statistics")
        print("0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        try:
            if choice == '1':
                title = input("Title: ")
                desc = input("Description (optional): ")
                priority = input("Priority (low/medium/high) [medium]: ") or "medium"
                due = input("Due date (YYYY-MM-DD, optional): ") or None
                tid = tm.create(title, desc, priority, due)
                print(f"✅ Task #{tid} created!")
            
            elif choice == '2':
                tasks = tm.read_all()
                if not tasks:
                    print("\n📭 No tasks found")
                else:
                    print(f"\n{'ID':<5}{'Title':<25}{'Priority':<10}{'Due Date':<12}{'Status'}")
                    print("-"*65)
                    for t in tasks:
                        print(f"{t[0]:<5}{t[1][:22]:<25}{t[3]:<10}{t[4] or 'N/A':<12}{t[5]}")
            
            elif choice == '3':
                tid = int(input("Task ID: "))
                task = tm.read_one(tid)
                if task:
                    print("\n" + "="*50)
                    print(f"ID: {task[0]}")
                    print(f"Title: {task[1]}")
                    print(f"Description: {task[2] or 'N/A'}")
                    print(f"Priority: {task[3]}")
                    print(f"Due Date: {task[4] or 'N/A'}")
                    print(f"Status: {task[5]}")
                    print(f"Created: {task[6]}")
                    print("="*50)
                else:
                    print("❌ Task not found")
            
            elif choice == '4':
                tid = int(input("Task ID: "))
                updates = {}
                if title := input("New title: "):
                    updates['title'] = title
                if desc := input("New description: "):
                    updates['description'] = desc
                if priority := input("New priority: "):
                    updates['priority'] = priority
                if due := input("New due date: "):
                    updates['due_date'] = due
                if updates:
                    tm.update(tid, **updates)
                    print("✅ Task updated!")
            
            elif choice == '5':
                tid = int(input("Task ID to complete: "))
                tm.update(tid, status='completed')
                print("✅ Task completed!")
            
            elif choice == '6':
                tid = int(input("Task ID to delete: "))
                tm.delete(tid)
                print("✅ Task deleted!")
            
            elif choice == '7':
                s = tm.stats()
                print("\nSTATISTICS")
                print("-"*30)
                print(s)
            
            elif choice == '0':
                tm.close()
                break
            
        except Exception as e:
            print(f"❌ Error: {e}")


# =========================
# QUICK ADD
# =========================
def quick_add():
    tm = TaskManager()
    print("\n🚀 QUICK ADD MODE (type 'done' to exit)")
    while True:
        title = input("Task title: ")
        if title.lower() == "done":
            break
        tm.create(title)
        print("✅ Added!")
    tm.close()


# =========================
# DASHBOARD
# =========================
def dashboard():
    tm = TaskManager()
    while True:
        stats = tm.stats()
        print("\n📊 DASHBOARD")
        print(stats)
        print("1. Complete Task  2. Add Task  0. Exit")
        choice = input("Choice: ")
        if choice == '1':
            tid = int(input("Task ID: "))
            tm.update(tid, status='completed')
        elif choice == '2':
            title = input("Title: ")
            tm.create(title)
        elif choice == '0':
            tm.close()
            break


# =========================
# MAIN MENU
# =========================
if __name__ == "__main__":
    print("\nPERSONAL TASK MANAGER")
    print("1. Simple CLI")
    print("2. Quick Add")
    print("3. Dashboard")
    print("4. GUI Table View (Non-Terminal)")
    print("0. Exit")
    
    mode = input("\nSelect mode: ").strip()
    
    if mode == '1':
        simple_cli()
    elif mode == '2':
        quick_add()
    elif mode == '3':
        dashboard()
    elif mode == '4':
        show_table_gui()
    else:
        print("👋 Goodbye!")
