"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the LearningPage class.
"""

# Third party imports
import tkinter as tk
from tkinter import ttk  # For the dropdown functionality
import webbrowser

# Local application imports
from util.utils import Utils
from interfaces.unit.empoweru_gui_quizzes import Quiz
from interfaces.empoweru_gui_button import HoverButton
from util.utils import VideoNotFoundError
from interfaces.unit.empoweru_progress_page import ProgressPage
from app.empoweru_app_learner import LearnerUser
from app.empoweru_app_admin import AdminUser
from interfaces.unit.empoweru_gui_teacher_quiz import TeacherQuiz
from app.empoweru_app_teacher import TeacherUser

import os

class LearningPage(tk.Frame):
    """
    This class represents the learning page of each unit
    """
    MAX_GOALS = 10
    MODULE_VIDEO_URL_MAPPING = {"pp1":"https://www.youtube.com/watch?v=fWjsdhR3z3c", 
                                "pp2":"https://www.youtube.com/watch?v=tvwo09N9QTQ", 
                                "pp3":"https://www.youtube.com/watch?v=89cGQjB5R4M",
                                "ai1":"https://youtu.be/ad79nYk2keg?feature=shared",
                                "ai2":"https://www.youtube.com/watch?v=E0Hmnixke2g", 
                                "ai3":"https://www.youtube.com/watch?v=fLvJ8VdHLA0",
                                "is1":"https://www.youtube.com/watch?v=gx0vlRpdFnc", 
                                "is2":"https://www.youtube.com/watch?v=9GZlVOafYTg", 
                                "is3":"https://www.youtube.com/watch?v=XLvPpirlmEs"}
    def __init__(self, master, unit_page, learner_user, title, type, module_names):
        super().__init__(master=master)
        
        self.master = master
        self.learner_user = learner_user
        self.unit_page = unit_page
        self.type = type
        self.title = title
        self.module_names = module_names
        self.current_module = None

        # Configure the main frame to use grid layout
        self.grid(row=0, column=0, sticky='nsew')

        # Configure grid rows and columns
        self.columnconfigure(0, weight=1)  # For navigation panel, fixed size
        self.columnconfigure(1, weight=3)  # For content area, takes remaining space
        self.rowconfigure(0, weight=0)  # Fixed size for header row
        self.rowconfigure(1, weight=0)  # Fixed size for module label
        self.rowconfigure(2, weight=1)  # Content area will take up remaining space
        self.rowconfigure(3, weight=0)  # Fixed size for the mark as complete button

        # Add Main Menu button at the very top
        self.return_to_units_home_page_btn = HoverButton(self, text="Return", command=self.return_unit_page)
        self.return_to_units_home_page_btn.grid(row=0, column=0, sticky='w', pady=5)

        # Add a label between the buttons with the topic
        self.title_label = tk.Label(self, text=self.title, font=("Arial", 14, "bold"))
        self.title_label.grid(row=0, column=1, sticky='w', pady=5)

        # Add label for module
        self.module_label_var = tk.StringVar()
        self.module_label_var.set("Overview")
        self.module_label = tk.Label(self, textvariable=self.module_label_var,font=("Arial", 10, "bold"))
        self.module_label.grid(row=1, column=1, sticky='w', pady=2)
        # Add button to bring up personal goals page
        self.goals_btn = HoverButton(self,text="Personal Goals", command=self.view_goals)
        
        # Create a frame for navigation (left panel)
        self.nav_frame = tk.Frame(self, width=110, bg="gray")
        self.nav_frame.grid(row=2, column=0, sticky='nsew', padx=10)
        self.nav_frame.grid_propagate(False)  # Prevent resizing of the nav frame
        NAV_OPTION_WIDTH=12
        # Nav option 1: Add "Overview" button
        self.overview_btn = HoverButton(self.nav_frame, fixed=True,text="Unit overview", anchor="w",width=NAV_OPTION_WIDTH, command=lambda: self.show_module(f"{self.type.lower()}0"),outline=False)
        self.overview_btn.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        default_font= self.overview_btn.cget("font")

        # Define style for the menu button
        style = ttk.Style()
        style.configure("Custom.TMenubutton",
                        background="gray",  # Set background color
                        foreground="black",      # Set text color
                        font=default_font)  # Customize font if needed

        style.map("Custom.TMenubutton",
                  foreground=[("active", "white")])  # Text color on hover

        # Nav option 2: Modules dropdown
        self.module_menu_btn = ttk.Menubutton(self.nav_frame, text="Modules", style="Custom.TMenubutton",direction="below", width=NAV_OPTION_WIDTH, padding=(2, 0, 0, 0))
        self.module_menu = tk.Menu(self.module_menu_btn, tearoff=0)
        for i in range(1, len(self.module_names)):
            self.module_menu.add_command(label=self.module_names[i], command=lambda i=i: self.show_module(f"{self.type.lower()}{i}"))
        self.module_menu_btn["menu"] = self.module_menu
        self.module_menu_btn.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        # Nav option 3: Quiz button
        self.quiz_btn = HoverButton(self.nav_frame, fixed=True, text="Quiz", command=self.show_test, anchor="w", width=NAV_OPTION_WIDTH, outline=False)
        self.quiz_btn.grid(row=2, column=0,padx=5,  pady=5, sticky="W")
        # Nav option 4: Progress button
        self.progress_btn = HoverButton(self.nav_frame,fixed=True,text="Progress", command=self.show_progress, anchor="w", width=NAV_OPTION_WIDTH, outline=False)
        self.progress_btn.grid(row=3, column=0,padx=5,  pady=5, sticky="W")

        # Create a content area (right part of the screen) for displaying dynamic content
        self.content_frame = tk.Frame(self)
        # self.content_frame.grid(row=2, column=1, sticky='nsew')
        self.content_frame.grid(row=2, column=1)

        self.progress = None
        # Right Content frame for displaying dynamic content based on the selected option
        self.content_text = tk.Text(self.content_frame, wrap="word")
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Add button for video
        self.video_btn = HoverButton(self, text="Video", command=self.launch_video)

        # Add button to mark as complete
        self.mark_complete_btn = HoverButton(self, text="Mark as complete", command= self.commit_progress)
        self.mark_complete_btn.grid(row=3, column=2, sticky="w", pady=2)
        # Initially, show the unit overview
        self.show_module(f"{self.type.lower()}0")

    def launch_video(self):
        """
        Returns True if the video was launched successfully

        Parameters:
        (None)

        Returns:
        success: bool, True when video is accessed and launched successfully, false otherwise
        """
        success = False
        resource_url = None

        # Error handles url
        try:
            resource_url = LearningPage.MODULE_VIDEO_URL_MAPPING[self.current_module]
            if resource_url == "":
                raise VideoNotFoundError()
            webbrowser.open(resource_url)
            success = True
        except KeyError:
            print(f"The module {self.current_module} does not have an associated video! This module may not exist")
        except VideoNotFoundError as e:
            print(e)
        return success
    
    def commit_progress(self):
        """
        Writes progress on completed modules to database

        Parameters:
        (None)

        Returns:
        (None)
        """

        filepath = f"./data/{self.type}/completed_modules/{self.learner_user.uid}.txt"
        completed_modules = []

        # Conducts error handling when reading from file
        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
                completed_modules = [int(line.strip()) for line in lines]
        except FileNotFoundError as e:
            print("No completed modules")
        if int(self.current_module[2:]) not in completed_modules:
            with open(filepath, "a") as f:
                f.write(
                    f"{int(self.current_module[2:])}\n" )

    def show_progress(self):
        """
        Replaces the content frame with the progress page

        Parameters:
        (None)

        Returns:
        (None)
        """
        
        # Shows the progress tracker elements
        if self.progress:
            self.progress.pack_forget()
        self.video_btn.grid_forget()
        self.goals_btn.grid(row=1,column=1,sticky='e')
        self.mark_complete_btn.grid_forget()
        self.module_label_var.set("Progress")

        # Hide the current content text
        self.content_text.pack_forget()
        self.progress = ProgressPage(self.content_frame, self, self.learner_user, self.type, wrap="word")
        self.progress.pack(fill=tk.BOTH, expand=True)

    def show_module(self, module_code):
        """
        Displays module content with scrollable text.

        Parameters:
        (None)

        Returns:
        (None)
        """
        self.goals_btn.grid_forget()
        self.video_btn.grid_forget()

        # Sets up module features
        self.current_module = module_code
        if int(self.current_module[2:]) != 0:
            self.video_btn.grid(row=3, column=1, sticky="w", pady=2)
            self.mark_complete_btn.grid(row=3, column=1, sticky="e", pady=2)
            self.mark_complete_btn.config(state="active")
        else:
            self.mark_complete_btn.grid_forget()

        if self.progress:
            # remove the progress and show the original content frame
            self.progress.pack_forget()
            self.progress = None
            self.content_text.pack(fill=tk.BOTH, expand=True)


        self.module_label_var.set(self.module_names[int(module_code[2:])])
        try:
            # Define the directory path using the self.type (assuming self.type exists)
            directory = f"./data/{self.type}"
            # List all files in the directory
            files_in_directory = os.listdir(directory)
            # Find the file that starts with the given module_code
            matching_files = [f for f in files_in_directory if f.startswith(module_code)]
            if not matching_files:
                raise FileNotFoundError(f"No file starting with {module_code} found in {directory}")
            # Assuming there's only one matching file, or you want the first match
            filepath = os.path.join(directory, matching_files[0])

            # Open the matching file and read its contents
            with open(filepath, "r",encoding="utf-8") as f:
                overview_text = f.read()

            # Clear the content_text widget and insert the file contents
            self.content_text.config(state="normal")
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, overview_text)
            self.content_text.config(state="disabled")

        except FileNotFoundError as e:
            print(f"Module {module_code} does not exist for this unit. Error: {e}")


    def show_test(self):
        """
        Shows the quiz popup.

        Parameters:
        (None)

        Returns:
        (None)
        """
        if self.progress:
            # remove the progress and show the original content frame
            self.progress.pack_forget()
            self.progress = None
            self.content_text.pack(fill=tk.BOTH, expand=True)
        
        # Finds correct file to extract quiz data from
        filepath = f"./data/{self.type}/{self.type.lower()}_quiz_data.txt"

        # Collects the quiz data from the file
        with open(filepath, "r") as file:
            lines = file.readlines()
            quiz_name = lines[0].strip()
            questions = lines[1].strip().split(",,")

            # Stores a list containing lists of options
            option_list = []
            for line in lines[2:2+len(questions)]:
                options = line.strip().split(",,")
                option_list.append(options)
            
            # Answers stored as the index of the correct answer from the list of option
            raw_answers = lines[2 + len(questions)].strip().split(",,")
            answers = [int(answer_idx) for answer_idx in raw_answers]
        
        # Creates class according to user
        if isinstance(self.learner_user, LearnerUser):
            quiz_popup = Quiz(
                self.master, self, self.learner_user, self.type, quiz_name, questions, option_list, answers)
        elif isinstance(self.learner_user, TeacherUser) or isinstance(self.learner_user, AdminUser):
            quiz_popup = TeacherQuiz(
                self.master, self, self.learner_user, self.type, quiz_name, questions, option_list, answers)

            
        quiz_popup.place(relx=.5, rely=.5, anchor=tk.CENTER)
        self.place_forget()

    def return_unit_page(self):
        """
        Handles the return to the unit home page.

        Parameters:
        (None)

        Returns:
        (None)
        """
        self.place_forget()
        self.unit_page.place(relx=.5, rely=.5, anchor=tk.CENTER)


    def view_goals(self):
        """
        Displays page of personal goals

        Parameters:
        (None)

        Returns:
        (None)
        """
        filepath = f"./data/{self.type.upper()}/goals/{self.learner_user.uid}.txt"
        goals = None
        try:
            with open(filepath, "r") as f:
                goals = f.readlines()
        except FileNotFoundError as e:
            print("No goals for this user")
            goals = []
                
        # Create a Toplevel window for entering and viewing goals
        new_post_window = tk.Toplevel()
        new_post_window.title("Personal Goals")
        new_post_window.geometry("600x410")
        new_post_window.grab_set()

        # Label for the goal entry
        tk.Label(new_post_window, text="Enter a new goal (max 100 characters):").pack(pady=10)

        # Textbox for entering a new goal
        goal_entry = tk.Entry(new_post_window, width=50)
        goal_entry.pack(pady=5)

        # Create a Frame to hold both buttons side by side
        button_frame = tk.Frame(new_post_window)
        button_frame.pack(pady=5)

        # Button to add the goal
        HoverButton(button_frame, text="Add Goal", command=lambda:self.add_goal(goal_entry, goals, listbox, filepath)).pack(side=tk.LEFT, padx=5)
        
        # Button to clear the entry
        HoverButton(button_frame, text="Clear", command=lambda: goal_entry.delete(0, tk.END)).pack(side=tk.LEFT, padx=5)

        # Label for the goal list
        tk.Label(new_post_window, text="Your Goals:").pack(pady=10)

        # Listbox for displaying goals
        listbox = tk.Listbox(new_post_window, width=50, height=10)
        listbox.pack(pady=5)

        # Populate the listbox with the current goals
        for goal in goals:
            listbox.insert(tk.END, goal)

        # Function to mark a goal as complete
        def mark_as_complete():
            try:
                selected_goal_index = listbox.curselection()[0]  # Get the selected goal index
                listbox.delete(selected_goal_index)  # Remove from the listbox
                del goals[selected_goal_index]  # Remove from the goals list
                with open(filepath, "w") as f: # update file
                    for goal in goals:
                        f.write(goal.strip() + "\n")
            except IndexError:
                Utils.error_message("Error: No goal selected")


        # Button to mark a goal as complete
        HoverButton(new_post_window, text="Mark as Complete", command=mark_as_complete).pack(pady=10)
        HoverButton(new_post_window, text="Finish", command=new_post_window.destroy).pack(pady=10)
        
    def add_goal(self, goal_entry, goals, listbox, filepath):
        """
        Returns True if personal goal was successfully added

        Parameters:
        (None)

        Returns:
        success: bool, True when message appended successfully, false otherwise
        """

        # Prints out error message accordingly
        success = False
        new_goal = goal_entry.get().strip()
        if len(goals) >= LearningPage.MAX_GOALS:
            Utils.error_message("Error: Maximum of 10 goals reached. Complete a goal before adding a new one.")
        elif len(new_goal) > 100:
            Utils.error_message("Error: Goal cannot exceed 50 characters.")
        elif new_goal == "":
            Utils.error_message("Error: Goal cannot be empty.")
        else:
            # Adds goals to personal goals list
            success = True
            goals.append(new_goal)
            listbox.insert(tk.END, new_goal)
            goal_entry.delete(0, tk.END)
            with open(filepath, "w") as f:
                for goal in goals:
                    f.write(goal.strip() + "\n")
        return success


