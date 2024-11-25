"""
FIT1056 2024 Semester 2
EmpowerU

This file contains the tests for the Account Creation and Login feature.
"""
# Related third party imports
import pytest
import tkinter as tk

# Local application imports
from interfaces.forum.empoweru_app_post import Post
from interfaces.forum.empoweru_gui_forum import Forum
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.empoweru_gui_homepage import HomePage
from interfaces.main_menu.empoweru_gui_admin_menu import AdminMenu
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from app.empoweru_app_admin import AdminUser
from app.empoweru_app_learner import LearnerUser

def test_submit_post():
    """
    Tests the various inputs that a user can enter when creating a post
    """
    root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
    homepage = HomePage(root)
    user = AdminUser.authenticate("rochelle","r0che11e")
    user_menu = AdminMenu(homepage.master, user)
    forum = Forum(user_menu.master, user_menu,user, [])
    new_post_window = tk.Toplevel()
    # Test 1: Empty post content, invalid
    assert Post.submit_post(new_post_window, "New post", "", 1, "General", forum) == "Post cannot be empty!"
    # Test 2: Empty title, invalid
    assert Post.submit_post(new_post_window, "", "Example content", 1, "General", forum) == "Title cannot be empty!"
    # Test 3: Title too long, invalid
    assert Post.submit_post(new_post_window, "123456789012345678901234567890123456789012345678901", "Example content", 1, "General", forum) == "Title is too long!"
    # Test 4: No topic chosen
    assert Post.submit_post(new_post_window, "New post", "Example content", 1, "<Select a topic>", forum) == "Please choose a topic tag for the post!"
    # Test 5: Success
    forum.topic_var =tk.StringVar()
    forum.topic_var.set("General")  
    assert Post.submit_post(new_post_window, "New post", "Example content", 1, "General", forum) == f"Successfully posted to General!"
    root.destroy()

def test_can_delete_comment():
    """
    Let A,B and C represent the conditions as follows:
    A = Comment is not deleted
    B = User is an admin
    C = User is the owner of the comment
    The statement to be tested is (A and B or C)
    
    Test A B C Outcome
    1    F F F    F
    2    F F T    F
    3    F T F    F
    4    F T T    F
    5    T F F    F
    6    T F T    T
    7    T T F    T
    8    T T T    T

    Candidate tests for
    A: (2,6), (3,7), {4,8}
    B: (5,7)
    C: (5,6)

    Given 3 conditions, the 4 optimal test cases found from MC/DC:
    Tests (2,5,6,7) or (3,5,6,7)
    We choose (2,5,6,7) here
    """
    # Setup
    root = EmpowerU(title="EmpowerU", width=1100, height=750, test=True)
    homepage = HomePage(root)
    admin_user = AdminUser.authenticate("rochelle", "r0che11e")  # setup different users for testing purposes
    learner_user = LearnerUser.authenticate("janel01","j@ned0e")
    user_menu = LearnerMenu(homepage.master, learner_user)
    forum = Forum(user_menu.master, user_menu,learner_user, [])

    # Test 2: FFT - comment is deleted, user is not an admin, user is owner of comment => invalid
    assert not forum.can_delete_comment(True, learner_user, learner_user)
    # Test 5: TFF - comment is not deleted, user is not an admin, user is not owner of comment => invalid
    assert not forum.can_delete_comment(False, learner_user, admin_user)
    # Test 6: TFT - comment is not deleted, user is not an admin, user is owner of comment => valid
    assert forum.can_delete_comment(False, learner_user, learner_user)
    # Test 7: TTF - comment is not deleted, user is admin, user is not owner of comment => valid
    assert forum.can_delete_comment(False, admin_user, learner_user)
    root.destroy()
