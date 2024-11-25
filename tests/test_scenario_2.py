"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the functional tests for the Interactive Tutorials feature.
Scenario: A learner views an interactive tutorial for the Python Programming unit, and attempts to view the video for it. 

"""

import pytest
import os
import tkinter as tk
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage
from interfaces.unit.empoweru_gui_modules import LearningPage
from app.empoweru_app_learner import LearnerUser

def test_scenario_2():
    """
    NOTE: When running this test case, videos will probably be launched in your browser
    """
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
    # simulate selecting the Units button from the learner menu
    unit_page = UnitPage(root, root.homepage.user_window, learner)
    # simulate selecting the 'Python Programming' button to launch the learning page for this
    unit_page.show_python_frame()
    module_names = ["Overview","Introduction to Python", "Variables, statements and expressions","Functions" ]
    python_learning_page = LearningPage(root, unit_page, learner, "Python Programming", "PP", module_names)
    assert python_learning_page.current_module == "pp0" # initially the user should see the overview of the unit, which has module code 'pp0'
    # simulate selecting each module option for Python Programming, and launching each module's associated video
    # Module 1
    python_learning_page.show_module("pp1")
    assert python_learning_page.current_module == "pp1"
    assert python_learning_page.launch_video() # simulate launching the video 
    # Module 2
    python_learning_page.show_module("pp2")
    assert python_learning_page.current_module == "pp2"
    assert python_learning_page.launch_video() # simulate launching the video 
    # Module 3
    python_learning_page.show_module("pp3")
    assert python_learning_page.current_module == "pp3"
    assert python_learning_page.launch_video() # simulate launching the video 
    root.destroy()

         

