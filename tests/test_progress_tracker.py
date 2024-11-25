"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the tests for the Account Creation and Login feature.
"""
# Related third party imports
import pytest
import tkinter as tk
# Local application imports
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.empoweru_gui_homepage import HomePage
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage
from interfaces.unit.empoweru_gui_modules import LearningPage
from interfaces.main_menu.empoweru_gui_admin_menu import AdminMenu
from app.empoweru_app_admin import AdminUser
from interfaces.unit.empoweru_progress_page import ProgressPage
def test_add_goal():
    """
    Tests the user attempting to add a personal goal
    Maximum of 10 goals allowed.
    Just below boundary: 9  - Valid
    Boundary value: 10      - Invalid
    Just above boundary: 11 - Invalid
    """
    # Setup
    root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
    user = AdminUser.authenticate("rochelle","r0che11e")
    user_menu = AdminMenu(root, user)
    unit_page = UnitPage(user_menu.master, user_menu, user)
    python_learning_page = LearningPage(unit_page.master, unit_page, user, "Python Programming", "PP",["Overview","Introduction to Python", "Variables, statements and expressions","Functions" ])
    new_post_window = tk.Toplevel()
    goal_entry = tk.Entry(new_post_window, width=50)
    goal_entry.insert(tk.END, "Example goal")
    goals = ['Test goal 1','Test goal 2', 'Test goal 3','Test goal 4','Test goal 5',
             'Test goal 6','Test goal 7','Test goal 8','Test goal 9','Test goal 10']
    listbox = tk.Listbox(new_post_window, width=50, height=10)
    filepath = f"./data/PP/goals/a01_test.txt"
    # Test on boundary value, 10 goals, invalid
    assert not python_learning_page.add_goal(goal_entry, goals, listbox, filepath)
    # Test just below boundary value, 9 goals, valid
    goals = ['Test goal 1','Test goal 2', 'Test goal 3','Test goal 4','Test goal 5',
             'Test goal 6','Test goal 7','Test goal 8','Test goal 9']
    assert python_learning_page.add_goal(goal_entry, goals, listbox, filepath)
    # Test just above boundary value, 11 goals, invalid (Should not be possible)
    goals = ['Test goal 1','Test goal 2', 'Test goal 3','Test goal 4','Test goal 5',
             'Test goal 6','Test goal 7','Test goal 8','Test goal 9', 'Test goal 10','Test goal 11']
    assert not python_learning_page.add_goal(goal_entry, goals, listbox, filepath)    
    root.destroy()
    
def test_load_quiz_attempts():
    # Setup
    root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
    user = AdminUser.authenticate("rochelle","r0che11e")
    user_menu = AdminMenu(root, user)
    unit_page = UnitPage(user_menu.master, user_menu, user)
    python_learning_page = LearningPage(unit_page.master, unit_page, user, "Python Programming", "PP",["Overview","Introduction to Python", "Variables, statements and expressions","Functions" ])
    content_frame = tk.Frame(python_learning_page)
    quiz_progres = ProgressPage(content_frame, python_learning_page, user, "PP")
    # test invalid file (means the user did not attempt the quiz for this unit), so no quiz scores
    assert len(quiz_progres.load_quiz_attempts("./data/quizzes/empoweru_PP_a01_scores.txt"))==0
    # test valid file containing 3 attempts 
    assert len(quiz_progres.load_quiz_attempts("./data/quizzes/empoweru_PP_a01_scores_test.txt"))==3
    root.destroy()


    


