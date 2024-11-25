"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the LearnerUser class which inherits from the User class. 
"""
# Standard library imports
import os
# Local application imports
from app.empoweru_app_user import User

class LearnerUser(User):
    def __init__(self, age,uid, first_name, last_name, email, username, password):
        """
        Constructor for the LearnerUser class
        """
        super().__init__(age,uid, first_name, last_name, email, username, password)
        self.role = "Learner"

    @staticmethod
    def authenticate(input_username, input_password):
        """
        Method to authenticate a Learner user.

        Parameter(s):
        - input_username: str
        - input_password: str

        Returns:
        - an instance of LearnerUser if successful,
          None otherwise
        """
        admin_path = "./data/accounts/empoweru_learners.txt"
        if os.path.exists(admin_path):
            with open(admin_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                age,learner_id, first_name, last_name, email, username, password= line.strip("\n").split(",")
                
                if input_username == username:
                    if input_password == password:
                        return LearnerUser(age,learner_id, first_name, last_name, email, username, password)
                    else:
                        return None # or return, or break
        else:
            print(f"Please check subdirectory and file {admin_path} exists.")       
if __name__ == "__main__":
    pass
