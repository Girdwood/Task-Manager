# Import modules, i don't think getpass was necessary for this project but it was nice to use it
import datetime
import getpass

# Function to read user credentials from 'user.txt' file


def user_data():
    user_credentials = {}

    # Read user data from 'user.txt'
    with open('user.txt', 'r') as file:
        for line in file:
            try:
                # Split each line into username and password
                username, password = line.strip().split(', ')
                user_credentials[username] = password
            except FileNotFoundError:
                print("user.txt was not found")

    return user_credentials


# Function for user login
def login():
    # Retrieve user credentials
    user_credentials = user_data()

    while True:
        # Prompt for username and password
        username = input("Please enter your username: ").lower()
        password = getpass.getpass("Please enter your password: ")

        # Check if entered credentials are valid
        if username in user_credentials and user_credentials[username] == password:
            print(f"Welcome {username}, Login successful!")
            return username
        else:
            print("Invalid username or password. Please try again.")


# Main menu function
def main_menu(logged_in_user):
    while True:
        # Display main menu options
        print("Menu:")
        print("1. Register a new user (enter 'r')")
        print("2. Add a new task (enter 'a')")
        print("3. View all tasks (enter 'va')")
        print("4. View my tasks (enter 'vm')")
        print("5. View statistics (enter 'stat')")
        print("6. Exit (enter 'exit')")

        # Get user choice
        choice = input("Enter your choice: ").lower()

        # Perform actions based on user's choice
        if choice == 'r':
            register_user(logged_in_user)
        elif choice == 'a':
            add_task()
        elif choice == 'va':
            view_all_tasks()
        elif choice == 'vm':
            view_user_tasks(logged_in_user)
        elif choice == 'stat' and logged_in_user == 'admin':
            view_statistics()
        elif choice == 'stat' and logged_in_user != 'admin':
            print("Only an admin can view statistics")
        elif choice == 'exit':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


# Function to register a new user
def register_user(logged_in_user):
    # Check if the logged-in user is an admin
    if logged_in_user != 'admin':
        print("Only an admin is allowed to register new users")
        return

    while True:
        try:
            # Prompt for new user credentials
            new_username = input("Please enter a new username: ").lower()
            new_password = getpass.getpass("Please enter a new password: ")
            confirm_new_password = getpass.getpass(
                "Please confirm the new password: ")

            # Check if password confirmation matches
            if new_password == confirm_new_password:
                # Write new user to 'user.txt' file
                with open('user.txt', 'a') as file:
                    file.write('\n')
                    file.write(f"{new_username}, {new_password}")
                print("New user added successfully!")
                break
            else:
                print("Password confirmation failed. Please try again.")
        except FileNotFoundError:
            print("Error: 'user.txt' not found.")
            break


# Function to add a new task
def add_task():
    # Prompt for task details
    user_assigned_to = input(
        "Enter the username of who this is assigned to: ").lower()
    task_title = input("Enter the title of the task: ")
    task_desc = input("Enter the task description: ")

    # Prompt for task due date
    while True:
        task_due = input(
            "Enter the due date of the task (format: DD-MM-YYYY): ")
        try:
            datetime.datetime.strptime(task_due, "%d-%m-%Y")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in the correct format.")

    # Get current date
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    # Prompt for task completion status
    while True:
        status = input("Is the task completed? (Yes or No): ").lower()
        if status in ["yes", "no"]:
            break
        else:
            print("Invalid input")

    # Write task to 'tasks.txt' file
    with open('tasks.txt', 'a') as file:
        file.write('\n')
        file.write(f"{user_assigned_to}, {task_title}, {task_desc}, "
                   f"{current_date}, {task_due}, {status}")

        print("Task added successfully!")


# Function to view all tasks
def view_all_tasks():
    with open('tasks.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            user_assigned_to = parts[0]
            task_title = parts[1]
            task_desc = ', '.join(parts[2:-3])
            current_date = parts[-3]
            task_due = parts[-2]
            status = parts[-1]

            # Display task details
            print("="*80)
            print(f"Task: {task_title}")
            print(f"Assigned to: {user_assigned_to}")
            print(f"Date assigned: {current_date}")
            print(f"Due date: {task_due}")
            print(f"Task Complete: {status}")
            print(f"Task Description: \n{task_desc}\n")


# Function to view tasks assigned to the logged-in user
def view_user_tasks(logged_in_user):
    tasks_found = False
    with open('tasks.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            user_assigned_to = parts[0]
            task_title = parts[1]
            task_desc = ', '.join(parts[2:-3])
            current_date = parts[-3]
            task_due = parts[-2]
            status = parts[-1]

            # Check if task is assigned to the logged-in user
            if logged_in_user == user_assigned_to:
                tasks_found = True
                print("="*80)
                print(f"Task: {task_title}")
                print(f"Assigned to: {user_assigned_to}")
                print(f"Date assigned: {current_date}")
                print(f"Due date: {task_due}")
                print(f"Task Complete: {status}")
                print(f"Task Description: \n{task_desc}\n")

    # Display a message if no tasks are found for the current user
    if not tasks_found:
        print("No tasks assigned for the current user")


# Function to view statistics (total number of users and tasks)
def view_statistics():
    total_users = count_users()
    total_tasks = count_tasks()

    print("="*80)
    print(f"Total number of users: {total_users}")
    print(f"Total number of tasks: {total_tasks}")
    print("="*80)


# Function to count the total number of users
def count_users():
    try:
        with open('user.txt', 'r') as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        return 0


# Function to count the total number of tasks
def count_tasks():
    try:
        with open('tasks.txt', 'r') as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        return 0


# Main entry point of the program
if __name__ == "__main__":
    # Perform user login and start the main menu
    logged_in_user = login()
    main_menu(logged_in_user)
