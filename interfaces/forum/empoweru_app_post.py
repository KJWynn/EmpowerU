"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the Post class.
"""

# Standard library imports
import re
import tkinter as tk
from tkinter import ttk
# Local application imports
from interfaces.forum.empoweru_app_comment import Comment
from interfaces.empoweru_gui_button import HoverButton
from util.utils import Utils

class Post():
    def __init__(self, user, title, timestamp, message, comments, anonymous, topic_tag,edited):
        """
        Constructor for the Post class
        user: string representation of currently logged in User instance with format "{full name} (role)" 
        title: string - title of the post
        timestamp: string - time the post was made with format dd:mm:yyyy hh:mm:ss
        message: string - the post content
        comments: Comment[] - the list of comment instances. these should be top level comments
        anonymous: bool - whether the poster posted anonymously
        topic_tag: string - the topic of this post
        views: int - number of views this post has
        edited: bool - whether this post was edited by the poster
        """
        self.user = user
        self.title = title
        self.timestamp = timestamp
        self.message = message
        self.comments = comments
        self.anonymous = anonymous
        self.topic_tag = topic_tag
        self.views = 0
        self.edited = edited

    @staticmethod
    def parse_forum_post(file_path):
        """
        Parses the forum post file.

        Parameters:
        - file_path: str : path to the forum post file

        Returns:
        - poster: str: the poster
        - title: str : the title of the post
        - message: str : the message content
        - comments: list : a list of comments
        - anonymous: boolean: whether the post is set to anonymous
        - tag: str: the tag associated witht the post (General, Python, AI, IS)
        - edited: boolean: whether the post has been edited
        """
        poster = title = message  = "Null"
        comments = []
        anonymous = False
        tag = "General"
        edited = False
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                poster_match = re.search(r'^Poster:(.*)$', content, re.MULTILINE)
            poster_raw = poster_match.group(1).strip()
            poster_components = poster_raw.split("-")
            poster = poster_components[0].strip() # the poster's string representation
            # two characters separated by a comma represent booleans for anonymous and edited
            anonymous = poster_components[1].split(",")[0].strip() == "Y" 
            edited = poster_components[1].split(",")[1].strip() == "Y"

            # Extract Title
            title_match = re.search(r'^Title:(.*)$', content, re.MULTILINE)
            title = title_match.group(1).strip() 

            # Extract Message (from "Message:" until "Tag:")
            message_match = re.search(r'Message:\s*(.*)\s*Tag:', content, re.DOTALL)
            message = message_match.group(1).strip() 

            tag_match = re.search(r'Tag:\s*(.*)\s*Comments:', content, re.DOTALL)
            tag = tag_match.group(1).strip() 
            # Extract Comments (split by special delimiter)
            comments_section = re.search(r'Comments:(.*)', content, re.DOTALL)
            comments_raw = comments_section.group(1).strip() 

            comments = Comment.parse_comment_string(comments_raw)
        except FileNotFoundError as e:
            print(e)
        finally:
            return poster, title, message, comments, anonymous,tag,edited 

    @staticmethod
    def create_post(forum):
        """
        Pops up a window to post (optional to post anonymously). 
        Clicking on the 'Post' button triggers submit_post()
        """
        # Create a Toplevel window for creating a new post
        new_post_window = tk.Toplevel()
        new_post_window.title("Create Post")  # Set the title of the window
        new_post_window.geometry("600x350")  # Set a default size for the window
        new_post_window.grab_set()

        # Create a frame with thicker borders
        new_post_frame = tk.Frame(new_post_window, bd=2, relief=tk.RAISED)
        new_post_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create a Label and Entry widget for the title, aligned side by side
        title_label = tk.Label(new_post_frame, text="Post Title:")
        title_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 5), sticky="w")  # Align to left

        title_entry = tk.Entry(new_post_frame, width=40)
        title_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="w")  # Right of the label

        # Create a Checkbutton for "Anonymous" option
        anonymous_var = tk.IntVar()
        anonymous_check = tk.Checkbutton(new_post_frame, text="Anonymous", variable=anonymous_var)
        anonymous_check.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")  # Align to the left

        # Create a Combobox for topic selection, right of the checkbox
        forum.topic_var = tk.StringVar()
        forum.topic_var.set("<Select a topic>")  # default value
        topic_combobox = ttk.Combobox(new_post_frame, textvariable=forum.topic_var, state="readonly")
        topic_combobox['values'] = ("General","Python", "Artificial Intelligence", "Information Security")
        topic_combobox.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="w")

        # Create a Text widget for post content, below the checkbox and dropdown
        text_widget = tk.Text(new_post_frame, width=50, height=10)
        text_widget.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")
        # Create a scrollbar for the Text widget
        scrollbar = tk.Scrollbar(new_post_frame, command=text_widget.yview)
        scrollbar.grid(row=2, column=2, sticky="ns", pady=(5, 10))

        text_widget.config(yscrollcommand=scrollbar.set)

        # Create a frame for buttons
        button_frame = tk.Frame(new_post_window)
        button_frame.pack(pady=5)
        # Add a button to save the new post and cancel button
        post_button = HoverButton(button_frame, text="Post", command=lambda: Post.submit_post(new_post_window, title_entry.get(), text_widget.get("1.0", tk.END).strip(), anonymous_var.get(),forum.topic_var.get(),forum))
        post_button.pack(side=tk.LEFT, padx=5)
        cancel_button = HoverButton(button_frame, text="Cancel", command=new_post_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Configure the grid layout for the new_post_frame
        new_post_frame.grid_columnconfigure(0, weight=1)
        new_post_frame.grid_columnconfigure(1, weight=1)
        new_post_frame.grid_rowconfigure(2, weight=1)

    @staticmethod
    def submit_post(new_post_window, title, text, anonymous_var,topic,forum):
        """
        Displays the post if all fields entered correctly
        Displays error popup if 
        (i) any required fields are empty
        (ii) title exceeds 50 character limit
        Returns message indicating any errors or success
        """
        message = ""
        if text == "":
            message = "Post cannot be empty!"
            Utils.error_message("Post cannot be empty!")
        elif title == "":
            message = "Title cannot be empty!"
            Utils.error_message("Title cannot be empty!")
        elif len(title)>50:
            message = "Title is too long!"
            Utils.error_message("Title is too long!")
        elif topic == "<Select a topic>":
            message = "Please choose a topic tag for the post!"
            Utils.error_message("Please choose a topic tag for the post!")
        else:
            new_post = Post(forum.user, title, Utils.parse_timestamp(Utils.get_current_timestamp()), text, [], bool(anonymous_var), forum.topic_var.get(), False)
            forum.posts.append(new_post) 
            item = f"({new_post.topic_tag}) {new_post.title} - {new_post.user} - {new_post.timestamp}"
            # update these tracked variables in the forum instance
            forum.post_listbox.insert(0, item)
            forum.listbox_posts.append((item, 0)) 
            forum.all_listbox_posts.append((item,0))
            forum.post_mapping[item]=new_post
            forum.topic_combobox.set("All")
            forum.current_post = new_post # update 
            forum.update_post_list()
            # hide the popup window and display this post in the forum
            new_post_window.destroy() 
            forum.new_post_created = True
            forum.display_post()
            forum.new_post_created = False
            message = f"Successfully posted to {new_post.topic_tag}!"
            Utils.success_message(f"Successfully posted to {new_post.topic_tag}!")
        return message

    def edit_post(self, post_content, forum):
        """
        Pops up a window allowing the user to edit a post (if they are the post owner).
        Clicking on the 'Save' button triggers self.save_post()
        """
        # Create a Toplevel window for editing comments
        edit_post_window = tk.Toplevel()
        edit_post_window.title("Edit post")  
        edit_post_window.geometry("600x350")  
        edit_post_window.grab_set()
        # Create a frame with thicker borders
        edit_post_frame = tk.Frame(edit_post_window, bd=2, relief=tk.RAISED) 
        edit_post_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create a Text widget with a limited height
        text_widget = tk.Text(edit_post_frame, width=50, height=5) 
        # if post is edited, copy all the contents after the 8 character header "[Edited]" 
        if self.edited:
            original_content = post_content.get("1.0", tk.END).strip()[9:]
        else:
            original_content = post_content.get("1.0", tk.END).strip()
        text_widget.insert(tk.END, original_content)
        text_widget.pack(side=tk.LEFT, fill='both', expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(edit_post_frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        text_widget.config(yscrollcommand=scrollbar.set)

        # Create a frame for buttons
        button_frame = tk.Frame(edit_post_window)
        button_frame.pack(pady=5)

        # Add a button to save the new post and a cancel button
        save_button = HoverButton(button_frame, text="Save", command=lambda: self.save_post(forum, edit_post_window, text_widget))
        save_button.pack(side=tk.LEFT, padx=5)
        cancel_button = HoverButton(button_frame, text="Cancel", command=edit_post_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def save_post(self, forum, edit_post_window, text_widget):
        """Updates post content if text is not empty, displays error popup otherwise."""
        text = text_widget.get("1.0", tk.END).strip()
        if text != "":
            # update post content
            forum.current_post.message = "[Edited]\n"+text
            edit_post_window.destroy() # remove the edit post window
            forum.edited_post = True
            forum.display_post()
            forum.edited_post = False
            self.edited = True
        else:
            Utils.error_message("Post cannot be empty!")


if __name__ == "__main__":
    pass
