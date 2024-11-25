"""
FIT1056 2024 Semester 2
Project Deliverable 2

This file contains the function definition to run the Unit selection GUI application for learners.
"""

# Third party imports
import tkinter as tk

# Local application imports
from interfaces.unit.empoweru_gui_modules import LearningPage
from interfaces.empoweru_gui_button import HoverButton

class UnitPage(tk.Frame):
    """
    UnitPage class shows the main page where learners can select from available units to study.
    This page is displayed after the learner select the Units button.
    
    Inherits:
    - tk.Frame: Base class for creating a frame widget in tkinter.
    """
    def __init__(self, master, user_menu, user):
        """
        Constructor for the Student's Unit page

        Parameter(s):
        - master: Master widget of this widget instance.
        - learner_user: An instance of the LearnerUser class representing the learner that has 
                        successfully logged in.
        - learner_menu: Reference to the menu page from which this page is accessed.
        """
        super().__init__(master=master)
        self.master = master
        self.user = user
        self.user_menu = user_menu

        # Label for the page header
        self.label1 = tk.Label(self, text="Select your unit:") 
        self.label1.pack(padx=10, pady=10)

        # Button for Python Programming unit
        self.python_btn = HoverButton(self, width=20,text="Python Programming", command=self.show_python_frame)
        self.python_btn.pack(padx=10, pady=10)

        # Button for Artificial Intelligence unit
        self.ai_btn = HoverButton(self, width=20,text="Artificial Intelligence", command=self.show_ai_frame)
        self.ai_btn.pack(padx=10, pady=10)

        # Button for Information Security unit
        self.is_btn = HoverButton(self, width=20,text="Information Security", command=self.show_is_frame)
        self.is_btn.pack(padx=10, pady=10)

        # Button to return to the user menu
        self.logout_btn = HoverButton(self, width=20,text="Return to Menu", command=self.return_user_menu)
        self.logout_btn.pack(padx=10, pady=10)
    
    @staticmethod
    def show_unit_homepage(parent):
        """
        Static method to show the UnitPage when a learner logs in.

        Parameters:
        - parent: The parent widget from which this method is called.
        """
        unit_page = UnitPage(parent.master, parent, parent.user)
        unit_page.place(relx=.5, rely=.5, anchor=tk.CENTER)
        parent.hide_menu()


    def show_python_frame(self):
        """
        Method to display the LearningPage for Python Programming.
        Shows the modules related to Python Programming and hides the unit page.
        """
        module_names = ["Overview","Introduction to Python", "Variables, statements and expressions","Functions" ] # to be refactored as argument
        search_teachers = LearningPage(self.master, self, self.user, "Python Programming","PP", module_names)
        search_teachers.place(relx=.5, rely=.5, anchor=tk.CENTER)
        self.place_forget()
    
    def show_ai_frame(self):
        """
        Method to display the LearningPage for Artificial Intelligence.
        Shows the modules related to Artificial Intelligence and hides the unit page.
        """
        module_names = ["Overview","Introduction and Applications of AI", "AI Concepts, Terminology and Application Domains","Business and Career Transformation Through AI" ] # to be refactored as argument
        search_teachers = LearningPage(self.master, self, self.user, "Artificial Intelligence", "AI",module_names) 
        search_teachers.place(relx=.5, rely=.5, anchor=tk.CENTER)
        self.place_forget()
    
    def show_is_frame(self):
        """
        Method to display the LearningPage for Information Security.
        Shows the modules related to Information Security and hides the unit page.
        """
        module_names = ["Overview","Introduction to Information Security", "Network Security","Ethical hacking and Incident Response" ] # to be refactored as argument
        search_teachers = LearningPage(self.master, self, self.user,"Information Security", "IS",module_names) 
        search_teachers.place(relx=.5, rely=.5, anchor=tk.CENTER)
        self.place_forget()
        
        

    def return_user_menu(self):
        """
        Method to return to the unit page and hide the module page.
        """
        self.place_forget()
        self.user_menu.place(relx=.5,rely=.5,anchor=tk.CENTER)
