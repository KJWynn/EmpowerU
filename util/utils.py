from datetime import datetime
import tkinter as tk
class Utils:
    @staticmethod
    def parse_timestamp(time_str):
        # Split the string into date and time components
        date_part = time_str[:8]  # '20240310' (yyyymmdd)
        time_part = time_str[8:]  # '100900' (hhmmss)
        
        # Convert the date and time components into a datetime object
        timestamp = datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
        
        # Format the datetime object as a timestamp string (dd/mm/yyyy HH:MM:SS)
        timestamp_string = timestamp.strftime("%d/%m/%Y %H:%M:%S")
        
        return timestamp_string
    @staticmethod
    def reverse_parse_timestamp(formatted_str):
        # Parse the formatted string (dd/mm/yyyy HH:MM:SS) into a datetime object
        timestamp = datetime.strptime(formatted_str, "%d/%m/%Y %H:%M:%S")
        
        # Convert the datetime object back into the original format (yyyymmddhhmmss)
        original_format = timestamp.strftime("%Y%m%d%H%M%S")
        
        return original_format    
    @staticmethod
    def get_current_timestamp():
        """
        Returns the current timestamp formatted as YYYYMMDDHHMMSS.
        """
        return datetime.now().strftime('%Y%m%d%H%M%S')
    
    @staticmethod
    def error_message(msg):
        # Create a Toplevel window for editing comments
        error_window = tk.Toplevel()
        error_window.title("Error")  # Set the title of the window
        error_window.geometry("400x200")  # Set a default size for the window
        # Make the window modal
        error_window.grab_set()
        # Create a frame with thicker borders
        error_frame = tk.Frame(error_window, bd=2, relief=tk.RAISED)  # Change bd and relief as needed
        error_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Create a Text widget with a limited height
        text_widget = tk.Text(error_frame, width=50, height=5)  # Set height here
        text_widget.insert(tk.END, msg)
        text_widget.pack(side=tk.LEFT, fill='both', expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(error_frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the Text widget to use the scrollbar
        text_widget.config(yscrollcommand=scrollbar.set)

        # Add a button to save changes
        ok_button = tk.Button(error_window, text="Ok", command=error_window.destroy)
        ok_button.pack(pady=5)
        ok_button.focus_set()

    @staticmethod
    def success_message(message):
        # Create a Toplevel window for showing the success message
        message_window = tk.Toplevel()
        message_window.title("Success")  # Set the title of the window
        message_window.geometry("400x150")  # Adjust window size to fit content
        message_window.grab_set()

        # Create a frame to hold the text and the button
        frame = tk.Frame(message_window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Add a Text widget to show the message
        message_label = tk.Text(frame, height=5, wrap=tk.WORD)  # Set height to ensure full message visibility
        message_label.insert(tk.END, message)
        message_label.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Disable the text widget to make it non-editable
        message_label.config(state=tk.DISABLED)

        # Add a button to close the window
        ok_button = tk.Button(frame, text="Ok", command=message_window.destroy)
        ok_button.pack(pady=10)

        # Make the window non-resizable for a cleaner look
        message_window.resizable(False, False)

    @staticmethod
    def get_duration(post_timestamp):
        # Parse the post timestamp string into a datetime object
        post_time = datetime.strptime(post_timestamp, "%d/%m/%Y %H:%M:%S")
        
        # Get the current time
        now = datetime.now()
        
        # Calculate the time difference
        time_diff = now - post_time
        
        # Get the difference in total seconds
        seconds = time_diff.total_seconds()
        
        # Determine the appropriate unit for the time difference
        if seconds < 60:
            return f"{int(seconds)} second{'s' if seconds >1 else ''} ago"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{int(minutes)} minute{'s' if int(minutes) >1 else ''} ago"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{int(hours)} hour{'s' if int(hours) >1 else ''} ago"
        elif seconds < 604800:
            days = seconds / 86400
            return f"{int(days)} day{'s' if int(days) >1 else ''} ago"
        elif seconds < 2628000:  # ~30 days in seconds
            weeks = seconds / 604800
            return f"{int(weeks)} week{'s' if int(weeks) >1 else ''} ago"
        elif seconds < 31536000:  # ~1 year in seconds
            months = seconds / 2628000
            return f"{int(months)} month{'s' if int(months) >1 else ''} ago"
        else:
            years = seconds / 31536000
            return f"{int(years)} year{'s' if int(years) >1 else ''} ago"
        

class VideoNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"Failed to open the video in browser. The video may not exist for this module")
