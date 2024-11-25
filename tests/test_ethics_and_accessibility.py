"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the tests for the Give Feedback feature and Policy reading from text file feature.
test_feedback_submission() still fails
"""
# Related third party imports
import pytest
import tkinter as tk
import os
# Local application imports
from app.empoweru_app_user import User
from interfaces.main_menu.empoweru_gui_base_menu import UserMenu
from interfaces.main_menu.empoweru_gui_privacy_policy import AboutPolicy
from interfaces.empoweru_gui_main_window import EmpowerU

def test_load_policy():
    # test on invalid file
    root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
    policy_page = AboutPolicy(root, root)
    assert policy_page.load_policy("data/policy.txtt") == ""

    # Test on valid file. Here we create a new one for testing purposes
    with open("data/test_policy.txt", "w") as file:
        file.write("Testing with policy")
    assert policy_page.load_policy("data/test_policy.txt") == "Testing with policy"
    os.remove("data/test_policy.txt") # finished testing, so remove this file

    root.destroy()


def test_submit_feedback():
    root = EmpowerU(title="EmpowerU", width=1100, height=750)
    user = User(
        age="18",
        uid="012",
        first_name="Test", 
        last_name="User",
        email="test_user@example.com",
        username="T3stUs3r",
        password="test123"
        )  # Instantiate a real User object
    user_menu = UserMenu(root, user)  # Pass the real user object
    
    user_menu.feedback_topic_var = tk.StringVar()

    # Test unsuccessful submission with empty text but topic selected, invalid 
    user_menu.feedback_topic_var.set("Bug report")  # default value
    assert not user_menu.submit_feedback("", tk.Toplevel())
        
    # Test unsuccessful submission with text but empty topic, invalid
    user_menu.feedback_topic_var.set("<Select a topic>")  # default value
    assert not user_menu.submit_feedback("Test feedback", tk.Toplevel())

    # Test successful submission, valid
    user_menu.feedback_topic_var.set("Bug report")  # default value
    assert user_menu.submit_feedback("Test feedback", tk.Toplevel())
    root.destroy()
