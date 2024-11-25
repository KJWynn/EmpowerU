"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the Comment class.
"""

# Third party imports
import tkinter as tk
import re

# Local application imports
from interfaces.empoweru_gui_button import HoverButton
from util.utils import Utils

class Comment():
    def __init__(self, user, timestamp, message, anonymous, edited,replies=None, parent=None):
        """
        Constructor for the Comment class.
        user: string representation of currently logged in User instance with format "{full name} (role)" 
        timestamp: string - The time this comment was written with format dd:mm:yyyy hh:mm:ss
        message: string - The comment content
        parent: Comment - the comment this comment is replying to
        replies: list of replies to this comment (optional). Replies are Comment instances
        deleted: bool - whether this comment is deleted
        anonymous: bool - whether the commenter is anonymous
        edited: bool - whether the comment was edited
        """
        self.user = user
        self.timestamp = timestamp
        self.message = message
        self.parent = parent
        self.replies = replies if replies else []  # Initialize with an empty list if no replies provided
        self.deleted = False
        self.anonymous = anonymous
        self.edited = edited

    @staticmethod
    def parse_comment_string(comment_string):
        """
        Parses the raw comment string into a list of comments with nested replies.
        
        The structure is identified by tags like <c1> (top-level comments), <c2> (replies to top-level), <c3>, etc.
        
        Returns a list of Comment objects with nested replies.
        """
        comment_pattern = r"(<c\d>)([^:]+):(\d+):(.+)"
        comments = re.findall(comment_pattern, comment_string)

        parsed_comments = []
        comment_stack = []  # Stack to manage nested comments by their level
        for tag, user, timestamp, message in comments:
            level = int(tag[2])  # Extract the level from the tag (e.g., 1 from <c1>, 2 from <c2>, etc.)
            user_components = user.split("-")
            user = user_components[0].strip()
            anonymous = user_components[1].split(",")[0].strip()=="Y"
            edited = user_components[1].split(",")[1].strip=="Y"
            new_comment = Comment(user=user, timestamp=timestamp, message=message, anonymous=anonymous,edited=edited)

            if level == 1:
                # It's a top-level comment, so we start fresh
                parsed_comments.append(new_comment)
                comment_stack = [(new_comment, level)]
            else:
                # It's a reply to a previous comment
                # Find the correct parent comment based on the level
                while comment_stack and comment_stack[-1][1] >= level:
                    comment_stack.pop()  # Remove deeper level comments

                if comment_stack:
                    parent_comment = comment_stack[-1][0]
                    parent_comment.replies.append(new_comment)
                    new_comment.parent = parent_comment  # Set the parent attribute for the reply


                # Add the current comment to the stack to handle future replies
                comment_stack.append((new_comment, level))

        return parsed_comments
    

    def edit_comment(self, message_label):
        """Pops up a window for editing the comment. Clicking on the 'Save' button triggers self.save_comment()"""
        # Create a Toplevel window for editing comments
        edit_window = tk.Toplevel()
        edit_window.title("Edit Comment") 
        edit_window.geometry("400x200") 
        edit_window.grab_set() # make this window the focus
        # Create a frame with thicker borders
        edit_frame = tk.Frame(edit_window, bd=2, relief=tk.RAISED)  
        edit_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create a Text widget to store the current comment content. The user is free to edit this content
        text_widget = tk.Text(edit_frame, width=50, height=5)  # Set height
        # if comment is edited, copy all the contents after the 8 character header "[Edited]" 
        if self.edited:
            text_widget.insert(tk.END, self.message[9:])
        else:
            text_widget.insert(tk.END, self.message)
        text_widget.pack(side=tk.LEFT, fill='both', expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(edit_frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        text_widget.config(yscrollcommand=scrollbar.set)

        # Add a button to save changes and cancel
        save_button = HoverButton(edit_window, text="Save", command=lambda: self.save_comment(edit_window, message_label, text_widget))
        save_button.pack(pady=5)
        cancel_button = HoverButton(edit_window, text="Cancel", command=edit_window.destroy)
        cancel_button.pack(pady=5)

    def save_comment(self,edit_window,message_label, text_widget):
        """Updates displayed message if text is not empty, displays error popup otherwise."""
        text = text_widget.get("1.0", tk.END).strip() # get the edited content
        if text != "":
            new_text = "[Edited]\n" + text_widget.get("1.0", tk.END).strip() # insert header to indicate that the comment was edited
            self.message = new_text
            message_label.config(text= new_text)  # Update displayed message
            edit_window.destroy()
            self.edited = True # this comment's edited status should be reflected too
        else:
            Utils.error_message("Comment cannot be empty!")

    def delete_comment(self, forum):
        """Sets the comment message to [Deleted], refreshes the comment section to reflect this"""
        self.deleted = True
        self.message = '[Deleted]'
        forum.refresh_comments()

    @staticmethod
    def add_comment(forum):
        """
        Pops up a window to add a comment (optional to comment anonymously). 
        Clicking on the 'Submit' button triggers submit_comment()
        """
        # Create a Toplevel window for adding a comment
        comment_window = tk.Toplevel()
        comment_window.title("Comment")  # Set the title of the window
        comment_window.geometry("600x350")  # Set a default size for the window
        comment_window.grab_set()
        # Create a frame with thicker borders
        comment_frame = tk.Frame(comment_window, bd=2, relief=tk.RAISED)  
        comment_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create a Text widget with a limited height
        comment_text_widget = tk.Text(comment_frame, width=50, height=5)  
        comment_text_widget.pack(side=tk.LEFT, fill='both', expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(comment_frame, command=comment_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        comment_text_widget.config(yscrollcommand=scrollbar.set)

        # Create a Checkbutton for "Anonymous" option
        anonymous_var = tk.IntVar()  # To hold the value of the checkbox
        anonymous_check = tk.Checkbutton(comment_frame, text="Anonymous", variable=anonymous_var)
        anonymous_check.pack(pady=10)

        # Create a frame for buttons
        button_frame = tk.Frame(comment_window)
        button_frame.pack(pady=5)
        # Add a button to save the new post and a cancel button
        submit_button = HoverButton(button_frame, text="Submit", command=lambda: Comment.submit_comment(comment_window, comment_text_widget, anonymous_var,forum))
        submit_button.pack(side=tk.LEFT, padx=5)
        cancel_button = HoverButton(button_frame, text="Cancel",command=lambda: comment_window.destroy())
        cancel_button.pack(side=tk.LEFT, padx=5)

    @staticmethod
    def submit_comment(comment_window, comment_text_widget, anonymous_var, forum):
        """
        Adds comment to current post, refreshes the comment section to reflect this
        Displays error popup if comment is empty
        """
        comment_text = comment_text_widget.get("1.0", tk.END).strip()
        if comment_text!="":
            comment_timestamp = Utils.get_current_timestamp()
            new_comment = Comment(user=forum.user, message=comment_text, timestamp=comment_timestamp, anonymous=bool(anonymous_var.get()),edited=False)
            # Add the new comment to the current post
            forum.current_post.comments.append(new_comment)
            comment_window.destroy()
            # Refresh display of comments
            forum.refresh_comments()
        else:
            Utils.error_message("Comment cannot be empty!")


    def add_reply(self,forum):
        """
        Pops up a window allowing the user to reply to a comment.
        Clicking on the 'Submit' button triggers self.submit_reply()
        """
        # Create a Toplevel window for editing comments
        reply_window = tk.Toplevel()
        reply_window.title("Reply")  # Set the title of the window
        reply_window.geometry("400x200")  # Set a default size for the window
        reply_window.grab_set()
        # Create a frame with thicker borders
        reply_frame = tk.Frame(reply_window, bd=2, relief=tk.RAISED)  # Change bd and relief as needed
        reply_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create a Text widget with a limited height
        reply_text_widget = tk.Text(reply_frame, width=50, height=5)  # Set height here
        reply_text_widget.pack(side=tk.LEFT, fill='both', expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(reply_frame, command=reply_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        reply_text_widget.config(yscrollcommand=scrollbar.set)

        anonymous_var = tk.IntVar()
        anonymous_check = tk.Checkbutton(reply_window, text="Anonymous", variable=anonymous_var)
        anonymous_check.pack(anchor='w', padx=10, pady=5)  # Align to the left

        # Create a frame for buttons (submit and cancel)
        button_frame = tk.Frame(reply_window)
        button_frame.pack(pady=5)

        # Add a button to submit the reply
        submit_button = HoverButton(button_frame, text="Submit", 
                                    command=lambda: self.submit_reply(reply_window, reply_text_widget, forum, anonymous_var))
        submit_button.pack(side=tk.LEFT, padx=5)

        # Add a button to cancel the reply action
        cancel_button = HoverButton(button_frame, text="Cancel", command=reply_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def submit_reply(self, reply_window, reply_text_widget,forum, anonymous_var):
        """
        Submits the reply by adding it to the comment's replies, and refreshes the comments section
        Displays error popup if reply is empty
        """
        reply_text = reply_text_widget.get("1.0", tk.END).strip()
        if reply_text != "":
            reply_timestamp = Utils.get_current_timestamp()  # Get current timestamp
            new_reply = Comment(user=forum.user, message=reply_text_widget.get("1.0", tk.END).strip(), timestamp=reply_timestamp,parent=self,edited=False,anonymous=bool(anonymous_var.get()))  
            self.replies.append(new_reply)
            reply_window.destroy()
            # Refresh display of comments
            forum.refresh_comments()
        else:
            Utils.error_message("Reply cannot be empty!")

if __name__ == "__main__":
    pass


