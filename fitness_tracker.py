# Import libraries
import bisect
import sqlite3
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

# Initialize database and connection
conn = sqlite3.connect('fitness_tracker_database.db')
cursor = conn.cursor()

# Create class for health metrics
class metrics:
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.last_recorded = None

# Create class for user
class users:
    def __init__(self, name):
        self.name = name
        self.height = 0
        self.height_unit = True
        self.gender = "M"
        self.age = 0
        self.activity = "S"


# Create user object using class
User = users("No User")

# Create BMI object using class and assign calculation method
BMI = metrics("BMI")
def calc_BMI(weight):
    if not User.height_unit:
        height = User.height / 2.54
    else:
        height = User.height
    BMI.value = (weight / (height**2)) * 703
BMI.calc = calc_BMI

# Create RHR object using class and assign calculation method
RHR = metrics("RHR")
def calc_RHR(beats):
    RHR.value = beats * 4
RHR.calc = calc_RHR

# Create waist measurement object using class and assign most recent value callback method
Measurements = metrics("Measurements")
def recent_measurement():
    if len(meas_tracking_arr):
        meas_key = meas_tracking_arr[-1]
        values = daily_data[int(meas_key)]
        meas = values[1]
    else:
        meas = 0
    
    return meas
Measurements.calc = recent_measurement

# Create weigth object and assign unit conversion method
Weight = metrics("Weight")
def convert_weight(lbs, kg):
    if lbs is None:
        lbs = kg * 2.20462262185
    elif kg is None:
        kg = lbs / 2.20462262185
    Weight.value = lbs
    Weight.value_k = kg
Weight.convert = convert_weight

# Create BMR object and assign calculation method
BMR = metrics("BMR")
def calc_BMR(weight):
    if User.height_unit:
        height = User.height * 2.54
    
    if User.gender == "M":
        BMR.value = 66.5 + (13.75 * weight) + (5.003 * height) - (6.75 *User.age)
    elif User.gender == "F":
        BMR.value = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * User.age)
BMR.calc = calc_BMR

# Create Maintenance Calories object and assign calculation method
MCal = metrics("MCal")
def calc_MCal():
    match User.activity:
        case "S":
            MCal.value = BMR.value * 1.2
        case "L":
            MCal.value = BMR.value * 1.375
        case "M":
            MCal.value = BMR.value * 1.55
        case "V":
            MCal.value = BMR.value * 1.725
        case "E":
            MCal.value = BMR.value * 1.9
MCal.calc = calc_MCal

