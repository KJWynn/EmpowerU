"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the LearnerMenu class.
"""

# Local application imports
from interfaces.empoweru_gui_button import HoverButton
from interfaces.main_menu.empoweru_gui_base_menu import UserMenu
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage

class LearnerMenu(UserMenu):

    def __init__(self, master, learner_user):
        """
        Constructor for the LearnerMenu

        Parameter(s):
        - unit_btn: HoverButton to access the 3 subjects
        - logout_btn: HoverButton to exit to login page
        """
        super().__init__(master=master, user=learner_user)
        self.unit_btn = HoverButton(self, text="Units", width= 20, command=lambda: UnitPage.show_unit_homepage(self))
        self.unit_btn.pack(padx=10,pady=10)

        self.logout_btn = HoverButton(self, text="Log out", width= 20, command=self.logout)
        self.logout_btn.pack(padx=10, pady=10)


if __name__ == "__main__":
    # DO NOT MODIFY
    pass

