"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the functional tests for the Progress Tracker feature.
Scenario: A learner goes through two modules for the Information Security unit and marks them as complete. 
Then, they attempt the quiz for the Information Security unit. They wish to view their progress up to that point.


"""

import pytest
import tkinter as tk
import os
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage
from interfaces.unit.empoweru_gui_modules import LearningPage
from app.empoweru_app_learner import LearnerUser
from interfaces.unit.empoweru_progress_page import ProgressPage
from interfaces.unit.empoweru_gui_quizzes import Quiz
from util.utils import Utils
def test_scenario_4():
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
    # simulate selecting the 'Information Security' button to launch the learning page for this
    unit_page.show_python_frame()
    module_names = ["Overview","Introduction to Information Security", "Network Security","Ethical hacking and Incident Response" ] # to be refactored as argument
    is_learning_page = LearningPage(root, unit_page, learner, "Information Security", "IS", module_names)
    assert is_learning_page.current_module == "is0" # initially the user should see the overview of the unit, which has module code 'is0'
    
    
    ########### GOOD PRACTICE FOR ACCURATE TESTING: save original progress data so that we can revert the changes once we're done testing
    original_progress = []
    data_directory = "./data/IS/completed_modules"
    filepath_to_save = os.path.join(data_directory, f"l01.txt")
    try:
        with open(filepath_to_save, "r") as f:
            original_progress = f.readlines()
    except FileNotFoundError as e:
        # no attempts so no need to save
        print("No need to save")
    original_quiz_data = []
    data_directory = "./data/quizzes"
    filepath_to_save = os.path.join(data_directory, f"empoweru_IS_l01_scores.txt")
    try:
        with open(filepath_to_save, "r") as f:
            original_quiz_data = f.readlines()
    except FileNotFoundError as e:
        # no attempts so no need to save
        print("No need to save")
    ######################################################################################


    # look at the first two modules, and mark them as complete
    is_learning_page.show_module("is1")     # simulate clicking on the first module
    assert is_learning_page.current_module == "is1"
    is_learning_page.commit_progress()     # simulate marking this module as complete
    is_learning_page.show_module("is2")     # simulate clicking on the second module
    assert is_learning_page.current_module == "is2"
    is_learning_page.commit_progress()     # simulate marking this module as complete
    # do the Information Security Test by simulating clicking on the quiz button 
    is_learning_page.show_test()
    # test quiz data, 3 questions
    quiz = Quiz(root, is_learning_page, learner, "IS", "Information Security Test", 
                ["What is the capital of France?","What is 2 + 2?","What is the largest ocean?"], 
                [["Paris","London","Berlin","Madrid"],["3","4","5","6"],["Atlantic", "Indian","Artic","Pacific"]], 
                [0,1,3])
    quiz.chosen_answers = []
    for i in range(len(quiz.answers)):
        quiz.chosen_answers.append(tk.IntVar(value = quiz.answers[i]))
    # user submits, marks should be 1
    assert quiz.check_answers() == 3
    # store current timestamp
    current_timestamp = Utils.get_current_timestamp()
    quiz.store_and_display_results()
    # user reviews their attempts, check that the received feedback for each question matches expectations
    expected_review_feedback = []
    for i in range(len(quiz.questions)):
        expected_review_feedback.append(f"Correct! The answer is {quiz.options[i][quiz.answers[i]]}") # correct
    received_feedback = quiz.show_review()
    for idx in range(len(received_feedback)):
        assert received_feedback[idx]==expected_review_feedback[idx]
    
    ################ CHECK THAT PROGRESS HAS BEEN RECORDED AND SAVED ####################
    # simulate clicking on progress button
    is_learning_page.show_progress()
    progress = ProgressPage(is_learning_page.content_frame, is_learning_page, learner, "IS")
    # check the quiz progress: the latest item should reflect this most recent attempt
    latest_attempt_score = progress.quiz_data[-1][0]
    assert int(latest_attempt_score) == 3 # because in the above we tested with all correct answers
    latest_attempt_timestamp = progress.quiz_data[-1][1]
    assert latest_attempt_timestamp == current_timestamp
    # check the completed modules progress
    filepath = f"./data/IS/completed_modules/l01.txt"
    modules_progress = progress.load_completed_modules(filepath)
    # check that the two modules are completed
    assert 1 in modules_progress
    assert 2 in modules_progress
         
    # DONE TESTING, REVERT CHANGES 
    data_directory = "./data/IS/completed_modules"
    filepath_to_save = os.path.join(data_directory, f"l01.txt")
    with open(filepath_to_save, "w") as f:
        for line in original_progress:
            f.write(line)

    data_directory = "./data/quizzes"
    filepath_to_save = os.path.join(data_directory, f"empoweru_IS_l01_scores.txt")
    with open(filepath_to_save, "w") as f:        
        for line in original_quiz_data:
            f.write(line)
    root.destroy()
