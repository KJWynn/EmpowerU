"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the functional tests for the Feedback and Collaboration feature.
Scenario: A learner visits the forum. They create a post to ask a question. They also attempt to 
privately chat with a teacher from the Artificial Intelligence department to request personalized feedback.


"""

import pytest
import tkinter as tk
import os
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from interfaces.forum.empoweru_gui_forum import Forum, Post
from app.empoweru_app_learner import LearnerUser
from interfaces.unit.empoweru_progress_page import ProgressPage
from interfaces.unit.empoweru_gui_quizzes import Quiz
from util.utils import Utils
def test_scenario_5():
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
    # simulate selecting the Public Forum button from the learner menu
    # simulate selecting option to create post
    forum = Forum(root, root.homepage.user_window, learner, []) # no posts
    Post.create_post(forum)
    # simulate entering details and submitting the post
    new_post_window = tk.Toplevel()
    forum.topic_var.set("General")
    message = Post.submit_post(new_post_window, "How to find contact details of admins", 
                     "Hi, \nI saw a post by an admin mentioning that we can contact them via email. I was wondering where we could find this information?",
                     1, "General", forum)
    assert message == f"Successfully posted to General!"

    # simulate starting a private chat with a supervisor
    forum.private_chat()
    # forum.private_chat_course_var.set("Artificial Intelligence") # simulate the learner choosing the Artificial Intelligence topic
    forum.teachers_combobox.set("Artificial Intelligence")
    forum.teachers_combobox.event_generate("<<ComboboxSelected>>")    # Trigger the event manually
    
    # check that the teachers dropdown is populated correctly with teachers teaching this subject
    for value in forum.teachers_combobox['values']:
        assert value in ["Ros BANDT", "Frederic CHOPIN"] # these are the teachers who teach the AI unit
    
    # simulate choosing a teacher, entering the fields, then submitting
    forum.teacher_var.set("Ros BANDT")
    new_chat_window = tk.Toplevel()
    assert forum.submit_chat(new_chat_window,"Additional Resources", 
                      "Hi! I recently attempted some tutorials for the second module. I was wondering if I could get\
personalised feedback for my work.")

    root.destroy()
