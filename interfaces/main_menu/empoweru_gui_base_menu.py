"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the UserMenu class. It is the base menu which all menus inherit from.
"""

# Third party imports
from tkinter import PhotoImage
from tkinter import font as tkfont
import tkinter as tk
import os
from tkinter import ttk
# Local application imports
from interfaces.main_menu.empoweru_gui_privacy_policy import AboutPolicy
from interfaces.forum.empoweru_gui_forum import Forum
from interfaces.empoweru_gui_button import HoverButton
from util.utils import Utils

class UserMenu(tk.Frame):
    def __init__(self, master, user):
        """
        Constructor for the UserMenu

        Parameter(s):
        - master: master widget of this widget instance, should be the tk.Tk EmpowerU window
        - user: an instance of the User class
        - welcome_label: label widget for greeting the user
        - prompt_label: label widget for prompting the user to choose an option
        - tutorial_btn: button to launch the tutorial
        - forum_btn: button to launch the forum page
        - settings_btn: button to view settings page (privacy policy and giving feedback)
        - images: store PhotoImages to ensure that they do get rendered
        """
        super().__init__(master=master)
        self.master = master
        self.user = user

        self.welcome_label = tk.Label(self, text=f"Welcome in, {user.first_name}!")
        self.welcome_label.pack(padx=10, pady=10)

        self.prompt_label = tk.Label(self, text="Choose one of the following:")
        self.prompt_label.pack(padx=10, pady=10)

        self.tutorial_btn = HoverButton(self, text="EmpowerU Tutorial", width= 20,command=self.show_tutorial)
        self.tutorial_btn.pack(padx=10, pady=10)

        self.forum_btn = HoverButton(self, text="Public forum", width= 20, command=lambda: Forum.show_forum(self))
        self.forum_btn.pack(padx=10, pady=10)

        self.settings_btn = HoverButton(self, text="Settings", width= 20, command=lambda:self.show_settings_page(self))
        self.settings_btn.pack(padx=10, pady=10)

        self.images=[]


    def show_tutorial(self):
        """Pops up a tutorial window for using the system"""
        root = tk.Toplevel()
        root.title("EmpowerU Walkthrough Tutorial")
        root.geometry("1000x600")
        root.grab_set()
        # Create a frame to contain the Text and Scrollbar
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a Text widget with a vertical scrollbar
        scrollbar = tk.Scrollbar(frame)
        tutorial_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, width=60, height=25, padx=10,pady=10)
        scrollbar.config(command=tutorial_text.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tutorial_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        original_font= tutorial_text.cget("font")
        # Define the font for bold and size (use tkinter's font module)
        bold_font = tkfont.Font(tutorial_text, original_font)
        bold_font.configure(weight="bold", size=14)  # Bold and size 14
        subsection_font = tkfont.Font(tutorial_text, original_font)
        subsection_font.configure(size=12)

        # Create tags for formatting
        tutorial_text.tag_configure("bold_title", font=bold_font)
        tutorial_text.tag_configure("subsection", font=subsection_font)

        # Prepare tutorial
        tutorial_text.insert(tk.END, "Welcome to the tutorial! Please maximize the screen for a better experience.\n\n")
        # Launch, register, login
        tutorial_text.insert(tk.END, "Launching, registering, login\n", "bold_title")  # The tag is applied to this text
        tutorial_text.insert(tk.END, "You are greeted with this interface when you launch the application:\n")
        current_dir = os.path.dirname(__file__)  # Get the directory of the current script
        image_path = os.path.join(current_dir, "1_launch_menu.png")
        img1 = PhotoImage(file=image_path)
        self.images.append(img1)
        tutorial_text.image_create(tk.END, image=img1)
        # Tag and configure alignment for images
        tutorial_text.tag_add("center", "5.0", "5.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')
        tutorial_text.insert(tk.END, "\nYou either register as a new user\n")
        image_path = os.path.join(current_dir, "2_registering.png")        
        img2 = PhotoImage(file=image_path)  
        self.images.append(img2)
        tutorial_text.image_create(tk.END, image=img2)    
        tutorial_text.tag_add("center", "7.0", "7.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')
        tutorial_text.insert(tk.END, "\nor login as an existing user\n")
        image_path = os.path.join(current_dir, "3_login.png")        
        img3 = PhotoImage(file=image_path) 
        self.images.append(img3)
        tutorial_text.image_create(tk.END, image=img3)    
        tutorial_text.tag_add("center", "9.0", "9.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')
        tutorial_text.insert(tk.END, "\nOn successful login you'll see your user home page:\n")
        image_path = os.path.join(current_dir, "4_successful_login_menu.png")        
        img4 = PhotoImage(file=image_path)  
        self.images.append(img4)                
        tutorial_text.image_create(tk.END, image=img4)    
        tutorial_text.tag_add("center", "11.0", "11.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')

        # Forum
        tutorial_text.insert(tk.END, "\nPublic Forum\n", "bold_title")  # The tag is applied to this text
        image_path = os.path.join(current_dir, "5_forum.png")        
        img5 = PhotoImage(file=image_path)    
        self.images.append(img5)              
        tutorial_text.image_create(tk.END, image=img5)    
        tutorial_text.tag_add("center", "13.0", "13.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')

        tutorial_text.insert(tk.END, "\n1. Filter posts by a specific topic")
        tutorial_text.insert(tk.END, "\n2. Sort posts by recency or views")
        tutorial_text.insert(tk.END, "\n3. Create a new post")
        tutorial_text.insert(tk.END, "\n4. Chat privately with a teacher")
        tutorial_text.insert(tk.END, "\n5. Comment on the post")
        tutorial_text.insert(tk.END, "\n6. Edit the post (if you are the owner)")
        tutorial_text.insert(tk.END, "\n7. Comments section (only admins can delete comments)\n")
        image_path = os.path.join(current_dir, "6_comment_section.png")        
        img6 = PhotoImage(file=image_path) 
        self.images.append(img6)        
        tutorial_text.image_create(tk.END, image=img6)    

        tutorial_text.insert(tk.END, "\nSettings\n", "bold_title")  # The tag is applied to this text
        image_path = os.path.join(current_dir, "7_settings_menu.png")        
        img7 = PhotoImage(file=image_path) 
        self.images.append(img7)
        tutorial_text.image_create(tk.END, image=img7)    
        tutorial_text.tag_add("center", "23.0", "23.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')
        tutorial_text.insert(tk.END, "\nFeedback\n", "subsection")  # The tag is applied to this text
        image_path = os.path.join(current_dir, "8_feedback.png")        
        img8 = PhotoImage(file=image_path) 
        self.images.append(img8)        
        tutorial_text.image_create(tk.END, image=img8)    
        tutorial_text.tag_add("center", "25.0", "25.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')
        tutorial_text.insert(tk.END, "\nPrivacy Policy\n", "subsection")  # The tag is applied to this text
        image_path = os.path.join(current_dir, "9_privacy_policy.png")        
        img9 = PhotoImage(file=image_path)         
        self.images.append(img9)        
        tutorial_text.image_create(tk.END, image=img9)    
        tutorial_text.tag_add("center", "27.0", "27.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')
        tutorial_text.insert(tk.END, "\nUnits\n", "bold_title")  # The tag is applied to this text
        image_path = os.path.join(current_dir, "10_units.png")        
        img10 = PhotoImage(file=image_path)            
        self.images.append(img10)        
        tutorial_text.image_create(tk.END, image=img10)    
        tutorial_text.tag_add("center", "29.0", "29.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')
        tutorial_text.insert(tk.END, "\nExample of a unit:\n","subsection")
        image_path = os.path.join(current_dir, "11_module.png")        
        img11 = PhotoImage(file=image_path)          
        self.images.append(img11)        
        tutorial_text.image_create(tk.END, image=img11)    
        tutorial_text.tag_add("center", "31.0", "31.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')
        tutorial_text.insert(tk.END, "\n1. Modules\n","subsection")
        image_path = os.path.join(current_dir, "12_module_dropdown.png")        
        img12 = PhotoImage(file=image_path)           
        self.images.append(img12)        
        tutorial_text.image_create(tk.END, image=img12)    
        tutorial_text.tag_add("center", "33.0", "33.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')    
        tutorial_text.insert(tk.END, "\nExample of module. Clicking on the 'Video' button opens up a video in a browser. The 'Mark as complete' button helps you track progress:\n")
        image_path = os.path.join(current_dir, "13_mark_complete_module.png")        
        img13 = PhotoImage(file=image_path)           
        self.images.append(img13)        
        tutorial_text.image_create(tk.END, image=img13)    
        tutorial_text.tag_add("center", "35.0", "35.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center') 
        tutorial_text.insert(tk.END, "\n2. Quiz\n","subsection")
        image_path = os.path.join(current_dir, "14_quiz.png")        
        img14 = PhotoImage(file=image_path)             
        self.images.append(img14)        
        tutorial_text.image_create(tk.END, image=img14)    
        tutorial_text.tag_add("center", "37.0", "37.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center') 
        tutorial_text.insert(tk.END, "\n3. Progress\n","subsection")
        image_path = os.path.join(current_dir, "15_progress.png")        
        img15 = PhotoImage(file=image_path)          
        self.images.append(img15)        
        tutorial_text.image_create(tk.END, image=img15)    
        tutorial_text.tag_add("center", "39.0", "39.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center') 
        tutorial_text.insert(tk.END, "\nYou can click on 'Personal Goals' to manage your goals (up to 10). Select a goal and click 'Mark as complete' to remove the goal from your list.\n")
        image_path = os.path.join(current_dir, "16_goals.png")        
        img16 = PhotoImage(file=image_path)            
        self.images.append(img16)        
        tutorial_text.image_create(tk.END, image=img16)    
        tutorial_text.tag_add("center", "41.0", "41.1")  # Tag only the image's line
        tutorial_text.tag_configure("center", justify='center')

        tutorial_text.insert(tk.END, "\n\nThis is the end of the tutorial. Don't hesitate to reach out in the forum if you're facing difficulties.")

        # Disable the Text widget to make it read-only
        tutorial_text.config(state=tk.DISABLED)


    def show_settings_page(self,parent):
        """Hides the user menu and displays the settings options"""
        parent.hide_menu()
        settings = tk.Frame(parent.master)
        settings.place(relx=.5, rely=.5, anchor=tk.CENTER)

        settings.feedback_button = HoverButton(settings, width=20,text="Provide Feedback", command=self.provide_feedback)
        settings.feedback_button.pack(padx=10, pady=10)

        settings.policy_button = HoverButton(settings, width=20,text="Privacy Policy", command=lambda:self.show_policy(settings))
        settings.policy_button.pack(padx=10, pady=10)

        settings.return_button = HoverButton(settings,width=20, text="Back", command=lambda:self.go_back(settings,parent))
        settings.return_button.pack(padx=10, pady=10)
        
    def provide_feedback(self):
        """
        Pops up a window for giving feedback. Returns this window
        Triggers self.submit_feedback() when the submit button is clicked
        """
         # Create a Toplevel window for creating a new post
        self.feedback_window = tk.Toplevel()
        self.feedback_window.title("Feedback")  # Set the title of the window
        self.feedback_window.geometry("600x350")  # Set a default size for the window
        self.feedback_window.grab_set()

        # Create a frame with thicker borders
        feedback_frame = tk.Frame(self.feedback_window, bd=2, relief=tk.RAISED)
        feedback_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # topic selection
        topic_label = tk.Label(feedback_frame, text="Select topic:")
        topic_label.grid(row=0,column=0, padx=(5, 10), pady=5, sticky="w")

        # Create a Combobox for topic selection
        self.feedback_topic_var = tk.StringVar()
        self.feedback_topic_var.set("<Select a topic>")  # default value
        self.feedback_combobox = ttk.Combobox(feedback_frame, textvariable=self.feedback_topic_var, state="readonly")
        self.feedback_combobox['values'] = ("Bug report", "Suggestions", "Others")
        self.feedback_combobox.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="w")

        # Create a Text widget for chat content, below the checkbox and dropdown
        text_widget = tk.Text(feedback_frame, width=50, height=10)
        text_widget.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")
        # Create a scrollbar for the Text widget
        scrollbar = tk.Scrollbar(feedback_frame, command=text_widget.yview)
        scrollbar.grid(row=1, column=2, sticky="ns", pady=(5, 10))

        text_widget.config(yscrollcommand=scrollbar.set)

        # Create a frame for buttons
        button_frame = tk.Frame(self.feedback_window)
        button_frame.pack(pady=5)

        # Add a button to save the new post
        post_button = HoverButton(button_frame, text="Submit", command=lambda:self.submit_feedback(text_widget.get("1.0", tk.END).strip(), self.feedback_window))
        post_button.pack(side=tk.LEFT, padx=5)

        # Add a cancel button
        cancel_button = HoverButton(button_frame, text="Cancel",command=self.feedback_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Configure the grid layout for the new_post_frame
        feedback_frame.grid_columnconfigure(0, weight=1)
        feedback_frame.grid_columnconfigure(1, weight=1)
        feedback_frame.grid_rowconfigure(1, weight=1)

        return self.feedback_window

    def submit_feedback(self, text, feedback_window):
        """Submits the feedback if the fields are not empty. Returns True is successful"""
        success = False
        topic = self.feedback_topic_var.get()
        if text == "":
            Utils.error_message("Feedback cannot be empty!")
        elif topic== "<Select a topic>":
            Utils.error_message("Please choose a topic tag for the post!")
        else:
            success = True
            feedback_window.destroy()
            Utils.success_message("Successfully submitted feedback!")
        return success
    
    def go_back(self,settings,parent):
        """Close settings window and show the user menu"""
        settings.place_forget()
        parent.show_menu()

    def show_policy(self,parent):
        """Popup the privacy policy. Returns an AboutPolicy instance"""
        about_policy = AboutPolicy(parent.master, parent)
        about_policy.place(relx=.5, rely=.5, anchor=tk.CENTER)
        return about_policy

    def logout(self):
        """
        Method to handle the logout upon button click.

        Parameter(s):
        (None)

        Return(s):
        (None)
        """
        self.hide_menu()
        self.master.show_homepage()

    def show_menu(self):
        """
        Method to show the user menu.
        """
        self.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def hide_menu(self):
        """
        Method to hide the user menu frame.
        """
        self.place_forget()




if __name__ == "__main__":
    # DO NOT MODIFY
    pass

