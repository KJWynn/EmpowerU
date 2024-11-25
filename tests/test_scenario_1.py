"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the functional tests for the Registration and Login feature.
Scenario: A user attempts to register an account as a teacher, and logs in with their registered credentials.

"""

import pytest
import os
import tkinter as tk
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.main_menu.empoweru_gui_teacher_menu import TeacherMenu

def test_scenario_1():
    root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
    # simulate registering, expect success
    mock_register_window = tk.Toplevel()
    assert (root.homepage.register_user("Jia Wynn", "Khor", "22", "jkho0044@student.monash.edu", "jkho0044", "1aB(2cD)", "Teacher", mock_register_window))
    # simulate agreeing to privacy policy, and registering into the database
    mock_privacy_policy_window = tk.Toplevel()
    data_directory = "./data/accounts"
    filepath_to_save = os.path.join(data_directory, f"empoweru_teachers.txt")
    # save original file content so that we can revert the changes once we're done testing
    original_lines = []
    with open(filepath_to_save, 'r') as file:  # Open file in read mode
        lines = file.readlines()
    original_unique_usernames = []
    with open(os.path.join("./data/accounts", "empoweru_unique_usernames.txt"),"r") as file2:
        original_unique_usernames = file2.readlines()
    entries = len(lines)
    root.homepage.user_agree("22", "Teacher", mock_register_window, mock_privacy_policy_window, filepath_to_save, entries, "Jia Wynn", "Khor", "jkho0044@student.monash.edu", "jkho0044", "1aB(2cD)")
    # simulate login as teacher
    mock_role_var = tk.StringVar()
    mock_role_var.set("Teacher")
    root.homepage.selected_role = mock_role_var
    mock_username_var = tk.StringVar()
    mock_username_var.set("jkho0044")
    mock_password_var = tk.StringVar()
    mock_password_var.set("1aB(2cD)")
    # login should be successful
    assert root.homepage.login(mock_username_var, mock_password_var)
    # check that the login was for a teacher
    assert isinstance(root.homepage.user_window, TeacherMenu)

    # Testing complete, revert changes to affected files 
    with open(filepath_to_save, 'w') as file:  # Open file in read mode
        for line in lines:
            file.write(line)
    with open(os.path.join("./data/accounts", "empoweru_unique_usernames.txt"),"w") as file2:
        for username in original_unique_usernames:
            file2.write(username)        

