"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the Quiz class.
"""

# Third party imports
import tkinter as tk
from interfaces.empoweru_gui_button import HoverButton
from util.utils import Utils

# Local application imports
import random

class Quiz(tk.Frame):
    """
    This class represents the multiple choice quizzes that appear on the learning platform
    """

    def __init__(self, master, lesson_page, learner_user, type, quiz_name, questions, options, answers): 
        """
        The contructor that initializes all they key attributes for attributes in the Quiz class
        """
        super().__init__(master=master) 
        self.master = master
        self.lesson_page = lesson_page # Stores the object of the previous page to navigate back when neccessary
        self.learner_user = learner_user
        self.type = type
        self.quiz_name = quiz_name

        # Ensures that the questions and options displayed are always shuffled for different users
        shuffled_idx = list(range(len(questions)))
        random.shuffle(shuffled_idx)
        self.questions = [questions[idx] for idx in shuffled_idx ]
        self.options = [options[idx] for idx in shuffled_idx]
        self.answers = [answers[idx] for idx in shuffled_idx]

        # Stores the index of answers chosen by the learner
        self.chosen_answers = [] 

        # Assigns a default index value of -1 for all the chosen answers
        for _ in range(len(self.questions)):
            chosen_answer = tk.IntVar(value=-1)
            self.chosen_answers.append(chosen_answer)
        
        self.idx = 0 # Stores the index of the question

        # Arranges the name of the quiz neatly in the middle
        self.columnconfigure(0, weight=1)
        self.title_label = tk.Label(self, text=self.quiz_name, font=("Arial", 16, "bold")) 
        self.title_label.pack(padx=10, pady=10)

        self.show_progress_tracker()

        # Sets up exit button to go back to the module
        self.exit_button = HoverButton(self, text="Back to Module", command=self.show_exit_warning)
        self.exit_button.pack(padx=10, pady=10)

        # Sets up submit button 
        self.submit_button = HoverButton(self, text="Submit", command=lambda: (self.check_answers(), self.show_confirmation()))
        self.submit_button.pack(padx=10, pady=5)

        self.show_current_question()
        

    def show_progress_tracker(self):
        """
        Method that shows the progress tracker that shows the status of question completion of the users

        Parameters:
        (None)

        Returns:
        (None)
        """
        
        # Sets up frame to display the progress tracker
        self.progress_frame = tk.Frame(self, bd=2, relief="groove", padx=10, pady=5)
        self.progress_frame.pack(fill="x", padx=20, pady=10)

        # Creates and sets up labels that show the question number in the tracker
        self.question_labels = []
        for i in range(len(self.questions)):
            progress_label = tk.Button(self.progress_frame, text=f"Q{i+1}", width=3, relief="groove", padx=5, pady=5, command=lambda i=i: self.go_to_question(i))
            progress_label.pack(side="left", padx=5)
            self.question_labels.append(progress_label) 

    def go_to_question(self, i):
        """
        This method calls for the display of the question navigated to

        Parameters:
        i: int, represents the index of the question that should be displayed

        Returns:
        (None)
        """

        self.idx = i # Assigns to the current index of the question
        self.question_frame.pack_forget()

        try:
            self.conf_frame.pack_forget()
        except AttributeError:
            pass
            
        self.show_current_question() # Displays question
 

    def update_progress_tracker(self):
        """
        This method updates the progress tracker with the correct colour
        depending on the completion status of each question

        Parameters:
        (None)

        Returns:
        (None)
        """
        
        for idx, label in enumerate(self.question_labels):
            if self.chosen_answers[idx].get() != -1:  
                label.config(bg="green", fg="white")  # Label is green when question has been answered
            else:
                label.config(bg="red", fg="white") # Label is red when question is unanswered (still at default value of -1) 
     

    def show_current_question(self):
        """
        This method displays the current question and the related options

        Parameters:
        (None)

        Returns:
        (None)
        """

        # Rearranges related frames and buttons on the page
        self.progress_frame.pack(fill="x", padx=20, pady=10)
        self.exit_button.pack(padx=10, pady=10)
        self.submit_button.pack(padx=10, pady=10)

        # Creates a frame to display the questions
        self.question_frame = tk.Frame(self, bd=2, relief="groove", width=500, height=400, padx=10, pady=10)
    
        # Prevent the frame from resizing with its contents
        self.question_frame.pack_propagate(False)
        self.question_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sets up the current question label
        question_label = tk.Label(self.question_frame, text=f"{self.idx+1}. {self.questions[self.idx]}") 
        question_label.pack(padx=10, pady=10)

        # Displays all the options for the current question
        for option_idx, option in enumerate(self.options[self.idx]):
            option_btn = tk.Radiobutton(self.question_frame, text=option, variable=self.chosen_answers[self.idx], value=option_idx)
            option_btn.pack(anchor='w', padx=20)
        
        # Shows the next button when the question is not the last question
        if self.idx+1 != len(self.questions):
            self.next_button = HoverButton(self.question_frame, text="Next", command=lambda i=self.idx+1: self.go_to_question(i))
            self.next_button.pack(padx=10, pady=5)

        # Shows the previous button when the current question is not the first one   
        if self.idx != 0:
            self.previous_button = HoverButton(self.question_frame, text="Back", command=lambda i=self.idx-1: self.go_to_question(i))
            self.previous_button.pack(padx=10, pady=5)
        
        self.update_progress_tracker()


    def check_answers(self):
        """
        This method checks the answers chosen by the learner with the answers from the system. Returns the score.

        Parameters:
        (None)

        Returns:
        int: score
        """

        self.update_progress_tracker()
        self.score = 0
        self.blanks = 0

        # Compares chosen answers with the answers
        for idx in range(len(self.answers)):
            answer = int(self.chosen_answers[idx].get())
            if self.answers[idx] == answer:
                self.score += 1
            elif answer == -1:
                self.blanks += 1
        return self.score
    
    def show_confirmation(self):
        """
        This method displays the confirmation message after the learner clicks the submit button

        Parameters:
        (None)

        Returns:
        (None)
        """

        # Removes all the buttons and existing frames on the display
        self.submit_button.pack_forget()
        self.exit_button.pack_forget()
        self.question_frame.pack_forget()

        # Creates a new frame for the confirmation 
        self.conf_frame = tk.Frame(self, bd=2, relief="groove", width=500, height=400, padx=10, pady=10)
    
        # Prevent the frame from resizing with its contents
        self.conf_frame.pack_propagate(False)
        self.conf_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Cretaes and places the title for the confirmation frame
        confirmation_title = tk.Label(self.conf_frame, text=f"Submission confirmation", font=("Arial", 14, "bold")) 
        confirmation_title.pack(padx=10, pady=10)

        # Creates and places the confirmation question in the frame
        confirmation_ques = tk.Label(self.conf_frame, text=f"Do you wish to proceed? You will not be able to edit your response after") 
        confirmation_ques.pack(padx=10, pady=10)

        # Creates and places the yes button to follow through with submission
        yes_button = HoverButton(self.conf_frame, text="Yes", command=lambda: (self.conf_frame.pack_forget(),self.store_and_display_results()))
        yes_button.pack(padx=10, pady=5)

        # Creates and places no button to go back to the questions
        no_button = HoverButton(self.conf_frame, text="No", command=lambda: (self.conf_frame.pack_forget(),self.show_current_question()))
        no_button.pack(padx=10, pady=5)

        # Displays warnings if they are questions left blank
        if self.blanks != 0:
            warning_label = tk.Label(self.conf_frame, text=f"WARNING: You have left {self.blanks} question(s) blank.") 
            warning_label.pack(padx=10, pady=10)
            

    def store_and_display_results(self):
        """
        This method stores the quiz score of the learner and displays the results

        Parameters:
        (None)

        Returns:
        (None)
        """
        
        # Writes the scores of the learners in the correct file
        if self.type == "PP":
            filepath = f"./data/quizzes/empoweru_PP_{self.learner_user.uid}_scores.txt"
        elif self.type == "AI":
            filepath = f"./data/quizzes/empoweru_AI_{self.learner_user.uid}_scores.txt"
        elif self.type == "IS":
            filepath = f"./data/quizzes/empoweru_IS_{self.learner_user.uid}_scores.txt"

        with open(filepath, "a") as f:
            f.write(
                f"{self.score}/{len(self.questions)} {Utils.get_current_timestamp()}\n" )
                
        # Hides the current frames on display
        self.question_frame.pack_forget()
        self.progress_frame.pack_forget()

        # Creates and places an exit button that does not show confirmation
        exit_button = HoverButton(self, text="Exit", command = self.return_to_module)
        exit_button.pack(padx=10, pady=10)

        # Creates the frame to display the results
        self.display_frame = tk.Frame(self, bd=2, relief="groove", padx=10, pady=10)
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Creates and displays label to display results
        self.result_label = tk.Label(self.display_frame, text=f"Your marks for this quiz is: ") 
        self.result_label.pack(padx=10, pady=10)

        self.result = tk.Label(self.display_frame, text=f"{self.score}/{len(self.questions)}", font=("Arial", 16, "bold"))
        self.result.pack(padx=10, pady=10)

        # Creates and displays button that allows the learner to review the right and wrong answers made
        self.review_button = HoverButton(self.display_frame, text="Review", command = self.show_review)
        self.review_button.pack(padx=10, pady=10)

    def show_review(self):
        """
        This method displays the review of all the questions in the quiz. Returns a list of feedback strings for each question.

        Parameters:
        (None)

        Returns:
        List of strings.
        """
        self.display_frame.pack_forget()
        feedback = []
        # Creates frame to display review and prevents it from resizing according to content
        self.review_frame = tk.Frame(self, bd=2, relief="groove", width=600, height=600, padx=10, pady=10)
        self.review_frame.pack_propagate(False)
        self.review_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Displays the questions of the quiz
        for question_idx in range(len(self.questions)):
            question_label = tk.Label(self.review_frame, text=f"{question_idx+1}.   {self.questions[question_idx]}")
            question_label.pack(padx=10, pady=10, expand = True)
            answer_idx = self.chosen_answers[question_idx].get()

            # Gets the appropriate feedback message according to learner response
            if answer_idx == self.answers[question_idx]:
                display_text = f"Correct! The answer is {self.options[question_idx][self.answers[question_idx]]}"
            elif answer_idx == -1:
                display_text = f"Question not answered. The answer is {self.options[question_idx][self.answers[question_idx]]}"
            else:
                display_text = f"Incorrect! The answer is {self.options[question_idx][self.answers[question_idx]]}"
            feedback.append(display_text)
            # Displays the options in the right colour according the learner response
            for option_idx in range(4):
                if option_idx == self.answers[question_idx]:
                    option = tk.Label(self.review_frame, text=self.options[question_idx][option_idx], relief="groove", bg="green", fg="white", width=60)
                elif option_idx == answer_idx:
                    option = tk.Label(self.review_frame, text=self.options[question_idx][option_idx], relief="groove", bg="red", fg="white", width=60)
                else:
                    option = tk.Label(self.review_frame, text=self.options[question_idx][option_idx], relief="groove", width=60)
                
                option.pack(anchor='center', padx=20,expand=True)

            # Displays the feedback message 
            feedback_label = tk.Label(self.review_frame, text=display_text)
            feedback_label.pack(padx=10, pady=10, expand=True)
        return feedback

    def show_exit_warning(self):
        """
        This method shows a warning message after the learner clicks the back to module button

        Parameters:
        (None)

        Returns:
        (None)
        """

        # Hides the widgets currently being displayed on screen
        self.question_frame.pack_forget()
        self.submit_button.pack_forget()
        self.exit_button.pack_forget()
        self.progress_frame.pack_forget()

        # Creates a frame for the exit warning
        self.exit_frame = tk.Frame(self, bd=2, relief="groove", width=500, height=400, padx=10, pady=10)
    
        # Prevent the frame from resizing with its contents
        self.exit_frame.pack_propagate(False)
        self.exit_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Creates and places the confirmation title
        confirmation_title= tk.Label(self.exit_frame, text=f"Exit confirmation", font=("Arial", 14, "bold")) 
        confirmation_title.pack(padx=10, pady=10)

        # Creates and places the confirmation question
        confirmation_ques = tk.Label(self.exit_frame, text=f"Do you wish to exit? All your progress will be lost") 
        confirmation_ques.pack(padx=10, pady=10)

        # Creates and places the yes button to go back to the learning pgae
        yes_button = HoverButton(self.exit_frame, text="Yes", command= self.return_to_module)
        yes_button.pack(padx=10, pady=5)

        # Creates and places the no button to go back to the current question
        no_button = HoverButton(self.exit_frame, text="No", command=lambda:(self.exit_frame.pack_forget(),self.show_current_question()))
        no_button.pack(padx=10, pady=5)
    

    def return_to_module(self):
        """
        This method allows the learner to return back to the learning page

        Parameters:
        (None)

        Returns:
        (None)
        """
        self.place_forget()  
        self.lesson_page.place(relx=.5, rely=.5, anchor=tk.CENTER)

