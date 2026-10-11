import argparse
import json
from datetime import datetime


def menu(filename):
    while True:
        option = input("""
1- List task
2- Add task
3- Complete task
4- Filter task
5- Sort task
6- Delete task
7- Exit
Choose option: 
""")

        if option == "1":
            list_tasks(filename)
        elif option == "2":
            add_task(filename)
        elif option == "3":
            complete_task(filename)
        elif option == "4":
            print("Filter options:")
            print("1- Show Completed tasks")
            print("2- Show Pending tasks")
            print("3- Show high priority tasks")

            sub_option = input("Choose option (1, 2 or 3): ")
            if sub_option == "1":
                filter_tasks(filename, status=True)
            elif sub_option == "2":
                filter_tasks(filename, status=False)
            elif sub_option == "3":
                filter_tasks(filename, priority="high")
        elif option == "5":
            field = input("Sort by (due_date or priority): ").strip().lower()
            while field not in ["due_date", "priority"]:
                print("You must enter 'due_date' or 'priority'.")
                field = input("Sort by (due_date or priority): ").strip().lower()
            sort_task(filename, by=field)
        elif option == "6":
            delete_task(filename)
        elif option == "7":
            break


def write_file(json_file, tasks):
    with open(json_file, "w") as f:
        json.dump(tasks, f, indent=4)

def load_json(json_file):
    try:
        with open (json_file, "r") as f:
            tasks = json.load(f)
        return tasks
    
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Invalid JSON")
        exit()

    
def create_task(tasks, task, json_file):
    tasks.append(task)
    write_file(json_file, tasks)


def validate_task(task):
    try:
        if "id" in task and "title" in task and "completed" in task and "priority" in task and "due_date" in task:
            if isinstance(task["id"], int) and task["id"] > 0 and task["title"] and isinstance(task["completed"], bool) and task["priority"] in ["low", "medium", "high"] and datetime.strptime(task["due_date"], "%Y-%m-%d"):
                return task
        else:
            return None
    except Exception:
        return None


