"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the Forum class.
"""

# Third party imports
import tkinter as tk
from tkinter import ttk
import os

# Local application imports
from app.empoweru_app_teacher import TeacherUser
from util.utils import Utils
from app.empoweru_app_admin import AdminUser
from interfaces.forum.empoweru_app_comment import Comment
from interfaces.forum.empoweru_app_post import Post
from interfaces.empoweru_gui_button import HoverButton

class Forum(tk.Frame):
    def __init__(self, master, user_menu, user, posts):
        """
        master: master widget (should be tk.TK EmpowerU instance)
        user_menu: UserMenu instance, i.e. the previous menu
        user: User instance
        posts: list of Post instances
        current_post: Currently displayed Post instance
        new_post_created: bool - whether a new post was created
        edited_post: bool - whether a post was edited
        listbox_posts: Tracks the list box items that should be displayed in the GUI (list of forum posts for user to select)
                       The items are tuples, i.e. (post_description, index), where 
                       (i) post_description is the text to be displayed in the GUI ListBox
                       (ii) index is the index of the item within the ListBox
        all_listbox_posts: tracks all posts posted to forum so far
        self.post_mapping: maps a post_description to a Post instance
        """
        super().__init__(master)
        self.master = master
        self.user_menu = user_menu
        self.user = user
        self.posts = posts 
        self.current_post = None
        self.new_post_created = False
        self.edited_post = False
        self.listbox_posts = [] 
        self.all_listbox_posts = []
        self.post_mapping = {}

        # Set up the grid layout
        self.grid(row=0, column=0, sticky='nsew')
        
        # Configure the main frame's column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3,weight=1)

        # Add Main Menu button at the very top
        self.main_menu_button = HoverButton(self, text="Return", command=self.return_to_menu)
        self.main_menu_button.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # Add title "EmpowerU Forum"
        self.forum_label = tk.Label(self, text="EmpowerU Forum", font=("Arial", 14, "bold"))
        self.forum_label.grid(row=0, column=1, sticky='w', padx=10, pady=10)

        # Add private chat option 
        self.private_chat_button = HoverButton(self, text="Private chat", command=self.private_chat)
        self.private_chat_button.grid(row = 0, column=2,sticky='e', padx=2, pady=10)
        if self.user.role == "Teacher": self.private_chat_button.config(state="disabled") # option only for learners

        # Add make post button at the very top
        self.make_post_button = HoverButton(self, text="Create post", command=lambda:Post.create_post(self))
        self.make_post_button.grid(row=0, column=3, sticky='e', padx=10, pady=10)

        # Create a new frame for category buttons
        self.category_frame = tk.Frame(self)
        self.category_frame.grid(row=1, column=0, sticky='nw', padx=10, pady=10)

        # Add "Topic" label
        self.category_label = tk.Label(self.category_frame, text="Topic:", font=("Arial", 9, "bold"))
        # self.category_label.pack(side=tk.LEFT)  # Reduced right padding for closer positioning
        self.category_label.grid(row=0, column=0)  # Reduced right padding for closer positioning

        # Add the sort dropdown box
        self.topic_combobox = ttk.Combobox(self.category_frame, values=["All","General", "Python", "Artificial Intelligence", "Information Security"], state="readonly")
        self.topic_combobox.grid(row=0, column=1)  # Adjust padding as needed
        self.topic_combobox.bind("<<ComboboxSelected>>", self.update_post_list)
        self.topic_combobox.current(0)  # Set default value to "Topic"

        # Add "Sort" label
        self.sort_label = tk.Label(self.category_frame, text="Sort by:", font=("Arial", 9, "bold"))
        self.sort_label.grid(row=1,column=0,pady=10)  # Reduced right padding for closer positioning
        # Add the sort dropdown box
        self.sort_combobox = ttk.Combobox(self.category_frame, values=["Most recent first", "Most viewed first"], state="readonly")
        self.sort_combobox.grid(row=1,column=1,pady=10)  # Adjust padding as needed
        self.sort_combobox.bind("<<ComboboxSelected>>", self.update_post_list)
        self.sort_combobox.current(0)  # Set default value to "Topic"

        # Create a PanedWindow that allows horizontal resizing
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=1, column=1, columnspan=3, sticky='nsew')

        # Left panel: List of posts (scrollable)
        self.left_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, weight=1)  # Allow left frame to resize

        # Create a Listbox
        self.post_listbox = tk.Listbox(self.left_frame, height=30)
        self.post_listbox.grid(row=0, column=0, sticky='nsew')  # Ensure it fills the frame
        self.post_listbox.bind('<<ListboxSelect>>', self.display_post)

        # Create a Scrollbar
        scrollbar = tk.Scrollbar(self.left_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')  # Place scrollbar in column 1

        # Link the scrollbar to the listbox
        self.post_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.post_listbox.yview)

        # Configure the grid weights to allow the Listbox to expand
        self.left_frame.grid_columnconfigure(0, weight=1)  # Column 0 for Listbox
        self.left_frame.grid_columnconfigure(1, weight=0)  # Column 1 for Scrollbar
        self.left_frame.grid_rowconfigure(0, weight=1)     # Row 0 for Listbox

        # Populate the listbox with post_description in reverse order because we display most recent posts first, by default
        for i, post in enumerate(reversed(posts)):
            # if the post is anonymous, only the owner can see the details of the poster; others see the poster as "Anonymous"
            if post.anonymous and str(self.user)!= str(post.user): 
                role = post.user.split("(")[1][:-1].strip()
                item = f"({post.topic_tag}) {post.title} - Anonymous ({role}) - {post.timestamp}"
            else:
                item = f"({post.topic_tag}) {post.title} - {post.user} - {post.timestamp}"
            self.post_listbox.insert(i, item)
            self.listbox_posts.append((item, i))
            self.all_listbox_posts.append((item,i))
            self.post_mapping[item]=post


        # Configure row and column weights for left frame
        self.left_frame.grid_rowconfigure(0, weight=1)  # Allow the row to expand
        self.left_frame.grid_columnconfigure(0, weight=1)  # Allow the column to expand

        # Right panel: Post content
        self.right_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, weight=3)  # Allow right frame to resize

        # Configure right frame's grid
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)  # Allow the column to expand

        # User information (name, role, timestamp)
        self.user_info_frame = tk.LabelFrame(self.right_frame)
        self.user_info_frame.grid(row=0, column=0, sticky='nsew')
        # add extra space in between
        self.user_info_label = tk.Label(self.user_info_frame, text="")
        self.user_info_label.grid(row=0, column=0, padx=5, pady=5)

        # Post content
        self.post_content = tk.Text(self.right_frame, wrap="word", height=20)
        self.post_content.grid(row=1, column=0, sticky='nsew')

        # initially no posts are selected
        self.current_post = None

        # Create a new frame for the comments label and button
        self.comments_control_frame = tk.Frame(self.right_frame)
        self.comments_control_frame.grid(row=2, column=0, sticky='ew', pady=2)

        # Add "Comments" label
        comments_label = tk.Label(self.comments_control_frame, text="Comments", font=("Arial", 10, "bold"))
        comments_label.pack(side=tk.LEFT, padx=10)

        # Add "Edit Post" button
        self.edit_post_button = HoverButton(self.comments_control_frame, text="Edit Post", command=lambda: self.current_post.edit_post(self.post_content, self))
        self.edit_post_button.config(state='disabled')
        self.edit_post_button.pack(side=tk.RIGHT, padx=10)

        # Add "Add Comment" button
        self.add_comment_button = HoverButton(self.comments_control_frame, text="Comment", command=lambda: Comment.add_comment(self))
        self.add_comment_button.config(state='disabled')
        self.add_comment_button.pack(side=tk.RIGHT, padx=10)

        # Comments section (scrollable)
        self.comments_frame = tk.Frame(self.right_frame)
        self.comments_frame.grid(row=3, column=0, sticky='nsew')

        self.comments_canvas = tk.Canvas(self.comments_frame)
        self.scrollbar = tk.Scrollbar(self.comments_frame, orient="vertical", command=self.comments_canvas.yview)
        self.comments_scrollable_frame = tk.Frame(self.comments_canvas)
        self.comments_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.comments_canvas.configure(
                scrollregion=self.comments_canvas.bbox("all")
            )
        )
        self.comments_canvas.create_window((0, 0), window=self.comments_scrollable_frame, anchor="nw")
        self.comments_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Add the canvas and scrollbar to the comments frame
        self.comments_canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # Configure weights for comments_frame
        self.comments_frame.grid_rowconfigure(0, weight=1)
        self.comments_frame.grid_columnconfigure(0, weight=1)
        # Bind mouse wheel scrolling to the canvas (only when the mouse is over the canvas)
        self.comments_canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.comments_canvas.bind("<Leave>", self._unbind_from_mousewheel)
        # By default, display the latest post
        if posts:
            self.display_post()

    def private_chat(self):
        """
        Pops up a window to start a private chat with a teacher
        A teacher has to be chosen from a dropdown
        Once a topic is chosen, the dropdown is populated with teachers who teach the course
        Triggers self.submit_chat() for validation 
        """
        # Create a Toplevel window for creating a new post
        new_chat_window = tk.Toplevel()
        new_chat_window.title("Private chat")  # Set the title of the window
        new_chat_window.geometry("600x350")  # Set a default size for the window
        new_chat_window.grab_set()

        # Create a frame with thicker borders
        new_chat_frame = tk.Frame(new_chat_window, bd=2, relief=tk.RAISED)
        new_chat_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create a Label and Entry widget for the title, aligned side by side
        title_label = tk.Label(new_chat_frame, text="Chat topic:")
        title_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 5), sticky="w")  # Align to left

        title_entry = tk.Entry(new_chat_frame, width=40)
        title_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="w")  # Right of the label

        # course selection
        topic_label = tk.Label(new_chat_frame, text="Select course:")
        topic_label.grid(row=1,column=0, padx=(5, 10), pady=5, sticky="w")

        # Create a Combobox for topic selection
        self.private_chat_course_var = tk.StringVar()
        self.private_chat_course_var.set("<Select a course>")  # default value
        self.private_course_combobox = ttk.Combobox(new_chat_frame, textvariable=self.private_chat_course_var, state="readonly")
        self.private_course_combobox['values'] = ("Python Programming", "Information Security", "Artificial Intelligence")
        self.private_course_combobox.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="w")

        # Bind the selection event to the topic combobox
        self.private_course_combobox.bind("<<ComboboxSelected>>", self.update_teachers)

        # Label for teacher selection
        teacher_label = tk.Label(new_chat_frame, text="Teacher:")
        teacher_label.grid(row=2,column=0, padx=(5, 10), pady=5, sticky="w")

        # Create a Combobox for teacher selection
        self.teacher_var = tk.StringVar()
        self.teacher_var.set("<Select a teacher>")  # default value
        self.teachers_combobox = ttk.Combobox(new_chat_frame, textvariable=self.teacher_var, state="readonly")
        self.teachers_combobox.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="w")

        # Create a Text widget for chat content, below the checkbox and dropdown
        text_widget = tk.Text(new_chat_frame, width=50, height=10)
        text_widget.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")
        # Create a scrollbar for the Text widget
        scrollbar = tk.Scrollbar(new_chat_frame, command=text_widget.yview)
        scrollbar.grid(row=3, column=2, sticky="ns", pady=(5, 10))

        text_widget.config(yscrollcommand=scrollbar.set)

        # Create a frame for buttons
        button_frame = tk.Frame(new_chat_window)
        button_frame.pack(pady=5)

        # Add a button to save the new post
        post_button = HoverButton(button_frame, text="Submit", command=lambda:self.submit_chat(new_chat_window,title_entry.get(),text_widget.get("1.0", tk.END).strip()))
        post_button.pack(side=tk.LEFT, padx=5)

        # Add a cancel button
        cancel_button = HoverButton(button_frame, text="Cancel", command=new_chat_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Configure the grid layout for the new_post_frame
        new_chat_frame.grid_columnconfigure(0, weight=1)
        new_chat_frame.grid_columnconfigure(1, weight=1)
        new_chat_frame.grid_rowconfigure(2, weight=1)


    def update_teachers(self, event):
        """
        Function to update the teacher combobox with available teachers based on the selected topic.
        Uses TeacherUser's static method to find teachers who teach the course
        """
        # Get the selected topic from the combobox
        selected_topic = self.private_chat_course_var.get()
        # Fetch teachers based on the selected topic
        teachers = tuple(TeacherUser.find_teachers_by_course(selected_topic))
        # Update the teacher combobox with the new values
        self.teachers_combobox['values'] = teachers
        # Reset the selection to the default value
        if teachers:
            self.teachers_combobox.set("<Select a teacher>")
        else:
            self.teachers_combobox.set("<No teachers available>")

    def submit_chat(self,new_chat_window,title,text):
        """
        Starts private chat if entries are not empty (including valid teacher) and title does not exceed 50 character limit.
        Returns True if the chat was sent successfully.
        """
        success = False
        if text == "":
            Utils.error_message("Chat cannot be empty!")
        elif title == "":
            Utils.error_message("Title cannot be empty!")
        elif len(title)>50:
            Utils.error_message("Title is too long!")
        elif self.teacher_var.get() == "<Select a teacher>":
            Utils.error_message("Please choose a teacher!")
        elif self.teacher_var.get() == "<No teachers available>":
            Utils.error_message("No teacher teachers this course, please contact the admin through feedback in the Settings page")
        else:
            success = True
            new_chat_window.destroy()
            Utils.success_message(f"Private chat with teacher {self.teacher_var.get()} started")    
        return success

    @staticmethod
    def show_forum(parent):
        """
        Method to show the public forum. Returns the forum
        parent: UserMenu instance
        """

        # find all the forum posts in the data/forum directory
        forum_directory = "./data/forum"
        posts = []
        # iterate over all files in the forum directory
        for filename in os.listdir(forum_directory):
            # get full path to the file
            file_path = os.path.join(forum_directory, filename)
            # get metadata from filename
            timestamp_comp=filename[:len(filename)-4].split('.')[0]
            timestamp_str = Utils.parse_timestamp(timestamp_comp)

            # parse the file to obtain title, content and comments from the post
            poster, title, content, comments, anonymous, tag,edited = Post.parse_forum_post(file_path)
            newPost = Post(poster, title,timestamp_str, content, comments, anonymous, tag,edited)
            posts.append(newPost)


        forum = Forum(parent.master, parent, parent.user, posts)
        forum.place(relx=.5, rely=.5, anchor=tk.CENTER)
        parent.hide_menu()
        return forum

    def _bind_to_mousewheel(self, event):
        """Bind mouse wheel scrolling when mouse enters the canvas."""
        self.comments_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _unbind_from_mousewheel(self, event):
        """Unbind mouse wheel scrolling when mouse leaves the canvas."""
        self.comments_canvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event):
        """Enable scrolling via the mouse wheel when cursor is over the canvas."""
        self.comments_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def update_post_list(self,event=None):
        """Update the list of posts in the ListBox depending on the sort criterion and filter options"""
        selected_topic = self.topic_combobox.get()
        sort_criterion = self.sort_combobox.get()
        # insert all (filter first)
        self.post_listbox.delete(0, tk.END) # clear previous
        # sort the list box
        if sort_criterion == "Most viewed first":
            self.all_listbox_posts.sort(key=lambda tuple:self.post_mapping[tuple[0]].views,reverse=True) # e.g. [(postdescr, 6), (post2, 5),...]
        elif sort_criterion == "Most recent first":
            self.all_listbox_posts.sort(key=lambda tuple:int(Utils.reverse_parse_timestamp(self.post_mapping[tuple[0]].timestamp)), reverse=True)
        self.listbox_posts = self.all_listbox_posts.copy()
        # insert into listbox
        for i in range(len(self.all_listbox_posts)):
            self.post_listbox.insert(i, self.all_listbox_posts[i][0])
        # delete irrelevant posts from the list box as part of filtering process
        if selected_topic != "All":
            for i in range(self.post_listbox.size() - 1, -1, -1):  # Iterate backwards to avoid index shifting
                item = self.post_listbox.get(i)
                if item.split(")", 1)[0][1:] != selected_topic:
                    self.post_listbox.delete(i)
                    self.listbox_posts.remove(self.listbox_posts[i])

    def display_post(self, event=None):
        """Display the content of the selected post on the right side."""
        # Get selected post from the Listbox
        selection = self.post_listbox.curselection()
        if selection or self.new_post_created or self.edited_post:
            self.add_comment_button.config(state='active')
            if selection:
                post = self.post_mapping[self.listbox_posts[selection[0]][0]]
            else: # display the first one in the post_listbox
                post = self.current_post

            if self.current_post!=post: # if a new post is clicked , increment the post count
                post.views+=1
            self.current_post = post
            # Clear the existing user info frame contents
            for widget in self.user_info_frame.winfo_children():
                widget.destroy()

            # Add post info
            # Title
            title_label = tk.Label(self.user_info_frame, text=f"{post.title.strip()}" , font=("Arial", 12, "bold"))
            title_label.grid(row=0, column=0, sticky='w', padx=5, pady=2)

            # views
            view_label = tk.Label(self.user_info_frame, text=f"Viewed: {post.views}",font=("Arial", 10, "italic"))
            view_label.grid(row=0, column=1, sticky="w",padx=5, pady=2)
            # post topic tag
            topic_label = tk.Label(self.user_info_frame, text=f"{Utils.get_duration(post.timestamp)} in {post.topic_tag}" , font=("Arial", 10, "italic"))
            topic_label.grid(row=1, column=0, sticky='w', padx=5)   

            # User label with left alignment
            post_owner = str(post.user)
            if (post.anonymous and str(self.user)!=post_owner): # anonymous option
                role = post_owner.split("(")[1][:-1]
                post_owner = f"Anonymous ({role})"
            elif (post.anonymous and str(self.user)==post_owner):
                post_owner = str(post_owner) + " [Private]"

            user_label = tk.Label(self.user_info_frame, text=f"{post_owner}", font=("Arial", 10))
            user_label.grid(row=2, column=0, sticky='w', padx=5, pady=2)

            # Timestamp label
            timestamp_label = tk.Label(self.user_info_frame, text=f"{post.timestamp}", font=("Arial", 10, "italic"))
            timestamp_label.grid(row=2, column=1, sticky='e', padx=5, pady=2)

            # Set weight for the columns to control expansion
            self.user_info_frame.grid_columnconfigure(0, weight=1)  # Left column (user label) can expand
            self.user_info_frame.grid_columnconfigure(1, weight=0)  # Right column (timestamp) does not expand

            # Display post content
            self.post_content.config(state="normal")
            self.post_content.delete(1.0, tk.END)
            if self.current_post.edited:
                self.post_content.insert(tk.END, f"[Edited]\n{post.message[9:]}")
            else:
                self.post_content.insert(tk.END, post.message)
            self.post_content.config(state="disabled")

            # Clear the existing comments frame contents
            for widget in self.comments_scrollable_frame.winfo_children():
                widget.destroy()

            # Display comments and replies recursively
            for comment in post.comments:
                self.display_comment(comment, self.comments_scrollable_frame)
            if str(self.user) == str(self.current_post.user): # only post owners can edit posts
                self.edit_post_button.config(state='active')
            else:
                self.edit_post_button.config(state='disabled')



    def refresh_comments(self):
        """Clears and redraws all comments to include new replies."""
        # Clear the current display
        for widget in self.comments_scrollable_frame.winfo_children():
            widget.destroy()

        # Re-display all comments
        for comment in self.current_post.comments:
            self.display_comment(comment, self.comments_scrollable_frame)

    def display_comment(self, comment, parent_frame, level=1):
        """Recursively display comments and their replies, indented by level."""
        # Create a container for the comment
        comment.container = tk.Frame(parent_frame, padx=10, pady=5, relief=tk.SUNKEN, bd=1)
        comment.container.pack(fill='x', padx=5 + 20 * (level - 1), pady=5)

        # Display the comment user, timestamp, and message
        comment_owner = comment.user
        if (comment.anonymous and str(self.user)!=str(comment_owner)): # anonymous option
            role = comment.user.split("(")[1][:-1]
            comment_owner = f"Anonymous ({role})"
        elif (comment.anonymous and str(self.user)==str(comment_owner)): # anonymous option
            comment_owner = str(comment_owner) + " [Private]"
        if comment.parent: # if the comment is a reply, add the 'reply from' prefix
            comment_user_label = tk.Label(comment.container, text=f"⤷ Reply from {comment_owner}", font=("Arial", 10, "bold"))
        else:
            comment_user_label = tk.Label(comment.container, text=f"{comment_owner}", font=("Arial", 10, "bold"))
        comment_user_label.pack(anchor='w')

        comment_timestamp_label = tk.Label(comment.container, text=Utils.parse_timestamp(comment.timestamp), font=("Arial", 8, "italic"))
        comment_timestamp_label.pack(anchor='w')
        comment_message_label = tk.Label(comment.container, text=comment.message, wraplength=400, justify='left')
        comment_message_label.pack(anchor='w', pady=2)

        # Add reply button
        if not comment.deleted:
            reply_button = HoverButton(comment.container, text="Reply", command=lambda:comment.add_reply(self))
            reply_button.pack(side=tk.LEFT, anchor='e', pady=5, padx=5)
        if not comment.deleted and str(comment.user) == str(self.user): # only comment owners can edit comment
            # Add edit button
            edit_button = HoverButton(comment.container, text="Edit", command=lambda:comment.edit_comment(comment_message_label))
            edit_button.pack(side=tk.LEFT, anchor='e', padx=5,pady=5)
        if self.can_delete_comment(comment.deleted, self.user, comment.user): # only admins or comment owners can delete comments
            # Add a button to delete comment
            delete_button = HoverButton(comment.container, text="Delete",command=lambda: comment.delete_comment(self))
            delete_button.pack(side=tk.LEFT, anchor='e', padx=5,pady=5)

        # If there are replies, recursively display them
        if comment.replies:
            for reply in comment.replies:
                self.display_comment(reply, parent_frame, level + 1)

    def can_delete_comment(self, is_comment_deleted, logged_in_user, comment_user):
        """Returns True if a comment can be deleted by the current user."""
        return not is_comment_deleted and (isinstance(logged_in_user, AdminUser) or str(logged_in_user)==str(comment_user))

    def return_to_menu(self):
        """
        This method handles the GUI logic to return to the receptionist's menu.

        Parameters:
        (None)

        Returns:
        (None)
        """
        self.place_forget()
        self.user_menu.place(relx=.5, rely=.5, anchor=tk.CENTER)

if __name__ == "__main__":
    # DO NOT MODIFY
    pass

