"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the functional tests for the Quizzes and Challenges feature.
Scenario: A learner attempts the quiz for the Artificial Intelligence unit. They answer one question correctly, 
leave one blank, and answer one incorrectly, then submit their answers. 
After reviewing their attempt, they attempt the quiz again to score full marks.


"""

import pytest
import tkinter as tk
import os
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage
from interfaces.unit.empoweru_gui_modules import LearningPage
from app.empoweru_app_learner import LearnerUser
from interfaces.unit.empoweru_gui_quizzes import Quiz

def test_scenario_3():
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
    # simulate selecting the 'Artificial Intelligence' button to launch the learning page for this
    unit_page.show_python_frame()
    module_names = ["Overview","Introduction and Applications of AI", "AI Concepts, Terminology and Application Domains","Business and Career Transformation Through AI" ] # to be refactored as argument
    ai_learning_page = LearningPage(root, unit_page, learner, "Artificial Intelligence", "AI", module_names)
    assert ai_learning_page.current_module == "ai0" # initially the user should see the overview of the unit, which has module code 'ai0'
    
    ###### GOOD PRACTICE FOR ACCURATE TESTING: save original quiz attempt data so that we can revert the changes once we're done testing
    original_lines = []
    data_directory = "./data/quizzes"
    filepath_to_save = os.path.join(data_directory, f"empoweru_AI_l01_scores.txt")
    with open(filepath_to_save, 'r') as file:  # Open file in read mode
        original_lines = file.readlines()
    ######
    
    ############################ simulate clicking on the quiz button, attempt 1 ########################
    ai_learning_page.show_test()
    # test quiz data, 3 questions
    quiz = Quiz(root, ai_learning_page, learner, "AI", "Artificial Intelligence Test", 
                ["What is the capital of France?","What is 2 + 2?","What is the largest ocean?"], 
                [["Paris","London","Berlin","Madrid"],["3","4","5","6"],["Atlantic", "Indian","Artic","Pacific"]], 
                [0,1,3])

    # simulate user leaving one answer blank (here we choose the second question), one incorrect (third question here) and one correct
    quiz.chosen_answers = []
    for i in range(len(quiz.answers)):
        if i == 2: # set third question to incorrect value
            if quiz.answers[i] > 0:
                quiz.chosen_answers.append(tk.IntVar(value=quiz.answers[i]-1))
            else:
                quiz.chosen_answers.append(tk.IntVar(value=quiz.answers[i]+1))
        else:
            quiz.chosen_answers.append(tk.IntVar(value = quiz.answers[i]))
    quiz.chosen_answers[1]=tk.IntVar(value=-1) # set second answer to blank (represented by -1)


    # user submits, marks should be 1
    assert quiz.check_answers() == 1
    quiz.store_and_display_results()
    # user reviews their attempts, check that the received feedback for each question matches expectations
    expected_review_feedback = []
    expected_review_feedback.append(f"Correct! The answer is {quiz.options[0][quiz.answers[0]]}") # correct
    expected_review_feedback.append(f"Question not answered. The answer is {quiz.options[1][quiz.answers[1]]}") # second question was left blank
    expected_review_feedback.append(f"Incorrect! The answer is {quiz.options[2][quiz.answers[2]]}") # third question was incorrect
    received_feedback = quiz.show_review()
    for idx in range(len(received_feedback)):
        assert received_feedback[idx]==expected_review_feedback[idx]
    # exit the review
    quiz.return_to_module()
    ##################### attempt 2 (success) ##############################
    ai_learning_page.show_test()
    # test quiz data, 3 questions
    quiz = Quiz(root, ai_learning_page, learner, "AI", "Artificial Intelligence Test", 
                ["What is the capital of France?","What is 2 + 2?","What is the largest ocean?"], 
                [["Paris","London","Berlin","Madrid"],["3","4","5","6"],["Atlantic", "Indian","Artic","Pacific"]], 
                [0,1,3])
    quiz.chosen_answers = []
    for i in range(len(quiz.answers)):
        quiz.chosen_answers.append(tk.IntVar(value = quiz.answers[i]))
    # user submits, marks should be 1
    assert quiz.check_answers() == 3
    quiz.store_and_display_results()
    # user reviews their attempts, check that the received feedback for each question matches expectations
    expected_review_feedback = []
    for i in range(len(quiz.questions)):
        expected_review_feedback.append(f"Correct! The answer is {quiz.options[i][quiz.answers[i]]}") # correct
    received_feedback = quiz.show_review()
    for idx in range(len(received_feedback)):
        assert received_feedback[idx]==expected_review_feedback[idx]

    # DONE TESTING, REVERT CHANGES
    data_directory = "./data/quizzes"
    filepath_to_save = os.path.join(data_directory, f"empoweru_AI_l01_scores.txt")
    with open(filepath_to_save, 'w') as file:  # Open file in read mode
        for line in original_lines:
            file.write(line)
    root.destroy()

