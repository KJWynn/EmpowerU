"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the functional tests for the Ethics and Accessibility feature.
Scenario: A learner wants to view EmpowerU's privacy policy. 
After reading it, they want to provide feedback to the EmpowerU team. 


"""

import pytest
import tkinter as tk
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from interfaces.main_menu.empoweru_gui_privacy_policy import AboutPolicy
from app.empoweru_app_learner import LearnerUser

def test_scenario_6():
    root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
    # simulate login as learner
    mock_role_var = tk.StringVar()
    mock_role_var.set("Learner")
    root.homepage.selected_role = mock_role_var
    mock_username_var = tk.StringVar()
    mock_username_var.set("janel01")
    mock_password_var = tk.StringVar()
    mock_password_var.set("j@ned0e")
    # login should be successful
    learner = LearnerUser("14","l01", "Jane", "Doe", "l01@gmail.com", "janel01", "j@ned0e")
    assert root.homepage.login(mock_username_var, mock_password_var)
    assert isinstance(root.homepage.user_window, LearnerMenu)
    # simulate selecting the Settings button from the learner menu
    root.homepage.user_window.show_settings_page(root.homepage.user_window)
    # simulate selecting the privacy policy button
    settings = tk.Frame(root.homepage.user_window.master)
    policy = root.homepage.user_window.show_policy(settings)
    assert isinstance(policy, AboutPolicy)
    # simulate clicking on 'Accept" button to exit to main menu
    policy.return_to_menu()

    # simulate clicking on "Provide Feedback" button
    feedback_window = root.homepage.user_window.provide_feedback()
    root.homepage.user_window.feedback_topic_var.set("Others")
    assert root.homepage.user_window.submit_feedback(
        "How long does EmpowerU retain my personal data after I deactivate my account, \
and is it possible to have it permanently deleted sooner?",feedback_window)


    root.destroy()
