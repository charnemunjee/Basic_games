# ===== Importing external modules ===========
import datetime
from datetime import datetime
# ==== Define classes ====

class Users:

    def __init__(self, username, password):
        """
            All users are stored in this class
            attributes: username, password
        """
        self.username = username
        self.password = password

class Tasks:

    def __init__(self, responsible_person, task_name, task_description, entry_date,
                 due_date, completed_indicator="No"):
        """
        All tasks are stored in this class
        :param responsible_person: The person responsible for the task
        :param task_name: The name of the task
        :param task_description: Description of the task
        :param entry_date: The date the task was entered into the task manager
        :param due_date: Due date of the task
        :param completed_indicator: Indicator to indicate if the task was completed
        """
        self.responsible_person = responsible_person
        self.task_name = task_name
        self.task_description = task_description
        self.entry_date = entry_date
        self.due_date = due_date
        self.completed_indicator = completed_indicator

task_list = []  # all task objects are stored in this list
user_info = []  # all user objects are stored in this list

def read_user_info():
    """
    This function reads the user info from the file user.txt
    and creates a user object for each combination of
    username and password
    :return: a list of user objects
    """
    try:
        with open('user.txt', 'r+') as user_file:
            users_txt = user_file.readlines()
            for j in range(0, len(users_txt)):
                username_details = users_txt[j].split(',')
                temp_user = Users(username_details[0].strip(), username_details[1].strip())
                user_info.append(temp_user)
            return user_info
    except FileNotFoundError:
        print("user file not found. Please check the path.")


def read_task_info():
    """
    This function reads the task info from the file task.txt
    and creates a task object for each task listed in the file
    :return: a list of task objects
    """
    try:
        with open('tasks.txt', 'r+') as task_file:
            tasks = task_file.readlines()
            format_string = "%d %b %Y"
            for k in range(len(tasks)):
                task = tasks[k].replace('\n', "").split(',')
                date_obj = datetime.strptime(task[3].strip(), format_string)
                temp_task = Tasks(task[0], task[1], task[2], date_obj, task[4], task[5])
                task_list.append(temp_task)
            return task_list
    except FileNotFoundError:
        print("Task file not found. Please check the path.")


def view_completed():
    """
    This function loops through the task_list and prints
    the task information for tasks that were completed
    :return: prints the task information for tasks that
    were completed
    """

    for task in task_list:
        if task.completed_indicator == "Yes":
            print("------------------------------------------------------------------------------")
            print(f'Task:               {task.task_name}')
            print(f'Assigned to:        {task.responsible_person}')
            print(f'Date assigned:      {task.entry_date}')
            print(f'Due Date:           {task.due_date}')
            print(f'Task Complete:      {task.completed_indicator}')
            print(f'Task description:   {task.task_description}')


def print_task_list():
    """
    This function prints the task information for all tasks in the task_list
    :return: information of all tasks in the task_list
    """
    task_number = 1
    for task in task_list:
        print("------------------------------------------------------------------------------")
        print(f'Task Number:        {task_number}')
        print(f'Task:               {task.task_name}')
        print(f'Assigned to:        {task.responsible_person}')
        print(f'Date assigned:      {task.entry_date}')
        print(f'Due Date:           {task.due_date}')
        print(f'Task Complete:      {task.completed_indicator}')
        print(f'Task description:   {task.task_description}')
        print()
        task_number += 1


def delete_task():
    """
    This function prints information for all tasks in the task_list
    then asks the user to select the task to delete
    The selected task is then deleted
    :return: prints the task information for all the remaining tasks
    in the task_list
    """
    print_task_list()

    task_to_delete = int(input("\nEnter the number of the task to delete: "))
    task_list.remove(task_list[task_to_delete-1])
    print("\nTask Deleted!")
    print("Here are the remaining tasks:\n")

    # open the tasks.txt file and write the remaining tasks to the file
    try:
        with open('tasks.txt', 'w') as task_file:
            task_file.seek(0)
            task_file.truncate()
            for task in task_list:
                task_file.write(
                    f'{task.responsible_person}, {task.task_name}, '
                    f'{task.task_description}, {task.due_date}, '
                    f'{task.entry_date}, {task.completed_indicator}\n')
    except FileNotFoundError:
        print("Task file not found. Please check the path.")

    print_task_list()


def view_all():
    """
    This tasks prints all the tasks in the task_list
    """
    print_task_list()