# Create function to allow new user to create a user profile
def subscribe():
    # Open subwindow
    window_subscribe = tk.Toplevel(window)
    window_subscribe.title("New User")

    # Create variables for text inputs
    name_var = tk.StringVar()
    age_var = tk.StringVar()
    gender_var = tk.StringVar()
    height_var = tk.StringVar()
    unit_var = tk.StringVar()
    activity_var = tk.StringVar()

    # Function to submit values of text inputs and store them to the User object
    def submit():
        # Assign values from text inputs to User object
        User.name = name_var.get()
        User.age = age_var.get()
        User.gender = gender_var.get()
        User.height = height_var.get()
        
        if unit_var.get() == "in":
            User.height_unit = True
        else:
            User.height_unit = False
        
        match activity_var.get():
            case "Sedentary":
                User.activity = "S"
            case "Light Excercise 1-2 times per week":
                User.activity = "L"
            case "Moderate Excercise 2-3 times per week":
                User.activity = "M"
            case "Hard Excercise 4-5 times per week":
                User.activity = "V"
            case "Physical Job or Hard Excercise 6-7 times/w":
                User.activity = "E"
        
        # Reset values of input variables
        name_var.set("")
        age_var.set("")
        height_var.set("")

        # Update main metric calculations and the main window
        update_calc()
        update_window()

        # Close current subwindow
        window_subscribe.destroy()

    # Create labels and text inputs
    name_label = tk.Label(window_subscribe, text = 'Name')
    name_entry = tk.Entry(window_subscribe, textvariable = name_var)
    age_label = tk.Label(window_subscribe, text = 'Age')
    age_entry = tk.Entry(window_subscribe, textvariable = age_var)
    gender_label = tk.Label(window_subscribe, text = 'Gender')

    # Dropdown menu options
    gender_options = [
        "M",
        "F"
        ]

    
    # initial menu text
    gender_var.set( "M" )
  
    # Create Dropdown menu
    gender_drop = tk.OptionMenu( window_subscribe , gender_var , *gender_options )
    
    # Create labels and text inputs
    height_label = tk.Label(window_subscribe, text = 'Height')
    height_entry = tk.Entry(window_subscribe, textvariable = height_var)
    unit_label = tk.Label(window_subscribe, text = 'Height Units')

    # Dropdown menu options
    unit_options = [
        "in",
        "cm"
        ]

    # initial menu text
    unit_var.set( "in" )
  
    # Create Dropdown menu
    unit_drop = tk.OptionMenu( window_subscribe , unit_var , *unit_options )

    # Create activity text label
    activity_label = tk.Label(window_subscribe, text = 'Activity')

    # Dropdown menu options
    activity_options = [
        "Sedentary",
        "Light Excercise 1-2 times per week",
        "Moderate Excercise 2-3 times per week",
        "Hard Excercise 4-5 times per week",
        "Physical Job or Hard Excercise 6-7 times/w"
        ]
    
    # initial menu text
    activity_var.set( "Sedentary" )
  
    # Create Dropdown menu
    activity_drop = tk.OptionMenu( window_subscribe , activity_var , *activity_options )
    
    # Create submit button
    sub_button = tk.Button(window_subscribe, text = 'Submit', command = submit)

    # Organize GUI elements on window
    name_label.grid(row=0,column=0)
    name_entry.grid(row=0,column=1)
    age_label.grid(row=1,column=0)
    age_entry.grid(row=1,column=1)
    gender_label.grid(row=2, column=0)
    gender_drop.grid(row=2, column=1)
    height_label.grid(row=3, column=0)
    height_entry.grid(row=3, column=1)
    unit_label.grid(row=4, column=0)
    unit_drop.grid(row=4, column=1)
    activity_label.grid(row=5, column=0)
    activity_drop.grid(row=5, column=1)
    sub_button.grid(row=6,column=1)

# Create function to allow previous users to login
def user_login():
    # Create subwindow
    window_login = tk.Toplevel(window)
    window_login.title("Login")

    # Create variable for text inputs
    name_var = tk.StringVar()

    # Function to submit values of text input and store user data to the User object
    def submit():
        # Assign text input variable to intermediary variable
        current_name = name_var.get()

        # Check if user already exists and assign user info to User object
        if str(current_name) in possible_users:
            values =  possible_users[str(current_name)]
            User.name = str(current_name)
            User.height = values[0]
            User.height_unit = values[1]
            User.gender = values[2]
            User.age = values[3]
            User.activity = values[4]
        # If user does not exist, rerun login function
        else:
            user_login()
        
        # Reset input variable
        name_var.set("")

        # Update main metrics and main window
        update_calc()
        update_window()

        # Close current window
        window_login.destroy()

    # Function to create a new user profile
    def New_User():
        # Run function to create new user profile
        subscribe()

        # Close current window
        window_login.destroy()

    # Create label and text entry for user name
    name_label = tk.Label(window_login, text = 'Name')
    name_entry = tk.Entry(window_login, textvariable = name_var)
    # Create buttons for logging in and creating a new user
    sub_button = tk.Button(window_login, text = 'Submit', command = submit)
    new_button = tk.Button(window_login, text = 'New User', command = New_User)
    
    # Organize GUI elements on window
    name_label.grid(row=0,column=0)
    name_entry.grid(row=0,column=1)
    sub_button.grid(row = 1, column = 1)
    new_button.grid(row = 2, column = 1)

