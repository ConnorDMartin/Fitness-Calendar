# Fitness-Calendar

The goal of this project is to be a helpful tool for people struggling to see progress in their weight loss or bulking journeys. Often, people get discouraged while trying to loose weight or gain muscle mass because they find it hard to see the gradual improvements they're making.
This project uses Python's built-in GUI library "Tkinter" and its' database library "SQlite3" to build an easy to use user interface with local information storage so that users can use the project as a long term fitness tool.

How it works:

This project uses Tkinter and SWlite3 for its database management and user interface needs because of its ease of use. Since they are both already included in the standard python library, installation of extra libraries isn't necessary to make the code run. Additionally, they are both very straight-forward and easy to use libraries, perfect for a first serious attempt at creating a code with both a GUI and a database.
The project also makes use of bisect, a library used to quickly use sorted insertion on a list, and datetime, a library used in this script to get the current date when operating the calendar or storing data. Both of these libraries are part of python's standard library so don't need to be installed seperately. However, tkcalendar, a library used to give tkinter the ability to create interactive calendars, needs to be installed through python's pip before running the code.
However, this project is limited by the language and the libraries it uses. Python's challenges with performance and speed make it so that as the data stored by this code grows, its response time and efficiency decrease. I plan on overcoming this challenge by introducing more efficient memory management techniques to the project and eventually switching the project to a more efficient language.
Visually, the use of SQlite3 limits how complex or visually pleasing the UI can be. I plan on improving the GUI by writing it in Javascript then, using a library like JS2PY (Javascript Runtime in Pure Python), interfacing it with the existing python script.

Usage:

When run, a window prompting the user to login or create a new profile opens. If the user already has a profile on their device, they shouold type their name into the text box and press submit to continue. If they do not already have a profile, they should press the 'New User' button then enter the information needed to create a new user profile.
Once the user has logged in to their profile, they can then start using the main window of the program. Displayed on the right side of this window is the profile currently logged in, buttons to display or edit the user information (Name, age, biological sex, height, and activity level) in a new window.
Displayed below this are the user's weight, BMI, RHR, waist measurement, BMR, and maintenance calories. This display updates as the user inputs new data.
On the right side of the window is an interactive calendar. Below this calendar are two buttons: one to display and one to edit and one to display the weight, waist measurement, and heart beats in 15 seconds on the selected day.
When the user is done with the program, all they need to do is close the main window and all changes made during runtime will be updated in the database.

Installation:

1. Before installing the project, make sure you have python installed onto your computer (you can download the latest version of python [here](https://www.python.org/downloads/)) and have the Tkcalendar library pip installed (enter the command "pip install tkcalendar" into your terminal once python is installed).
2. Download the .py file from this project's main branch.
3. Use your terminal or a program like VS Code to run the downoaded .py file.
