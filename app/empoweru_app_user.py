"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the User class which represents a generic user of EmpowerU
"""

class User:

    def __init__(self, age, uid, first_name, last_name, email, username, password):
        """
        Constructor for the User class.
        """
        self.age = age
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.role = "Not assigned"
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def __str__(self):
        """
        String representation of the user. Useful for checking EmpowerU user instances. 
        For example, checking if the logged in user is also the owner of a post in the Forum
        """
        return f"{self.first_name} {self.last_name} ({self.role})"

if __name__ == "__main__":
    pass
