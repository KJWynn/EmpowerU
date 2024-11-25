"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the function definition to run the Unit selection GUI application for learners.
"""

# Third party imports
import tkinter as tk 

# Local application imports
from util.utils import Utils

class ProgressPage(tk.Text):
    def __init__(self, master, learning_page, user,type,**kwargs):
        super().__init__(master)
        self.master = master
        self.learning_page = learning_page
        self.user = user
        self.type=type
        
        # define stlying tags
        self.tag_configure("bold", font=("Arial", 9, "bold"))

        # Load quiz attempts data
        user_quiz_progress_file = f"./data/quizzes/empoweru_{self.type}_{self.user.uid}_scores.txt"
        self.quiz_data = self.load_quiz_attempts(user_quiz_progress_file)

        # Clear the content_text widget and insert the file contents
        self.config(state="normal")
        self.delete(1.0, tk.END)
        if len(self.quiz_data)>0:
            self.insert("1.0", "Quiz Progress\n")
            self.insert("2.0", f"Highest score: {self.get_highest_score()}/{self.quiz_max_marks}\n")
            self.insert("3.0", f"{len(self.quiz_data)} attempts:\n")
            for i in range(4,len(self.quiz_data)+4):
                self.insert(f"{i}.0", f"\t{Utils.parse_timestamp(self.quiz_data[i-4][1])}: {self.quiz_data[i-4][0]}/{self.quiz_max_marks}\n")

            self.tag_add("bold", "1.0", "1.13")
            last_index = len(self.quiz_data)+4
        else:
            self.insert("1.0", "Quiz not attempted\n")
            self.tag_add("bold", "1.0", "1.18")
            last_index = 2

        # insert the progress of the modules
        filepath = f"./data/{self.type}/completed_modules/{self.user.uid}.txt"
        completed_modules = self.load_completed_modules(filepath)

        percentage = round(len(completed_modules)/(len(self.learning_page.module_names)-1)*100,2)
        self.insert(str(last_index)+".0", f"Modules ({percentage} % complete)\n")
        self.tag_add("bold", str(last_index)+".0", f"{last_index}.26")

        # add completion status for each module
        for j in range(1, len(self.learning_page.module_names)):
            status = "Complete" if j in completed_modules else "Incomplete"
            self.insert(f"{last_index+j}.0", f"{self.learning_page.module_names[j]} : {status}\n")

        self.config(state="disabled")   

    def load_completed_modules(self, file_path):
        """Returns a list of strings of completed module numbers for the student"""
        completed_modules = None
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
                completed_modules = [int(line.strip()) for line in lines]
        except FileNotFoundError as e:
            completed_modules = []    
        return completed_modules    


    def load_quiz_attempts(self, file_path):
        """
        Reads the file content and returns a list of tuples of the quiz attempt's score and timestamp
        If the file doesn't exist, return an empty list.
        """
        try:
            with open(file_path, 'r') as f:
                attempts = f.readlines()                    
            component_tuple_list = [(line.strip().split(" ")[0], line.strip().split(" ")[1]) for line in attempts]
            self.quiz_max_marks = component_tuple_list[0][0].split("/")[1]
            return [(tup[0].split("/")[0], tup[1]) for tup in component_tuple_list]
        except FileNotFoundError:
            # Handle the case where the file does not exist
            return []

    def get_attempts(self):
        """Returns the total number of attempts."""
        return len(self.quiz_data)
    
    def get_highest_score(self):
        """Returns the highest score achieved so far"""
        max_score = 0
        for tuple in self.quiz_data:
            if int(tuple[0]) > max_score:
                max_score = int(tuple[0])
        return max_score



