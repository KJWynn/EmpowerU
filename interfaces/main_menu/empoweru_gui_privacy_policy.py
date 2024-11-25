"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the AboutPolicy class.
"""

# Third party imports
import tkinter as tk
import tkinter.scrolledtext as st

class AboutPolicy(tk.Frame):
    """
    A class to create a GUI for displaying the privacy policy.

    Attributes:
    master: The main window of the application.
    parent: The parent frame or widget.
    """
    def __init__(self, master, parent):
        """
        Initializes the AboutPolicy frame.
        
        Parameters:
        master: The main window of the application.
        parent: The parent frame or widget.
        """
        super().__init__(master)
        self.master = master
        self.parent = parent

        # Theme label widget
        self.policy_label = tk.Label(self, text="Privacy Policy")
        self.policy_label.pack(pady=5, anchor='center')

        # Text box for policy details
        # Creating scrolled text area (Read only)
        self.text_area = st.ScrolledText(self, width=100,  height=25, wrap=tk.WORD) 
        self.text_area.pack(pady = 5, padx = 10) 

        lines = self.load_policy("data/policy.txt")
        self.text_area.insert(tk.INSERT, lines)

        # Making the text read only 
        self.text_area.configure(state ='disabled') #self added

        # Accept button
        self.accept_btn = tk.Button(self, text="Accept", command=self.return_to_menu)
        self.accept_btn.pack(pady=10, anchor='center')    


    def load_policy(self, filepath):
        lines = ""
        try:
            with open(file=filepath, mode="r", encoding="utf8") as f:
                lines = f.read()
        except FileNotFoundError:
            print (f"Error: File not found for {filepath}")
        except IOError:
            print (f"Error: An IOError occur for {filepath}")
        finally:
            return lines


    def return_to_menu(self):
        """
        Hides the AboutPolicy frame and returns to the main menu.
        """
        self.place_forget()
