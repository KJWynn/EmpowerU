# Third party imports
import pytest

# Local application imports
from interfaces.unit.empoweru_gui_unit_homepage import UnitPage
from interfaces.unit.empoweru_gui_modules import LearningPage
from interfaces.empoweru_gui_main_window import EmpowerU
from interfaces.main_menu.empoweru_gui_learner_menu import LearnerMenu
from app.empoweru_app_learner import LearnerUser


def test_launch_video():
    """
    Test all scenarios of the launch_video() function:
    - Successful video launch
    - Module does not exist in mapping of modules to video urls (KeyError)
    - No video URL associated with the module (VideoNotFoundError)

    NOTE: When running this test case, a video will probably be launched in your browser
    """
    root = EmpowerU(title="EmpowerU", width=1100, height=750,test=True)
    learner = LearnerUser("14","l01", "Jane", "Doe", "l01@gmail.com", "janel01", "j@ned0e")
    learner_menu = LearnerMenu(root,learner)
    unit_page = UnitPage(root, learner_menu, learner)
    module_names = ["Overview","Introduction to Python", "Variables, statements and expressions","Functions" ]
    python_learning_page = LearningPage(root, unit_page, learner, "Python Programming", "PP", module_names)
    
    # test with valid case
    python_learning_page.current_module = "pp1" # this maps to "https://www.youtube.com/watch?v=fWjsdhR3z3c", a valid URL
    assert python_learning_page.launch_video() # simulate launching the video, should be successful

    # test with invalid case - KeyError because module does not exist
    python_learning_page.current_module = "pp4" # this module does not exist
    assert not python_learning_page.launch_video()

    # test with invalid case - VideoNotFoundError because URL is invalid
    python_learning_page.current_module = "pp1"
    # Simulate a module that does not have an associated video by change mapping of "pp1" to empty string
    LearningPage.MODULE_VIDEO_URL_MAPPING["pp1"] = ""
    assert not python_learning_page.launch_video()

