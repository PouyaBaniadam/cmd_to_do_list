import csv
from datetime import datetime
from uuid import uuid4
from tabulate import tabulate
from colorama import Fore, Style, init

init()

indent = "-" * 200


class Task:
    #TODO: Fix the completes_status problem always being False!
    task_list = []

    def see_all(self):
        print(Fore.YELLOW + indent + Style.RESET_ALL)
        print(Fore.CYAN + "List of tasks:" + Style.RESET_ALL)

        # Prepare task data for tabular display
        task_data = []
        for data in self.task_list:
            print('KHR1')
            print(data.get("completes_status"))

            task_data.append([
                data.get("title"),
                data.get("completes_status"),
                data.get("due_date"),
                data.get("priority"),
                data.get("uuid")
            ])


        # Use tabulate to format and print the task table
        print(Fore.MAGENTA + tabulate(task_data, headers=["Title", "Completed", "Due Date", "Priority", "UUID"], tablefmt="grid") + Style.RESET_ALL)
        print(Fore.YELLOW + indent + Style.RESET_ALL)

    def add(self, title: str, due_date: datetime, priority: int = 1, completes_status=False):
        new_uuid = str(uuid4())
        with open("tasks.csv", mode="a", newline="") as csvfile:
            csvfile.write(f"{title}, {completes_status}, {due_date}, {priority}, {new_uuid}\n")

        self.task_list.append({
            "title": title,
            "completes_status": completes_status,
            "due_date": due_date,
            "priority": priority,
            "uuid": new_uuid,
        })

        print(Fore.GREEN + indent + Style.RESET_ALL)
        print(Fore.GREEN + "Task added successfully." + Style.RESET_ALL)
        print(Fore.GREEN + indent + Style.RESET_ALL)

    def remove(self, uuid: str):
        uuid = f" {uuid}"

        found_flag = False
        updated_task_list = []

        # Check if task exists in task_list and remove it
        for data in self.task_list:
            if data["uuid"] == uuid:
                self.task_list.remove(data)
                print(Fore.RED + indent + Style.RESET_ALL)
                print(Fore.RED + "Task removed successfully." + Style.RESET_ALL)
                print(Fore.RED + indent + Style.RESET_ALL)
                found_flag = True
                break
            else:
                updated_task_list.append(data)

        # If task wasn't found, notify the user
        if not found_flag:
            print(Fore.RED + indent + Style.RESET_ALL)
            print(Fore.RED + "Task not found!" + Style.RESET_ALL)
            print(Fore.RED + indent + Style.RESET_ALL)
            return

        # Update the CSV file by rewriting it with the remaining tasks
        with open("tasks.csv", mode="w", newline="") as csvfile:
            csvfile.write("title, completes_status, due_date, priority, uuid\n")
            for task in self.task_list:
                csvfile.write(f"{task['title']}, {task['completes_status']}, {task['due_date']}, {task['priority']}, {task['uuid']}\n")

    def update(self, uuid: str):
        uuid = f" {uuid}"
        found_flag = False

        # Find the task by UUID
        for data in self.task_list:
            if data["uuid"] == uuid:
                found_flag = True
                print(Fore.YELLOW + indent + Style.RESET_ALL)
                print(Fore.CYAN + "Updating task:" + Style.RESET_ALL)
                print(Fore.MAGENTA + f"Current Title: {data['title']}, Due Date: {data['due_date']}, Completed Status: {data['completes_status']}" + Style.RESET_ALL)

                # Prompt for new values, leave unchanged if empty
                new_title = input("Enter new title (leave blank to keep current): ")
                new_due_date = input("Enter new due date (YYYY-MM-DD, leave blank to keep current): ")
                new_status = input("Enter new status (True or False, leave blank to keep current): ")

                # Update title
                if new_title.strip():
                    data['title'] = new_title

                # Update due date
                if new_due_date.strip():
                    try:
                        data['due_date'] = datetime.strptime(new_due_date, "%Y-%m-%d")
                    except ValueError:
                        print(Fore.RED + "Invalid date format. Keeping the current due date." + Style.RESET_ALL)

                # Update completion status
                if new_status.strip().lower() == 'true':
                    data['completes_status'] = True
                elif new_status.strip().lower() == 'false':
                    data['completes_status'] = False

                print(Fore.GREEN + "Task updated successfully!" + Style.RESET_ALL)
                print(Fore.YELLOW + indent + Style.RESET_ALL)
                break

        if not found_flag:
            print(Fore.RED + "Task not found!" + Style.RESET_ALL)
            return

        with open("tasks.csv", mode="w", newline="") as csvfile:
            csvfile.write("title, completes_status, due_date, priority, uuid\n")
            for task in self.task_list:
                csvfile.write(f"{task['title']}, {task['completes_status']}, {task['due_date']}, {task['priority']}, {task['uuid']}\n")


    def read_csv_db(self):
        self.task_list.clear()

        try:
            with open("tasks.csv", mode="r") as csvfile:
                row = csv.reader(csvfile, delimiter=',', quotechar='|')
                next(row)  # Skip the header row

                for task in row:
                    title = task[0]
                    completes_status = task[1].lower() == 'true'  # Convert to boolean
                    due_date = task[2]
                    priority = int(task[3])  # Convert to integer
                    uuid = task[4]

                    self.task_list.append({
                        "title": title,
                        "completes_status": completes_status,
                        "due_date": due_date,
                        "priority": priority,
                        "uuid": uuid,
                    })

        except FileNotFoundError:
            with open("tasks.csv", mode="w", newline="") as csvfile:
                csvfile.write("title, completes_status, due_date, priority, uuid\n")


def main():
    task = Task()
    task.read_csv_db()

    print(Fore.CYAN + "Welcome to my to-do app. Please choose an option. (1, 2, 3, 4, 5)" + Style.RESET_ALL)
    option = input(f"""1) See all tasks
2) Add a task
3) Delete a task (by uuid)
4) Update a task (by uuid)
5) Exit
{Fore.YELLOW}{indent}{Style.RESET_ALL}
""")

    match option:
        case "1":
            task.see_all()

        case "2":
            title = input("What is the title? : ")
            year = input("What is the due date year? : ")
            month = input("What is the due date month? : ")
            day = input("What is the due date day? : ")
            priority = input("What is the priority? : ")

            try:
                due_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                task.add(title=title, due_date=due_date, priority=int(priority))

            except ValueError:
                print(Fore.RED + indent + Style.RESET_ALL)
                print(Fore.RED + "Sorry, that's not a valid date! Please try again." + Style.RESET_ALL)
                print(Fore.RED + indent + Style.RESET_ALL)

        case "3":
            unique_id = input("What is the unique id? : ")
            task.remove(uuid=unique_id)

        case "4":
            unique_id = input("Enter the unique id of the task to update: ")
            task.update(uuid=unique_id)

        case "5":
            print(Fore.GREEN + indent + Style.RESET_ALL)
            print(Fore.GREEN + "Exiting..." + Style.RESET_ALL)
            print(Fore.GREEN + indent + Style.RESET_ALL)
            exit()

        case _:
            print(Fore.RED + indent + Style.RESET_ALL)
            print(Fore.RED + "Invalid option" + Style.RESET_ALL)
            print(Fore.RED + indent + Style.RESET_ALL)


if __name__ == "__main__":
    while True:
        main()
