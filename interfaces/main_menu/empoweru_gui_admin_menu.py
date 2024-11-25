"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the the class definition for the AdminMenu class.
"""

# Local application imports
from interfaces.main_menu.empoweru_gui_base_menu import UserMenu
from interfaces.empoweru_gui_button import HoverButton
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage

class AdminMenu(UserMenu):

    def __init__(self, master, admin_user):
        """
        Constructor for the AdminMenu

        Parameter(s):
        - master: master widget of this widget instance
        - admin_user: an instance of the AdminUser class
                             representing the admin that has 
                             successfully logged in
        """
        super().__init__(master=master, user=admin_user)

        self.inbox_btn = HoverButton(self, text="Inbox", width= 20, command=self.show_private_chats)
        self.inbox_btn.pack(padx=10, pady=10)

        self.unit_btn = HoverButton(self, text="Units", width= 20, command=lambda: UnitPage.show_unit_homepage(self))
        self.unit_btn.pack(padx=10,pady=10)

        self.maintenance_btn = HoverButton(self, text="Schedule Maintenance", width= 20, command=self.schedule_maintenance)
        self.maintenance_btn.pack(padx=10,pady=10)

        self.logout_btn = HoverButton(self, text="Log out", width= 20, command=self.logout)
        self.logout_btn.pack(padx=10, pady=10)
    
    def show_private_chats(self):
        """TO BE COMPLETED SUBSEQUENTLY"""
        pass

    def schedule_maintenance(self):
        """TO BE COMPLETED SUBSEQUENTLY"""
        pass

if __name__ == "__main__":
    # DO NOT MODIFY
    pass