def add_task():
    """
    This code block allows the user to add a new task to task.txt file
            - The user is prompted for the following:
                - the username of the person whom the task is assigned to,
                - the title of the task,
                - the description of the task, and
                - the due date of the task.
            - The current date is entered into the task manager.
            - An task object is created for the task
            - The task information is added to the file task.txt
            - The task completed indicator is set to "No" by default.
    """
    add_more_tasks = True
    # user is prompted to add information about the task
    while add_more_tasks:
        responsible_person = input('Enter the person whom the task is assigned to: ')
        task_name = input('Enter the name of the task: ')
        task_description = input('Enter the description of the task: ')
        task_due = input('Enter the due date of the task: ')
        completed_indicator = "No"
        date_of_entry = datetime.date.today()

        # create a new task object and append to task_list
        new_task = Tasks(responsible_person, task_name, task_description, date_of_entry,
                         task_due, completed_indicator)
        task_list.append(new_task)

        # append the task information to the tasks.txt file
        try:
            with open('tasks.txt', 'a') as task_file:
                task_file.write(
                    f'\n{responsible_person}, {task_name}, {task_description}, {task_due}, '
                    f'{date_of_entry}, {completed_indicator}')
        except FileNotFoundError:
            print("Task file not found. Please check the path.")

        # ask the user if they would like to continue adding tasks
        user_continue = input('Do you want to continue adding more tasks? [y/n]: ').lower()
        if user_continue == "y":
            add_more_tasks = True
        else:
            add_more_tasks = False


def view_mine():
    """This code block allows the user to view all the tasks
    in the task_list for which they are responsible
    The user is prompted for the following:
    - Whether they would like to edit the task of return to the main menu
    - If they would like to edit a task, they are prompted to either:
        1) Mark the task as complete
        2) Edit the responsible person of the task
        3) Edit the due date of the task
     """

    # view all the tasks that the user is responsible for
    for i in range(len(task_list)):
        if username_input == task_list[i].responsible_person:
            print("------------------------------------------------------------------------------")
            print(f'Task number:        {i + 1}')
            print(f'Task:               {task_list[i].task_name}')
            print(f'Assigned to:        {task_list[i].responsible_person}')
            print(f'Date assigned:      {task_list[i].entry_date}')
            print(f'Due Date:           {task_list[i].due_date}')
            print(f'Task Complete:      {task_list[i].completed_indicator}')
            print(f'Task description:   {task_list[i].task_description}')

    # ask the user to enter the task number of the task that
    # they would like to edit or return to the main menu
    task_number = int(input('Enter the task number that you would like to edit '
                            'or press -1 to return to the main menu: '))
    if task_number != -1:
        edit_task = input("Would you like to edit the task? (y/n): ")
        if edit_task == 'y':
            # ask user what they would like to edit
            task_instruct = input("What would you like to do?: \n"
                                  "1 - Mark a task as completed: \n"
                                  "2 - Edit the responsible person: \n"
                                  "3 - Edit the due date: \n")

            if task_instruct == '1':
                # change the completed indicator to yes
                task_list[task_number - 1].completed_indicator = "Yes"
            elif task_instruct == '2':
                # change the name of the responsible person
                new_responsible_person = input("Enter the new responsible person: ")
                task_list[task_number - 1].responsible_person = new_responsible_person
            elif task_instruct == '3':
                # change the due date
                new_due_date= input("Enter the due date (d/mmm/yyyy): ")
                task_list[task_number - 1].due_date = new_due_date
    elif task_number == -1:  # return to the main menu
        show_menu()


def reg_user():
    """
    This code block allows admin to add a new user to the user.txt file
            - You can use the following steps:
                - Request input of a new username
                - Request input of a new password
                - Request input of password confirmation.
                - Check if the new password and confirmed password are the same
                - If they are the same, add them to the user.txt file,
                  otherwise present a relevant message
    """
    user_continue = True
    while user_continue:
        username_found = False

        if username_input == "admin":
            new_user = input('Enter new username: ')
            for users in user_info:
                if users.username == new_user:
                    print('Username already exists.')
                    username_found = True
                    break
            if not username_found:
                new_user_password = input('Enter new password: ')
                new_user_password_confirm = input('Confirm new password: ')
                if new_user_password == new_user_password_confirm:
                    new_user = Users(new_user, new_user_password)
                    user_info.append(new_user) # append the new user to user_info
                    with open('user.txt', 'a') as user_file:
                        user_file.write(f'{new_user.username}, {new_user.password}\n')
                else:
                    print('New password and confirmed password do not match')
            user_continue_input = input('Do you want to continue adding more users? [y/n]: ').lower()
            if user_continue_input == 'y':
                user_continue = True
            else:
                user_continue = False


