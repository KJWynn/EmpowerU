"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the unit tests for the Challenges and Quizzes feature
"""

# Third party imports
import tkinter as tk

# Local application imports
from interfaces.unit.empoweru_gui_quizzes import Quiz
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage
from interfaces.unit.empoweru_gui_modules import LearningPage
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from app.empoweru_app_learner import LearnerUser

# Create setup for tests
root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
user = LearnerUser.authenticate("janel01","j@ned0e")
user_menu = LearnerMenu(root, user)
unit_page = UnitPage(root, user_menu, user)
learning_page = LearningPage(root, unit_page, user, "Python Programming", "PP", ["Overview","Introduction to Python", "Variables, statements and expressions","Functions" ])


# Create a sample quiz that has 4 questions for testing purposes
quiz = Quiz(
    root, learning_page, user, type="PP", quiz_name="Sample_Test", questions=["Question 1", "Question 2", "Question 3", "Question 4", "Question 5"],
    options=[["Option 1", "Option 2", "Option 3", "Option 4"], ["Option 1", "Option 2", "Option 3", "Option 4"], 
    ["Option 1", "Option 2", "Option 3", "Option 4"], ["Option 1", "Option 2", "Option 3", "Option 4"],
    ["Option 1", "Option 2", "Option 3", "Option 4"]],
    answers=[0,1,2,3,3])
            

def test_check_answers():
    """
    This test checks if correct results are displayed according to the sample test above
    """
    quiz.answers = [0,1,2,3,3] # Resets answer list to bypass random arrangement for testing purposes

    # Tests a mix of blank and correct answers
    quiz.chosen_answers[0].set(0)
    quiz.chosen_answers[1].set(1)
    quiz.chosen_answers[2].set(-1)
    quiz.chosen_answers[3].set(3)
    quiz.chosen_answers[4].set(-1)

    quiz.check_answers()

    assert quiz.blanks == 2
    assert quiz.score == 3
    
    # Tests a mix of blank, incorrect and correct answers
    quiz.chosen_answers[0].set(-1)
    quiz.chosen_answers[1].set(1)
    quiz.chosen_answers[2].set(3)
    quiz.chosen_answers[3].set(-1)
    quiz.chosen_answers[4].set(0)
    quiz.check_answers()

    assert quiz.blanks == 2
    assert quiz.score == 1

    # Tests a mix of correct and incorrect answers
    quiz.chosen_answers[0].set(0)
    quiz.chosen_answers[1].set(1)
    quiz.chosen_answers[2].set(3)
    quiz.chosen_answers[3].set(2)
    quiz.chosen_answers[4].set(2)
    quiz.check_answers()

    assert quiz.blanks == 0
    assert quiz.score == 2

    # Tests a mixture of blank and incorrect answers
    quiz.chosen_answers[0].set(-1)
    quiz.chosen_answers[1].set(2)
    quiz.chosen_answers[2].set(-1)
    quiz.chosen_answers[3].set(2)
    quiz.chosen_answers[4].set(0)
    quiz.check_answers()

    assert quiz.blanks == 2
    assert quiz.score == 0


def test_show_current_question():
    """
    This test checks if the "next" and the "back" buttons are displayed according to the boundaries.
    
    With a total of 5 questions:

    Equivalence classes for Next button: idx >= 0, idx <= 3 (questions 1 to 4)
    Equivalence classes for Back button: idx >= 1, idx <= 4 (questions 2 to 5)

    Test Cases: -1, 0, 1, 3, 4, 5

    As -1 and 5 are invalid indexes that will return index error, these test cases are excluded
    """

    # Tests the off-point upper boundary of the next button
    quiz.idx = 4
    quiz.show_current_question()

    next_btn_list = [child for child in quiz.question_frame.winfo_children() if child.cget("text") == "Next"]
    assert len(next_btn_list) == 0  # Absence of button widget in list shows that next button is not displayed


    # Tests the off-point lower boundary of the back button
    quiz.idx = 0
    quiz.show_current_question()

    back_button_list = [child for child in quiz.question_frame.winfo_children() if child.cget("text") == "Back"]
    assert len(back_button_list) == 0 # Absence of button widget in list shows that back button is not displayed

    # Tests the on-point upper boundary of the next button
    quiz.idx = 3
    quiz.show_current_question()

    next_btn_list = [child for child in quiz.question_frame.winfo_children() if child.cget("text") == "Next"]
    assert len(next_btn_list) == 1  # Presence of button widget in list shows that next button is displayed


    # Tests the on-point lower boundart of the back button
    quiz.idx = 1
    quiz.show_current_question()

    back_button_list = [child for child in quiz.question_frame.winfo_children() if child.cget("text") == "Back"]
    assert len(back_button_list) == 1 # Presence of button widget in list shows that back button is displayed






