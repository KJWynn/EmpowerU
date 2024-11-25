"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the HomePage class.
"""

# Third party imports
import tkinter as tk
from tkinter import ttk
import os
import tkinter.scrolledtext as st

# Local application imports
from app.empoweru_app_admin import AdminUser
from app.empoweru_app_teacher import TeacherUser
from app.empoweru_app_learner import LearnerUser
from interfaces.main_menu.empoweru_gui_admin_menu import AdminMenu
from interfaces.main_menu.empoweru_gui_teacher_menu import TeacherMenu
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from interfaces.empoweru_gui_button import HoverButton
from util.utils import Utils
import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 20
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.image_path = ""

        # Welcome heading
        self.login_title = tk.Label(master=self, text="Welcome to EmpowerU", font=("Arial Bold", 20))
        self.login_title.grid(row=1, columnspan=3, padx=10, pady=10)

        # Create Register and Login and Shutdown buttons
        self.register_button = HoverButton(self, text="Register", command=self.show_register)
        self.register_button.grid(row=2, column=0, padx=5, pady=10)

        self.login_button = HoverButton(self, text="Login", command=self.show_login_form)
        self.login_button.grid(row=2, column=1, padx=5, pady=10)

        self.shutdown_button = HoverButton(self, text="Shut down", command=master.destroy)
        self.shutdown_button.grid(row=2, column=2,padx=5, pady=10)

        # Login form widgets (hidden initially)
        self.role_label = tk.Label(master=self, text="Select your role:")
        self.selected_role = tk.StringVar()
        self.selected_role.set("<Not selected>")
        self.role_combobox = ttk.Combobox(self, textvariable=self.selected_role, state="readonly")
        self.role_combobox['values'] = ("Learner", "Teacher", "Admin")

        self.username_label = tk.Label(master=self, text="Username:")
        self.username_var = tk.StringVar(master=self)
        self.username_entry = tk.Entry(master=self, textvariable=self.username_var)

        self.password_label = tk.Label(master=self, text="Password:")
        self.password_var = tk.StringVar(master=self)
        self.password_entry = tk.Entry(master=self, textvariable=self.password_var, show="●")

        self.alert_var = tk.StringVar(master=self)
        self.alert_label = tk.Label(master=self, textvariable=self.alert_var)

        self.login_confirm_button = HoverButton(master=self, text="Login", command=lambda: self.login(self.username_var, self.password_var))
        self.back_button = HoverButton(master=self, text="Back",command=self.go_back)

    def set_image_path(self, image_path):
        self.image_path = image_path
        # Logo image
        self.logo_photoimage = tk.PhotoImage(master=self, file=self.image_path)
        self.logo_label = tk.Label(master=self, image=self.logo_photoimage, width=300, height=300)
        self.logo_label.grid(row=0, columnspan=3, sticky=tk.S, padx=10, pady=5)

    def go_back(self):
        # Hide login form widgets
        self.role_label.grid_forget()
        self.role_combobox.grid_forget()
        self.username_label.grid_forget()
        self.username_entry.grid_forget()
        self.password_label.grid_forget()
        self.password_entry.grid_forget()
        self.alert_label.grid_forget()
        self.login_confirm_button.grid_forget()
        self.back_button.grid_forget()
        self.register_button.grid(row=2, column=0, padx=5, pady=5)
        self.login_button.grid(row=2, column=1, padx=5, pady=5)
        self.shutdown_button.grid(row=2, column=2,padx=5, pady=10)

    def show_login_form(self):
        """Method to display login form and hide register/login/shutdown buttons"""
        self.register_button.grid_forget()
        self.login_button.grid_forget()
        self.shutdown_button.grid_forget()

        # Show login form widgets
        self.role_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.role_combobox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        self.selected_role.set("<Not selected>")
        self.username_var.set("")
        self.password_var.set("")   
        self.username_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
        self.username_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        self.password_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
        self.password_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
        self.alert_label.grid(row=5, columnspan=2, padx=10, pady=10)
        self.login_confirm_button.grid(row=6, column=1, padx=10, pady=10,sticky=tk.W)
        self.back_button.grid(row=6,column=0,padx=10, pady=10,sticky=tk.E)

    def show_register(self):
        """Method to open the registration window"""
        self.register_window = tk.Toplevel(self)
        self.register_window.title("Register")
        self.register_window.geometry("500x300")  # Set a default size for the window
        self.register_window.grab_set()
        
        # Registration fields
        reg_label = tk.Label(self.register_window, text="Please enter your details:")
        reg_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        reg_firstname_label = tk.Label(self.register_window, text="First name:")
        reg_firstname_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        reg_firstname_entry = tk.Entry(self.register_window)
        reg_firstname_entry.grid(row=1, column=1, padx=10, pady=5,sticky=tk.W)

        reg_lastname_label = tk.Label(self.register_window, text="Last name:")
        reg_lastname_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        reg_lastname_entry = tk.Entry(self.register_window)
        reg_lastname_entry.grid(row=2, column=1, padx=10, pady=5,sticky=tk.W)

        reg_age_label = tk.Label(self.register_window, text="Age:")
        reg_age_label.grid(row=3, column=0, padx=10, pady=5,sticky=tk.W)
        reg_age_combobox = ttk.Combobox(self.register_window, state="readonly")
        reg_age_combobox['values'] = [age for age in range(13,100)]
        reg_age_combobox.grid(row=3, column=1, padx=10, pady=5)

        reg_email_label = tk.Label(self.register_window, text="Email:")
        reg_email_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        reg_email_entry = tk.Entry(self.register_window)
        reg_email_entry.grid(row=4, column=1, padx=10, pady=5,sticky=tk.W)
        
        reg_username_label = tk.Label(self.register_window, text="Username:")
        reg_username_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        reg_username_entry = tk.Entry(self.register_window)
        reg_username_entry.grid(row=5, column=1, padx=10, pady=5,sticky=tk.W)
        
        reg_password_label = tk.Label(self.register_window, text="Password:")
        reg_password_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        reg_password_entry = tk.Entry(self.register_window, show="●")
        reg_password_entry.grid(row=6, column=1, padx=10, pady=5,sticky=tk.W)
        
        reg_role_label = tk.Label(self.register_window, text="Role:")
        reg_role_label.grid(row=7, column=0, padx=10, pady=5,sticky=tk.W)
        reg_role_combobox = ttk.Combobox(self.register_window, state="readonly")
        reg_role_combobox['values'] = ("Learner", "Teacher", "Admin")
        reg_role_combobox.grid(row=7, column=1, padx=10, pady=5)

        # Submit and Cancel buttons
        submit_button = HoverButton(self.register_window, text="Submit", 
                                    command=lambda: self.register_user(reg_firstname_entry.get().strip(),
                                                                       reg_lastname_entry.get().strip(),
                                                                       reg_age_combobox.get().strip(),
                                                                       reg_email_entry.get().strip(),
                                                                       reg_username_entry.get().strip(),
                                                                       reg_password_entry.get().strip(),
                                                                       reg_role_combobox.get().strip(),
                                                                       self.register_window))
        submit_button.grid(row=8, column=0, padx=10, pady=10)

        cancel_button = HoverButton(self.register_window, text="Cancel", command=self.register_window.destroy)
        cancel_button.grid(row=8, column=1, padx=10, pady=10)

    def register_user(self,firstname,lastname,age,email,username,password,role, register_window):
        """Method for handling user registration. Returns True if it is successful"""
        register_success = False
        if age == "":
            Utils.error_message("Age cannot be left empty")
        elif role == "":
            Utils.error_message("Role cannot be empty")
        elif firstname == "":
            Utils.error_message("First name cannot be empty")
        elif lastname == "":
            Utils.error_message("Last name cannot be empty")
        elif email == "":
            Utils.error_message("Email cannot be empty")       
        elif username == "":
            Utils.error_message("Username cannot be empty")  
        elif password == "":
            Utils.error_message("Password cannot be empty")                               
        else:
            data_directory = "./data/accounts"
            filepath_to_check = os.path.join(data_directory, f"empoweru_{role.lower()}s.txt")
            emails = []
            entries = None
            with open(filepath_to_check, 'r') as file:  # Open file in read mode
                lines = file.readlines()
                entries = len(lines)
                for line in lines:
                    values = line.strip().split(',')  # Split the line by commas and strip any extra whitespace
                    if len(values) >= 4:  # Ensure the line has at least 4 values
                        emails.append(values[4])  # Append the 4th value (index 3) to the emails list
            password_status = self.check_strong_password(password)
            if email in emails:
                Utils.error_message("An account exists for this email. Please use another email.")
            elif not self.is_unique_username(username):
                Utils.error_message(f"The username '{username}' has been taken. Please choose another.")
            elif password_status != "":
                Utils.error_message(password_status)
            else:
                register_success = True
                # privacy policy 
                privacy_policy_window = tk.Toplevel()
                privacy_policy_window.title("EmpowerU Privacy Policy")  # Set the title of the window
                privacy_policy_window.geometry("600x500")  # Set a default size for the window
                privacy_policy_window.grab_set()


                # Theme label widget
                policy_label = tk.Label(privacy_policy_window, text="About Policy")
                policy_label.pack(pady=5, anchor='center')

                # Text box for policy details
                # Creating scrolled text area (Read only)
                text_area = st.ScrolledText(privacy_policy_window, width=100,  height=25, wrap=tk.WORD) 
                text_area.pack(pady = 5, padx = 10) 

                with open("data/policy.txt", "r")as file:
                    content = file.read()
                    text_area.insert(tk.INSERT, content)

                # Making the text read only 
                text_area.configure(state ='disabled') 

                # accept button
                accept_button = tk.Button(privacy_policy_window, text="Accept", 
                                          command=lambda:self.user_agree(age,role,register_window,privacy_policy_window,
                                                                         filepath_to_check,entries,firstname,
                                                                         lastname, email,username,password))
                accept_button.pack(pady=10, anchor='center')   
        return register_success


    def user_agree(self,age,role,register_window,privacy_policy_window,filepath,entries,firstname,lastname,email,username,password):
        """Triggered when the user accepts the privacy policy, completing the registration"""
        entries += 1
        with open(filepath, 'a') as file:  # Open file in read mode
            file.write(f"{age},{role[0].lower()}{entries:02d},{firstname.title()},\
{lastname.title()},{email},{username},{password}\n")
        with open(os.path.join("./data/accounts", "empoweru_unique_usernames.txt"),"a") as file2:
            file2.write(username+"\n")
        Utils.success_message(f"Successfully registered as {role}! You can view the Privacy Policy anytime by logging in, then going to Privacy Policy")
        privacy_policy_window.destroy()
        register_window.destroy()

    def is_unique_username(self,username):
        """Returns True if the chosen username is unique"""
        with open(os.path.join("./data/accounts", "empoweru_unique_usernames.txt"),"r") as file:
            lines = file.readlines()
            for line in lines:
                if username== line.strip():
                    return False
            return True
        
    def check_strong_password(self, password):
        """Returns an error message indicating any issues with the chosen password"""
        error_message = ""
        if len(password) < HomePage.MIN_PASSWORD_LENGTH:
            error_message += "Password too short (less than 8 characters)"
        elif len(password) > HomePage.MAX_PASSWORD_LENGTH:
            error_message += "Password too long (max 20 characters)"
        at_least_one_upper = False
        at_least_one_lower = False
        at_least_one_digit = False
        at_least_one_special = False
        contains_space = False
        for char in password:
            if char == " ":
                contains_space = True
            if char.isupper():
                at_least_one_upper = True
            if char.islower():
                at_least_one_lower = True
            if char.isdigit():
                at_least_one_digit = True
            if char in "~!@#$%^&*()_+={}[]:><?":
                at_least_one_special = True
        if contains_space:
            error_message += "\nPassword cannot contain spaces"
        if not at_least_one_upper:
            error_message += "\nNeed an uppercase letter"
        if not at_least_one_lower:
            error_message += "\nNeed a lowercase letter"
        if not at_least_one_digit:
            error_message += "\nNeed a digit"
        if not at_least_one_special:
            error_message += "\nNeed a special character"
        return error_message
    
    def login(self, username_var, password_var):
        """Method to handle the login upon button click. Returns True if successful"""
        success = False
        self.alert_var.set("")
        user = None
        no_role_selected = False
        if self.selected_role.get() == "Learner":
            user = LearnerUser.authenticate(username_var.get(), password_var.get())
            user_menu = LearnerMenu
        elif self.selected_role.get() == "Teacher":
            user = TeacherUser.authenticate(username_var.get(), password_var.get())
            user_menu = TeacherMenu
        elif self.selected_role.get() == "Admin":
            user = AdminUser.authenticate(username_var.get(), password_var.get())
            user_menu = AdminMenu
        else:
            self.alert_var.set("Please select a role.")
            no_role_selected = True
        
        if user:
            success = True
            self.user_window = user_menu(self.master, user)
            self.master.hide_homepage()
            self.user_window.show_menu()
        else:
            if not no_role_selected:
                self.alert_var.set("Invalid username and/or password. Please try again.")
        if not no_role_selected:
            username_var.set("")
            password_var.set("")
        self.selected_role.set("<Not selected>")
        return success
if __name__ == "__main__":
    pass