# Create function to edit user profile
def edit_user():
    # Create subwindow
    window_edit_user = tk.Toplevel(window)
    window_edit_user.title("Edit User Information")

    # Create variables for text input
    name_var = tk.StringVar()
    age_var = tk.StringVar()
    gender_var = tk.StringVar()
    height_var = tk.StringVar()
    unit_var = tk.StringVar()
    activity_var = tk.StringVar()

    # Create function to store submitted information to User object
    def submit():
        # Create intermediary variables for text input variables
        current_age = age_var.get()
        current_gender = gender_var.get()
        current_height = height_var.get()
        current_unit = unit_var.get()
        current_activity = activity_var.get()

        # Store text inputs to User object
        User.name = name_var.get()
        User.age = age_var.get()
        User.gender = gender_var.get()
        User.height = height_var.get()
        
        # Store unit values as boolean value in User object
        if unit_var.get() == "in":
            User.height_unit = True
        else:
            User.height_unit = False
        
        # Store value of activity dropdown in User object
        match activity_var.get():
            case "Sedentary":
                User.activity = "S"
            case "Light Excercise 1-2 times per week":
                User.activity = "L"
            case "Moderate Excercise 2-3 times per week":
                User.activity = "M"
            case "Hard Excercise 4-5 times per week":
                User.activity = "V"
            case "Physical Job or Hard Excercise 6-7 times/w":
                User.activity = "E"
        
        # Reset text input values
        name_var.set("")
        age_var.set("")
        height_var.set("")

        # Update main metrics and main window
        update_calc()
        update_window()

        # Close current window
        window_edit_user.destroy()

    # Create labels and text inputs
    name_label = tk.Label(window_edit_user, text = 'Name')
    name_entry = tk.Entry(window_edit_user, textvariable = name_var)
    age_label = tk.Label(window_edit_user, text = 'Age')
    age_entry = tk.Entry(window_edit_user, textvariable = age_var)
    gender_label = tk.Label(window_edit_user, text = 'Gender')

    # Dropdown menu options
    gender_options = [
        "M",
        "F"
        ]

    # initial menu text
    gender_var.set( "M" )
  
    # Create Dropdown menu
    gender_drop = tk.OptionMenu( window_edit_user , gender_var , *gender_options )
    
    # Create labels and text inputs
    height_label = tk.Label(window_edit_user, text = 'Height')
    height_entry = tk.Entry(window_edit_user, textvariable = height_var)
    unit_label = tk.Label(window_edit_user, text = 'Height Units')

    # Dropdown menu options
    unit_options = [
        "in",
        "cm"
        ]

    # initial menu text
    unit_var.set( "in" )
  
    # Create Dropdown menu
    unit_drop = tk.OptionMenu( window_edit_user , unit_var , *unit_options )
    
    # Create activity dropdown label
    activity_label = tk.Label(window_edit_user, text = 'Activity')

    # Dropdown menu options
    activity_options = [
        "Sedentary",
        "Light Excercise 1-2 times per week",
        "Moderate Excercise 2-3 times per week",
        "Hard Excercise 4-5 times per week",
        "Physical Job or Hard Excercise 6-7 times/w"
        ]
    
    # initial menu text
    activity_var.set( "Sedentary" )
  
    # Create Dropdown menu
    activity_drop = tk.OptionMenu( window_edit_user , activity_var , *activity_options )
    
    # Create submit button
    sub_button = tk.Button(window_edit_user, text = 'Submit', command = submit)

    # Organize GUI elements on window
    name_label.grid(row=0,column=0)
    name_entry.grid(row=0,column=1)
    age_label.grid(row=1,column=0)
    age_entry.grid(row=1,column=1)
    gender_label.grid(row=2, column=0)
    gender_drop.grid(row=2, column=1)
    height_label.grid(row=3, column=0)
    height_entry.grid(row=3, column=1)
    unit_label.grid(row=4, column=0)
    unit_drop.grid(row=4, column=1)
    activity_label.grid(row=5, column=0)
    activity_drop.grid(row=5, column=1)
    sub_button.grid(row=6,column=1)

# Function to display user information in subwindow
def disp_user():
    # Create new subwindow
    window_disp_user = tk.Toplevel(window)
    window_disp_user.title("Display User Data")

    # Create labels displaying Age and User name
    tk.Label(master = window_disp_user, text = "User: " + str(User.name)).pack(pady = 5)
    tk.Label(master = window_disp_user, text = "Age: " + str(User.age)).pack(pady = 5)
    
    # Create label displaying biological Sex
    if User.gender == "M" and User.name == "No User":
        tk.Label(master = window_disp_user, text = "Biological Sex: No Info").pack(pady = 5)
    else:
        tk.Label(master = window_disp_user, text = "Biological Sex: " + str(User.gender)).pack(pady = 5)
    
    # Create label displaying height unit in use
    height_unit = "in" if User.height_unit else "cm"

    # Create label displaying height
    tk.Label(master = window_disp_user, text = "Height: " + str(User.height) + " " + height_unit).pack(pady = 5)

    # Initialize activity string display based on value provided by User.activity
    match User.activity:
        case "S":
            activity_str = "Sedentary"
        case "L":
            activity_str = "Light Excercise 1-2 times per week"
        case "M":
            activity_str = "Moderate Excercise 2-3 times per week"
        case "V":
            activity_str = "Hard Excercise 4-5 times per week"
        case "E":
            activity_str = "Physical Job or Hard Excercise 6-7 times/w"
    
    # Create label displaying user activity level
    tk.Label(master = window_disp_user, text = "Activity: " + activity_str).pack(pady = 5)

