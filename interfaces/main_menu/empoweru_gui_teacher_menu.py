"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the TeacherMenu class.
"""

# Local application imports
from interfaces.empoweru_gui_button import HoverButton
from interfaces.main_menu.empoweru_gui_base_menu import UserMenu
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage

class TeacherMenu(UserMenu):

    def __init__(self, master, teacher_user):
        """
        Constructor for the TeacherMenu

        Parameter(s):
        - inbox_btn: HoverButton to show the private chats with students
        - logout_btn: HoverButton to exit to login page
        """
        super().__init__(master=master, user=teacher_user)

        self.inbox_btn = HoverButton(self, text="Inbox", width= 20, command=self.show_private_chats)
        self.inbox_btn.pack(padx=10, pady=10)

        self.unit_btn = HoverButton(self, text="Units", width= 20, command=lambda: UnitPage.show_unit_homepage(self))
        self.unit_btn.pack(padx=10,pady=10)

        self.logout_btn = HoverButton(self, text="Log out", width= 20, command=self.logout)
        self.logout_btn.pack(padx=10, pady=10)

    def show_private_chats(self):
        """TO BE COMPLETED SUBSEQUENTLY"""
        pass


if __name__ == "__main__":
    pass