def add_task(json_file, title=None, priority=None, due_date=None):
    tasks = load_json(json_file)
    try:
        if len(tasks) == 0:
            new_id = 1
        else:
            new_id = max([task["id"] for task in tasks]) + 1

        if due_date:
            while True:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                    break

                except ValueError:
                    print("Invalid date format! Please use YYYY-MM-DD.")
                    return

        if priority:
            if priority not in ["low", "medium", "high"]:
                print("You must enter one of these three (low, medium, high)")
                return 



        if not title:    
            while True:
                title = input("Enter task: ")
                if not title:
                    print("You have to enter a title.")
                else:
                    break
        if not priority:
            while True:
                priority = input("Enter priority (high, medium, low): ").strip().lower()
                if priority not in ["low", "medium", "high"]:
                    print("You must enter one of these three (low, medium, high)")
                else:
                    break
                    
        if not due_date:
            while True:
                try:
                    due_date = input("Enter due date (YYYY-MM-DD): ")
                    datetime.strptime(due_date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format! Please use YYYY-MM-DD.")

            

        while priority not in ["high", "medium", "low"]:
            print("Priority must be High, Medium or low.")
            priority = input("Enter priority (high, medium, low): ").strip().lower()
        while title == "":
            title = input("Enter task: ")
        new_task = {"id": new_id, "title": title, "completed": False, "priority": priority, "due_date": due_date}
        validate = validate_task(new_task)
        if not validate:
            print("Invalid task")
        else:
            create_task(tasks, new_task, json_file)

    except Exception as e:
        print(f"Error: {e}")
    

def complete_task(json_file, complete_id=None):
    try:
        if not complete_id:
            complete_id = int(input("Enter the ID of the completed task: "))
        tasks = load_json(json_file)
        for task in tasks:
            if task["id"] == complete_id:
                if task["completed"] != True:
                    task["completed"] = True
                    write_file(json_file, tasks)
                    print(f"{task['title']} completed!")
                    return
                else:
                    print("This task is already completed.")
                    return
            
        print("ID not found.")
    except ValueError:
        print("You entered a non numerical value!")


def filter_tasks(json_file, status=None, priority=None):
    tasks = load_json(json_file)
    try:
        filtered = []

        if status == "completed":
            status = True
        elif status == "pending":
            status = False

        for task in tasks:
            if status is not None and task.get("completed") != status:
                continue
            if priority is not None and task.get("priority") != priority:
                continue

            filtered.append(task)

        if not filtered:
            print("No matching tasks found.")
        else:
            for t in filtered:
                state = "Completed" if t["completed"] else "Pending"
                prior = t.get("priority", "N/A")
                print(f"ID:{t['id']} {t['title']} | {state} | {prior}")

    except Exception as e:
        print(f"Error: {e}")


def sort_task(json_file, by= None):
    tasks = load_json(json_file)

    try:
        if by == "due_date":
            sorted_tasks = sorted(tasks, key=lambda task: task.get(by, "9999-99-99"))
            for task in sorted_tasks:
                print(f"ID: {task['id']}- {task['title']} | {task['due_date']}")

        elif by == "priority":
            priority_tasks = []
            for task in tasks:
                title = task["title"]
                id = task["id"]
                priority = task["priority"]

                if task["priority"] == "low":
                    priority_tasks.append({"title": title, "id": id, "priority": priority, "sort": 3})
                elif task["priority"] == "medium":
                    priority_tasks.append({"title": title, "id": id, "priority": priority, "sort": 2})
                elif task["priority"] == "high":
                    priority_tasks.append({"title": title, "id": id, "priority": priority, "sort": 1})

            sorted_priority = sorted(priority_tasks, key=lambda task: task.get("sort"))

            for task in sorted_priority:
                print(f"ID: {task['id']}- {task['title']} | {task['priority']}")

    except Exception as e:
        print(f"Error: {e}")

def list_tasks(json_file):
    tasks = load_json(json_file) 
    try:
        if len(tasks) == 0:
            print("List empty.")
            return

        else:
            try:
                for task in tasks:
                    print(f"ID: {task['id']}- {task['title']} {'[Completed]' if task['completed'] == True else '[Pending]'} {task['due_date']}")

            except TypeError as e:
                print(f"Error: {e}")
                exit()

    except Exception as e:
        print(f"Error: {e}")



def delete_task(json_file, del_task=None):
    try:
        if not del_task:
            del_task = int(input("Enter the ID of the task you want to delete: "))
        tasks = load_json(json_file) 

        index = -1
        for task in tasks:
            index += 1
            if task["id"] != del_task:
                continue

            else:
                del tasks[index]
                write_file(json_file, tasks)
                print("Task deleted!")
                return
        print("ID doesn't exist!")

    except ValueError:
        print("You entered a non numerical value!")
        

if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Enter file name.")
    sub_parser = parser.add_subparsers(dest="command")

    list_parser = sub_parser.add_parser("list")

    add_parser = sub_parser.add_parser("add")
    add_parser.add_argument("title")
    add_parser.add_argument("priority")
    add_parser.add_argument("due_date")

    complete_parser = sub_parser.add_parser("complete")
    complete_parser.add_argument("id", type=int)

    filter_parser = sub_parser.add_parser("filter")
    filter_parser.add_argument("--status")
    filter_parser.add_argument("--priority")

    sort_parser = sub_parser.add_parser("sort")
    sort_parser.add_argument("--by", required=True, choices = ["due_date", "priority"])

    delete_parser = sub_parser.add_parser("delete")
    delete_parser.add_argument("delete", type=int)

    args = parser.parse_args()

    if args.command == "list":
        list_tasks(args.filename)

    elif args.command == "add":
        add_task(args.filename, args.title, args.priority, args.due_date)

    elif args.command == "complete":
        complete_task(args.filename, args.id)

    elif args.command == "filter":
        filter_tasks(args.filename, args.status, args.priority)

    elif args.command == "sort":
        sort_task(args.filename, args.by)

    elif args.command == "delete":
        delete_task(args.filename, args.delete)

    else:
        menu(args.filename)