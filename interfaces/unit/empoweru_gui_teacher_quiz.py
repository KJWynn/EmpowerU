"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the TeacherQuiz
"""

# Third party imports
import tkinter as tk
from tkinter import messagebox

# Local application imports
from interfaces.empoweru_gui_button import HoverButton
from util.utils import Utils


class TeacherQuiz(tk.Frame):
    """
    Class that represents the layout of the quiz in the teachers perspective (to add and remove questions)
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

        self.questions = questions
        self.options = options
        self.answers = answers

        # Stores the index of answers chosen by the learner
        self.chosen_answers = [] 

        # Assigns a default index value of -1 for all the chosen answers
        for idx in range(len(self.questions)):
            chosen_answer = tk.IntVar(value=self.answers[idx])
            self.chosen_answers.append(chosen_answer)

        self.idx = 0 # Stores the index of the question

        # Arranges the name of the quiz neatly in the middle
        self.columnconfigure(0, weight=1)
        self.title_label = tk.Label(self, text=self.quiz_name, font=("Arial", 16, "bold")) 
        self.title_label.pack(padx=10, pady=10)

        # Instructions for better usability
        self.desc_label = tk.Label(self, text="Please choose the correct answer using the radiobuttons below\n"
                                    "Navigate to the question you wish to using the buttons right below") 
        self.desc_label.pack(padx=10, pady=10)

        self.show_progress_tracker()

        # Sets up exit button to go back to the module
        self.exit_button = HoverButton(self, text="Back to Module", command=self.show_exit_warning)
        self.exit_button.pack(padx=10, pady=10)

        # Sets up submit button 
        self.submit_button = HoverButton(self, text="Submit", command=lambda: (self.show_confirmation()))
        self.submit_button.pack(padx=10, pady=5)

        # Sets up add button to add new questions
        self.add_button = HoverButton(self, text="Add Question", command=lambda: (self.add_question()))
        self.add_button.pack(padx=10, pady=5)

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

    def go_to_question(self, idx):
        """
        This method calls for the display of the question navigated to

        Parameters:
        idx: int, represents the index of the question that should be displayed

        Returns:
        (None)
        """

        self.idx = idx # Assigns to the current index of the question
        self.question_frame.pack_forget()

        try:
            self.conf_frame.pack_forget()
        except AttributeError:
            pass
            
        self.show_current_question() # Displays question

    
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
        self.add_button.pack(padx=10, pady=5)

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

        # Sets up button to remove current question
        self.remove_button = HoverButton(self.question_frame, text="Remove question", command=lambda i=self.idx: self.destroy_question(i))
        self.remove_button.pack(padx=10, pady=5)
    
    def destroy_question(self,i):
        """
        Method that removes the current question

        Parameters:
        i: int, represents the index of the question that is being removed

        Returns:
        (None)
        """

        # Removes all data related to question
        self.questions.pop(i)
        self.answers.pop(i)
        self.options.pop(i)
        self.chosen_answers.pop(i)

        # Removes labels in progress tracker
        for labels in self.question_labels:
            labels.destroy()
        
        # Rearranges the labels in the progress tracker
        self.question_labels = []
        for i in range(len(self.questions)):
            progress_label = tk.Button(self.progress_frame, text=f"Q{i+1}", width=3, relief="groove", padx=5, pady=5, command=lambda i=i: self.go_to_question(i))
            progress_label.pack(side="left", padx=5)
            self.question_labels.append(progress_label)
        
        # Adjusts index if last question is removed
        if self.idx == len(self.questions):
            self.idx -= 1
        
        self.question_frame.pack_forget()
        if self.idx >= 0:
            self.show_current_question()
    
    def add_question(self):
        """
        Method that requests user input to create a new question

        Parameters:
        (None)

        Returns:
        (None)
        """
        self.adding_frame = tk.Toplevel(self)

        # Variable for input question
        self.question_var = tk.StringVar(self.adding_frame)
        self.question_label = tk.Label(self.adding_frame, text="Enter the question:")
        self.question_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # To collects user input regarding the new question
        self.question_entry = tk.Entry(self.adding_frame, textvariable=self.question_var, width=50)
        self.question_entry.grid(row=0, column=1, padx=10, pady=5)

        self.new_answer = tk.IntVar(value=-1)

        # Stores option variables so it can be accessed later
        self.options_var = []

        for idx in range(4):
            # Variable for options
            option_var = tk.StringVar(self.adding_frame)

            option_btn = tk.Radiobutton(self.adding_frame, textvariable=option_var, variable=self.new_answer, value=idx)
            option_btn.grid(row=idx+1, column=0, sticky="w", padx=10, pady=5)

            option_entry = tk.Entry(self.adding_frame, textvariable=option_var)
            option_entry.grid(row=idx+1, column=1, padx=10, pady=5)

            self.options_var.append(option_var)

        # Calls for error checking
        self.done_button = HoverButton(self.adding_frame, text="Done", command=self.check_for_blanks)
        self.done_button.grid(row=5, sticky= "e",column=1, padx=10, pady=5)
    
    def check_for_blanks(self):
        """
        Method that makes sure none of the columns are left blank when adding a new question

        Parameters:
        (None)

        Returns:
        (None)
        """
        wrong_option = False
        wrong_question = False

        # Checks if question is inputted
        if self.question_var.get() == "":
            Utils.error_message("Error! You cannot leave the question column blank.")
            wrong_question = True

        # Checks if all options are inputted 
        for options in self.options_var:
            if options.get() == "" and wrong_question == False:
                Utils.error_message("Error! You cannot leave any of the options blank.")
                self.adding_frame.lift()
                wrong_option = True
                break
        
        # Checks if answer is inputted
        if self.new_answer.get() == -1 and wrong_option == False and wrong_question == False:
            Utils.error_message("Error! You must choose an answer to be the correct one")
            self.adding_frame.lift()
        
        # Only calls function when all variables are not empty
        elif wrong_option == False and wrong_question == False:
            self.store_questions()

    def store_questions(self):
        """
        Method that stores the added question to be displayed on the frame

        Parameters:
        (None)

        Returns:
        (None)
        """

        # Updates all data regarding question
        question = self.question_var.get()
        self.questions.append(question)

        answer = int(self.new_answer.get())
        self.answers.append(answer)

        option_list = []

        for i in range(4):
            option = self.options_var[i].get()
            option_list.append(option)
        
        self.options.append(option_list)
        
        chosen_answer = tk.IntVar(value=answer)
        self.chosen_answers.append(chosen_answer)

        # Updates progress tracker
        progress_label = tk.Button(self.progress_frame, text=f"Q{len(self.questions)}", width=3, relief="groove", padx=5, pady=5, command=lambda i=len(self.questions) - 1: self.go_to_question(i))
        progress_label.pack(side="left", padx=5)
        self.question_labels.append(progress_label) 

        self.adding_frame.destroy()
        
        
    def show_confirmation(self):
        """
        This method displays the confirmation message after the learner clicks the submit button

        Parameters:
        (None)

        Returns:
        (None)
        """

        # Removes all the buttons and existing frames on the display
        self.progress_frame.pack_forget()
        self.submit_button.pack_forget()
        self.exit_button.pack_forget()
        self.question_frame.pack_forget()
        self.add_button.pack_forget()

        # Creates a new frame for the confirmation 
        self.conf_frame = tk.Frame(self, bd=2, relief="groove", width=500, height=400, padx=10, pady=10)
    
        # Prevent the frame from resizing with its contents
        self.conf_frame.pack_propagate(False)
        self.conf_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Cretaes and places the title for the confirmation frame
        confirmation_title = tk.Label(self.conf_frame, text=f"Quiz Editing Completion Confirmation", font=("Arial", 14, "bold")) 
        confirmation_title.pack(padx=10, pady=10)

        # Creates and places the confirmation question in the frame
        confirmation_ques = tk.Label(self.conf_frame, text=f"Do you wish to proceed? The new questions and answers will be stored in the database") 
        confirmation_ques.pack(padx=10, pady=10)

        # Creates and places the yes button to follow through with submission
        yes_button = HoverButton(self.conf_frame, text="Yes", command=self.return_to_module)
        yes_button.pack(padx=10, pady=5)

        # Creates and places no button to go back to the questions
        no_button = HoverButton(self.conf_frame, text="No", command=lambda: (self.conf_frame.pack_forget(),self.show_current_question()))
        no_button.pack(padx=10, pady=5)
    

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
        self.add_button.pack_forget()
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