def generate_task_overview():
    """
    This function generates a summary of all the tasks
    in a text file called 'task_overview.txt'
    :return: a file called 'task_overview.txt' that contains the following:
        1) Total number of tasks
        2) Total number of completed tasks
        3) Total number of uncompleted tasks
        4) Total number of uncompleted, overdue tasks
        5) Percentage of incomplete tasks
        6) Percentage of overdue tasks
    """
    # calculate the number of tasks
    num_tasks = len(task_list)

    # calculate the number of completed tasks
    num_completed = 0
    for i in range(num_tasks):
        if task_list[i].completed_indicator == 'Yes':
            num_completed += 1

    # calculate the number of incomplete tasks
    num_uncompleted = num_tasks - num_completed

    # calculate the number of overdue tasks and
    # the number of overdue, incomplete tasks
    num_overdue = 0
    num_uncompleted_overdue = 0
    for i in range(num_tasks):
        formatted_date = datetime.strptime(task_list[i].due_date.strip(), "%d %b %Y")
        if formatted_date < datetime.today():
            num_overdue += 1
        if (task_list[i].completed_indicator == 'No' and
                formatted_date < datetime.date.today()):
            num_uncompleted_overdue += 1

    # calculate the percentage of incomplete tasks
    # and the number of overdue and incomplete tasks
    incomplete_perc = round(num_uncompleted / num_tasks * 100,2)
    overdue_perc = round(num_uncompleted_overdue / num_tasks * 100, 2)

    # write the calculated numbers to the task_overview.txt file
    try:
        with open('task_overview.txt', 'w') as task_overview_file:
            task_overview_file.write(
                f'---------------------------------------------------------------\n'
                f'Total number of tasks:                    {num_tasks}\n'
                f'Number of completed tasks:                {num_completed}\n'
                f'Number of uncompleted tasks:              {num_uncompleted}\n'
                f'Number of overdue uncompleted tasks:      {num_overdue}\n'
                f'Percentage incomplete:                    {incomplete_perc}%\n'
                f'Percentage overdue:                       {overdue_perc}%\n'
                f'----------------------------------------------------------------\n'
            )
    except FileNotFoundError:
        print('Task overview file not found')

def generate_user_overview():
    """
    This function generates a summary of all tasks per user
    The function calculate the following and writes the info
    to the user_overview:
    1) Total number of tasks per user
    2) Total number of completed tasks per user
    3) Total number of uncompleted tasks per user
    4) Total number of uncompleted, overdue tasks per user
    """
    # counts the number of users and number of tasks
    num_users = len(user_info)
    num_tasks = len(task_list)

    # opens the user_overview.txt file and writes the
    # number of tasks and number of users to the file
    try:
        with open('user_overview.txt', 'w') as user_overview_file:
            user_overview_file.write(f'Total number of tasks:   {num_tasks}\n'
                                     f'Total number of users:   {num_users}\n')
    except FileNotFoundError:
        print('User overview file not found')

    # creates a username list from user_info
    username_list = [user_info[i].username for i in range(num_users)]
    # creates a list of responsible persons per task from task_list
    responsible_person_list = [task_list[i].responsible_person for i in range(num_tasks)]

    # calculates the following:
    # 1) percentage of tasks assigned
    # 2) percentage of tasks completed
    # 3) percentage of incomplete tasks
    # 4) percentage of overdue, incomplete tasks
    # the numbers are written to user_overview.txt file

    for i in range(num_users):
        user_task_num = 0
        complete_task_count = 0
        overdue_incomplete_task_count = 0
        if username_list[i] in responsible_person_list:
            for j in range(num_tasks):
                if task_list[j].responsible_person == username_list[i]:
                    user_task_num += 1
                if task_list[j].completed_indicator == 'Yes':
                    complete_task_count += 1
                else:
                    formatted_date = datetime.strptime(task_list[i].due_date.strip(), "%d %b %Y")
                    if formatted_date < datetime.today():
                        overdue_incomplete_task_count += 1

        if user_task_num == 0:
            perc_tasks_assigned = "0%"
            complete_perc_tasks_assigned = "0%"
            incomplete_perc_tasks_assigned = "0%"
            overdue_incomplete_task_count = "0%"
        else:
            perc_tasks_assigned = round(user_task_num / num_tasks * 100,2)
            complete_perc_tasks_assigned = round(complete_task_count / user_task_num * 100,2)
            incomplete_perc_tasks_assigned = round((user_task_num - complete_task_count) / num_tasks * 100,2)
            overdue_incomplete_task_count = round(overdue_incomplete_task_count / user_task_num * 100,2)

        try:
            with open('user_overview.txt', 'a') as user_overview_file:
                user_overview_file.write(
                    f'-----------------------------------------------------------------\n'
                    f'User:                             {user_info[i].username}\n'
                    f'Perc tasks assigned:              {perc_tasks_assigned}\n'
                    f'Perc completed tasks assigned:    {complete_perc_tasks_assigned}\n'
                    f'Perc incomplete tasks assigned:   {incomplete_perc_tasks_assigned}\n'
                    f'Perc incomplete and overdue:      {overdue_incomplete_task_count}\n'
                )
        except FileNotFoundError:
            print('User overview file not found')

