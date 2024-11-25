# Project: EmpowerU

MA_TUE_Group_N<br>
Members:<br>
Khor Jia Wynn <br>
Jeevana a/p Sivakumar<br>
Chong Yew Sze<br>
Katrin Lee Shin Ern<br>
Lau Shuen Wei<br>

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [Features Implemented](#features-implemented)

## Overview

EmpowerU is a multi-user platform:

1. Learners to access tutorials, modules, and quizzes, track their performance, and participate in discussions via the forum.
2. Teachers to create and manage educational content, quizzes, and track student progress.
3. Admins to oversee system-wide activities and maintain the platform.

The app emphasizes user feedback, collaboration through forums, and adherence to privacy policies.

## Project structure

Root folder (extracted folder): empoweru_group_n

empoweru_main.py is the main python file to be run to launch the application. To login and test the functionalities, use the credentials: <br>
Role: Admin <br>
Username: rochelle <br>
Password: r0che11e

empoweru_group_n/data : Contains data files. The 'database' layer.<br>
empoweru_group_n/images: Contains image for logo of EmpowerU.<br>
empoweru_group_n/interfaces: Contains folders and files for the GUI.<br>
empoweru_group_n/tests: Contains test files.<br>
empoweru_group_n/util: Contains utils file.<br>

To run a test file, run `pytest tests/[filename]` in the terminal from the root folder<br>
Example:
`pytests tests/test_scenario_1.py`

## How to Use

1. Click "Register" button at the homepage, the app will navigate to another small widget to fill in details, make sure that all the inputs are correct

   \*Note that: Password length is between 8 and 20 characters inclusive, need a special character, and must have a uppercase letter

   After every details is being filled in correctly, press submit.
   There will be a widget showing Privacy Policy info. You have to accept it to proceed.
   Then, a message will pop up and inform that your account is created successfully

2. Click "Login" button at the homepage, the app will navigate to the login page. Fill in the details required and press login.
3. Upon successful login, the app will automatically show the user menu page. The page will greet user with their first name, and ask the user to choose on one of the following button. A list of buttons will shown up.
4. Can click on the "EmpowerU Tutorial" to see on how each pages function.

## Features implemented

1. Registration and login

   - The system shall require users to provide their first name, last name, age, username and email address when creating an account on the platform.
   - The system shall require users to give explicit consent from the user regarding the use of data by the system during the account creation process
   - The system shall require users to provide their username and password if they wish to log into their account

2. Interactive tutorials

   - The system shall allow the learners to access modules within the main 3 technological courses where the lesson content can be inputted.
   - The system shall allow the learners to view module related videos in a web browser.
   - The system shall be able to allow the user to view, access and interact with all content questions of the modules in the course

3. Quizzes and challenges

   - The system shall allow educators to include quizzes and challenges at the end of each module with questions
   - The system shall allow the learner to attempt to answer the quizzes at the end of the module of the course when the user is on the course page

4. Progress Tracker

   - While the learner is on the progress tracker page, the system shall allow the learner to be able to view the status of completion of modules, as well as the quiz scores in text format
   - While the learner is on the progress tracker page, the system shall allow the learner to be able to type out their personal goals on the page

5. Feedback and Collaboration

   - While the user is on the forum page, the system shall be able to allow users to make posts and upload comments on the page
   - While the learner is on the forum page, the system shall allow learners to access a private channel to communicate with a course coordinator
   - The system shall allow admins to remove comments made by other users on the forum portal

6. Ethics and Accessibility
   - While the user is on the settings page, the system shall allow the users to view and access information on how their data is collected and used
   - While the user is at the tutorial page, the system shall allow users to view a tutorial on how to navigate the platform
   - While the user is on the settings page, the system shall allow users to submit feedback to the EmpowerU team (bug reports, suggestions, etc.)
