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

def test_register_user():
    """
    Tests the various inputs that a user can enter when registering. 
    """
    root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
    homepage = HomePage(root)
    root.homepage = homepage
    register_window = tk.Toplevel(homepage)
    assert not (homepage.register_user("", "Doe", "45", "abc@gmail.com", "abc123", "aB(123**", "Admin", register_window)) # firstname empty
    assert not (homepage.register_user("Jane", "", "45", "abc@gmail.com", "abc123", "aB(123**", "Admin", register_window)) # lastname empty
    assert not (homepage.register_user("Jane", "Doe", "", "abc@gmail.com", "abc123", "aB(123**", "Admin", register_window)) # age empty
    assert not (homepage.register_user("Jane", "Doe", "45", "abc@gmail.com", "abc123", "aB(123**", "", register_window)) # role empty
    assert not (homepage.register_user("Jane", "Doe", "45", "", "abc123", "aB(123**", "Admin", register_window)) # email empty
    assert not (homepage.register_user("Jane", "Doe", "45", "abc@gmail.com", "", "aB(123**", "Admin", register_window)) # username empty
    assert not (homepage.register_user("Jane", "Doe", "45", "abc@gmail.com", "abc123", "", "Admin", register_window)) # password empty
    assert not (homepage.register_user("Jane", "Doe", "45", "a02@gmail.com", "abc123", "aB(123**", "Admin", register_window)) # email already taken
    assert not (homepage.register_user("Jane", "Doe", "45", "abc@gmail.com", "rochelle", "aB(123**", "Admin", register_window)) # username already taken
    assert not (homepage.register_user("Jane", "Doe", "45", "abc@gmail.com", "abc123", "aB(1*", "Admin", register_window)) # password not strong
    assert (homepage.register_user("Jane", "Doe", "45", "abc@gmail.com", "abc123", "aB(123**", "Admin", register_window)) # success
    root.destroy()

def test_check_strong_password():
    """
    Uses boundary value analysis and equivalence classes to check different password lengths.
    8 <= Valid password length <= 20

    BVA:
    Lower bound value = 8
    Upper bound value = 20

    Equivalence classes:
    1 <= length <= 7 (Invalid)
    8 <= length <= 20 (Valid)
    length >= 21 (Invalid) 
    """
    root = EmpowerU(title="EmpowerU", width=1100, height=750)
    homepage = HomePage(root)
    # just below lower bound, in first equivalence class, invalid
    assert homepage.check_strong_password("aB1234(") == "Password too short (less than 8 characters)" 
    # lower bound, second equivalence class, valid
    assert homepage.check_strong_password("aB1234()") == "" 
    # just above lower bound, second equivalence class, valid
    assert homepage.check_strong_password("aB1234()(") == "" 
    # just below upper bound, second equivalence class, valid
    assert homepage.check_strong_password("1234567890123456aB(") == ""
    # upper bound, second equivalence class, valid
    assert homepage.check_strong_password("1234567890123456aB()") == ""
    # just above upper bound, third equivalence class, invalid
    assert homepage.check_strong_password("1234567890123456aB()(") == "Password too long (max 20 characters)"
    root.destroy()


