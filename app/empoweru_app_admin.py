"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the AdminUser class which inherits from the User class.
"""

# Standard library imports
import os

# Local application imports
from app.empoweru_app_user import User

class AdminUser(User):
    @staticmethod
    def authenticate(input_username, input_password):
        """
        Method to authenticate an Admin user.

        Parameter(s):
        - input_username: str
        - input_password: str

        Returns:
        - an instance of AdminUser if successful,
          None otherwise
        """
        admin_path = "./data/accounts/empoweru_admins.txt"
        if os.path.exists(admin_path):
            with open(admin_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                age, recept_id, first_name, last_name, email, username, password,courses = line.strip("\n").split(",")
                
                if input_username == username:
                    if input_password == password:
                        return AdminUser(age, recept_id, first_name, last_name, email, input_username, input_password,courses)
                    else:
                        return None # or return, or break
        else:
            print(f"Please check subdirectory and file {admin_path} exists.")
        

    def __init__(self, age, uid, first_name, last_name, email, username, password,courses):
        """
        Constructor method for the AdminUser class
        """
        super().__init__(age, uid, first_name, last_name, email, username, password)
        self.role = "Admin"
        self.courses = courses


if __name__ == "__main__":
    pass