# Function to edit the data of a given calendar day
def edit_day_info():
    # Create subwindow
    window_edit_day = tk.Toplevel(window)
    window_edit_day.title("Edit Data")

    # Create text input variables
    weight_var = tk.StringVar()
    measurement_var = tk.StringVar()
    beat_var = tk.StringVar()

    # Function to store input values to corresponding short term memory arrays
    def submit():
        # Create intermediary variables
        current_weight = int(weight_var.get())
        current_measurement = int(measurement_var.get())
        current_beat = int(beat_var.get())

        # Fetch date in yymmdd integer format
        date = convert_date()
        
        # Store inputs to daily data dictionary
        daily_data[str(date)] = (current_weight, current_measurement, current_beat)

        # Remove day from tracking list if weight is 0, else add date to tracking list
        if str(weight_var.get()) == "0" or str(weight_var.get()) == "":
            remove_from_list(weight_tracking_arr)
        else:
            instert_to_list(weight_tracking_arr)
        
        # Remove day from tracking list if measurement is 0, else add date to tracking list
        if str(measurement_var.get()) == "0" or str(measurement_var.get()) == "":
            remove_from_list(meas_tracking_arr)
        else:
            instert_to_list(meas_tracking_arr)

        # Remove day from tracking list if beats is 0, else add date to tracking list
        if str(beat_var.get()) == "0" or str(beat_var.get()) == "":
            remove_from_list(beat_tracking_arr)
        else:
            instert_to_list(beat_tracking_arr)

        # Reset values for input variable
        weight_var.set("")
        measurement_var.set("")
        beat_var.set("")

        # Update main metrics and main window
        update_calc()
        update_window()

        # Close current window
        window_edit_day.destroy()

    # Create labels and text inputs
    weight_label = tk.Label(window_edit_day, text = 'Weight')
    weight_entry = tk.Entry(window_edit_day, textvariable = weight_var)
    meas_label = tk.Label(window_edit_day, text = 'Waist Measurement')
    meas_entry = tk.Entry(window_edit_day, textvariable = measurement_var)
    beat_label = tk.Label(window_edit_day, text = 'Heartbeats in 15 sec')
    beat_entry = tk.Entry(window_edit_day, textvariable = beat_var)

    # Create submission button
    sub_button = tk.Button(window_edit_day, text = 'Submit', command = submit)

    # Organize GUI elements on window
    weight_label.grid(row=0,column=0)
    weight_entry.grid(row=0,column=1)
    meas_label.grid(row=1,column=0)
    meas_entry.grid(row=1,column=1)
    beat_label.grid(row=2,column=0)
    beat_entry.grid(row=2,column=1)
    sub_button.grid(row=3,column=1)

# Function to display data for particular calendar date on main window
def disp_day_info():
    # Fetch date in yymmdd integer format
    date = convert_date()

    # If data exist for this date, retrieve it from daily data and assign it to weight var
    if date in weight_tracking_arr:
        values = daily_data[str(date)]
        weight = values[0]
    else:
        weight = 0
    
    # If data exist for this date, retrieve it from daily data and assign it to measurement var
    if date in meas_tracking_arr:
        values = daily_data[str(date)]
        meas = values[1]
    else:
        meas = 0

    # If data exist for this date, retrieve it from daily data and assign it to beats var
    if date in beat_tracking_arr:
        values = daily_data[str(date)]
        beats = values[2]
    else:
        beats = 0
    
    # Display data on main window
    cal_data.config(text = "Weight: " + str(weight) + "\nWaist Measurements: " + str(meas) + "\nHeartbeats in 15 sec: " + str(beats))

