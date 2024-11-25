"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the EmpowerU class which represents the main window
"""

# Third party imports
import tkinter as tk

# Local application imports
from interfaces.empoweru_gui_homepage import HomePage

class EmpowerU(tk.Tk):

    def __init__(self, title, width, height,test=False):
        """
        Constructor for the EmpowerU class.

        Parameter(s):
        - title: str
        - width: int, width of window in pixels
        - height: int, height of window in pixels
        """
        super().__init__()
        super().title(title)
        super().geometry(f"{width}x{height}")

        self.homepage = HomePage(master=self)
        if not test: # if we are not testing, insert the logo
            self.homepage.set_image_path("./images/logo.png")
        self.show_homepage()

    def show_homepage(self):
        """
        Displays the home page to make it visible in the main window.
        """
        self.homepage.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def hide_homepage(self):
        """
        Hides the home page to make it invisible in the main window.
        """
        self.homepage.place_forget()



if __name__ == "__main__":
    # DO NOT MODIFY
    pass

