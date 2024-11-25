"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the TeacherUser class which inherits from the User class. 
"""

# Local application imports
from app.empoweru_app_user import User
import os
class TeacherUser(User):

    def __init__(self, age,uid, first_name, last_name, email, username, password,courses):
        """
        Constructor for the TeacherUser class
        """
        super().__init__(age,uid, first_name, last_name, email, username, password)
        self.role = "Teacher"
        self.courses = courses

    @staticmethod
    def authenticate(input_username, input_password):
        """
        Method to authenticate an Teacher user.

        Parameter(s):
        - input_username: str
        - input_password: str

        Returns:
        - an instance of TeacherUser if successful,
          None otherwise
        """
        admin_path = "./data/accounts/empoweru_teachers.txt"
        if os.path.exists(admin_path):
            user_instance = None
            with open(admin_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                age,teacher_id, first_name, last_name, email ,username, password,courses = line.strip("\n").split(",")
                
                if input_username == username:
                    if input_password == password:
                        user_instance = TeacherUser(age,teacher_id, first_name, last_name, email,input_username, input_password,courses)
                        return user_instance
                    else:
                        return None # or return, or break
        else:
            print(f"Please check subdirectory and file {admin_path} exists.")

    @staticmethod
    def find_teachers_by_course(course_string):
        """Return a list of teacher names for the given course"""
        teachers = []
        teacher_path = "./data/accounts/empoweru_teachers.txt"
        if os.path.exists(teacher_path):
            with open(teacher_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                age,teacher_id, first_name, last_name, email ,username, password,courses = line.strip("\n").split(",")
                course_components = course_string.split(" ")
                course = course_components[0][0].upper() + course_components[1][0].upper() # get abbreviation of course from course string
                # teacher's courses are the abbreviations separated by '&' (e.g. PP&AI means this teacher teaches Python Programming and Artificial Intelligence)
                if course in courses.split("&"): 
                    teachers.append(f"{first_name} {last_name.upper()}")
            return teachers
        else:
            print(f"Please check subdirectory and file {teacher_path} exists.")
        
if __name__ == "__main__":
    pass
