# ============================================================
# School Management System 🏫
# A simple JSON-backed app that stores students and teachers.
# Uses: OOP, Abstraction (ABC), Inheritance, Polymorphism,
#       File I/O, JSON, Static Methods.
# ============================================================

# Import json — to read/write data as JSON files
import json

# Import ABC and abstractmethod — to make abstract base classes
from abc import ABC, abstractmethod

# Import Path — to check if a file exists easily
from pathlib import Path


# ------------------------------------------------------------
# STEP 1: DATABASE SETUP
# ------------------------------------------------------------

# Name of the JSON file we'll use as our "database"
database = "school_data.json"

# Default data structure — starts empty if no file exists yet
data = {"students": [], "teachers": []}


# If the JSON file already exists on disk, load its contents
if Path(database).exists():
    with open(database, 'r') as f:
        content = f.read()
        if content:                      # only load if file isn't empty
            data = json.loads(content)   # parse the JSON string into a dict


# Helper function — saves the current `data` dict back to the file
def save():
    with open(database, "w") as f:
        json.dump(data, f, indent=4)     # indent=4 makes the file pretty/readable


# ------------------------------------------------------------
# STEP 2: ABSTRACT BASE CLASS — the rulebook for all persons
# ------------------------------------------------------------
class Persons(ABC):
    # Every subclass MUST implement get_roles() to say who they are
    @abstractmethod
    def get_roles(self):
        pass

    # Every subclass MUST implement register() to add themselves to the database
    @abstractmethod
    def register(self):
        pass

    # Every subclass MUST implement show_details() to display their info
    @abstractmethod
    def show_details(self):
        pass

    # Static method — doesn't use self or the class, just a utility function.
    # Returns True if the email looks valid (has "@" and "."), otherwise False.
    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
            return True
        else:
            return False


# ------------------------------------------------------------
# STEP 3: STUDENT CLASS — implements the Person contract
# ------------------------------------------------------------
class Student(Persons):

    # Identifies this class's role
    def get_roles(self):
        return "student"

    # Collects student info from the user and stores it in the JSON database
    def register(self):
        name    = input("tell your name :- ")
        age     = int(input("tell your age :- "))
        email   = input("tell your mail :- ")
        roll_no = input("tell your roll number :- ")

        # Validate the email — if it's not valid, stop and return
        if not Persons.validate_email(email):
            print("invalid Email ")
            return

        # Check if a student with this roll number already exists
        for i in data['students']:
            if i['roll_no'] == roll_no:
                print("student already exist")
                return

        # Append the new student to the data dict (with an empty grades dict)
        data['students'].append({
            "name":    name,
            "age":     age,
            "email":   email,
            "roll_no": roll_no,
            "grades":  {}
        })

        save()   # persist changes to disk
        print(f"Student {name} registered")

    # Looks up a student by roll number and prints their details
    def show_details(self):
        roll_no = input("roll no :- ")

        # Search through students list for a matching roll number
        for s in data['students']:
            if s['roll_no'] == roll_no:
                grades = s['grades']

                # Compute average — guard against empty dict (avoid ZeroDivisionError)
                avg = sum(grades.values()) / len(grades) if grades else 0

                # Pretty-print the student's info
                print(f"\n  Name    : {s['name']}")
                print(f"  Roll no : {s['roll_no']}")
                print(f"  Grades  : {grades}")
                print(f"  Average : {avg:.1f}")
                return

    # Adds/updates a grade (subject → marks) for a student
    def add_grade(self):
        roll_no = input("tell the roll number :- ")
        subject = input("Subject : ")
        marks   = float(input("Marks : "))

        # Find the student and update their grades dict
        for i in data['students']:
            if i["roll_no"] == roll_no:
                i['grades'][subject] = marks   # add/overwrite the subject's marks
                save()                          # persist to disk
                print("grade added successfully")
                return

        # If loop finishes without finding the student
        print("student not found")


# ------------------------------------------------------------
# STEP 4: TEACHER CLASS — also implements the Person contract
# ------------------------------------------------------------
class Teacher(Persons):

    # Identifies this class's role
    def get_roles(self):
        return "Teacher"

    # Collects teacher info from the user and stores it in the JSON database
    def register(self):
        name    = input("tell your name :- ")
        age     = int(input("tell your age :- "))
        email   = input("tell your mail :- ")
        subject = input("subject : ")
        emp_id  = input("tell your emp_id number :- ")

        # Validate email — same static helper as Student
        if not Persons.validate_email(email):
            print("invalid Email ")
            return

        # Check for duplicate employee ID
        for i in data['teachers']:
            if i['emp_id'] == emp_id:
                print("Teacher already exist")
                return

        # Append new teacher to the data dict
        data['teachers'].append({
            "name":    name,
            "age":     age,
            "email":   email,
            "subject": subject,
            "emp_id":  emp_id,
        })

        save()   # persist to disk
        print(f"Teacher {name} registerd")    # (typo — should be "registered")

    # Looks up a teacher by employee ID and prints their details
    def show_details(self):
        emp_id = input("Employee ID: ")

        # Search through teachers list for a matching emp_id
        for t in data["teachers"]:
            if t["emp_id"] == emp_id:
                print(f"\n  Name    : {t['name']}")
                print(f"  Subject : {t['subject']}")
                print(f"  Emp ID  : {t['emp_id']}")
                return

        # If no teacher matched the emp_id
        print("Teacher not found.")


# ------------------------------------------------------------
# STEP 5: MAIN MENU — the app's entry point
# ------------------------------------------------------------

# Create one instance of each class so we can call their methods later
stud = Student()
tech = Teacher()

# Show the menu options to the user
print("press 1  to register a student")
print("press 2  to register a teacher")
print("press 3  to add grades")
print("press 4  to show a student detail")
print("press 5  to show a teacher detail")

# Read the user's choice
choice = int(input("please tell your choice :- "))

# Dispatch based on choice — simple if/elif menu
if choice == 1:
    stud.register()          # register a new student
elif choice == 2:
    tech.register()          # register a new teacher
elif choice == 3:
    stud.add_grade()         # add a grade to a student
elif choice == 4:
    stud.show_details()      # show student's details
elif choice == 5:
    tech.show_details()      # show teacher's details