def generate_reports():
    """ This function calls the generate_task_overview
    and generate_user_overview and generates all the reports """
    generate_task_overview()
    generate_user_overview()
    print('\nTask and user summaries have been generated\n')

def display_statistics():
    """ This function displays all the statistics for each user"""

    # calculates and prints the number of users and number of tasks
    num_users = len(user_info)
    num_tasks = len(task_list)
    print(f'\nTotal number of tasks:          {num_tasks}\n'
          f'Total number of users:            {num_users}')

    # creates a responsible_person_list and user_name_list
    username_list = [user_info[i].username
                     for i in range(num_users)]
    responsible_person_list = [task_list[i].responsible_person
                               for i in range(num_tasks)]

    user_task_num = 0
    complete_task_count = 0
    overdue_incomplete_task_count = 0

    # calculates and prints the statistics for each user
    for i in range(num_users):
        if username_list[i] in responsible_person_list:
            for j in range(num_tasks):
                if task_list[j].responsible_person == username_list[i]:
                    user_task_num += 1
                if task_list[j].completed_indicator == 'Yes':
                    complete_task_count += 1
                else:
                    formatted_date = datetime.strptime(
                        task_list[i].due_date.strip(), "%d %b %Y")
                    if formatted_date < datetime.today():
                        overdue_incomplete_task_count += 1

            perc_tasks_assigned = round(
                user_task_num / num_tasks * 100, 2)
            complete_perc_tasks_assigned = round(
                complete_task_count / user_task_num * 100, 2)
            incomplete_perc_tasks_assigned = round(
                (user_task_num - complete_task_count) / num_tasks * 100, 2)
            overdue_incomplete_task_count = round(
                overdue_incomplete_task_count / user_task_num * 100, 2)

            print(
                f'-----------------------------------------------------------------\n'
                f'User:                             {user_info[i].username}\n'
                f'Perc tasks assigned:              {perc_tasks_assigned}\n'
                f'Perc completed tasks assigned:    {complete_perc_tasks_assigned}\n'
                f'Perc incomplete tasks assigned:   {incomplete_perc_tasks_assigned}\n'
                f'Perc incomplete and overdue:      {overdue_incomplete_task_count}\n')


def show_menu():
    """ This function displays the main menu.
    A different manu is displayed if the username is 'admin'
    """
    if username_input == 'admin':
        menu = input(
            '''Select one of the following options:
            r - register a user
            a - add task
            va - view all tasks
            vm - view my tasks
            vc - view completed tasks
            del - delete tasks
            ds - display statistics
            gr - generate reports
            e - exit: ''').lower()

    else:
        menu = input(
            '''Select one of the following options:
            a - add task
            va - view all tasks
            vm - view my tasks
            e - exit: ''').lower()
    return menu

# read the user info and task info and store
# them as objects in the user_list and task_list
read_user_info()
read_task_info()

correct_password = False
correct_username = False

# prompt the user to enter the username and check that it
# is the same as the usernames for any of the user
# objects in the user_info
i = 0
while not correct_username:
    username_input = input('Enter your username: ')
    if username_input == user_info[i].username:
        correct_username = True
    else:
        correct_username = False
        i += 1

# prompt the user to enter the password and check that it
# is the same as the passwords for any of the user
# objects in the user_info
j = 0
while not correct_password:
    password_input = input('Enter your password: ')
    if password_input == user_info[i].password:
        correct_password = True
    else:
        correct_password = False
        j += 1

# show the menu and ask the user to enter
# what they would like to do
while True:
    menu_to_show = show_menu()

    if menu_to_show == 'r':
        reg_user()
    elif menu_to_show == 'a':
        add_task()
    elif menu_to_show == 'va':
        view_all()
    elif menu_to_show == 'vm':
        view_mine()
    elif menu_to_show == 'vc':
        view_completed()
    elif menu_to_show == 'del':
        delete_task()
    elif menu_to_show == 'gr':
        generate_reports()
    elif menu_to_show == 'ds':
        display_statistics()
    elif menu_to_show == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have entered an invalid input. Please try again")