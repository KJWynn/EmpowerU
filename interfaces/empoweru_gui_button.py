"""
FIT1056 2024 Semester 2
MA_TUE_GroupN
EmpowerU

This file contains the class definition for the HoverButton class. It inherits from tk.Button, 
and its background colour will change when the user hovers the cursor over it.
"""

import tkinter as tk

class HoverButton(tk.Button):
    def __init__(self, master=None, outline=True, fixed=False,**kwargs):
        """
        outline: bool - if False, the button will not have an outline
        fixed: bool - if True, the button will be set to a fixed gray colour (no changes when cursor hovers in/out of the button)
        """
        tk.Button.__init__(self, master, **kwargs)
        self.fixed = fixed
        if fixed:
            self.config(bg='gray')
            self.original_bg = 'gray'
            self.on_enter_colour = 'gray'
        else:
            self.original_bg = self["bg"] # Store default background color
            self.on_enter_colour = 'lightgrey' # colour when cursor hovers over button

        # Apply the outline argument
        if not outline:
            self.config(bd=0, highlightthickness=0)  # Remove border and outline
        # Bind events for hover effect
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        """Apply effects when mouse enters."""
        if self.cget("state") != "disabled":
            self.config(bg=self.on_enter_colour)  
        if self.fixed: # make the foreground text white to show contrast against gray background
            self.config(fg="white") 

    def on_leave(self, event):
        """Revert the background color when mouse leaves."""
        self.config(bg=self.original_bg)
        if self.fixed: # revert the foreground text back to black
            self.config(fg="black")