# Function to update calculations for main metrics
def update_calc():
    # If weight data exists, calculate BMI, BMR, and MCal
    if len(weight_tracking_arr):
        # Retrieve most recent weight data
        weight_key = weight_tracking_arr[-1]
        values = daily_data[str(weight_key)]
        weight = values[0]

        # Calculate BMI, BMR, and MCal
        BMI.calc(weight)
        BMR.calc(weight)
        MCal.calc()

    # If beats data exist, calculate RHR
    if len(beat_tracking_arr):
        # Retrieve most recent beat data
        beat_key = beat_tracking_arr[-1]
        values = daily_data[str(beat_key)]
        beat = values[2]

        # Calculate RHR
        RHR.calc(beat)

# Update main metric displays on main window
def update_window():
    # Update txt values of main window labels
    user_label['text'] = "User: " + User.name
    weight_label['text'] = "Weight: " + str(Weight.value)
    BMI_label['text'] = "BMI: " + str(round(BMI.value, 2))
    RHR_label['text'] = "RHR: " + str(RHR.value)
    meas_label['text'] = "Measurements: " + str(Measurements.calc())
    BMR_label['text'] = "BMR: " + str(round(BMR.value, 2))
    mcal_label['text'] = "Mainenance Calories: " + str(round(MCal.value, 2))

# Sorted insert a date to a list
def instert_to_list(list):
    # Fetch date in yymmdd integer format
    date = convert_date()

    # If this date does not already exist in list, sorted insert it to the list
    if date not in list:
        bisect.insort(list, date)

# Remove a date on a list
def remove_from_list(list):
    # Fetch date in yymmdd integer format
    date = convert_date()

    # If this date exist in list, remove it from list
    if date in list:
        list.remove(date)

# Function to convert selected calendar date to yymmdd integer format and return result
def convert_date():
    # Retrieve date from calendar widget
    str_date = str(cal.get_date())
    
    # Initialize loop variables 
    i = ""
    c = 0
    i = str_date[c]
    
    # Initialize intermediary variables
    month = 0
    day = 0
    year = 0

    # Extract integer month value
    while i != "/":
        month = month * 10 + int(i)
        c += 1
        i = str_date[c]
    
    # Iterate past /
    c+= 1
    i = str_date[c]

    # Extract integer day value
    while i != "/":
        day = day * 10 + int(i)
        c += 1
        i = str_date[c]

    # Iterate pas /
    c += 1

    # Extract integer year value
    while c < len(str_date):
        i = str_date[c]
        year = year * 10 + int(i)
        c += 1
    
    # Combine year, month, and day into integer date value
    date = year * 10000 + month * 100 + day

    # Return integer date
    return date

# Extract value of a dictionary from long term memory database and store in short term memory dictionary
def extract_dict(name):
    # Execute a SELECT query to retrieve the data from the table
    cursor.execute("SELECT day, weight, measure FROM " + name)
    rows = cursor.fetchall()

    # Convert the rows into a dictionary
    Dict = {}
    for row in rows:
        key = row[0]
        value1 = row[1]
        value2 = row[2]
        Value3 = row[3]
        Dict[key] = (value1, value2, Value3)
    
    # Return dictionary
    return Dict

# Extract value of a list from long term memory database and store in short term memory list
def extract_list(name):
    # Retrieve all records from the table
    cursor.execute("SELECT day FROM " + name)
    rows = cursor.fetchall()

    # Extract the values into a one-dimensional array
    List = [row[0] for row in rows]

    # Return list
    return List

# Extract user data from database and store it in dictionary
def extract_users():
    # Execute a SELECT query to retrieve the data from the table
    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()

    # Convert the rows into a dictionary
    Dict = {}
    for row in rows:
        key = row[0]
        value1 = row[1]
        value2 = row[2]
        value3 = row[3]
        value4 = row[4]
        value5 = row[5]
        Dict[key] = (value1, value2, value3, value4, value5)
        
    # Return value of dictionary
    return Dict


