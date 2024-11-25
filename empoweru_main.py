"""
FIT1056 2024 Semester 2
Programming Concepts Task 4

This file contains the function definition to run the GUI application.
"""

# Third party imports
import tkinter as tk

# Local application imports
from interfaces.empoweru_gui_main_window import EmpowerU

def main():
    """
    The main function definition.

    Parameters:
    (None)

    Returns:
    (None)
    """
    root = EmpowerU(title="EmpowerU", width=1100, height=750)
    
    root.mainloop()
    print("EmpowerU proper shutdown completed.")


if __name__ == "__main__":
    # DO NOT MODIFY
    main()