# Create user data table in database if does not already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                    user TEXT PRIMARY KEY,
                    height REAL,
                    height_unit BOOLEAN,
                    gender TEXT,
                    age REAL,
                    activity TEXT
                )''')

# Extract user data from database table
possible_users = extract_users()

# Create main window
window = tk.Tk()

# Format main window frames
frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1, height=75, width=30)
frame.grid(row=1, column=1)
window.columnconfigure(1, weight=1, minsize=75)
window.rowconfigure(1, weight=1, minsize=50)

# Retrieve user information from user
user_login()

# Create dialy data and tracking table if don't already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS daily_data(
                    day TEXT PRIMARY KEY,
                    weight REAL,
                    measure REAL,
                    beats INTEGER
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS weight_tracking(
                    id INTEGER PRIMARY KEY,
                    day INTEGER
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS waist_tracking(
                    id INTEGER PRIMARY KEY,
                    day INTEGER
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS beat_tracking(
                    id INTEGER PRIMARY KEY,
                    day INTEGER
                )''')


# Extract the values of database tables for daily data and tracking data
daily_data = extract_dict("daily_data")
weight_tracking_arr = extract_list("weight_tracking")
meas_tracking_arr = extract_list("waist_tracking")
beat_tracking_arr = extract_list("beat_tracking")

# Set current time for calendar
current_time = datetime.now()

# Create calendar widget
cal = Calendar(master = frame, selectmode = "day", year = current_time.year, month = current_time.month, day = current_time.day)
cal.pack(pady = 5)

# Add Button and Label for dialy data display and editing
tk.Button(master = frame, text = "Display Data", command = disp_day_info).pack(pady = 5)
tk.Button(master = frame, text = "Edit Data", command = edit_day_info).pack(pady = 5)

# Create widget for displaying day data to user
cal_data = tk.Label(master = frame, text = "")
cal_data.pack(pady = 20)

# Create second frame in main window
frame2 = tk.Frame(master = window, relief=tk.RAISED, borderwidth=1, height=75, width=30)
frame2.grid(row=1, column=2)
window.columnconfigure(2, weight=1, minsize=75)

# Create label for current user
user_label = tk.Label(master = frame2, text = "User: " + User.name)

# Create buttons to display and edit user information
disp_button = tk.Button(master = frame2, text = "Display User Info", command = disp_user)
edit_button = tk.Button(master = frame2, text = "Edit User Info", command = edit_user)

# Create labels to display main metrics to user
weight_label = tk.Label(master = frame2, text = "Weight: " + str(Weight.value))
BMI_label = tk.Label(master = frame2, text = "BMI: " + str(round(BMI.value, 2)))
RHR_label = tk.Label(master = frame2, text = "RHR: " + str(RHR.value))
meas_label = tk.Label(master = frame2, text = "Measurements: " + str(Measurements.calc()))
BMR_label = tk.Label(master = frame2, text = "BMR: " + str(round(BMR.value, 2)))
mcal_label = tk.Label(master = frame2, text = "Mainenance Calories: " + str(round(MCal.value, 2)))

# Format Widgets in second frame of main window
user_label.pack(pady = 5)
disp_button.pack(pady = 5)
edit_button.pack(pady = 5)
weight_label.pack(pady = 5)
BMI_label.pack(pady = 5)
RHR_label.pack(pady = 5)
meas_label.pack(pady = 5)
BMR_label.pack(pady = 5)
mcal_label.pack(pady = 5)

# Execute main loop for GUI
window.mainloop()

# Store user object data to possible users
possible_users[User.name] = (User.height, User.height_unit, User.gender, User.age, User.activity)

# Update values of short term memory storage dictionaries and lists in database
for key, values in possible_users.items():
    value1, value2, value3, value4, value5 = values
    cursor.execute("INSERT OR REPLACE INTO user_data (user, height, height_unit, gender, age, activity) VALUES (?, ?, ?, ?, ?, ?)", (key, value1, value2, value3, value4, value5))

for key, values in daily_data.items():
    value1, value2, value3 = values
    cursor.execute("INSERT OR REPLACE INTO daily_data (day, weight, measure, beats) VALUES (?, ?, ?, ?)", (key, value1, value2, value3))

for index, value in enumerate(weight_tracking_arr):
    cursor.execute("INSERT OR REPLACE INTO weight_tracking (id, day) VALUES (?, ?)", (index+1, value))

for index, value in enumerate(meas_tracking_arr):
    cursor.execute("INSERT OR REPLACE INTO waist_tracking (id, day) VALUES (?, ?)", (index+1, value))

# close connection to database
conn.commit()
cursor.close()
conn.close()